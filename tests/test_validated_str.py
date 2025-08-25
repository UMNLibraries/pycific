from typing import Mapping, Sequence
import re

import pytest

from pycific.validated import ValidatedStr, ValidationError

class ExampleStr(ValidatedStr):
    def _validate(self) -> str:
        if not re.match(r'^\d{1,5}$', self):
            raise ValueError(f'ExampleStr value {self} is invalid: must be one to five characters, all digits')
        return self

def test_types():
    example = ExampleStr('123')
    for type in [str, ValidatedStr, ExampleStr]:
        assert isinstance(example, type)
    assert example == '123'

def test_int_input():
    example = ExampleStr(123)
    for type in [str, ValidatedStr, ExampleStr]:
        assert isinstance(example, type)
    assert example == '123'
    assert not isinstance(example, int)

def test_invalid_value():
    with pytest.raises(ValidationError):
        invalid_value_example = ExampleStr('bogus')
