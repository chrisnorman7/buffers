"""Provides the Buffer and Container classes."""

class Buffer:
    """A buffer of information."""

    def get_current_item(self):
        """Get the current item."""
        return self.get_item(self.position)

    def get_next_item(self, wrap = True):
        """
        Shift the focus to the next item in the buffer.

        If wrap evaluates to True and we try to move past the end of the buffer, move back to the beginning instead.

        If wrap evaluates to False, RuntimeError will be raised.
        """
        position = self.position + 1
        if position >= self.length():
            if wrap:
                position = 0
            else:
                raise RuntimeError('Ran off the end of the buffer.')
        self.position = position
        return self.get_item()

    def get_previous_item(self, wrap = True):
        """
        Shift the focus to the previous item in the buffer.

        If wrap evaluates to True and we try to move past the beginning of the buffer, move back to the end instead.

        If wrap evaluates to False, RuntimeError will be raised.
        """
        position = self.position - 1
        if position < 0:
            if wrap:
                position = self.length() - 1
            else:
                raise RuntimeError('Ran off the beginning of the buffer.')
        self.position = position
        return self.get_item()

    def get_first_item(self):
        """Shift the focus to the first item in the buffer."""
        self.position = 0
        return self.get_item()

    def get_last_item(self):
        """Shift focus to the last item in the buffer."""
        self.position = self.length() - 1
        return self.get_item()

    def get_item(self, position = None):
        """
        Get the item at the provided position.

        If position is None, use self.position.

        This function does not shift the focus, however if self.position is None, it will be set to 0 to avoid future errors.
        """
        if self.position is None:
            self.position = 0
        if position is None:
            position = self.position
        return self.format_item(self.items[position])

    def format_item(self, item):
        """Return the properly-formatted item."""
        return item

    def append_item(self, item):
        """Append an item to self.items."""
        self.items.append(item)

    def prepend_item(self, item):
        """Push an item at the start of self.items."""
        if self.items:
            self.insert_item(0, item)
        else:
            self.append_item(item)

    def insert_item(self, position, item):
        """Insert the provided item at the provided position."""
        if position == -1:
            return self.append_item(item)
        else:
            self.items.insert(position, item)

    def remove_item(self, item):
        """Remove the provided item from self.items."""
        self.items.remove(item)

    def clear_items(self):
        """Clear self.items."""
        self.items.clear()

    def length(self):
        """Return the number of items this buffer holds."""
        return len(self.items)

    def __init__(self, name):
        """Set the name."""
        self.name = name
        self.items = []
        self.position = None


class Container:
    """A container for 0 or more buffers."""

    def next_buffer(self, wrap = True):
        """
        Switch focus to the next buffer.

        If wrap evaluates to True and we are already at the end of the buffer,
        switch to the first buffer instead.

        If wrap evaluates to False, RuntimeError will be raised.
        """
        if self.buffer is None:
            pos = 0
        else:
            pos = self.buffers.index(self.buffer) + 1
            if pos >= len(self.buffers):
                if wrap:
                    pos = 0
                else:
                    raise RuntimeError('No next buffer.')
        self.buffer = self.buffers[pos]
        return self.buffer

    def previous_buffer(self, wrap = True):
        """
        Set focus to the previous buffer.

        If wrap evaluates to True and we fall off the beginning of the buffer,
        return tue last item instead.

        If wrap evaluates to False, raise RuntimeError.
        """
        try:
            pos = self.buffers.index(self.buffer)
        except ValueError:
            pos = len(self.buffers)
        pos -= 1
        if pos < 0:
            if wrap:
                pos = len(self.buffers) - 1
            else:
                raise RuntimeError('No previous buffer.')
        self.buffer = self.buffers[pos]
        return self.buffer

    def append_buffer(self, buffer):
        """Append a buffer to self.buffers."""
        self.buffers.append(buffer)

    def prepend_buffer(self, buffer):
        """Push buffer onto the start of self.buffers."""
        if self.buffers:
            self.insert_buffer(0, buffer)
        else:
            self.append_buffer(buffer)

    def insert_buffer(self, position, buffer):
        """Insert buffer at position in self.buffers."""
        if self.buffers:
            self.buffers.insert(position, buffer)
        else:
            self.append_buffer(buffer)

    def remove_buffer(self, buffer):
        """Remove a buffer from self.buffers."""
        self.buffers.remove(buffer)

    def buffer_names(self):
        """Return the names of all buffers."""
        return [x.name for x in self.buffers]

    def buffer_dict(self):
        """Return a dictionary of name: buffer pares."""
        return {x.name: x for x in self.buffers}

    def __init__(self):
        """Initialise the container."""
        self.buffers = []
        self.buffer = None
