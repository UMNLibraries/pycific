import re

import pytest

from pycific.validated import ValidatedStr, ValidationError

class NumericStr(ValidatedStr):
    def _validate(self) -> str:
        if not re.match(r'^\d{1,5}$', self):
            raise ValueError(f'NumericStr value {self} is invalid: must be one to five characters, all digits')
        return self

def test_types():
    numstr = NumericStr('123')
    for type in [str, ValidatedStr, NumericStr]:
        assert isinstance(numstr, type)
    assert numstr == '123'

def test_int_input():
    numstr = NumericStr(123)
    for type in [str, ValidatedStr, NumericStr]:
        assert isinstance(numstr, type)
    assert numstr == '123'
    assert not isinstance(numstr, int)

def test_invalid_value():
    with pytest.raises(ValidationError):
        NumericStr('bogus')
