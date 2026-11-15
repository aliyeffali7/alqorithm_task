"""2-ci mövzu: Singly və Doubly Linked List."""


class _SNode:
    __slots__ = ("value", "next")

    def __init__(self, value):
        self.value = value
        self.next = None


class SinglyLinkedList:
    """Hər node yalnız növbətini göstərir. head və tail saxlayırıq."""

    def __init__(self):
        self.head = None
        self.tail = None
        self._size = 0

    def __len__(self):
        return self._size

    def __iter__(self):
        node = self.head
        while node:
            yield node.value
            node = node.next

    def push_front(self, value):          # O(1)
        node = _SNode(value)
        node.next = self.head
        self.head = node
        if self.tail is None:
            self.tail = node
        self._size += 1

    def push_back(self, value):           # O(1) — tail sayəsində
        node = _SNode(value)
        if self.tail is None:
            self.head = self.tail = node
        else:
            self.tail.next = node
            self.tail = node
        self._size += 1

    def pop_front(self):                  # O(1)
        if self.head is None:
            raise IndexError("siyahı boşdur")
        node = self.head
        self.head = node.next
        if self.head is None:
            self.tail = None
        self._size -= 1
        return node.value

    def pop_back(self):                   # O(n) — əvvəlki node-u tapmaq üçün başdan getmək lazımdır
        if self.head is None:
            raise IndexError("siyahı boşdur")
        if self.head is self.tail:
            value = self.head.value
            self.head = self.tail = None
            self._size -= 1
            return value
        node = self.head
        while node.next is not self.tail:
            node = node.next
        value = self.tail.value
        node.next = None
        self.tail = node
        self._size -= 1
        return value

    def search(self, value):              # O(n)
        for i, v in enumerate(self):
            if v == value:
                return i
        return -1

    def remove(self, value):              # O(n)
        prev, node = None, self.head
        while node:
            if node.value == value:
                if prev is None:
                    self.head = node.next
                else:
                    prev.next = node.next
                if node is self.tail:
                    self.tail = prev
                self._size -= 1
                return True
            prev, node = node, node.next
        return False

    def to_list(self):
        return list(self)


class _DNode:
    __slots__ = ("value", "next", "prev")

    def __init__(self, value):
        self.value = value
        self.next = None
        self.prev = None


class DoublyLinkedList:
    """Hər node həm növbətini, həm əvvəlkini göstərir."""

    def __init__(self):
        self.head = None
        self.tail = None
        self._size = 0

    def __len__(self):
        return self._size

    def __iter__(self):
        node = self.head
        while node:
            yield node.value
            node = node.next

    def reversed(self):
        node = self.tail
        while node:
            yield node.value
            node = node.prev

    def push_front(self, value):          # O(1)
        node = _DNode(value)
        node.next = self.head
        if self.head:
            self.head.prev = node
        else:
            self.tail = node
        self.head = node
        self._size += 1

    def push_back(self, value):           # O(1)
        node = _DNode(value)
        node.prev = self.tail
        if self.tail:
            self.tail.next = node
        else:
            self.head = node
        self.tail = node
        self._size += 1

    def _unlink(self, node):
        if node.prev:
            node.prev.next = node.next
        else:
            self.head = node.next
        if node.next:
            node.next.prev = node.prev
        else:
            self.tail = node.prev
        self._size -= 1
        return node.value

    def pop_front(self):                  # O(1)
        if self.head is None:
            raise IndexError("siyahı boşdur")
        return self._unlink(self.head)

    def pop_back(self):                   # O(1) — prev göstəricisi sayəsində
        if self.tail is None:
            raise IndexError("siyahı boşdur")
        return self._unlink(self.tail)

    def peek_front(self):
        if self.head is None:
            raise IndexError("siyahı boşdur")
        return self.head.value

    def peek_back(self):
        if self.tail is None:
            raise IndexError("siyahı boşdur")
        return self.tail.value

    def search(self, value):              # O(n)
        for i, v in enumerate(self):
            if v == value:
                return i
        return -1

    def remove(self, value):              # O(n) axtarış + O(1) silmə
        node = self.head
        while node:
            if node.value == value:
                self._unlink(node)
                return True
            node = node.next
        return False

    def to_list(self):
        return list(self)
