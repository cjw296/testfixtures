# TODO1: Redesign Implementation for Explicit Parameter Signatures

## Overview
Redesign the `mock_datetime`, `mock_date`, and `mock_time` function implementations to use explicit parameter signatures instead of `*args/**kwargs` patterns, enabling proper overload compatibility while maintaining all existing functionality.

## Requirements and Constraints

### MUST Requirements
- Use `foo | None` instead of `Optional[foo]` for all type annotations
- Replace all ellipsis (`...`) with correct types inferred from tests, documentation, and implementation
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
- MUST NOT change any external API behavior
- MUST NOT break any existing test cases
- MUST NOT use `Any` or `object` types

### MAY Use
- `type: ignore` inside method implementations if absolutely necessary
- Internal helper functions to manage complexity
- Function signature variations that maintain backward compatibility

## Implementation Strategy

### Iterative Approach
1. Work on one function at a time: `mock_datetime` → `mock_date` → `mock_time`
2. For each function: analyze → redesign → implement → test → commit
3. Each commit should be atomic and easily rollable
4. Auto-commit when both mypy and pytest pass (no confirmation needed)

## Phase 1: Analysis and Planning

### Step 1.1: Analyze Current Usage Patterns
**Task**: Document all actual usage patterns for each function from test files.

**Actions**:
```bash
# Find all mock_datetime calls
grep -rn "mock_datetime(" testfixtures/tests/ > datetime_usage.txt
# Find all mock_date calls  
grep -rn "mock_date(" testfixtures/tests/ > date_usage.txt
# Find all mock_time calls
grep -rn "mock_time(" testfixtures/tests/ > time_usage.txt
```

**Deliverable**: Document categorizing all call patterns:
- Keyword-only calls: `mock_datetime(delta=0.5, strict=True)`
- Positional datetime args: `mock_datetime(2001, 1, 2, 3, 4, 5, 6, tzinfo)`
- Single instance: `mock_datetime(datetime(2001, 1, 1))`
- Explicit None: `mock_datetime(None, strict=True)`

### Step 1.2: Define Target Signatures
**Task**: Design explicit parameter signatures that support all identified usage patterns.

**Example Target for mock_datetime**:
```python
# Union overloads approach
@overload
def mock_datetime(*, tzinfo: TZInfo | None = None, delta: float | None = None, 
                 delta_type: str = 'seconds', date_type: type[date] = date, 
                 strict: bool = False) -> type[MockDateTime]: ...

@overload  
def mock_datetime(year: int, month: int, day: int, hour: int = 0, minute: int = 0,
                 second: int = 0, microsecond: int = 0, tzinfo: TZInfo | None = None, 
                 /, *, delta: float | None = None, delta_type: str = 'seconds',
                 date_type: type[date] = date, strict: bool = False) -> type[MockDateTime]: ...

@overload
def mock_datetime(default: datetime, /, *, tzinfo: TZInfo | None = None,
                 delta: float | None = None, delta_type: str = 'seconds', 
                 date_type: type[date] = date, strict: bool = False) -> type[MockDateTime]: ...

@overload
def mock_datetime(default: None, /, *, tzinfo: TZInfo | None = None,
                 delta: float | None = None, delta_type: str = 'seconds',
                 date_type: type[date] = date, strict: bool = False) -> type[MockDateTime]: ...

def mock_datetime(year_or_default=None, month=None, day=None, hour=0, minute=0, 
                 second=0, microsecond=0, tzinfo_pos=None, /, *,
                 tzinfo: TZInfo | None = None, delta: float | None = None,
                 delta_type: str = 'seconds', date_type: type[date] = date,
                 strict: bool = False) -> type[MockDateTime]:
```

**Key Insights**:
- Use positional-only parameters (`/`) for datetime components to prevent conflicts
- Use keyword-only parameters (`*`) for configuration options
- Handle tzinfo as both 8th positional argument AND keyword argument
- Maintain exact backward compatibility

## Phase 2: Implementation

### Step 2.1: Implement mock_datetime Redesign
**Task**: Replace `*args/**kwargs` with explicit signature supporting all usage patterns.

**Implementation Steps**:
1. Create new signature with positional-only and keyword-only sections
2. Add logic to handle tzinfo as both positional and keyword argument
3. Maintain exact compatibility with existing argument parsing logic
4. Add overloads that match the new signature exactly

**Key Compatibility Requirements**:
- `mock_datetime()` → keyword-only overload
- `mock_datetime(2001, 1, 1)` → positional overload (3 args)
- `mock_datetime(2001, 1, 1, 1, 2, 3)` → positional overload (6 args)
- `mock_datetime(2001, 1, 1, 1, 2, 3, 4, tz)` → positional overload (8 args)
- `mock_datetime(datetime_instance)` → single instance overload
- `mock_datetime(None)` → explicit None overload
- `mock_datetime(None, strict=True)` → None + keywords overload

**Test and Commit**:
```bash
mypy testfixtures && pytest testfixtures && git add -A && git commit -m "Redesign mock_datetime with explicit parameters"
```

