import pytest

from merakicommons.ghost import Ghost, GhostLoadingRequiredError

TEST_VALUE = "TEST VALUE"
VALUE_COUNT = 100


class GhostObject(Ghost):
    def __init__(self) -> None:
        self.load_calls = 0
        self.last_loaded = None

    def __load__(self, load_group) -> None:
        self.load_calls += 1
        self._value = TEST_VALUE
        self.last_loaded = load_group

    @Ghost.property
    def value(self) -> str:
        try:
            return self._value
        except AttributeError:
            raise GhostLoadingRequiredError

    @Ghost.property
    def constant_value(self) -> str:
        return TEST_VALUE

    @Ghost.property
    def bad_value(self) -> None:
        return self._bad_value

    @property
    def unloaded_value(self) -> str:
        return TEST_VALUE

    def unloaded_method(self) -> str:
        return TEST_VALUE


def test_ghost_property():
    x = GhostObject()
    for _ in range(VALUE_COUNT):
        value = x.value
        assert type(value) is type(TEST_VALUE)
        assert value == TEST_VALUE
        assert x.last_loaded == "value"


def test_constant_value():
    x = GhostObject()
    for _ in range(VALUE_COUNT):
        value = x.constant_value
        assert type(value) is type(TEST_VALUE)
        assert value == TEST_VALUE
        assert x.last_loaded is None


def test_bad_value():
    x = GhostObject()
    for _ in range(VALUE_COUNT):
        with pytest.raises(AttributeError):
            x.bad_value
        assert x.last_loaded is None


def test_ghost_load_normal_attribute():
    x = GhostObject()
    assert x.load_calls == 0

    for _ in range(VALUE_COUNT):
        x.unloaded_value
        assert x.load_calls == 0
        assert x.last_loaded is None

    for _ in range(VALUE_COUNT):
        x.unloaded_method()
        assert x.load_calls == 0
        assert x.last_loaded is None


def test_ghost_load_required():
    x = GhostObject()
    assert x.load_calls == 0

    for _ in range(VALUE_COUNT):
        x.value
        assert x.load_calls == 1
        assert x.last_loaded == "value"


def test_ghost_load_not_required():
    x = GhostObject()
    assert x.load_calls == 0

    for _ in range(VALUE_COUNT):
        x.constant_value
        assert x.load_calls == 0
        assert x.last_loaded is None


def test_ghost_load_bad_value():
    x = GhostObject()
    assert x.load_calls == 0

    for count in range(VALUE_COUNT):
        with pytest.raises(AttributeError):
            x.bad_value
        assert x.load_calls == 0
        assert x.last_loaded is None
