from typing import Type, TypeVar, Mapping, Callable, Union, Iterable, Any, Generator, Tuple, Optional

T = TypeVar("T")


class SearchError(TypeError):
    pass


def searchable(search_key_types: Mapping[Type, Union[str, Iterable[str]]]) -> Callable[[T], T]:
    search_key_types = dict(search_key_types)

    # For each key type, we want to store the ordered attributes to query.
    # We accept attribute.sub_attribute, so split all target attributes on "."
    for key, types in search_key_types.items():
        if isinstance(types, str):
            types = [types]
        types = [type.split(".") for type in types]
        search_key_types[key] = types

    def search(instance: T, item: Any) -> bool:
        try:
            search_keys = search_key_types[type(item)]
        except KeyError:
            raise SearchError("Attempted to search for invalid type! Accepted types are {types}".format(types=[key_type.__name__ for key_type in search_key_types.keys()]))

        for search_key in search_keys:
            failed = False
            value = instance
            for sub_attribute in search_key:
                try:
                    value = getattr(value, sub_attribute)
                except AttributeError:
                    failed = True
                    break

            # This search key didn't exist for the item
            if failed:
                continue

            # Found the search item directly as an attribute
            if not isinstance(value, LazyList) and value == item:
                return True

            # Try to pass it along to the attribute's __contains__
            try:
                if item in value:
                    return True
            except (TypeError, SearchError):
                # The attribute doesn't define __contains__ or is searchable and doesn't accept this key type
                continue

    def decorator(cls: T) -> T:
        if hasattr(cls, "__contains__"):
            contains = cls.__contains__

            def new_contains(self, item: Any) -> bool:
                result = contains(self, item)

                # If it's contained by normal means, short circuit
                if result:
                    return True
                try:
                    # Try a search
                    if search(self, item):
                        return True
                except SearchError:
                    # Search doesn't accept that type
                    pass

                # Search and normal __contains__ implementations both were False
                return False
        else:
            new_contains = search

        cls.__contains__ = new_contains

        if cls.__doc__ is not None:
            cls.__doc__ += "\n\n"
        else:
            cls.__doc__ = ""
        cls.__doc__ += "Searchable by {types}".format(types=[key_type.__name__ for key_type in search_key_types.keys()])

        return cls

    return decorator


class SearchableList(list):
    def filter(self, function):
        return SearchableList(filter(function, self))

    def __getitem__(self, item: Any) -> Any:
        try:
            return list.__getitem__(self, item)
        except TypeError:
            return self.find(item)

    def __contains__(self, item: Any) -> bool:
        return self.contains(item)

    def __delitem__(self, item: Any) -> None:
        try:
            list.__delitem__(self, item)
        except TypeError:
            self.delete(item)

    def _search_generator(self, item: Any, reverse: bool = False) -> Generator[Any, None, None]:
        """A helper method for `self.search` that returns a generator rather than a list."""
        results = 0
        for _, x in self.enumerate(item, reverse=reverse):
            yield x
            results += 1
        if results == 0:
            raise SearchError(str(item))

    def search(self, item: Any, streaming: bool = False, reverse: bool = False) -> Union["SearchableList", Generator[Any, None, None]]:
        if streaming:
            return self._search_generator(item, reverse=reverse)
        else:
            result = SearchableList(x for _, x in self.enumerate(item, reverse=reverse))
            if len(result) == 0:
                raise SearchError(str(item))
            return result

    def find(self, item: Any, reverse: bool = False) -> Any:
        for _, x in self.enumerate(item, reverse=reverse):
            return x
        raise SearchError(str(item))

    def contains(self, item: Any) -> bool:
        for _, _ in self.enumerate(item):
            return True
        return False

    def enumerate(self, item: Any, reverse: bool = False) -> Generator[Tuple[int, Any], None, None]:
        items = self
        if reverse:
            max = len(items) - 1
            items = reversed(items)
        for index, x in enumerate(items):
            if x == item:
                yield max - index if reverse else index, x
                continue

            try:
                if item in x:
                    yield max - index if reverse else index, x
            except TypeError:
                # x doesn't define __contains__
                pass

    def delete(self, item: Any) -> None:
        deleted = 0
        for index, _ in self.enumerate(item, reverse=True):
            del self[index]
            deleted += 1
        if deleted == 0:
            raise SearchError(str(item))


