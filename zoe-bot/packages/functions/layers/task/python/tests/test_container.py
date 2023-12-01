import pytest

from merakicommons.container import SearchError, searchable, SearchableList, SearchableSet, SearchableDictionary, LazyList, SearchableLazyList

VALUE_COUNT = 100

# Seriously where is this in the std lib...
GENERATOR_CLASS = (None for _ in range(0)).__class__


@searchable({str: "strings"})
class Inner(object):
    def __init__(self, strings):
        self.strings = strings


@searchable({Inner: "inner", str: ["strings", "inner"], int: "integer", float: "normal.value"})
class Outer(object):
    def __init__(self, inner, normal, strings, integer):
        self.inner = inner
        self.normal = normal
        self.strings = strings
        self.integer = integer


@searchable({str: "strings"})
class ContainsDefined(object):
    def __init__(self, strings):
        self.strings = strings

    def __contains__(self, item):
        return isinstance(item, int)


class NonSearchable(object):
    def __init__(self, value):
        self.value = value


inner = Inner(["hello", "world"])
normal = NonSearchable(100.0)
outer = Outer(inner, normal, ["cat", "dog"], 100)
other = Inner(["foo", "bar"])
defined = ContainsDefined(["larry", "moe", "curly"])
list_ = SearchableList([other, normal, outer, inner, defined])
set_ = SearchableSet({other, normal, outer, inner, defined})
dict_ = SearchableDictionary({other: outer, inner: normal, "value": defined})


def test_simple_search():
    assert 100 in outer
    assert 0 not in outer


def test_bad_type():
    with pytest.raises(SearchError):
        100.0 in inner


def test_nested_key():
    assert 100.0 in outer
    assert 0.0 not in outer


def test_pass_through():
    assert "hello" in inner
    assert "world" in inner
    assert "cat" not in inner
    assert "dog" not in inner
    assert "foo" not in inner
    assert "bar" not in inner


def test_nested_object():
    assert inner in outer
    assert other not in outer

    assert "hello" in outer
    assert "world" in outer
    assert "foo" not in outer
    assert "bar" not in outer


def test_contains_defined():
    assert 0 in defined
    assert 100 in defined

    assert 0.0 not in defined
    assert 100.0 not in defined

    assert "larry" in defined
    assert "moe" in defined
    assert "curly" in defined
    assert "hello" not in defined
    assert "world" not in defined


# List #

def test_list_index():
    assert list_[0] is other
    assert list_[1] is normal
    assert list_[2] is outer
    assert list_[3] is inner
    assert list_[4] is defined
    for i in range(5, VALUE_COUNT):
        with pytest.raises(IndexError):
            list_[i]


def test_simple_list_membership():
    assert other in list_
    assert normal in list_
    assert outer in list_
    assert inner in list_
    assert defined in list_


def test_simple_list_contains():
    assert list_.contains(other)
    assert list_.contains(normal)
    assert list_.contains(outer)
    assert list_.contains(inner)
    assert list_.contains(defined)


def test_nested_list_membership():
    assert "hello" in list_
    assert "world" in list_
    assert "cat" in list_
    assert "dog" in list_
    assert "foo" in list_
    assert "bar" in list_
    assert "larry" in list_
    assert "moe" in list_
    assert "curly" in list_
    assert 0 in list_
    assert 100 in list_
    assert 100.0 in list_

    assert "value" not in list_
    assert 0.0 not in list_
    assert bytes() not in list_


def test_nested_list_contains():
    assert list_.contains("hello")
    assert list_.contains("world")
    assert list_.contains("cat")
    assert list_.contains("dog")
    assert list_.contains("foo")
    assert list_.contains("bar")
    assert list_.contains("larry")
    assert list_.contains("moe")
    assert list_.contains("curly")
    assert list_.contains(0)
    assert list_.contains(100)
    assert list_.contains(100.0)

    assert not list_.contains("value")
    assert not list_.contains(0.0)
    assert not list_.contains(bytes())


def test_enumerate_list():
    result = list_.enumerate("dog")
    assert isinstance(result, GENERATOR_CLASS)
    result = zip(result, [2], [outer])
    for one, index, two in result:
        i, one = one
        assert index == i
        assert one is two

    result = list_.enumerate("hello")
    assert isinstance(result, GENERATOR_CLASS)
    result = zip(result, [2, 3], [outer, inner])
    for one, index, two in result:
        i, one = one
        assert index == i
        assert one is two

    result = list_.enumerate("hello", reverse=True)
    assert isinstance(result, GENERATOR_CLASS)
    result = zip(result, [3, 2], [inner, outer])
    for one, index, two in result:
        i, one = one
        assert index == i
        assert one is two

    result = list_.enumerate("value")
    assert isinstance(result, GENERATOR_CLASS)
    result = zip(result, [], [])
    for one, index, two in result:
        i, one = one
        assert index == i
        assert one is two


