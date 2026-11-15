"""1-ci mövzu: Array (statik) və Dynamic Array."""


class StaticArray:
    """Sabit tutumlu massiv. Yer bitəndə yeni element əlavə etmək olmur."""

    def __init__(self, capacity):
        self._data = [None] * capacity
        self._capacity = capacity
        self._size = 0

    def __len__(self):
        return self._size

    def get(self, index):
        if not 0 <= index < self._size:
            raise IndexError("indeks hüdudlardan kənardadır")
        return self._data[index]

    def append(self, value):
        if self._size == self._capacity:
            raise OverflowError("statik massiv doludur")
        self._data[self._size] = value
        self._size += 1

    def insert(self, index, value):
        """index mövqeyinə əlavə edir, sağdakı elementləri bir addım sürüşdürür: O(n)."""
        if self._size == self._capacity:
            raise OverflowError("statik massiv doludur")
        if not 0 <= index <= self._size:
            raise IndexError("indeks hüdudlardan kənardadır")
        for i in range(self._size, index, -1):
            self._data[i] = self._data[i - 1]
        self._data[index] = value
        self._size += 1

    def delete(self, index):
        """index-dəki elementi silir, sağdakıları sola sürüşdürür: O(n)."""
        if not 0 <= index < self._size:
            raise IndexError("indeks hüdudlardan kənardadır")
        value = self._data[index]
        for i in range(index, self._size - 1):
            self._data[i] = self._data[i + 1]
        self._data[self._size - 1] = None
        self._size -= 1
        return value

    def search(self, value):
        """Xətti axtarış: O(n). Tapılmasa -1."""
        for i in range(self._size):
            if self._data[i] == value:
                return i
        return -1

    def to_list(self):
        return [self._data[i] for i in range(self._size)]


class DynamicArray:
    """Dinamik massiv: tutum dolanda iki dəfə böyüyür (amortized O(1) append)."""

    def __init__(self, capacity=4):
        self._capacity = max(1, capacity)
        self._data = [None] * self._capacity
        self._size = 0
        self.resize_count = 0

    def __len__(self):
        return self._size

    @property
    def capacity(self):
        return self._capacity

    def _resize(self, new_capacity):
        new_data = [None] * new_capacity
        for i in range(self._size):
            new_data[i] = self._data[i]
        self._data = new_data
        self._capacity = new_capacity
        self.resize_count += 1

    def get(self, index):
        if not 0 <= index < self._size:
            raise IndexError("indeks hüdudlardan kənardadır")
        return self._data[index]

    def append(self, value):
        if self._size == self._capacity:
            self._resize(self._capacity * 2)
        self._data[self._size] = value
        self._size += 1

    def insert(self, index, value):
        if not 0 <= index <= self._size:
            raise IndexError("indeks hüdudlardan kənardadır")
        if self._size == self._capacity:
            self._resize(self._capacity * 2)
        for i in range(self._size, index, -1):
            self._data[i] = self._data[i - 1]
        self._data[index] = value
        self._size += 1

    def delete(self, index):
        if not 0 <= index < self._size:
            raise IndexError("indeks hüdudlardan kənardadır")
        value = self._data[index]
        for i in range(index, self._size - 1):
            self._data[i] = self._data[i + 1]
        self._data[self._size - 1] = None
        self._size -= 1
        # Massiv 1/4-ə qədər boşalanda yaddaşı yarıya endiririk
        if 0 < self._size <= self._capacity // 4 and self._capacity > 4:
            self._resize(self._capacity // 2)
        return value

    def search(self, value):
        for i in range(self._size):
            if self._data[i] == value:
                return i
        return -1

    def to_list(self):
        return [self._data[i] for i in range(self._size)]
