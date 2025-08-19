import pytest

from tests import immutable_module as module

def test_modify_attribute():
    with pytest.raises(AttributeError):
        module.attribute = 'bar'

def test_add_attribute():
    with pytest.raises(AttributeError):
        module.nonexistent_attribute = 'baz'

def test_delete_attribute():
    with pytest.raises(AttributeError):
        del module.attribute

# Functions are attributes, too. The following functions exist
# mostly to remind and reassure ourselves that immutability
# works the same way for functions.

def test_modify_function():
    with pytest.raises(AttributeError):
        module.fun = lambda x: print(f'Hello, {x}!')

def test_add_function():
    with pytest.raises(AttributeError):
        module.nonexistent_function = lambda x: print(f'Hello, {x}!')

def test_delete_function():
    with pytest.raises(AttributeError):
        del module.fun