def test_find_list():
    result = list_.find("dog")
    assert result is outer

    result = list_.find("hello")
    assert result is outer

    result = list_.find("hello", reverse=True)
    assert result is inner

    with pytest.raises(SearchError):
        list_.find("value")


def test_search_list():
    result = list_.search("dog")
    assert isinstance(result, SearchableList)
    result = zip(result, [outer])
    for one, two in result:
        assert one is two

    result = list_.search("hello")
    assert isinstance(result, SearchableList)
    result = zip(result, [outer, inner])
    for one, two in result:
        assert one is two

    result = list_.search("hello", reverse=True)
    assert isinstance(result, SearchableList)
    result = zip(result, [inner, outer])
    for one, two in result:
        assert one is two

    with pytest.raises(SearchError):
        list_.search("value")


def test_delete_list_index():
    list_ = SearchableList([other, normal, outer, inner, defined])
    for i in range(5, VALUE_COUNT):
        with pytest.raises(IndexError):
            del list_[i]

    assert list_ == [other, normal, outer, inner, defined]

    del list_[2]
    assert list_ == [other, normal, inner, defined]

    del list_[0]
    assert list_ == [normal, inner, defined]

    del list_[2]
    assert list_ == [normal, inner]

    del list_[1]
    assert list_ == [normal]

    del list_[0]
    assert list_ == []


def test_delete_list_key():
    list_ = SearchableList([other, normal, outer, inner, defined])

    with pytest.raises(SearchError):
        del list_["value"]

    with pytest.raises(SearchError):
        del list_[0.0]

    with pytest.raises(SearchError):
        del list_[bytes()]

    assert list_ == [other, normal, outer, inner, defined]

    del list_["hello"]
    assert list_ == [other, normal, defined]

    del list_[normal]
    assert list_ == [other, defined]

    del list_["foo"]
    assert list_ == [defined]

    del list_[defined]
    assert list_ == []


def test_list_delete():
    list_ = SearchableList([other, normal, outer, inner, defined])

    with pytest.raises(SearchError):
        list_.delete("value")

    with pytest.raises(SearchError):
        list_.delete(0.0)

    with pytest.raises(SearchError):
        list_.delete(bytes())

    assert list_ == [other, normal, outer, inner, defined]

    list_.delete("hello")
    assert list_ == [other, normal, defined]

    list_.delete(normal)
    assert list_ == [other, defined]

    list_.delete(0)
    assert list_ == [other]

    list_.delete("foo")
    assert list_ == []


# Set #

def test_simple_set_membership():
    assert other in set_
    assert normal in set_
    assert outer in set_
    assert inner in set_
    assert defined in set_


def test_simple_set_contains():
    assert set_.contains(other)
    assert set_.contains(normal)
    assert set_.contains(outer)
    assert set_.contains(inner)
    assert set_.contains(defined)


def test_nested_set_membership():
    assert "hello" in set_
    assert "world" in set_
    assert "cat" in set_
    assert "dog" in set_
    assert "foo" in set_
    assert "bar" in set_
    assert "larry" in set_
    assert "moe" in set_
    assert "curly" in set_
    assert 0 in set_
    assert 100 in set_
    assert 100.0 in set_

    assert "value" not in set_
    assert 0.0 not in set_
    assert bytes() not in set_


def test_nested_set_contains():
    assert set_.contains("hello")
    assert set_.contains("world")
    assert set_.contains("cat")
    assert set_.contains("dog")
    assert set_.contains("foo")
    assert set_.contains("bar")
    assert set_.contains("larry")
    assert set_.contains("moe")
    assert set_.contains("curly")
    assert set_.contains(0)
    assert set_.contains(100)
    assert set_.contains(100.0)

    assert not set_.contains("value")
    assert not set_.contains(0.0)
    assert not set_.contains(bytes())


def test_enumerate_set():
    result = set_.enumerate("dog")
    assert isinstance(result, GENERATOR_CLASS)
    expected = {outer}
    assert expected == set(result)

    result = set_.enumerate("hello")
    assert isinstance(result, GENERATOR_CLASS)
    expected = {outer, inner}
    assert expected == set(result)

    result = set_.enumerate("value")
    assert isinstance(result, GENERATOR_CLASS)
    expected = set()
    assert expected == set(result)


