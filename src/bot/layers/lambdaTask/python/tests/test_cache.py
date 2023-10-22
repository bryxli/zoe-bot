import pytest

from merakicommons.cache import lazy_property, Cache

TEST_VALUE_1 = "TEST VALUE_1"
TEST_VALUE_2 = "TEST_VALUE_2"
VALUE_COUNT = 100


class LazyProperty(object):
    def __init__(self, value) -> None:
        self.property_calls = 0
        self.value = value

    @lazy_property
    def property(self) -> str:
        self.property_calls += 1
        return self.value


def test_lazy_property_type():
    assert type(LazyProperty.property) is property


def test_lazy_property_value():
    x = LazyProperty(TEST_VALUE_1)
    y = LazyProperty(TEST_VALUE_2)
    for _ in range(VALUE_COUNT):
        value = x.property
        assert type(value) is type(TEST_VALUE_1)
        assert value == TEST_VALUE_1

        value = y.property
        assert type(value) is type(TEST_VALUE_2)
        assert value == TEST_VALUE_2


def test_lazy_property_loading():
    x = LazyProperty(TEST_VALUE_1)
    y = LazyProperty(TEST_VALUE_2)
    assert x.property_calls == 0
    assert y.property_calls == 0
    for _ in range(VALUE_COUNT):
        x.property
        y.property
        assert x.property_calls == 1
        assert y.property_calls == 1


#########
# Cache #
#########

def test_cache_simple():
    x = Cache()
    assert not x.contains(int, "test")
    assert not x.contains(int, 1)

    x.put(int, "test", 1)
    assert x.contains(int, "test")
    assert not x.contains(int, 1)

    # x[1] = "test"
    x.put(str, 1, "test")
    assert x.contains(int, "test")
    assert x.contains(str, 1)

    assert x.get(str, 1) == "test"
    assert x.get(int, "test") == 1

    with pytest.raises(KeyError):
        x.get(int, 2)


def test_cache_delete():
    x = Cache()

    x.put(int, "test", 1)
    assert x.contains(int, "test")
    assert x.get(int, "test") == 1

    x.put(str, 1, "test")
    assert x.contains(str, 1)
    assert x.get(str, 1) == "test"

    x.delete(int, "test")
    assert not x.contains(int, "test")
    with pytest.raises(KeyError):
        x.get(int, "test")

    x.delete(str, 1)
    assert not x.contains(str, 1)
    with pytest.raises(KeyError):
        x.get(str, 1)