### Step 2.2: Implement mock_date Redesign
**Task**: Similar redesign for mock_date (simpler - no tzinfo complexity).

**Target Signature**:
```python
def mock_date(year_or_default=None, month=None, day=None, /, *,
             delta: float | None = None, delta_type: str = 'days', 
             strict: bool = False) -> type[MockDate]:
```

**Test and Commit**: Same pattern as Step 2.1

### Step 2.3: Implement mock_time Redesign  
**Task**: Similar redesign for mock_time (similar to datetime but no tzinfo allowed).

**Target Signature**:
```python
def mock_time(year_or_default=None, month=None, day=None, hour=0, minute=0,
             second=0, microsecond=0, /, *, delta: float | None = None,
             delta_type: str = 'seconds') -> type[MockTime]:
```

**Test and Commit**: Same pattern as Step 2.1

## Phase 3: Overload Implementation

### Step 3.1: Add Comprehensive Overloads
**Task**: Add properly typed overloads for each redesigned function.

**For each function**:
1. Uncomment original overload structure
2. Fix all ellipsis with proper types (int = 0, TZInfo | None = None, etc.)
3. Ensure overload signatures exactly match implementation capabilities
4. Test that all usage patterns work with proper type checking

**Validation**:
```bash
# Should show improved type checking
mypy testfixtures --strict
# Should show no type errors in IDE/editor
```

## Phase 4: Method Overloads

### Step 4.1: Implement Method Overloads
**Task**: Apply same approach to MockDateTime.add, .set, .tick methods and equivalents for MockDate and MockTime.

**Process per method**:
1. Uncomment method overloads
2. Fix types (replace `...` with proper defaults)
3. Ensure compatibility with inherited base class methods
4. Test and commit

**Order**: MockDateTime methods → MockDate methods → MockTime methods

## Critical Implementation Details

### Tzinfo Handling Complexity
The most complex requirement is supporting tzinfo as both 8th positional argument AND keyword argument:

```python
# Both must work:
mock_datetime(2001, 1, 1, 1, 2, 3, 4, SampleTZInfo())  # 8th positional
mock_datetime(2001, 1, 1, tzinfo=SampleTZInfo())        # keyword
```

**Solution Strategy**:
```python
def mock_datetime(year_or_default=None, month=None, day=None, hour=0, minute=0,
                 second=0, microsecond=0, tzinfo_positional=None, /, *,
                 tzinfo: TZInfo | None = None, ...):
    # Resolve tzinfo from positional vs keyword
    resolved_tzinfo = tzinfo_positional if tzinfo_positional is not None else tzinfo
    # Continue with existing logic...
```

### Backward Compatibility Validation
**Essential Test**: All existing usage patterns must continue to work:

```python
# Test comprehensive compatibility
test_cases = [
    mock_datetime(),
    mock_datetime(tzinfo=SampleTZInfo()),
    mock_datetime(2002, 1, 1, 1, 2, 3),
    mock_datetime(2001, 1, 2, 3, 4, 5, 6, SampleTZInfo()),
    mock_datetime(datetime(2002, 1, 1, 1)),
    mock_datetime(None),
    mock_datetime(None, strict=True),
    mock_datetime(None, tzinfo=SampleTZInfo()),
    # ... etc for all patterns found in analysis
]
```

### Type Annotation Precision
**Goal**: Achieve maximum type safety while maintaining flexibility:

```python
# Before: Limited type information
mock_result = mock_datetime(2001, 1, 1)  # Returns type[MockDateTime] with no parameter hints

# After: Full type safety  
mock_result = mock_datetime(2001, 1, 1)  # MyPy knows exactly what parameters are valid
```

## Success Criteria

### Functional Requirements
- [ ] All 966 tests pass
- [ ] All existing usage patterns work identically
- [ ] MyPy shows no errors with `--strict` mode
- [ ] No type ignores on public APIs
- [ ] No casts introduced

### Type Safety Improvements
- [ ] IDE provides accurate parameter hints for all overloads
- [ ] Invalid usage caught at type-check time
- [ ] Return types properly inferred
- [ ] Method overloads provide precise signatures

### Maintainability
- [ ] Code is more readable with explicit signatures
- [ ] Type errors provide clear guidance to users
- [ ] Future changes easier to validate

## Rollback Strategy
Each commit is atomic, so rollback to any previous state is straightforward:
```bash
git log --oneline  # Find last working commit
git reset --hard <commit-hash>
```

## Expected Challenges

1. **Tzinfo dual-mode handling**: Requires careful parameter resolution logic
2. **Parameter name conflicts**: Need to avoid breaking keyword usage
3. **Overload precedence**: MyPy picks first matching overload, order matters
4. **Default value consistency**: Must match exact behavior of original implementation

## Validation Commands
Run after each change:
```bash
source .venv/bin/activate
mypy testfixtures
pytest testfixtures  
# If both pass, auto-commit and continue
```