"""
Alqoritmlər və Verilənlər Strukturları — konsol tətbiqi.

İşə salmaq:
    python main.py          # interaktiv menyu
    python main.py --demo   # bütün ölçmələri və nümayişləri avtomatik göstərir
"""

import random
import sys

import benchmarks
from ds import (Stack, Queue, Deque, HashTable, BinarySearchTree,
                SinglyLinkedList, DoublyLinkedList)


def ask(prompt):
    try:
        return input(prompt).strip()
    except EOFError:
        return "0"


def header(text):
    print("\n" + "─" * 60)
    print(f" {text}")
    print("─" * 60)


# =====================================================================
# 3. STACK — Mətn redaktoru: Undo / Redo
# =====================================================================
class TextEditor:
    """Hər dəyişiklikdən əvvəlki vəziyyət undo stack-ə qoyulur (LIFO)."""

    def __init__(self):
        self.text = ""
        self.undo_stack = Stack()
        self.redo_stack = Stack()

    def write(self, s):
        self.undo_stack.push(self.text)
        self.redo_stack = Stack()        # yeni əməliyyat redo tarixçəsini sıfırlayır
        self.text += s

    def delete(self, k):
        self.undo_stack.push(self.text)
        self.redo_stack = Stack()
        self.text = self.text[:-k] if k else self.text

    def undo(self):
        if self.undo_stack.is_empty():
            return False
        self.redo_stack.push(self.text)
        self.text = self.undo_stack.pop()
        return True

    def redo(self):
        if self.redo_stack.is_empty():
            return False
        self.undo_stack.push(self.text)
        self.text = self.redo_stack.pop()
        return True


def check_brackets(expr):
    """Stack ilə mötərizələrin balansını yoxlayır."""
    pairs = {")": "(", "]": "[", "}": "{"}
    st = Stack()
    for i, ch in enumerate(expr):
        if ch in "([{":
            st.push((ch, i))
        elif ch in pairs:
            if st.is_empty() or st.peek()[0] != pairs[ch]:
                return False, i
            st.pop()
    if not st.is_empty():
        return False, st.peek()[1]
    return True, -1


def editor_menu():
    ed = TextEditor()
    while True:
        header("STACK — Mətn redaktoru (Undo/Redo)")
        print(f" Mətn: \"{ed.text}\"   | undo: {len(ed.undo_stack)}  redo: {len(ed.redo_stack)}")
        print(" 1) Yaz   2) Sondan sil   3) Undo   4) Redo   5) Mötərizə yoxla   0) Geri")
        c = ask(" Seçim: ")
        if c == "1":
            ed.write(ask(" Əlavə ediləcək mətn: "))
        elif c == "2":
            k = ask(" Neçə simvol silinsin? ")
            ed.delete(int(k) if k.isdigit() else 1)
        elif c == "3":
            print(" Undo edildi." if ed.undo() else " Undo üçün heç nə yoxdur.")
        elif c == "4":
            print(" Redo edildi." if ed.redo() else " Redo üçün heç nə yoxdur.")
        elif c == "5":
            ok, pos = check_brackets(ed.text)
            print(" Mötərizələr balanslıdır ✓" if ok else f" Balans pozulub, mövqe: {pos}")
        elif c == "0":
            return


# =====================================================================
# 3. QUEUE — Sifariş növbəsi (FIFO)
# =====================================================================
def order_queue_menu():
    q = Queue()
    counter = 1
    while True:
        header("QUEUE — Kafe sifariş növbəsi (FIFO)")
        print(" Növbədə:", " → ".join(q.to_list()) if not q.is_empty() else "(boş)")
        print(" 1) Sifariş əlavə et   2) Növbəti sifarişi hazırla   3) Kim növbədədir?   0) Geri")
        c = ask(" Seçim: ")
        if c == "1":
            name = ask(" Müştəri / sifariş adı: ") or f"Sifariş-{counter}"
            q.enqueue(f"#{counter} {name}")
            counter += 1
        elif c == "2":
            print(" Hazırlandı:", q.dequeue() if not q.is_empty() else "növbə boşdur")
        elif c == "3":
            print(" Növbəti:", q.peek() if not q.is_empty() else "heç kim")
        elif c == "0":
            return


# =====================================================================
# 3. DEQUE — Son baxılanlar tarixçəsi + palindrom yoxlayıcı
# =====================================================================
def is_palindrome(text):
    d = Deque()
    for ch in text.lower():
        if ch.isalnum():
            d.push_back(ch)
    while len(d) > 1:
        if d.pop_front() != d.pop_back():
            return False
    return True


