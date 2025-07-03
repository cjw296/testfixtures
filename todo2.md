# TODO2: Alternative Typing Approaches (TypedDict/Protocol-based)

## Overview
Explore alternative typing approaches using TypedDict, Protocol, or other advanced typing features to provide better type safety for the `mock_datetime`, `mock_date`, and `mock_time` functions while preserving their flexible `*args/**kwargs` signatures.

## Requirements and Constraints

### MUST Requirements
- Use `foo | None` instead of `Optional[foo]` for all type annotations
- All type checks with `mypy testfixtures` MUST pass after each commit
- All tests with `pytest testfixtures` MUST pass after each commit
- No `Any` types MUST be used
- No `object` types MUST be used
- External API behavior MUST remain identical
- All 966 existing tests MUST continue to pass
- Modern Python 3.11+ type annotations with `|` syntax MUST be used
- Proper `Self` return types MUST be used where applicable

### MUST NOT Requirements
- MUST NOT use `type: ignore` on any public/external APIs
- MUST NOT introduce any casts in public APIs
- MUST NOT change any external API behavior or signatures
- MUST NOT break any existing test cases
- MUST NOT use `Any` or `object` types

### MAY Use
- `type: ignore` inside method implementations if absolutely necessary
- TypedDict for structured parameter validation
- Protocol classes for interface definitions
- Generic typing with constraints
- Union types for parameter variations
- ParamSpec for advanced callable typing

## Implementation Strategy

### Iterative Approach
1. Explore each alternative approach independently
2. Compare type safety improvements vs implementation complexity
3. Work on one function at a time: `mock_datetime` → `mock_date` → `mock_time`
4. Each experiment: design → implement → test → commit
5. Auto-commit when both mypy and pytest pass (no confirmation needed)

## Approach 2A: TypedDict Parameter Specifications

### Concept
Use TypedDict to define structured parameter sets, allowing the `*args/**kwargs` signature to be more precisely typed while maintaining runtime flexibility.

### Step 2A.1: Design TypedDict Specifications

**Task**: Create TypedDict classes that capture all valid parameter combinations.

```python
from typing import TypedDict, Unpack

class DateTimeKwargs(TypedDict, total=False):
    tzinfo: TZInfo | None
    delta: float | None
    delta_type: str
    date_type: type[date]
    strict: bool

class DateTimeArgs(TypedDict, total=False):
    year: int
    month: int  
    day: int
    hour: int
    minute: int
    second: int
    microsecond: int

class DateKwargs(TypedDict, total=False):
    delta: float | None
    delta_type: str
    strict: bool

class DateArgs(TypedDict, total=False):
    year: int
    month: int
    day: int

class TimeKwargs(TypedDict, total=False):
    delta: float | None
    delta_type: str

class TimeArgs(TypedDict, total=False):
    year: int
    month: int
    day: int
    hour: int
    minute: int
    second: int
    microsecond: int
```

**Commit**: `git commit -m "Add TypedDict parameter specifications"`

### Step 2A.2: Implement TypedDict-based Overloads

**Task**: Create overloads using TypedDict and Unpack for precise parameter typing.

```python
@overload
def mock_datetime(**kwargs: Unpack[DateTimeKwargs]) -> type[MockDateTime]: ...

@overload  
def mock_datetime(default: datetime, **kwargs: Unpack[DateTimeKwargs]) -> type[MockDateTime]: ...

@overload
def mock_datetime(default: None, **kwargs: Unpack[DateTimeKwargs]) -> type[MockDateTime]: ...

@overload
def mock_datetime(year: int, month: int, day: int, **kwargs: Unpack[DateTimeKwargs]) -> type[MockDateTime]: ...

@overload
def mock_datetime(year: int, month: int, day: int, hour: int, **kwargs: Unpack[DateTimeKwargs]) -> type[MockDateTime]: ...

# Continue for all valid combinations...

def mock_datetime(*args: int | datetime | None | TZInfo, **kwargs: Unpack[DateTimeKwargs]) -> type[MockDateTime]:
    # Existing implementation unchanged
```

**Benefits**:
- Preserves existing `*args/**kwargs` signature
- Provides structured typing for keyword arguments
- MyPy can validate keyword parameter names and types
- IDE autocomplete for keyword arguments

**Test and Commit**: 
```bash
mypy testfixtures && pytest testfixtures && git add -A && git commit -m "Implement TypedDict overloads for mock_datetime"
```

