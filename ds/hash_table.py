"""4-cü mövzu: Chaining üsulu ilə collision-u həll edən Hash Table."""


class _Entry:
    __slots__ = ("key", "value", "next")

    def __init__(self, key, value, next_entry=None):
        self.key = key
        self.value = value
        self.next = next_entry


class HashTable:
    """
    Hər bucket bir zəncirdir (singly linked list).
    Eyni bucket-ə düşən açarlar (collision) həmin zəncirə əlavə olunur.
    load factor > 0.75 olanda tutum iki dəfə artırılır və hər şey yenidən hash olunur.
    """

    MAX_LOAD_FACTOR = 0.75

    def __init__(self, capacity=8):
        self._capacity = max(1, capacity)
        self._buckets = [None] * self._capacity
        self._size = 0
        self.collisions = 0

    def __len__(self):
        return self._size

    @property
    def capacity(self):
        return self._capacity

    @property
    def load_factor(self):
        return self._size / self._capacity

    @staticmethod
    def _hash(key):
        """Sətirlər üçün öz polinom hash funksiyamız (djb2), digər tiplər üçün hash()."""
        if isinstance(key, str):
            h = 5381
            for ch in key:
                h = ((h * 33) + ord(ch)) & 0xFFFFFFFF
            return h
        return hash(key) & 0xFFFFFFFF

    def _index(self, key):
        return self._hash(key) % self._capacity

    def put(self, key, value):
        idx = self._index(key)
        entry = self._buckets[idx]
        while entry:
            if entry.key == key:      # açar artıq var — dəyəri yenilə
                entry.value = value
                return
            entry = entry.next
        if self._buckets[idx] is not None:
            self.collisions += 1
        # Zəncirin başına əlavə: O(1)
        self._buckets[idx] = _Entry(key, value, self._buckets[idx])
        self._size += 1
        if self.load_factor > self.MAX_LOAD_FACTOR:
            self._rehash(self._capacity * 2)

    def get(self, key, default=None):
        entry = self._buckets[self._index(key)]
        while entry:
            if entry.key == key:
                return entry.value
            entry = entry.next
        return default

    def contains(self, key):
        sentinel = object()
        return self.get(key, sentinel) is not sentinel

    def remove(self, key):
        idx = self._index(key)
        prev, entry = None, self._buckets[idx]
        while entry:
            if entry.key == key:
                if prev is None:
                    self._buckets[idx] = entry.next
                else:
                    prev.next = entry.next
                self._size -= 1
                return True
            prev, entry = entry, entry.next
        return False

    def _rehash(self, new_capacity):
        old = self._buckets
        self._capacity = new_capacity
        self._buckets = [None] * new_capacity
        self._size = 0
        self.collisions = 0
        for head in old:
            entry = head
            while entry:
                self.put(entry.key, entry.value)
                entry = entry.next

    def items(self):
        for head in self._buckets:
            entry = head
            while entry:
                yield entry.key, entry.value
                entry = entry.next

    def chain_lengths(self):
        lengths = []
        for head in self._buckets:
            n, entry = 0, head
            while entry:
                n += 1
                entry = entry.next
            lengths.append(n)
        return lengths

    def bucket_view(self):
        """Hər bucket-in açarlarını qaytarır (vizuallaşdırma üçün)."""
        view = []
        for head in self._buckets:
            keys, entry = [], head
            while entry:
                keys.append(entry.key)
                entry = entry.next
            view.append(keys)
        return view
