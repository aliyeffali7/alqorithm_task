"""Vaxt ölçmələri: Array vs Dynamic Array, Singly vs Doubly Linked List, BST təcrübəsi."""

import math
import random
import time

from ds import (StaticArray, DynamicArray, SinglyLinkedList, DoublyLinkedList,
                BinarySearchTree)

DEFAULT_SIZES = (1_000, 5_000, 20_000)


def _measure(fn, repeats):
    """fn-i repeats dəfə çağırır, bir əməliyyatın orta vaxtını mikrosaniyə ilə qaytarır."""
    start = time.perf_counter()
    for i in range(repeats):
        fn(i)
    return (time.perf_counter() - start) / repeats * 1e6


def _table(title, headers, rows):
    widths = [max(len(str(h)), *(len(str(r[i])) for r in rows)) for i, h in enumerate(headers)]
    line = "+".join("-" * (w + 2) for w in widths)
    out = [f"\n{title}", "+" + line + "+",
           "|" + "|".join(f" {str(h):<{w}} " for h, w in zip(headers, widths)) + "|",
           "+" + line + "+"]
    for r in rows:
        out.append("|" + "|".join(f" {str(c):>{w}} " for c, w in zip(r, widths)) + "|")
    out.append("+" + line + "+")
    print("\n".join(out))


def _fmt(us):
    return f"{us:,.2f} µs"


# ---------------------------------------------------------------- 1. Array
def benchmark_arrays(sizes=DEFAULT_SIZES, ops=200):
    print("\n" + "=" * 70)
    print(" 1. ARRAY vs DYNAMIC ARRAY — bir əməliyyatın orta vaxtı")
    print("=" * 70)
    rows = []
    for n in sizes:
        for name in ("Static Array", "Dynamic Array"):
            if name == "Static Array":
                arr = StaticArray(n + 2 * ops)        # tutumu əvvəlcədən bilməliyik
            else:
                arr = DynamicArray(4)               # kiçik başlayır, özü böyüyür
            t0 = time.perf_counter()
            for i in range(n):
                arr.append(i)
            build = (time.perf_counter() - t0) / n * 1e6

            append_t = _measure(lambda i: arr.append(n + i), ops)
            insert_t = _measure(lambda i: arr.insert(0, -i), ops)       # başa əlavə — O(n)
            delete_t = _measure(lambda i: arr.delete(0), ops)           # başdan silmə — O(n)
            delete_end_t = _measure(lambda i: arr.delete(len(arr) - 1), ops)  # sondan — O(1)
            targets = [random.randrange(n) for _ in range(ops)]
            search_t = _measure(lambda i: arr.search(targets[i]), ops)  # xətti — O(n)
            extra = f"resize={arr.resize_count}" if isinstance(arr, DynamicArray) else "-"
            rows.append([f"{n:,}", name, _fmt(build), _fmt(append_t), _fmt(insert_t),
                         _fmt(delete_t), _fmt(delete_end_t), _fmt(search_t), extra])
    _table("Nəticələr (µs/əməliyyat):",
           ["n", "Struktur", "build(append)", "append", "insert[0]",
            "delete[0]", "delete[son]", "search", "qeyd"], rows)
    print("""
Şərh:
 • append: hər ikisində ~O(1). Dynamic Array arabir resize edir (köçürmə O(n)),
   amma tutum 2x artdığı üçün amortized dəyər yenə O(1)-dir.
 • insert[0] / delete[0]: hər ikisində O(n) — bütün elementlər sürüşdürülür,
   n böyüdükcə vaxt təxminən xətti artır.
 • delete[son]: O(1) — heç nə sürüşdürülmür.
 • search: sırasız massivdə xətti axtarış, O(n).
 • Fərq: Static Array-in tutumu sabitdir (dolanda OverflowError), Dynamic Array
   yaddaşı özü idarə edir — bunun qiyməti resize anlarında olan əlavə köçürmədir.""")


