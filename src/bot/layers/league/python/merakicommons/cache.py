from functools import wraps
from typing import Callable, Any, TypeVar
from threading import Lock
from collections import defaultdict
import datetime

T = TypeVar("T")


def lazy(method: Callable[[Any], T]) -> Callable[[Any], T]:
    @wraps(method)
    def wrapper(self) -> T:
        s = "_lazy__{}".format(method.__name__)
        try:
            return getattr(self, s)
        except AttributeError:
            value = method(self)
            setattr(self, s, value)
            return value

    def _lazy_reset(self) -> None:
        s = "_lazy__{}".format(method.__name__)
        try:
            delattr(self, s)
        except KeyError:
            pass

    def _lazy_set(self, value) -> None:
        s = "_lazy__{}".format(method.__name__)
        setattr(self, s, value)

    wrapper._lazy_reset = _lazy_reset
    wrapper._lazy_set = _lazy_set

    return wrapper


def lazy_property(method: Callable[[Any], T]) -> property:
    return property(lazy(method))


class _CacheSegment(object):
    def __init__(self) -> None:
        self._data = defaultdict(dict)
        self._lock = Lock()

    def put(self, type: Any, key: Any, value: Any, timeout: int = -1) -> None:
        if timeout != 0:
            with self._lock:
                if timeout != -1:
                    timeout = datetime.timedelta(seconds=timeout)
                self._data[type][key] = (value, timeout, datetime.datetime.now())

    def get(self, type: Any, key: Any) -> Any:
        with self._lock:
            item, timeout, entered = self._data[type][key]
            if timeout == -1:
                return item
            now = datetime.datetime.now()
            if now > entered + timeout:
                self._data[type].pop(key)
                raise KeyError
            else:
                return item

    def get_all(self, type: Any):
        with self._lock:
            results = []
            for key, (item, timeout, entered) in self._data[type].items():
                if timeout == -1:
                    results.append(item)
                now = datetime.datetime.now()
                if now > entered + timeout:
                    self._data[type].pop(key)
                else:
                    results.append(item)
        return results

    def delete(self, type: Any, key: Any) -> None:
        with self._lock:
            del self._data[type][key]

    def contains(self, type: Any, key: Any) -> bool:
        with self._lock:
            return self._data[type].__contains__(key)

    def expire(self, type: Any = None):
        if type is None:
            types = set(self._data.keys())
        else:
            types = {type}
        for type in types:
            for key in self._data[type]:
                self.get(type, key)


# TODO: In development. Interface here for beginning integration.
class Cache(_CacheSegment):
    pass
