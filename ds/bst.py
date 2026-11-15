"""5-ci mövzu: Binary Search Tree — əlavə, axtarış, silmə.

Bütün əməliyyatlar iterativ yazılıb ki, sıralanmış verilənlərlə ağac
"zəncirə" çevriləndə (hündürlük = n) Python-un rekursiya limiti aşılmasın.
"""

from collections import deque as _bfs_queue


class _Node:
    __slots__ = ("key", "left", "right")

    def __init__(self, key):
        self.key = key
        self.left = None
        self.right = None


class BinarySearchTree:
    def __init__(self):
        self.root = None
        self._size = 0

    def __len__(self):
        return self._size

    def insert(self, key):
        """Yeni açar əlavə edir. Təkrar açar əlavə olunmur. False — artıq var idi."""
        if self.root is None:
            self.root = _Node(key)
            self._size += 1
            return True
        node = self.root
        while True:
            if key == node.key:
                return False
            if key < node.key:
                if node.left is None:
                    node.left = _Node(key)
                    break
                node = node.left
            else:
                if node.right is None:
                    node.right = _Node(key)
                    break
                node = node.right
        self._size += 1
        return True

    def search(self, key):
        """(tapıldı?, müqayisə sayı) qaytarır."""
        node, comparisons = self.root, 0
        while node:
            comparisons += 1
            if key == node.key:
                return True, comparisons
            node = node.left if key < node.key else node.right
        return False, comparisons

    def contains(self, key):
        return self.search(key)[0]

    def delete(self, key):
        """3 hal: yarpaq, bir uşaqlı, iki uşaqlı (inorder varis ilə əvəz)."""
        parent, node = None, self.root
        while node and node.key != key:
            parent = node
            node = node.left if key < node.key else node.right
        if node is None:
            return False

        # İki uşaq: sağ alt ağacın ən kiçiyini (inorder successor) tapıb yerinə qoyuruq
        if node.left and node.right:
            succ_parent, succ = node, node.right
            while succ.left:
                succ_parent, succ = succ, succ.left
            node.key = succ.key
            parent, node = succ_parent, succ   # indi varisi silirik (onun ən çox 1 uşağı var)

        child = node.left if node.left else node.right
        if parent is None:
            self.root = child
        elif parent.left is node:
            parent.left = child
        else:
            parent.right = child
        self._size -= 1
        return True

    def height(self):
        """Kənarların sayı ilə yox, səviyyələrin sayı ilə (boş ağac = 0)."""
        if self.root is None:
            return 0
        h, q = 0, _bfs_queue([self.root])
        while q:
            h += 1
            for _ in range(len(q)):
                n = q.popleft()
                if n.left:
                    q.append(n.left)
                if n.right:
                    q.append(n.right)
        return h

    def inorder(self):
        """Sıralanmış ardıcıllıq (iterativ)."""
        result, stack, node = [], [], self.root
        while stack or node:
            while node:
                stack.append(node)
                node = node.left
            node = stack.pop()
            result.append(node.key)
            node = node.right
        return result

    def min(self):
        node = self.root
        if node is None:
            return None
        while node.left:
            node = node.left
        return node.key

    def max(self):
        node = self.root
        if node is None:
            return None
        while node.right:
            node = node.right
        return node.key

    def pretty(self, max_nodes=31):
        """Kiçik ağacları yan tərəfdən çəkir (kök solda)."""
        if self.root is None:
            return "(boş ağac)"
        if self._size > max_nodes:
            return f"(ağac çox böyükdür: {self._size} node — çəkilmir)"
        lines = []

        def walk(node, prefix, is_left):
            # Kiçik ağac üçün rekursiya təhlükəsizdir (≤ max_nodes)
            if node.right:
                walk(node.right, prefix + ("│   " if is_left else "    "), False)
            lines.append(prefix + ("└── " if is_left else "┌── ") + str(node.key))
            if node.left:
                walk(node.left, prefix + ("    " if is_left else "│   "), True)

        if self.root.right:
            walk(self.root.right, "", False)
        lines.append(str(self.root.key))
        if self.root.left:
            walk(self.root.left, "", True)
        return "\n".join(lines)