# ---------------------------------------------------------- 2. Linked List
def benchmark_linked_lists(sizes=DEFAULT_SIZES, ops=200):
    print("\n" + "=" * 70)
    print(" 2. SINGLY vs DOUBLY LINKED LIST — bir əməliyyatın orta vaxtı")
    print("=" * 70)
    rows = []
    for n in sizes:
        for cls in (SinglyLinkedList, DoublyLinkedList):
            lst = cls()
            for i in range(n):
                lst.push_back(i)
            pf = _measure(lambda i: lst.push_front(-i - 1), ops)
            pb = _measure(lambda i: lst.push_back(n + i), ops)
            popf = _measure(lambda i: lst.pop_front(), ops)
            popb = _measure(lambda i: lst.pop_back(), ops)
            targets = [random.randrange(n) for _ in range(ops)]
            srch = _measure(lambda i: lst.search(targets[i]), ops)
            rm_targets = random.sample(range(n), ops)
            rm = _measure(lambda i: lst.remove(rm_targets[i]), ops)
            rows.append([f"{n:,}", cls.__name__, _fmt(pf), _fmt(pb), _fmt(popf),
                         _fmt(popb), _fmt(srch), _fmt(rm)])
    _table("Nəticələr (µs/əməliyyat):",
           ["n", "Struktur", "push_front", "push_back", "pop_front",
            "pop_back", "search", "remove(value)"], rows)
    print("""
Şərh:
 • push_front / push_back / pop_front: hər ikisində O(1).
 • pop_back: Singly-də O(n) — sondan əvvəlki node-u tapmaq üçün başdan getmək
   lazımdır. Doubly-də O(1) — tail.prev birbaşa məlumdur. Cədvəldə ən böyük fərq budur.
 • search / remove(value): hər ikisində O(n) (dəyəri axtarmaq lazımdır).
   Doubly-də node tapılandan sonra silmə O(1)-dir, çünki prev artıq məlumdur.
 • Doubly-nin qiyməti: hər node-da əlavə 'prev' göstəricisi (daha çox yaddaş)
   və hər əməliyyatda bir az daha çox göstərici yeniləmə.""")


# -------------------------------------------------------------------- 5. BST
def bst_shape_experiment(n=2_000, searches=500):
    print("\n" + "=" * 70)
    print(" 5. BST — TƏSADÜFİ vs SIRALANMIŞ verilənlərin əlavə edilməsi")
    print("=" * 70)
    keys = list(range(n))
    shuffled = keys[:]
    random.shuffle(shuffled)
    lookups = [random.randrange(n) for _ in range(searches)]
    rows = []
    for label, data in (("Təsadüfi sıra", shuffled), ("Sıralanmış (artan)", keys)):
        tree = BinarySearchTree()
        t0 = time.perf_counter()
        for k in data:
            tree.insert(k)
        ins = (time.perf_counter() - t0) / n * 1e6
        t0 = time.perf_counter()
        total_cmp = 0
        for k in lookups:
            total_cmp += tree.search(k)[1]
        srch = (time.perf_counter() - t0) / searches * 1e6
        rows.append([label, f"{n:,}", tree.height(), f"{total_cmp / searches:,.1f}",
                     _fmt(ins), _fmt(srch)])
    _table("Nəticələr:",
           ["Daxil etmə sırası", "n", "hündürlük", "orta müqayisə", "insert", "search"], rows)
    print(f"""
İzah:
 • İdeal (balanslı) ağacın hündürlüyü ≈ log2(n) = {math.log2(n):.1f}.
   Təsadüfi sıra ilə əlavə edəndə hündürlük buna yaxın olur (adətən ~2–3·log2 n),
   ona görə axtarış O(log n) olur — bir neçə on müqayisə.
 • Sıralanmış verilənlər əlavə olunanda hər yeni açar əvvəlkindən böyükdür və
   həmişə SAĞ uşağa gedir. Ağac budaqlanmır, faktiki olaraq linked list-ə
   çevrilir: hündürlük = n. Axtarış da O(n) olur — orta hesabla ~n/2 müqayisə.
 • Əlavə etmə də pisləşir: k-cı açarı yerləşdirmək üçün k addım lazımdır,
   cəmi O(n²). Yuxarıdakı cədvəldə insert və search vaxtlarının dəfələrlə
   artması bunu göstərir.
 • Həll: verilənləri qarışdırmaq və ya özü-balanslaşan ağaclardan
   (AVL, Red-Black) istifadə etmək — onlar hündürlüyü həmişə O(log n) saxlayır.""")


def run_all():
    benchmark_arrays()
    benchmark_linked_lists()
    bst_shape_experiment()
