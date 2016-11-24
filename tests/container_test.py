from pytest import raises
from buffers import Container, Buffer

def test_create():
    c = Container()
    assert c.buffers == []
    assert c.buffer is None


def test_append_buffer():
    c = Container()
    b = Buffer('test')
    c.append_buffer(b)
    assert c.buffers == [b]
    assert c.buffer is None
    b2 = Buffer('test2')
    c.append_buffer(b2)
    assert c.buffers == [b, b2]
    assert c.buffer is None


def test_next_buffer():
    c = Container()
    b = Buffer('test')
    c.append_buffer(b)
    assert c.next_buffer() is b
    with raises(RuntimeError):
        c.next_buffer(wrap = False)
    assert c.next_buffer() is b
    b2 = Buffer('test2')
    c.append_buffer(b2)
    assert c.next_buffer() is b2
    with raises(RuntimeError):
        c.next_buffer(wrap = False)
    assert c.next_buffer() is b


    def test_previous_buffer():
        c = Container()
        b = Buffer('test')
        b2 = Buffer('test2')
        c.append_buffer(b)
        assert c.previous_buffer() is b
        with raises(RuntimeError):
            c.previous_buffer()
        c.append_buffer(b2)
        assert c.previous_buffer() is b2
        assert c.previous_buffer is b
        with raises(RuntimeError):
            c.previous_buffer()


def test_prepend_buffer():
    c = Container()
    b = Buffer('test')
    c.prepend_buffer(b)
    assert c.buffers == [b]
    assert c.buffer is None
    b2 = Buffer('test2')
    c.prepend_buffer(b2)
    assert c.buffers == [b2, b]


def test_insert_buffer():
    c = Container()
    b1 = Buffer('First')
    b2 = Buffer('Middle')
    b3 = Buffer('Last')
    c.append_buffer(b3)
    c.insert_buffer(0, b1)
    assert c.buffers == [b1, b3]
    c.insert_buffer(1, b2)
    assert c.buffers == [b1, b2, b3]


def test_remove_buffer():
    c = Container()
    b = Buffer('test')
    b2 = Buffer('test2')
    c.append_buffer(b)
    c.remove_buffer(b)
    assert c.buffers == []
    c.append_buffer(b)
    c.append_buffer(b2)
    c.remove_buffer(b2)
    assert c.buffers == [b]


def test_buffer_names():
    c = Container()
    names = ['first', 'second', 'third', 'fourth', 'fifth']
    for name in names:
        c.append_buffer(Buffer(name))
    assert c.buffer_names() == names


def test_buffer_dict():
    c = Container()
    names = ['first', 'second', 'third', 'fourth', 'fifth', 'sixth']
    d = {name: Buffer(name) for name in names}
    for buffer in d.values():
        c.append_buffer(buffer)
    assert c.buffer_dict() == d