def test_find_set():
    result = set_.find("dog")
    assert result in {outer}

    result = set_.find("hello")
    assert result in {outer, inner}

    with pytest.raises(SearchError):
        set_.find("value")


def test_search_set():
    result = set_.search("dog")
    assert isinstance(result, SearchableSet)
    expected = {outer}
    assert expected == set(result)

    result = set_.search("hello")
    assert isinstance(result, SearchableSet)
    expected = {outer, inner}
    assert expected == set(result)

    with pytest.raises(SearchError):
        set_.search("value")


def test_delete_set_key():
    set_ = SearchableSet({other, normal, outer, inner, defined})

    with pytest.raises(SearchError):
        del set_["value"]

    with pytest.raises(SearchError):
        del set_[0.0]

    with pytest.raises(SearchError):
        del set_[bytes()]

    assert set_ == {other, normal, outer, inner, defined}

    del set_["hello"]
    assert set_ == {other, normal, defined}

    del set_[normal]
    assert set_ == {other, defined}

    del set_["foo"]
    assert set_ == {defined}

    del set_[defined]
    assert set_ == set()


def test_set_delete():
    set_ = SearchableSet({other, normal, outer, inner, defined})
    with pytest.raises(SearchError):
        set_.delete("value")

    with pytest.raises(SearchError):
        set_.delete(0.0)

    with pytest.raises(SearchError):
        set_.delete(bytes())

    assert set_ == {other, normal, outer, inner, defined}

    set_.delete("hello")
    assert set_ == {other, normal, defined}

    set_.delete(normal)
    assert set_ == {other, defined}

    set_.delete(0)
    assert set_ == {other}

    set_.delete("foo")
    assert set_ == set()


# Dictionary #

def test_dict_key():
    assert dict_[other] is outer
    assert dict_[inner] is normal
    assert dict_["value"] is defined

    with pytest.raises(SearchError):
        dict_["tionary"]


def test_simple_dict_membership():
    assert other in dict_
    assert normal in dict_
    assert outer in dict_
    assert inner in dict_
    assert "value" in dict_
    assert defined in dict_


def test_simple_dict_contains():
    assert dict_.contains(other)
    assert dict_.contains(normal)
    assert dict_.contains(outer)
    assert dict_.contains(inner)
    assert dict_.contains("value")
    assert dict_.contains(defined)


def test_nested_dict_membership():
    assert "hello" in dict_
    assert "world" in dict_
    assert "cat" in dict_
    assert "dog" in dict_
    assert "foo" in dict_
    assert "bar" in dict_
    assert "larry" in dict_
    assert "moe" in dict_
    assert "curly" in dict_
    assert 0 in dict_
    assert 100 in dict_
    assert 100.0 in dict_
    assert "value" in dict_

    assert "tionary" not in dict_
    assert 0.0 not in dict_
    assert bytes() not in dict_


def test_nested_dict_contains():
    assert dict_.contains("hello")
    assert dict_.contains("world")
    assert dict_.contains("cat")
    assert dict_.contains("dog")
    assert dict_.contains("foo")
    assert dict_.contains("bar")
    assert dict_.contains("larry")
    assert dict_.contains("moe")
    assert dict_.contains("curly")
    assert dict_.contains(0)
    assert dict_.contains(100)
    assert dict_.contains(100.0)
    assert dict_.contains("value")

    assert not dict_.contains("tionary")
    assert not dict_.contains(0.0)
    assert not dict_.contains(bytes())


def test_enumerate_dict():
    result = dict_.enumerate("dog")
    assert isinstance(result, GENERATOR_CLASS)
    expected = {(other, outer)}
    assert expected == set(result)

    result = dict_.enumerate("hello")
    assert isinstance(result, GENERATOR_CLASS)
    expected = {(other, outer), (inner, normal)}
    assert expected == set(result)

    result = dict_.enumerate("tionary")
    assert isinstance(result, GENERATOR_CLASS)
    expected = set()
    assert expected == set(result)


def test_find_dict():
    result = dict_.find("dog")
    assert result in {(other, outer)}

    result = dict_.find("hello")
    assert result in {(other, outer), (inner, normal)}

    with pytest.raises(SearchError):
        dict_.find("tionary")


def test_search_dict():
    result = dict_.search("dog")
    assert isinstance(result, SearchableDictionary)
    expected = {other: outer}
    assert expected == result

    result = dict_.search("hello")
    assert isinstance(result, SearchableDictionary)
    expected = {other: outer, inner: normal}
    assert expected == result

    with pytest.raises(SearchError):
        dict_.search("tionary")


