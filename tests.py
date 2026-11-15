"""Sadə unit testlər:  python -m unittest tests.py"""

import random
import unittest

from ds import (StaticArray, DynamicArray, SinglyLinkedList, DoublyLinkedList,
                Stack, Queue, Deque, HashTable, BinarySearchTree)
from main import TextEditor, check_brackets, is_palindrome


class ArrayTests(unittest.TestCase):
    def test_static_and_dynamic(self):
        for arr in (StaticArray(10), DynamicArray(1)):
            for i in range(5):
                arr.append(i)
            arr.insert(0, 99)
            self.assertEqual(arr.to_list(), [99, 0, 1, 2, 3, 4])
            self.assertEqual(arr.delete(2), 1)
            self.assertEqual(arr.search(3), 3)
            self.assertEqual(arr.search(42), -1)

    def test_static_overflow(self):
        a = StaticArray(1)
        a.append(1)
        with self.assertRaises(OverflowError):
            a.append(2)

    def test_dynamic_grows(self):
        a = DynamicArray(1)
        for i in range(100):
            a.append(i)
        self.assertGreaterEqual(a.capacity, 100)
        self.assertEqual(a.to_list(), list(range(100)))


class LinkedListTests(unittest.TestCase):
    def test_both(self):
        for cls in (SinglyLinkedList, DoublyLinkedList):
            lst = cls()
            for i in range(5):
                lst.push_back(i)
            lst.push_front(-1)
            self.assertEqual(lst.pop_back(), 4)
            self.assertEqual(lst.pop_front(), -1)
            self.assertTrue(lst.remove(2))
            self.assertFalse(lst.remove(42))
            self.assertEqual(lst.to_list(), [0, 1, 3])
            self.assertEqual(lst.search(3), 2)
            lst.remove(3)
            lst.push_back(7)        # tail düzgün yenilənməlidir
            self.assertEqual(lst.to_list(), [0, 1, 7])


class SQDTests(unittest.TestCase):
    def test_stack_queue_deque(self):
        s, q, d = Stack(), Queue(), Deque(maxlen=2)
        for i in range(3):
            s.push(i); q.enqueue(i); d.push_back(i)
        self.assertEqual(s.pop(), 2)
        self.assertEqual(q.dequeue(), 0)
        self.assertEqual(d.to_list(), [1, 2])

    def test_app_functions(self):
        ed = TextEditor()
        ed.write("ab"); ed.write("cd")
        ed.undo()
        self.assertEqual(ed.text, "ab")
        ed.redo()
        self.assertEqual(ed.text, "abcd")
        self.assertTrue(check_brackets("{[()]}")[0])
        self.assertFalse(check_brackets("([)]")[0])
        self.assertTrue(is_palindrome("Ana"))
        self.assertFalse(is_palindrome("kitab"))


class HashTableTests(unittest.TestCase):
    def test_basic_and_collisions(self):
        ht = HashTable(capacity=2)
        data = {f"k{i}": i for i in range(200)}
        for k, v in data.items():
            ht.put(k, v)
        ht.put("k5", 555)
        self.assertEqual(len(ht), 200)
        self.assertEqual(ht.get("k5"), 555)
        self.assertTrue(ht.remove("k7"))
        self.assertIsNone(ht.get("k7"))
        self.assertLessEqual(ht.load_factor, HashTable.MAX_LOAD_FACTOR)


class BSTTests(unittest.TestCase):
    def test_random_ops(self):
        t, ref = BinarySearchTree(), set()
        for _ in range(2000):
            k = random.randrange(300)
            if random.random() < 0.6:
                t.insert(k); ref.add(k)
            else:
                self.assertEqual(t.delete(k), k in ref); ref.discard(k)
        self.assertEqual(t.inorder(), sorted(ref))
        for k in range(300):
            self.assertEqual(t.contains(k), k in ref)

    def test_sorted_degenerates(self):
        t = BinarySearchTree()
        for k in range(5000):
            t.insert(k)
        self.assertEqual(t.height(), 5000)


if __name__ == "__main__":
    unittest.main()
