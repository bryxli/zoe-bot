"""
This file defines one class, called Ghost, that can be instantiated with a subset of its data, and any data that is
accessed is loaded when accessed for the first time. (See also https://en.wikipedia.org/wiki/Lazy_loading#Ghost)

When a Ghost is instantiated with a subset of its data, any attribute that is accessed that only needs data that was
give at init will not trigger a load.

Creating a Ghost object:

Ghost objects should have property methods that are decorated with `@Ghost.property`, indicating that the underlying
method is a property and should be ghost loaded if it throws a GhostLoadingRequiredError (i.e. if the data it is
accessing does not exist).

`Ghost.property` takes an optional argument specifying which load group it belongs to. Methods that belong to the same
load group will be tagged as loaded when any one of the methods triggers a load. If a load group is not given to the
decorator, the load group will be set as the method name. Only one load group is allowed per method (currently).

The object must define a `__load__` method which sets the necessary data on the object.

If an object is instantiated with all of its data, it is not considered loaded.

Methods cannot be ghost loaded because it is impossible to know if the method will fail a priori.
Therefore `Ghost.method` does not exist, and only properties can use ghost loading.
"""
from abc import abstractmethod
from typing import Callable, Union, Any
import functools

from merakicommons.cache import lazy_property


class GhostLoadingRequiredError(Exception):
    pass


def ghost_load_on(*errors):
    def decorator(method):
        @functools.wraps(method)
        def wrapper(*args, **kwargs):
            try:
                return method(*args, **kwargs)
            except errors as error:
                raise GhostLoadingRequiredError(str(error))
        return wrapper
    return decorator


class Ghost(object):
    @lazy_property
    def __load_groups(self) -> set:
        load_groups = set()
        for cls in self.__class__.__mro__:
            if cls is Ghost:
                # We won't have any Ghost properties in the mro past Ghost
                break

            for attr in vars(cls).values():
                if isinstance(attr, Ghost.__property):
                    load_groups.add(attr.fget._Ghost__load_group)
        return load_groups

    @abstractmethod
    def __load__(self, load_group: Any) -> None:
        pass

    def __is_loaded(self, load_group: Any) -> bool:
        try:
            return load_group in self._Ghost__loaded_groups
        except AttributeError:
            return False

    @property
    def __all_loaded(self) -> bool:
        try:
            return self._Ghost__all_loaded_status
        except AttributeError:
            return False

    class __property(property):
        def __get__(self, obj: Any, obj_type: type = None) -> Any:
            if obj is None:
                return self
            if self.fget is None:
                raise AttributeError("unreadable attribute")

            try:
                return self.fget(obj)
            except GhostLoadingRequiredError:
                load_group = self.fget._Ghost__load_group
                obj.__load__(load_group)
                obj._Ghost__set_loaded(load_group)

                return self.fget(obj)

    def __set_loaded(self, load_group) -> None:
        try:
            self._Ghost__loaded_groups.add(load_group)
        except AttributeError:
            self._Ghost__loaded_groups = {load_group}

        if self._Ghost__load_groups.issubset(self._Ghost__loaded_groups):
            self._Ghost__all_loaded_status = True

    @staticmethod
    def property(load_group_or_method: Union[Callable[[Any], Any], Any]) -> Union[property, Callable[[Callable[[Any], Any]], property]]:
        # Default behavior when no load group is provided. Set the load group to the method name.
        if isinstance(load_group_or_method, Callable) and not isinstance(load_group_or_method, type):
            method = load_group_or_method
            load_group = method.__name__
            method._Ghost__load_group = load_group

        # Set the load group as provided in the decorator
        else:
            load_group = load_group_or_method

        # The load_group and method variables need to be set correctly before this function defintion.
        def decorator(method: Callable) -> property:
            method._Ghost__load_group = load_group
            prop = Ghost.__property(method)
            prop._Ghost__load_group = load_group
            return prop

        if isinstance(load_group_or_method, Callable) and not isinstance(load_group_or_method, type):
            return decorator(method)
        else:
            return decorator