### Step 2A.3: Enhanced TypedDict with Parameter Validation

**Task**: Add runtime parameter validation using TypedDict structure.

```python
from typing import get_type_hints

def validate_kwargs(kwargs: dict, expected_type: type[TypedDict]) -> None:
    """Runtime validation of kwargs against TypedDict structure."""
    hints = get_type_hints(expected_type)
    required_keys = getattr(expected_type, '__required_keys__', set())
    optional_keys = getattr(expected_type, '__optional_keys__', set())
    
    # Check for unknown parameters
    unknown = set(kwargs.keys()) - (required_keys | optional_keys)
    if unknown:
        raise TypeError(f"Unknown parameters: {unknown}")
    
    # Check required parameters
    missing = required_keys - set(kwargs.keys())
    if missing:
        raise TypeError(f"Missing required parameters: {missing}")
    
    # Type check each parameter
    for key, value in kwargs.items():
        expected_type = hints.get(key)
        if expected_type and not isinstance(value, expected_type):
            # Add more sophisticated type checking here
            pass

def mock_datetime(*args: int | datetime | None | TZInfo, 
                 **kwargs: Unpack[DateTimeKwargs]) -> type[MockDateTime]:
    validate_kwargs(kwargs, DateTimeKwargs)
    # Continue with existing implementation
```

**Test and Commit**: Same pattern

## Approach 2B: Protocol-based Interface Definitions

### Concept
Define Protocol classes that specify the expected interface for mock objects, allowing for more flexible typing while maintaining implementation independence.

### Step 2B.1: Design Mock Protocols

**Task**: Create Protocol classes defining the expected interface for each mock type.

```python
from typing import Protocol, Self

class MockDateTimeProtocol(Protocol):
    @classmethod
    def add(cls, *args: int | datetime, **kwargs: int | TZInfo | None) -> None: ...
    
    @classmethod  
    def set(cls, *args: int | datetime, **kwargs: int | TZInfo | None) -> None: ...
    
    @classmethod
    def tick(cls, *args: timedelta, **kwargs: float) -> None: ...
    
    @classmethod
    def now(cls, tz: TZInfo | None = None) -> Self: ...
    
    @classmethod
    def utcnow(cls) -> Self: ...

class MockDateProtocol(Protocol):
    @classmethod
    def add(cls, *args: int | date, **kwargs: int) -> None: ...
    
    @classmethod
    def set(cls, *args: int | date, **kwargs: int) -> None: ...
    
    @classmethod
    def tick(cls, *args: timedelta, **kwargs: float) -> None: ...
    
    @classmethod
    def today(cls) -> Self: ...

class MockTimeProtocol(Protocol):
    @classmethod
    def add(cls, *args: int | datetime, **kwargs: int) -> None: ...
    
    @classmethod
    def set(cls, *args: int | datetime, **kwargs: int) -> None: ...
    
    @classmethod
    def tick(cls, *args: timedelta, **kwargs: float) -> None: ...
    
    def __call__(self) -> float: ...
```

**Commit**: `git commit -m "Add Protocol definitions for mock interfaces"`

### Step 2B.2: Protocol-based Function Signatures

**Task**: Use Protocols in function return types for better interface specification.

```python
@overload
def mock_datetime(**kwargs: Any) -> type[MockDateTimeProtocol]: ...  # Use more specific kwargs

@overload
def mock_datetime(*args: int | datetime | None | TZInfo, 
                 **kwargs: Any) -> type[MockDateTimeProtocol]: ...

def mock_datetime(*args: int | datetime | None | TZInfo,
                 **kwargs: Any) -> type[MockDateTimeProtocol]:
    # Existing implementation, but return type now provides Protocol interface
    return mock_factory(...)  # type: ignore[return-value] - temporarily
```

**Benefits**:
- Clearer interface contracts
- Better documentation of expected behavior
- Flexible implementation while maintaining type safety
- Protocol structural typing allows duck typing validation

**Test and Commit**: Same pattern

## Approach 2C: Generic Type Variables with Constraints

### Concept
Use advanced generic typing with constraints to provide flexible yet type-safe parameter handling.

### Step 2C.1: Design Constrained Generics

**Task**: Create type variables with constraints that capture parameter relationships.