class SearchableSet(set):
    def filter(self, function):
        return SearchableSet(filter(function, self))

    def __getitem__(self, item: Any) -> Any:
        return self.find(item)

    def __contains__(self, item: Any) -> bool:
        return self.contains(item)

    def __delitem__(self, item: Any) -> None:
        self.delete(item)

    def _search_generator(self, item: Any) -> Generator[Any, None, None]:
        """A helper method for `self.search` that returns a generator rather than a list."""
        results = 0
        for x in self.enumerate(item):
            yield x
            results += 1
        if results == 0:
            raise SearchError(str(item))

    def search(self, item: Any, streaming: bool = False) -> Union["SearchableSet", Generator[Any, None, None]]:
        if streaming:
            return self._search_generator(item)
        else:
            result = SearchableSet(self.enumerate(item))
            if len(result) == 0:
                raise SearchError(str(item))
            return result

    def find(self, item: Any) -> Any:
        for x in self.enumerate(item):
            return x
        raise SearchError(str(item))

    def contains(self, item: Any) -> bool:
        for _ in self.enumerate(item):
            return True
        return False

    def enumerate(self, item: Any) -> Generator[Any, None, None]:
        for x in self:
            if x == item:
                yield x
                continue

            try:
                if item in x:
                    yield x
            except TypeError:
                # x doesn't define __contains__
                pass

    def delete(self, item: Any) -> None:
        to_delete = set(self.enumerate(item))
        if len(to_delete) == 0:
            raise SearchError(str(item))
        for x in to_delete:
            self.remove(x)


class SearchableDictionary(dict):
    def filter(self, function):
        return SearchableDictionary(filter(function, self.items()))

    def __getitem__(self, item: Any) -> Any:
        try:
            return dict.__getitem__(self, item)
        except KeyError:
            return self.find(item)

    def __contains__(self, item: Any) -> bool:
        return self.contains(item)

    def __delitem__(self, item: Any) -> None:
        try:
            dict.__delitem__(self, item)
        except KeyError:
            self.delete(item)

    def _search_generator(self, item: Any) -> Generator[Tuple[Any, Any], None, None]:
        """A helper method for `self.search` that returns a generator rather than a list."""
        results = 0
        for key, value in self.enumerate(item):
            yield key, value
            results += 1
        if results == 0:
            raise SearchError(str(item))

    def search(self, item: Any, streaming: bool = False) -> Union["SearchableDictionary", Generator[Tuple[Any, Any], None, None]]:
        if streaming:
            return self._search_generator(item)
        else:
            result = SearchableDictionary(self.enumerate(item))
            if len(result) == 0:
                raise SearchError(str(item))
            return result

    def find(self, item: Any) -> Tuple[Any, Any]:
        for key, value in self.items():
            if key == item:
                return key, value

            try:
                if item in key:
                    return key, value
            except TypeError:
                # key doesn't define __contains__
                pass

            if value == item:
                return key, value

            try:
                if item in value:
                    return key, value
            except TypeError:
                # value doesn't define __contains__
                pass
        raise SearchError(str(item))

    def contains(self, item: Any) -> bool:
        for _, _ in self.enumerate(item):
            return True
        return False

    def enumerate(self, item: Any) -> Generator[Tuple[Any, Any], None, None]:
        for key, value in self.items():
            if key == item:
                yield key, value
                continue

            try:
                if item in key:
                    yield key, value
                    continue
            except TypeError:
                # key doesn't define __contains__
                pass

            if value == item:
                yield key, value
                continue

            try:
                if item in value:
                    yield key, value
                    continue
            except TypeError:
                # value doesn't define __contains__
                pass

    def delete(self, item: Any) -> None:
        to_delete = {key for key, _ in self.enumerate(item)}
        if len(to_delete) == 0:
            raise SearchError(str(item))
        for key in to_delete:
            del self[key]


