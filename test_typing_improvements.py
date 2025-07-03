#!/usr/bin/env python3
"""
Test script to demonstrate the typing improvements.

Run with: mypy test_typing_improvements.py

This should show type errors for invalid delta_type values.
"""

from testfixtures import mock_datetime, mock_date, mock_time

# These should work fine (valid literal values)
dt_mock1 = mock_datetime(delta_type='seconds')  # ✓ Valid
dt_mock2 = mock_datetime(delta_type='hours')    # ✓ Valid  
dt_mock3 = mock_datetime(delta_type='days')     # ✓ Valid

date_mock1 = mock_date(delta_type='days')       # ✓ Valid
date_mock2 = mock_date(delta_type='weeks')      # ✓ Valid

time_mock1 = mock_time(delta_type='seconds')    # ✓ Valid
time_mock2 = mock_time(delta_type='milliseconds')  # ✓ Valid

# These should produce mypy errors (invalid literal values) 
dt_mock_bad1 = mock_datetime(delta_type='invalid')     # ✗ Should error
dt_mock_bad2 = mock_datetime(delta_type='years')       # ✗ Should error

date_mock_bad1 = mock_date(delta_type='invalid')       # ✗ Should error  
date_mock_bad2 = mock_date(delta_type='months')        # ✗ Should error

time_mock_bad1 = mock_time(delta_type='invalid')       # ✗ Should error
time_mock_bad2 = mock_time(delta_type='years')         # ✗ Should error

print("If mypy reports errors above, the Literal typing is working!")