from typing import Mapping, Sequence

import pytest

from pycific.validated import ValidatedPMap, ValidatedPMapSpec, ValidationError
#from pyrsistent.typing import PMap
from pyrsistent._pmap import PMap
from pyrsistent._pvector import PVector

from returns.result import Failure, Result, Success

class ExampleMapValidated(ValidatedPMapSpec):
    foo: str
    bar: PVector
    baz: PMap

class ExampleMap(ValidatedPMap):
    def _validate(self) -> ExampleMapValidated:
        return ExampleMapValidated(
            foo=self.foo,
            bar=self.bar,
            baz=self.baz,
        )

example_dict = {
    'foo': 'manchoo',
    'bar': ['the', 'door'],
    'baz': {
        'names': {'given': 'Mark', 'middle': ['Anthony'], 'nick': ['Baz'], 'surname': 'Luhrmann'},
        'titles': ['AC'],
        'movies': ['Strictly Ballroom', 'Romeo + Juliet', 'Moulin Rouge!'],
    },
    'extra': {'extra': 'Read all about it!'},
}

@pytest.fixture
def example():
    return ExampleMap(example_dict)

def test_types(example):
    for type in [PMap, ValidatedPMap, ExampleMap]:
        assert isinstance(example, type)
    
    assert isinstance(example.foo, str)

    # Verify that nested values are also pyrsistent:
    assert isinstance(example.bar, PVector)
    assert isinstance(example.baz, PMap)
    assert isinstance(example.baz.names, PMap)
    assert isinstance(example.baz.names.middle, PVector)
    assert isinstance(example.baz.names.nick, PVector)
    assert isinstance(example.baz.movies, PVector)

    assert isinstance(example.validated, ExampleMapValidated)

    # Verify that the elements of the validated subset have the correct types:
    assert isinstance(example.validated.foo, str)
    assert isinstance(example.validated.bar, PVector)
    assert isinstance(example.validated.baz, PMap)

def test_inclusion_exclusion(example):
    # Verify that the 'validated' property is excluded from the ValidatedPMap keys:
    assert 'validated' not in example.keys()

    # Verify that extra, unvalidated fields are included:
    assert isinstance(example.extra, PMap)

def test_missing_key():
    with pytest.raises(ValidationError):
        missing_key_example = ExampleMap({'foo': 'kung', 'bar': [1, 2, 3]})

def test_bogus_value():
    with pytest.raises(ValidationError):
        bogus_value_example = ExampleMap({'foo': 'kung', 'bar': None, 'baz': {'profession': 'filmmaker'}})

def test_factory():
    match ExampleMap.factory(example_dict):
        case Success(ExampleMap() as example):
            assert isinstance(example, ExampleMap)
        case Failure(ValidationError as should_not_happen):
            raise should_not_happen

    match ExampleMap.factory({'foo': 'kung', 'bar': None, 'baz': {'profession': 'filmmaker'}}):
        case Success(ExampleMap() as bogus_value_example):
            raise Exception(f'Attempt to validate {bogus_value_example} should have raised an exception')
        case Failure(ValidationError as validation_error):
            assert isinstance(validation_error, Exception)
            #print(f'{validation_error=}')
