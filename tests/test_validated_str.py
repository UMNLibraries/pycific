import re
from typing import Self

import pytest
from returns.result import Failure, Result, Success

from pycific.validated import ValidatedStr, ValidationError

class NumericStr(ValidatedStr):
    def _validate(self) -> Self:
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

def test_factory():
    match NumericStr.factory('123'):
        case Success(NumericStr() as numstr):
            assert isinstance(numstr, NumericStr)
        case Failure(ValidationError as should_not_happen):
            raise should_not_happen

    match NumericStr.factory('bogus'):
        case Success(NumericStr() as invalid_numeric_str):
            raise Exception(f'Attempt to validate {invalid_numeric_str} should have raised an exception')
        case Failure(ValidationError as validation_error):
            assert isinstance(validation_error, Exception)
            #print(f'{validation_error=}')
