from pytest import raises
from buffers import Buffer

name = 'test'


def test_create():
    b = Buffer(name)
    assert b.name == name
    assert b.items == []


def test_get_items():
    """Test all the get_*_items functions."""
    b = Buffer(name)
    b.append_item(name)
    assert b.get_current_item() is name
    for x in range(10):
        b.append_item(x)
    for x in range(10):
        assert b.get_next_item() is x
    assert b.get_first_item() is name
    assert b.get_last_item() is 9
    with raises(RuntimeError):
        b.get_next_item(wrap = False)
    assert b.get_next_item() is name
    with raises(RuntimeError):
        b.get_previous_item(wrap = False)
    assert b.get_previous_item() is 9


def test_format_item():
    class TestBuffer(Buffer):
        def format_item(self, item):
            """Make it possible to catch the override."""
            raise ValueError
    b = TestBuffer(name)
    with raises(ValueError):
        b.format_item(name)
    b = Buffer(name)
    assert b.format_item(name) is name


def test_append_item():
    b = Buffer(name)
    assert len(b.items) == 0
    b.append_item(name)
    assert b.items[-1] is name
    assert len(b.items) == 1
    other = name * 2
    b.append_item(other)
    assert b.items[-1] is other
    assert len(b.items) == 2


def test_prepend_item():
    b = Buffer(name)
    b.prepend_item(name)
    assert b.items[0] == name
    other = name * 2
    b.prepend_item(other)
    assert b.items[0] == other
    assert len(b.items) == 2


def test_insert_item():
    b = Buffer(name)
    b.append_item(name)
    other = name * 2
    b.insert_item(0, other)
    assert b.items[0] == other


def test_remove_item():
    b = Buffer(name)
    b.append_item(name)
    assert len(b.items) == 1
    assert b.items[0] == name
    b.remove_item(name)
    assert b.items == []


def test_clear_items():
    b = Buffer(name)
    for x in range(10):
        b.append_item(x)
    b.clear_items()
    assert b.items == []


def test_length():
    b = Buffer(name)
    b.append_item(name)
    assert b.length() == 1
    for x in range(10):
        b.append_item(name)
        assert b.length() == x + 2