def history_menu():
    recent = Deque(maxlen=5)   # yeni səhifə öndən girir, ən köhnə arxadan düşür
    while True:
        header("DEQUE — Son baxılan səhifələr (maks. 5) və palindrom")
        print(" Tarixçə (yenidən köhnəyə):", ", ".join(recent.to_list()) or "(boş)")
        print(" 1) Səhifəyə daxil ol   2) Geri (son səhifəni sil)   3) Ən köhnəni sil")
        print(" 4) Palindrom yoxla     0) Geri")
        c = ask(" Seçim: ")
        if c == "1":
            page = ask(" Səhifə adı: ")
            if page:
                recent.push_front(page)
        elif c == "2":
            print(" Silindi:", recent.pop_front() if not recent.is_empty() else "boşdur")
        elif c == "3":
            print(" Silindi:", recent.pop_back() if not recent.is_empty() else "boşdur")
        elif c == "4":
            w = ask(" Söz/cümlə: ")
            print(" Palindromdur ✓" if is_palindrome(w) else " Palindrom deyil ✗")
        elif c == "0":
            return


def sqd_menu():
    while True:
        header("3. STACK, QUEUE, DEQUE")
        print(" 1) Stack  — Mətn redaktoru (Undo/Redo, mötərizə yoxlama)")
        print(" 2) Queue  — Kafe sifariş növbəsi")
        print(" 3) Deque  — Brauzer tarixçəsi və palindrom")
        print(" 0) Geri")
        c = ask(" Seçim: ")
        if c == "1":
            editor_menu()
        elif c == "2":
            order_queue_menu()
        elif c == "3":
            history_menu()
        elif c == "0":
            return


# =====================================================================
# 4. HASH TABLE — Telefon kitabçası
# =====================================================================
def show_buckets(ht):
    for i, chain in enumerate(ht.bucket_view()):
        print(f"  [{i:>2}] " + (" -> ".join(chain) if chain else "∅"))
    print(f"  ölçü={len(ht)}  tutum={ht.capacity}  load factor={ht.load_factor:.2f}"
          f"  collision={ht.collisions}")


def phonebook_menu():
    book = HashTable(capacity=8)
    for name, phone in (("Alı", "050 111 11 11"), ("Ləman", "055 222 22 22"),
                        ("Tahir", "070 333 33 33"), ("Nərmin", "051 444 44 44")):
        book.put(name, phone)
    while True:
        header("4. HASH TABLE — Telefon kitabçası (chaining)")
        print(" 1) Kontakt əlavə et/yenilə  2) Axtar  3) Sil  4) Hamısı")
        print(" 5) Bucket-ləri göstər       6) Collision nümayişi   0) Geri")
        c = ask(" Seçim: ")
        if c == "1":
            name = ask(" Ad: ")
            if name:
                book.put(name, ask(" Telefon: "))
        elif c == "2":
            name = ask(" Ad: ")
            print(" Tapıldı:", book.get(name) if book.contains(name) else "yoxdur")
        elif c == "3":
            print(" Silindi." if book.remove(ask(" Ad: ")) else " Belə kontakt yoxdur.")
        elif c == "4":
            for k, v in sorted(book.items()):
                print(f"  {k:<15} {v}")
        elif c == "5":
            show_buckets(book)
        elif c == "6":
            collision_demo()
        elif c == "0":
            return


def collision_demo():
    print("\n Kiçik tutumlu (4) cədvələ 6 açar — collision qaçılmazdır.")
    print(" Rehash-ı söndürürük ki, zəncirlər görünsün:")
    ht = HashTable(capacity=4)
    ht.MAX_LOAD_FACTOR = float("inf")
    for k in ("alma", "armud", "heyva", "nar", "üzüm", "gilas"):
        print(f"  put('{k}') → bucket {ht._index(k)}")
        ht.put(k, len(k))
    show_buckets(ht)
    print(" Eyni bucket-ə düşən açarlar bir zəncirdə saxlanır; axtarış zəncir boyu gedir.")
    print(" Normal rejimdə load factor > 0.75 olanda tutum 2x artır və açarlar yenidən bölünür.")


# =====================================================================
# 5. BST
# =====================================================================
def bst_menu():
    tree = BinarySearchTree()
    for k in (50, 30, 70, 20, 40, 60, 80):
        tree.insert(k)
    while True:
        header("5. BINARY SEARCH TREE")
        print(tree.pretty())
        print(f" ölçü={len(tree)}  hündürlük={tree.height()}  inorder={tree.inorder()[:20]}")
        print(" 1) Əlavə et  2) Axtar  3) Sil  4) Boşalt")
        print(" 5) Sıralanmış 1..10 əlavə et (formaya bax)  6) Təsadüfi 10 ədəd əlavə et")
        print(" 7) Təcrübə: təsadüfi vs sıralanmış (ölçmə + izah)   0) Geri")
        c = ask(" Seçim: ")
        try:
            if c == "1":
                print(" Əlavə olundu." if tree.insert(int(ask(" Ədəd: "))) else " Artıq var.")
            elif c == "2":
                found, cmp_ = tree.search(int(ask(" Ədəd: ")))
                print(f" {'Tapıldı' if found else 'Tapılmadı'} ({cmp_} müqayisə)")
            elif c == "3":
                print(" Silindi." if tree.delete(int(ask(" Ədəd: "))) else " Belə açar yoxdur.")
            elif c == "4":
                tree = BinarySearchTree()
            elif c == "5":
                tree = BinarySearchTree()
                for k in range(1, 11):
                    tree.insert(k)
                print(" Diqqət: ağac sağa doğru düz xəttə çevrildi — hündürlük 10 oldu.")
            elif c == "6":
                tree = BinarySearchTree()
                for k in random.sample(range(1, 100), 10):
                    tree.insert(k)
            elif c == "7":
                benchmarks.bst_shape_experiment()
            elif c == "0":
                return
        except ValueError:
            print(" Tam ədəd daxil edin.")