```python
from typing import TypeVar, Generic, Literal

# Constrained type variables for different call patterns
DefaultT = TypeVar('DefaultT', datetime, date, None, type(None))
ConfigT = TypeVar('ConfigT', bound=dict)

class MockFactory(Generic[DefaultT, ConfigT]):
    """Generic factory for creating mock objects with typed parameters."""
    
    def __init__(self, default: DefaultT, config: ConfigT): ...
    
    def create(self) -> type[MockedCurrent]: ...

# Specialized factories for each pattern
DateTimeFactory = MockFactory[datetime | None, DateTimeKwargs]
DateFactory = MockFactory[date | None, DateKwargs]  
TimeFactory = MockFactory[datetime | None, TimeKwargs]
```

**Commit**: `git commit -m "Add generic type variable constraints"`

### Step 2C.2: Implement Generic-based Overloads

**Task**: Use generic types to create more precise overload specifications.

```python
@overload
def mock_datetime() -> DateTimeFactory[None, DateTimeKwargs]: ...

@overload
def mock_datetime(default: datetime) -> DateTimeFactory[datetime, DateTimeKwargs]: ...

@overload
def mock_datetime(default: None) -> DateTimeFactory[None, DateTimeKwargs]: ...

def mock_datetime(*args, **kwargs) -> type[MockDateTime]:
    # Implementation remains the same, but type system understands relationships
```

**Test and Commit**: Same pattern

## Approach 2D: ParamSpec for Advanced Callable Typing

### Concept
Use ParamSpec to capture and forward parameter specifications through the typing system.

### Step 2D.1: Design ParamSpec Specifications

**Task**: Create ParamSpec-based typing for flexible parameter forwarding.

```python
from typing import ParamSpec, Concatenate

P = ParamSpec('P')

class MockCallable(Generic[P]):
    """Callable with precise parameter specification."""
    
    def __call__(self, *args: P.args, **kwargs: P.kwargs) -> type[MockedCurrent]: ...

# Define specific parameter specifications
DateTimeParams = ParamSpec('DateTimeParams')
DateParams = ParamSpec('DateParams')
TimeParams = ParamSpec('TimeParams')
```

**Commit**: `git commit -m "Add ParamSpec-based callable typing"`

### Step 2D.2: Implement ParamSpec-based Overloads

**Task**: Use ParamSpec to maintain precise parameter forwarding.

```python
def create_datetime_mock(
    *args: DateTimeParams.args, 
    **kwargs: DateTimeParams.kwargs
) -> type[MockDateTime]: ...

def mock_datetime(*args, **kwargs) -> type[MockDateTime]:
    return create_datetime_mock(*args, **kwargs)
```

**Test and Commit**: Same pattern

## Approach 2E: Hybrid TypedDict + Overload Strategy

### Concept
Combine the best of TypedDict precision with strategic overloads for maximum type safety.

### Step 2E.1: Design Hybrid Approach

**Task**: Create a combination approach that provides both runtime and compile-time validation.

```python
# Comprehensive parameter specification
class MockDateTimeConfig(TypedDict, total=False):
    # Core datetime parameters
    year: int
    month: int
    day: int
    hour: int
    minute: int
    second: int
    microsecond: int
    
    # Configuration parameters
    tzinfo: TZInfo | None
    delta: float | None
    delta_type: Literal['seconds', 'minutes', 'hours', 'days', 'weeks']
    date_type: type[date]
    strict: bool

# Strategic overloads for common patterns
@overload
def mock_datetime() -> type[MockDateTime]: ...

@overload
def mock_datetime(*, **config: Unpack[MockDateTimeConfig]) -> type[MockDateTime]: ...

@overload
def mock_datetime(default: datetime | None, *, **config: Unpack[MockDateTimeConfig]) -> type[MockDateTime]: ...

# Runtime implementation with validation
def mock_datetime(*args: int | datetime | None | TZInfo, **kwargs) -> type[MockDateTime]:
    # Validate kwargs against TypedDict structure
    # Convert args to structured parameters
    # Maintain existing logic
```

**Benefits**:
- Maximum type safety for keyword arguments
- Strategic overloads for common patterns
- Runtime validation possible
- Maintains backward compatibility

**Test and Commit**: Same pattern

## Approach 2F: Advanced Union Types with Literal

### Concept
Use advanced Union types with Literal values to create precise parameter specifications.

### Step 2F.1: Design Literal-based Types

