from typing import Mapping, Sequence
import re

import pytest

from pycific.validated import ValidatedStr, ValidationError

class ExampleStr(ValidatedStr):
    def _validate(self) -> str:
        if not re.match(r'^\d{1,5}$', self):
            raise ValueError(f'ExampleStr value {self} is invalid: must be one to five characters, all digits')
        return self

@pytest.fixture
def example():
    return ExampleStr('123')

def test_types(example):
    assert isinstance(example, (str, ValidatedStr, ExampleStr))

def test_invalid_value():
    with pytest.raises(ValidationError):
        invalid_value_example = ExampleStr('bogus')