# =====================================================================
# Əsas menyu
# =====================================================================
def linked_list_menu():
    header("2. SINGLY vs DOUBLY LINKED LIST")
    s, d = SinglyLinkedList(), DoublyLinkedList()
    for x in (1, 2, 3, 4, 5):
        s.push_back(x)
        d.push_back(x)
    print(" Singly:", " -> ".join(map(str, s)))
    print(" Doubly:", " <-> ".join(map(str, d)), "| tərsinə:", list(d.reversed()))
    print(" pop_back → Singly:", s.pop_back(), " Doubly:", d.pop_back())
    print(" remove(3), push_front(0) ...")
    s.remove(3); d.remove(3); s.push_front(0); d.push_front(0)
    print(" Singly:", s.to_list(), " Doubly:", d.to_list())
    benchmarks.benchmark_linked_lists()


def demo():
    """Qeyri-interaktiv: hər bölməni ardıcıl göstərir."""
    benchmarks.benchmark_arrays()
    linked_list_menu()

    header("3. STACK / QUEUE / DEQUE nümayişi")
    ed = TextEditor()
    ed.write("Salam"); ed.write(", dünya"); ed.delete(5)
    print(f" Redaktor: \"{ed.text}\"")
    ed.undo(); print(f" Undo →     \"{ed.text}\"")
    ed.undo(); print(f" Undo →     \"{ed.text}\"")
    ed.redo(); print(f" Redo →     \"{ed.text}\"")
    print(" Mötərizə '(a[b]{c})':", check_brackets("(a[b]{c})")[0],
          "| '(a[b)]':", check_brackets("(a[b)]")[0])
    q = Queue()
    for o in ("Çay", "Qəhvə", "Paxlava"):
        q.enqueue(o)
    print(" Sifariş növbəsi:", q.to_list(), "→ hazırlanır:", q.dequeue(), "→ qalan:", q.to_list())
    h = Deque(maxlen=3)
    for p in ("ana səhifə", "xəbərlər", "idman", "hava"):
        h.push_front(p)
    print(" Son 3 səhifə:", h.to_list())
    for w in ("Ana", "kitab", "Ey Edip Adanada pide ye"):
        print(f" Palindrom '{w}':", is_palindrome(w))

    header("4. HASH TABLE nümayişi")
    collision_demo()
    big = HashTable()
    for i in range(1000):
        big.put(f"user{i}", i)
    lens = big.chain_lengths()
    print(f"\n 1000 açar sonra: tutum={big.capacity}, load factor={big.load_factor:.2f}, "
          f"ən uzun zəncir={max(lens)}, boş bucket={lens.count(0)}")
    print(" get('user500') =", big.get("user500"), "| remove →", big.remove("user500"),
          "| get →", big.get("user500"))

    header("5. BST nümayişi")
    t = BinarySearchTree()
    for k in (50, 30, 70, 20, 40, 60, 80, 65):
        t.insert(k)
    print(t.pretty())
    print(" search(65):", t.search(65), "| delete(70) (iki uşaqlı node)")
    t.delete(70)
    print(t.pretty())
    print(" inorder:", t.inorder())
    s = BinarySearchTree()
    for k in range(1, 8):
        s.insert(k)
    print("\n Sıralanmış 1..7 əlavə edəndə:")
    print(s.pretty())
    benchmarks.bst_shape_experiment()


def main():
    if "--demo" in sys.argv:
        demo()
        return
    while True:
        header("ALQORİTMLƏR VƏ VERİLƏNLƏR STRUKTURLARI")
        print(" 1) Array vs Dynamic Array — vaxt ölçmələri")
        print(" 2) Singly vs Doubly Linked List — müqayisə")
        print(" 3) Stack, Queue, Deque — tətbiq funksiyaları")
        print(" 4) Hash Table (chaining) — telefon kitabçası")
        print(" 5) Binary Search Tree — əlavə/axtarış/silmə və forma")
        print(" 6) Hamısını avtomatik göstər (demo)")
        print(" 0) Çıxış")
        c = ask(" Seçim: ")
        if c == "1":
            benchmarks.benchmark_arrays()
        elif c == "2":
            linked_list_menu()
        elif c == "3":
            sqd_menu()
        elif c == "4":
            phonebook_menu()
        elif c == "5":
            bst_menu()
        elif c == "6":
            demo()
        elif c == "0":
            print(" Sağ olun!")
            return


if __name__ == "__main__":
    main()