**Task**: Create Union types with Literal constraints for precise parameter control.

```python
from typing import Literal

# Precise parameter types
DeltaType = Literal['seconds', 'minutes', 'hours', 'days', 'weeks', 'microseconds', 'milliseconds']
DateDeltaType = Literal['days', 'weeks']
TimeDeltaType = Literal['seconds', 'minutes', 'hours', 'days', 'weeks', 'microseconds', 'milliseconds']

# Parameter unions for different contexts
DateTimeCallable = Union[
    Callable[[], type[MockDateTime]],
    Callable[[datetime], type[MockDateTime]], 
    Callable[[None], type[MockDateTime]],
    Callable[..., type[MockDateTime]]  # Fallback for complex cases
]
```

**Test and Commit**: Same pattern

## Evaluation and Comparison Framework

### Step E.1: Implement Comparison Metrics

**Task**: Create systematic evaluation of each approach.

**Metrics to Compare**:
1. **Type Safety Score**: How many invalid usages caught at compile time
2. **IDE Experience**: Quality of autocomplete and error messages  
3. **Runtime Performance**: Any overhead introduced
4. **Implementation Complexity**: Lines of code and maintainability
5. **Backward Compatibility**: Percent of existing usage preserved
6. **MyPy Strictness**: Compatibility with `--strict` mode

**Test Suite for Each Approach**:
```python
def test_type_safety_coverage():
    # Valid calls that should type-check
    valid_calls = [
        lambda: mock_datetime(),
        lambda: mock_datetime(2001, 1, 1),
        lambda: mock_datetime(None, strict=True),
        # ... all documented usage patterns
    ]
    
    # Invalid calls that should be caught
    invalid_calls = [
        lambda: mock_datetime("invalid"),  # Wrong type
        lambda: mock_datetime(year="2001"),  # Wrong kwarg type
        lambda: mock_datetime(unknown_param=True),  # Unknown parameter
    ]
    
    # Test each approach's handling
```

### Step E.2: Performance Benchmarking

**Task**: Measure runtime impact of each typing approach.

```python
import timeit

def benchmark_approach(approach_name: str, callable_func):
    # Measure function call overhead
    setup_time = timeit.timeit(lambda: callable_func(), number=10000)
    return {
        'approach': approach_name,
        'calls_per_second': 10000 / setup_time,
        'overhead_percent': ...
    }
```

## Success Criteria

### Type Safety Improvements
- [ ] IDE provides accurate parameter hints
- [ ] Invalid parameter combinations caught at type-check time
- [ ] Return types precisely inferred
- [ ] No loss of existing functionality

### Implementation Quality
- [ ] All 966 tests pass
- [ ] MyPy `--strict` mode compliance
- [ ] No type ignores on public APIs
- [ ] Clean, maintainable code

### User Experience
- [ ] Better error messages for invalid usage
- [ ] Improved IDE autocomplete
- [ ] Clear documentation through types
- [ ] Minimal learning curve for existing users

## Expected Outcomes

### Most Promising Approaches
1. **Hybrid TypedDict + Overload** (Approach 2E): Best balance of type safety and implementation simplicity
2. **Enhanced TypedDict** (Approach 2A): Good type safety with minimal implementation changes
3. **Protocol-based** (Approach 2B): Excellent interface documentation, moderate implementation complexity

### Likely Challenges
1. **Runtime Validation Overhead**: TypedDict validation may impact performance
2. **MyPy Limitations**: Some advanced typing features may not work perfectly
3. **Backward Compatibility**: Ensuring existing code continues to work exactly as before
4. **IDE Support**: Not all IDEs support all advanced typing features equally

### Fallback Strategy
If no approach provides significant improvements over current implementation:
- Document the typing limitations
- Provide type stubs for better IDE experience
- Focus on improving documentation and examples
- Consider this a learning exercise for future reference

## Validation Commands
Run after each implementation:
```bash
source .venv/bin/activate
mypy testfixtures --strict
pytest testfixtures -v
python -c "import testfixtures; help(testfixtures.mock_datetime)"  # Check docstring
# If all pass, auto-commit and continue
```

## Final Deliverable
A comprehensive report comparing all approaches with recommendations for:
1. **Best overall approach** for this specific codebase
2. **Lessons learned** about advanced typing in Python
3. **Future considerations** for similar typing challenges
4. **Implementation guide** if proceeding with selected approach