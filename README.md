# alqorithm_task — Verilənlər strukturları konsol tətbiqi

Python 3 ilə yazılmış kiçik konsol tətbiqi. Beş mövzunun hamısı **xarici kitabxana olmadan, sıfırdan** yazılıb (`ds/` qovluğu).

## İşə salmaq

```bash
python main.py          # interaktiv menyu
python main.py --demo   # bütün ölçmələri və nümayişləri avtomatik göstərir
python -m unittest tests.py   # testlər
```

Python 3.8+ kifayətdir, əlavə paket lazım deyil.

## Struktur

```
alqorithm_task/
├── main.py              # konsol menyusu + tətbiq funksiyaları (redaktor, növbə, tarixçə, telefon kitabçası)
├── benchmarks.py        # vaxt ölçmələri və BST təcrübəsi
├── tests.py             # unit testlər
└── ds/
    ├── arrays.py             # StaticArray, DynamicArray
    ├── linked_lists.py       # SinglyLinkedList, DoublyLinkedList
    ├── stack_queue_deque.py  # Stack, Queue, Deque
    ├── hash_table.py         # HashTable (separate chaining)
    └── bst.py                # BinarySearchTree
```

## 1. Array və Dynamic Array

- `StaticArray` — sabit tutum; dolanda `OverflowError`.
- `DynamicArray` — dolanda tutumu **2 dəfə** artırır, 1/4-ə qədər boşalanda yarıya endirir.
- Ölçülən əməliyyatlar: `append`, başa `insert`, başdan və sondan `delete`, xətti `search` — **1 000, 5 000, 20 000** elementlik verilənlər üzərində.

Nümunə nəticə (µs / əməliyyat, maşından asılı olaraq dəyişir):

| n | Struktur | append | insert[0] | delete[0] | delete[son] | search |
|---|---|---|---|---|---|---|
| 1 000 | Static | 0.12 | 57 | 42 | 0.27 | 10 |
| 1 000 | Dynamic | 0.22 | 50 | 43 | 0.30 | 12 |
| 20 000 | Static | 0.14 | 904 | 1 132 | 0.58 | 294 |
| 20 000 | Dynamic | 0.11 | 887 | 913 | 0.33 | 226 |

**Nəticə:** `append` və sondan silmə O(1) — n artanda vaxt dəyişmir. Başa əlavə/başdan silmə və axtarış O(n) — n 20 dəfə artanda vaxt da ~15–25 dəfə artır. Dynamic Array arabir `resize` edir (20 000 element üçün cəmi 13 dəfə), ona görə amortized `append` yenə O(1)-dir.

## 2. Singly və Doubly Linked List

| Əməliyyat | Singly | Doubly |
|---|---|---|
| push_front / push_back / pop_front | O(1) | O(1) |
| **pop_back** | **O(n)** — sondan əvvəlki node-u tapmaq üçün başdan getmək lazımdır | **O(1)** — `tail.prev` var |
| search / remove(value) | O(n) | O(n) (tapılandan sonra silmə O(1)) |
| Yaddaş | node-da 1 göstərici | node-da 2 göstərici |

Ölçmədə ən böyük fərq `pop_back`-dadır: 20 000 elementdə Singly ~440 µs, Doubly ~0.2 µs.

## 3. Stack, Queue, Deque — tətbiqdə istifadəsi

Hər üçü öz linked list-lərimiz üzərində qurulub.

- **Stack (LIFO)** → **Mətn redaktoru: Undo / Redo.** Hər dəyişiklikdən əvvəlki vəziyyət undo stack-ə qoyulur, undo edəndə oradan çıxarılıb redo stack-ə keçir. Əlavə olaraq stack ilə **mötərizə balansı** yoxlanır.
- **Queue (FIFO)** → **Kafe sifariş növbəsi.** Gələn sifarişlər sona əlavə olunur, ilk gələn ilk hazırlanır.
- **Deque** → **Brauzer "son baxılanlar" tarixçəsi** (maks. 5): yeni səhifə öndən girir, limit aşanda ən köhnəsi arxadan düşür. Həmçinin **palindrom yoxlayıcı**: hər iki ucdan simvol çıxarıb müqayisə edir.

## 4. Hash Table (chaining)

- Hər bucket bir **singly linked list zənciridir**. Eyni indeksə düşən açarlar (collision) həmin zəncirə əlavə olunur.
- Sətirlər üçün öz hash funksiyası (djb2), indeks = `hash % capacity`.
- `load factor > 0.75` olanda tutum 2 dəfə artır və bütün açarlar yenidən paylanır (rehash) — zəncirlər qısa qalır, orta `get/put/remove` O(1).
- Tətbiqdə: **telefon kitabçası** (əlavə/axtar/sil, bucket-ləri göstər) və collision nümayişi (4 bucket-ə 6 açar — zəncirlər ekranda görünür).

## 5. Binary Search Tree

- `insert`, `search` (müqayisə sayını da qaytarır), `delete` (3 hal: yarpaq, bir uşaqlı, iki uşaqlı — inorder varis ilə əvəz), `height`, `inorder`, `min/max`.
- Əməliyyatlar iterativdir ki, degenerasiya olunmuş ağacda rekursiya limiti aşılmasın.

### Sıralanmış verilənlərin təsiri

2 000 açar ilə təcrübə (`main.py` → 5 → 7):

| Daxil etmə sırası | Hündürlük | Orta müqayisə (axtarış) |
|---|---|---|
| Təsadüfi | ~24 | ~14 |
| Sıralanmış (artan) | **2000** | **~1000** |

**İzah:** BST-də hər yeni açar kökdən başlayaraq kiçikdirsə sola, böyükdürsə sağa gedir. Verilənlər **sıralanmış** gələndə hər yeni açar əvvəlkilərin hamısından böyükdür və həmişə **sağ** uşağa düşür. Ağac budaqlanmır və faktiki olaraq **linked list-ə çevrilir**:

```
1
 └─ 2
     └─ 3
         └─ 4 ...
```

- Hündürlük `log2(n)` əvəzinə `n` olur.
- Axtarış O(log n)-dən **O(n)**-ə düşür (orta ~n/2 müqayisə).
- Bütün verilənləri əlavə etmək O(n log n) əvəzinə **O(n²)** olur.

Təsadüfi sıra ilə əlavə edəndə ağac təxminən balanslı qalır (hündürlük ~2–3·log2 n). Həll yolu: verilənləri qarışdırmaq və ya özü-balanslaşan ağaclardan (**AVL, Red-Black Tree**) istifadə etmək.
