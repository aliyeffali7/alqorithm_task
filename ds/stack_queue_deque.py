"""3-cü mövzu: Stack, Queue və Deque (öz linked list-lərimiz üzərində)."""

from .linked_lists import SinglyLinkedList, DoublyLinkedList


class Stack:
    """LIFO — son girən ilk çıxır. Singly linked list-in başı üzərində işləyir."""

    def __init__(self):
        self._list = SinglyLinkedList()

    def push(self, value):
        self._list.push_front(value)

    def pop(self):
        if self.is_empty():
            raise IndexError("stack boşdur")
        return self._list.pop_front()

    def peek(self):
        if self.is_empty():
            raise IndexError("stack boşdur")
        return self._list.head.value

    def is_empty(self):
        return len(self._list) == 0

    def __len__(self):
        return len(self._list)

    def to_list(self):
        """Yuxarıdan aşağıya."""
        return self._list.to_list()


class Queue:
    """FIFO — ilk girən ilk çıxır. Sona əlavə (tail), başdan çıxarma (head): hər ikisi O(1)."""

    def __init__(self):
        self._list = SinglyLinkedList()

    def enqueue(self, value):
        self._list.push_back(value)

    def dequeue(self):
        if self.is_empty():
            raise IndexError("növbə boşdur")
        return self._list.pop_front()

    def peek(self):
        if self.is_empty():
            raise IndexError("növbə boşdur")
        return self._list.head.value

    def is_empty(self):
        return len(self._list) == 0

    def __len__(self):
        return len(self._list)

    def to_list(self):
        return self._list.to_list()


class Deque:
    """Hər iki ucdan O(1) əlavə/silmə. Doubly linked list üzərində."""

    def __init__(self, maxlen=None):
        self._list = DoublyLinkedList()
        self.maxlen = maxlen

    def push_front(self, value):
        self._list.push_front(value)
        if self.maxlen is not None and len(self._list) > self.maxlen:
            self._list.pop_back()

    def push_back(self, value):
        self._list.push_back(value)
        if self.maxlen is not None and len(self._list) > self.maxlen:
            self._list.pop_front()

    def pop_front(self):
        if self.is_empty():
            raise IndexError("deque boşdur")
        return self._list.pop_front()

    def pop_back(self):
        if self.is_empty():
            raise IndexError("deque boşdur")
        return self._list.pop_back()

    def peek_front(self):
        return self._list.peek_front()

    def peek_back(self):
        return self._list.peek_back()

    def is_empty(self):
        return len(self._list) == 0

    def __len__(self):
        return len(self._list)

    def to_list(self):
        return self._list.to_list()