def test_delete_dict_normal():
    dict_ = SearchableDictionary({other: outer, inner: normal, "value": defined})
    with pytest.raises(SearchError):
        del dict_["tionary"]

    assert dict_ == {other: outer, inner: normal, "value": defined}

    del dict_[other]
    assert dict_ == {inner: normal, "value": defined}

    del dict_["value"]
    assert dict_ == {inner: normal}

    del dict_[inner]
    assert dict_ == {}


def test_delete_dict_key():
    dict_ = SearchableDictionary({other: outer, inner: normal, "value": defined})

    with pytest.raises(SearchError):
        del dict_["tionary"]

    with pytest.raises(SearchError):
        del dict_[0.0]

    with pytest.raises(SearchError):
        del dict_[bytes()]

    assert dict_ == {other: outer, inner: normal, "value": defined}

    del dict_["hello"]
    assert dict_ == {"value": defined}

    del dict_[defined]
    assert dict_ == {}


def test_dict_delete():
    dict_ = SearchableDictionary({other: outer, inner: normal, "value": defined})

    with pytest.raises(SearchError):
        dict_.delete("tionary")

    with pytest.raises(SearchError):
        dict_.delete(0.0)

    with pytest.raises(SearchError):
        dict_.delete(bytes())

    assert dict_ == {other: outer, inner: normal, "value": defined}

    dict_.delete("hello")
    assert dict_ == {"value": defined}

    dict_.delete(defined)
    assert dict_ == {}


def test_lazy_list():
    ll = LazyList(generator=(i for i in range(10)), known_data=None)
    assert ll[0] == 0
    assert ll[5] == 5
    assert list.__len__(ll) == 6
    with pytest.raises(IndexError):
        non_existent = ll[10]

    assert len(ll) == 10


def test_lazy_list_contains():
    ll = LazyList(generator=(i for i in range(10)), known_data=None)
    assert 5 in ll
    assert list.__len__(ll) == 6
    assert 50 not in ll


def test_lazy_list_delete():
    ll = LazyList(generator=(i for i in range(10)), known_data=None)
    item = ll[5]
    del ll[5]
    assert list.__len__(ll) == 5
    assert 5 not in ll

    del ll[8]

    with pytest.raises(IndexError):
        del ll[50]


def test_lazy_list_list_functionality():
    # Append
    ll = LazyList(generator=(i for i in range(10)), known_data=None)
    ll.append(50)
    assert ll[-1] == 50

    # Clear
    ll = LazyList(generator=(i for i in range(10)), known_data=None)
    item = ll[5]
    ll.clear()
    assert len(ll) == 0

    # Copy
    ll = LazyList(generator=(i for i in range(10)), known_data=None)
    item = ll[5]
    new = ll.copy()
    assert item == new[5]

    # Count
    ll = LazyList(generator=(i for i in range(10)), known_data=None)
    assert ll.count(5) == 1

    # Extend
    ll.extend([1,2,3])
    assert list.__eq__([1,2,3], ll[-3:])
    assert len(ll) == 13

    # Index
    ll = LazyList(generator=(i for i in range(10)), known_data=None)
    assert ll.index(5) == 5

    # Insert
    ll = LazyList(generator=(i for i in range(10)), known_data=None)
    item = ll[5]
    ll.insert(1, 'j')
    assert ll[1] == 'j'
    ll.insert(50, 'a')
    assert ll[-1] == 'a'
    assert len(ll) == 12

    # Pop
    ll = LazyList(generator=(i for i in range(10)), known_data=None)
    assert ll.pop() == 9

    # Reverse
    ll = LazyList(generator=(i for i in range(10)), known_data=None)
    first = ll[0]
    ll.reverse()
    assert ll[-1] == first

    # Remove
    ll = LazyList(generator=(i for i in range(10)), known_data=None)
    ll.remove(5)
    assert 5 not in ll

    # Sort
    ll = LazyList(generator=(i for i in range(10)), known_data=None)
    ll.reverse()
    ll.sort()
    assert ll[0] == 0 and ll[-1] == 9


def test_searchable_lazy_list():
    @searchable({str: ['name'], int: ['id']})
    class Person:
        def __init__(self, name: str, id: int):
            self.name = name
            self.id = id

    larry = Person('Larry', 1)
    moe = Person('Moe', 2)
    curly = Person('Curly', 3)
    stooges = [larry, moe, curly]
    stooges = SearchableLazyList(generator=(p for p in stooges))
    assert stooges['Larry'].id == 1
    assert stooges['Moe'].id == 2
    assert stooges['Curly'].id == 3
    assert len(stooges) == 3

    stooges.delete('Moe')
    assert len(stooges) == 2
    assert 'Larry' in stooges
    assert 'Moe' not in stooges