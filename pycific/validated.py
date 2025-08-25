from abc import ABC, abstractmethod
from functools import cached_property
from typing import Mapping

from pydantic import BaseModel

from pyrsistent import freeze, pmap, pvector
from pyrsistent._pmap import PMap

class ValidationError(ValueError):
    pass

class ValidatedStr(str, ABC):
    def __new__(cls, value):
        self = super().__new__(cls, value)
        try:
            self._validate()
        except Exception as e:
            raise ValidationError('Attempt to validate input failed during ValidatedStr instantiation')
        return self

    @abstractmethod
    def _validate(self):
        ...

class ValidatedPMap(PMap, ABC):
    def __new__(cls, initial:Mapping={}, pre_size=0, *args, **kwargs):

        # Ensure that all values within the initial Mapping are pyrsistent (immutable):
        for k, v in initial.items():
            initial[k] = freeze(v)

        initial, buckets = cls._turbo_mapping(initial, pre_size)

        #return PMap(len(initial), pvector().extend(buckets))
        self = super().__new__(cls, len(initial), pvector().extend(buckets), *args, **kwargs)

        try:
            self._validate()
            # TODO: Explain why we don't use the following, due to pyrsistent confusion in the case of validation errors.
            # Also explain why we wanted to use it, to cahce the reuslt right away.
            #valid = self.validated
        # TODO: Explain why we don't use pydantic's validation error, which is because other pyrsistent or other things
        # may also throw errors/exceptions. We just catch all of them and report that the attempt to validate failed.
        #except ValidationError as ve: 
        except Exception as e:
            raise ValidationError('Attempt to validate input failed during ValidatedPMap instantiation')
        return self

    @abstractmethod
    def _validate(self):
        ...

    @cached_property
    def validated(self):
        return self._validate()

    @classmethod
    def _turbo_mapping(cls, initial:Mapping={}, pre_size=0):
        # TODO: Add explanation for copying and pasting this function from pyrsistent.
        if pre_size:
            size = pre_size
        else:
            try:
                size = 2 * len(initial) or 8
            except Exception:
                # Guess we can't figure out the length. Give up on length hinting,
                # we can always reallocate later.
                size = 8

        buckets = size * [None]

        if not isinstance(initial, Mapping):
            # Make a dictionary of the initial data if it isn't already,
            # that will save us some job further down since we can assume no
            # key collisions
            initial = dict(initial)

        for k, v in initial.items():
            h = hash(k)
            index = h % size
            bucket = buckets[index]

            if bucket:
                bucket.append((k, v))
            else:
                buckets[index] = [(k, v)]

        return (initial, buckets)

# TODO: Add explanation for why we don't use strict=True
class ValidatedPMapSpec(BaseModel, frozen=True, arbitrary_types_allowed=True):
    pass