class LazyList(list):
    """A list where the values of the list are generated on-demand.

    Arguments:
        constructor (callable): A function that returns a generator of the values to be put in the list.
    """
    def __init__(self, generator: Optional[Generator]=None, known_data: Optional[list]=None):
        self._generator = generator
        if self._generator is None:
            self._empty = True
        else:
            self._empty = False
        if known_data:
            super().__init__(known_data)  # initialize from known data
        else:
            super().__init__()  # initialize an empty list

    def __str__(self):
        if self._empty:
            return list.__str__(self)
        else:
            string = list.__str__(self)
            if string == "[]":
                return "[...]"
            else:
                return string[:-1] + ", ...]"

    def __iter__(self):
        for item in super().__iter__():
            yield item
        while not self._empty:
            try:
                yield next(self)
            except StopIteration:
                return

    def __len__(self):
        if self._empty:
            return super().__len__()
        else:
            self._generate_more()
            return super().__len__()

    def __next__(self):
        try:
            value = next(self._generator)
            super().append(value)
        except StopIteration as error:
            self._empty = True
            raise error
        return value

    def _generate_more(self, count: Optional[int] = None):
        if count is not None:
            for _ in range(count):
                next(self)
        else:
            for _ in self:
                pass
            assert self._empty

    def _create_sliced_lazy_list(self, s: slice) -> "LazyList":
        num_already_generated = super().__len__()

        def gen(start, stop, step):
            count = start
            while count < stop:
                try:
                    x = self[count]
                    if not self._empty:
                        yield x
                    else:
                        raise StopIteration
                except SearchError:
                    raise StopIteration
                count += step

        already_known = []
        if s.start < num_already_generated:
            already_known_end = min(s.stop, num_already_generated)
            already_known = self[s.start:already_known_end]
            gen_start = already_known_end + 1
        else:
            gen_start = s.start
        gen = gen(gen_start, s.stop, s.step)
        new = LazyList(generator=gen, known_data=already_known)
        return new

    def __getitem__(self, item: Any) -> Any:
        """
        Options:

        `item` is a single integer:
            Simply return the one item in the list.
            Generate data up until that item if necessary.

        `item` is a slice:
            Options:

            list[:]    start=0, stop=None, step=1
            list[x:]   start=x, stop=None, step=1
            list[:y]   start=0, stop=y, step=1
            list[x:y]  start=x, stop=y, step=1
            all of the above with step!=1

            Returns a generator.
        """
        is_slice = isinstance(item, slice)
        if not is_slice:
            if isinstance(item, int) and item < 0:
                stop = None  # Generate data until the end so that we can iterate backwards
            else:
                stop = item
        else:
            # If all the data has been generated, just return the sliced list
            if self._empty:
                return LazyList(generator=None, known_data=list.__getitem__(self, item))

            # Even if we don't have all the data, we might have enough of it to return normally
            if item.stop is not None and super().__len__() >= item.stop - 1:
                # [:10] requires super().__len__() >= 9 = 10 - 1
                return LazyList(generator=None, known_data=list.__getitem__(self, item))

            # We don't have enough data, so we need to generate the data on-the-fly as the list is iterated over
            item = slice(item.start or 0, item.stop or float("inf"), item.step or 1)
            return self._create_sliced_lazy_list(item)

        # If we reach this code, `item` is not a slice (although it might be part of a slice)
        try:
            return list.__getitem__(self, item)
        except IndexError:
            # Generate new values until: 1) we get to position `item` (which is an int) or 2) no more values are left
            generate_n_more = stop - super().__len__() + 1 if stop is not None else None
            try:
                self._generate_more(generate_n_more)
            except StopIteration:
                pass
            # Now that we have 1) enough or 2) all the values, try returning again.
            return list.__getitem__(self, item)

    def __delitem__(self, item: Any) -> None:
        is_slice = isinstance(item, slice)
        if not is_slice:
            if isinstance(item, int) and item < 0:
                stop = None  # Generate data until the end so that we can iterate backwards
            else:
                stop = item
            try:
                return list.__delitem__(self, item)
            except IndexError:
                # Generate new values until: 1) we get to position `item` (which is an int) or 2) no more values are left
                generate_n_more = stop - super().__len__() + 1 if stop is not None else None
                try:
                    self._generate_more(generate_n_more)
                except StopIteration:
                    pass
                # Now that we have 1) enough or 2) all the values, try deleting again.
                return list.__delitem__(self, item)
        else:
            # If all the data has been generated, just delete the sliced list
            if self._empty:
                return list.__delitem__(self, item)

            # Even if we don't have all the data, we might have enough of it to delete normally
            if item.stop is not None and super().__len__() >= item.stop - 1:
                # [:10] requires super().__len__() >= 9 = 10 - 1
                return list.__delitem__(self, item)

            # We don't have enough data, so we need to generate the data on-the-fly as the list is iterated over
            item = slice(item.start or 0, item.stop or float("inf"), item.step or 1)
            if item.stop is None or item.stop is float("inf"):
                self._generate_more()
            else:
                last = range(item.start, item.stop, item.step)[-1]
                try:
                    self._generate_more(last)
                except StopIteration:
                    pass
            return list.__delitem__(self, item)

    def __reversed__(self):
        self._generate_more()
        return super().__reversed__()

    def __contains__(self, item):
        if super().__contains__(item):
            return True
        while not self._empty:
            try:
                self._generate_more(1)
                if list.__getitem__(self, -1) == item:
                    return True
            except StopIteration:
                pass
        return False

    def append(self, item):
        if not self._empty:
            self._generate_more()
        super().append(item)

    def clear(self):
        self._generator = None
        self._empty = True
        return super().clear()

    def copy(self):
        if not self._empty:
            self._generate_more()
        return LazyList(known_data=list(self))

    def count(self, object):
        if not self._empty:
            self._generate_more()
        return super().count(object)

    def extend(self, iterable):
        if not self._empty:
            self._generate_more()
        return super().extend(iterable)

    def index(self, object, start: int = 0, stop: int = 9223372036854775807):
        try:
            return super().index(object, start, stop)
        except ValueError:
            while not self._empty:
                self._generate_more(1)
                if list.__getitem__(self, -1) == object:
                    return super().__len__() -1
        raise ValueError(f"{object} is not in LazyList")

    def insert(self, index: int, object):
        if not self._empty and super().__len__() < index:
            generate_n_more = index - super().__len__()
            try:
                self._generate_more(generate_n_more)
            except StopIteration:
                pass
        return super().insert(index, object)

    def pop(self, index: int = -1):
        if not self._empty:
            self._generate_more()
        return super().pop(index)

    def remove(self, object):
        for i, item in enumerate(self):
            if item == object:
                del self[i]

    def reverse(self):
        self._generate_more()
        return super().reverse()

    def sort(self, *, key=None, reverse=False):
        if not self._empty:
            self._generate_more()
        return super().sort(key=key, reverse=reverse)

    def __add__(self, other):
        raise NotImplementedError

    def __eq__(self, other):
        raise NotImplementedError

    def __ne__(self, other):
        raise NotImplementedError

    def __ge__(self, other):
        raise NotImplementedError

    def __le__(self, other):
        raise NotImplementedError


class SearchableLazyList(LazyList, SearchableList):
    def __getitem__(self, item):
        try:
            if not isinstance(item, (int, slice)):
                raise TypeError
            return LazyList.__getitem__(self, item)
        except TypeError:
            return SearchableList.__getitem__(self, item)
