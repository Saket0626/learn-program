# Part 4 continued: Chapters 4.4–4.5

## Chapter 4.4: Hash maps and hash sets

### Analogy: routing mail to a mailbox group

Imagine sorting mail into numbered groups.

A rule converts the recipient’s name into a group number. You go directly to that group, then locate the intended recipient.

A hash table follows a related idea:

- Compute a hash from the key.
- Convert that hash into a storage position.
- Locate the key there.
- Resolve collisions when several keys share the location.

### Hash maps

A hash map associates keys with values using hash-based lookup.

Python’s dict is a hash-based mapping.

A bucket is a location holding entries assigned to the same table position.

### Hash function and collision

A hash function produces an integer from a key.

The table can convert that integer into a bucket index: hash_value % bucket_count.

A collision occurs when different keys map to the same bucket or otherwise compete within the lookup scheme.

Collisions are normal. A correct hash table must handle them.

### Separate chaining

Separate chaining stores a collection of entries at each bucket.

Our implementation uses:

- An outer list of buckets.
- A list of key-value pairs in each bucket.

For eight buckets and integer keys:

- 1 % 8 = 1
- 9 % 8 = 1
- 17 % 8 = 1

All three keys occupy bucket 1.

Python’s actual dictionary uses a different collision-resolution design. We use chaining because its mechanics are easier to inspect.

### Load factor

The load factor is α = number of entries / number of buckets.

As the table fills, buckets tend to contain more entries.

Resizing increases the bucket count and redistributes the entries.

### Our contract

To keep the first implementation focused:

- Keys must be integers.
- Values may be any Python objects.
- Setting an existing key replaces its value.
- Missing lookup and deletion raise KeyError.
- No iteration-order promise is made.

Integer keys serve directly as our teaching hash values. This is not a sophisticated hash function, so patterned keys can create many collisions.

```python
class IntegerHashMap:
    def __init__(self):
        self._size = 0
        self._buckets = self._make_buckets(8)

    def _make_buckets(self, count):
        buckets = []

        # Create independent bucket lists.
        for index in range(count):
            buckets.append([])

        return buckets

    def __len__(self):
        return self._size

    def _bucket_index(self, key):
        return key % len(self._buckets)

    def _resize(self):
        old_buckets = self._buckets

        # Allocate twice as many buckets.
        self._buckets = self._make_buckets(len(old_buckets) * 2)

        # Recompute bucket positions using the new bucket count.
        for bucket in old_buckets:
            for key, value in bucket:
                index = self._bucket_index(key)
                self._buckets[index].append((key, value))

        # The number of entries has not changed.

    def contains(self, key):
        index = self._bucket_index(key)

        for stored_key, stored_value in self._buckets[index]:
            if stored_key == key:
                return True

        return False

    def get(self, key):
        index = self._bucket_index(key)

        for stored_key, stored_value in self._buckets[index]:
            if stored_key == key:
                return stored_value

        raise KeyError(key)

    def put(self, key, value):
        index = self._bucket_index(key)
        bucket = self._buckets[index]

        # Update without creating another copy of the key.
        for position in range(len(bucket)):
            stored_key, stored_value = bucket[position]

            if stored_key == key:
                bucket[position] = (key, value)
                return

        # Keep the load factor at or below 0.75 after insertion.
        if (self._size + 1) * 4 > len(self._buckets) * 3:
            self._resize()
            index = self._bucket_index(key)

        self._buckets[index].append((key, value))
        self._size = self._size + 1

    def remove(self, key):
        index = self._bucket_index(key)
        bucket = self._buckets[index]

        for position in range(len(bucket)):
            stored_key, stored_value = bucket[position]

            if stored_key == key:
                bucket.pop(position)
                self._size = self._size - 1
                return stored_value

        raise KeyError(key)

    def keys(self):
        result = []

        for bucket in self._buckets:
            for key, value in bucket:
                result.append(key)

        return result
```

### Worked trace: collisions and updates

```python
mapping = IntegerHashMap()

mapping.put(1, "apple")
mapping.put(9, "banana")
mapping.put(1, "pear")

assert mapping.get(1) == "pear"
assert mapping.get(9) == "banana"
assert len(mapping) == 2
```

Bucket 1 evolves as follows:

| Operation | Bucket 1 |
| --- | --- |
| Insert key 1 | [(1, "apple")] |
| Insert key 9 | [(1, "apple"), (9, "banana")] |
| Update key 1 | [(1, "pear"), (9, "banana")] |

A collision does not mean one key overwrites the other.

The key comparison distinguishes the entries.

### Hash sets

A hash set records keys without meaningful associated values.

We can build one using the map above:

```python
class IntegerHashSet:
    def __init__(self):
        self._map = IntegerHashMap()

    def __len__(self):
        return len(self._map)

    def add(self, value):
        # The stored True is only a placeholder.
        self._map.put(value, True)

    def contains(self, value):
        return self._map.contains(value)

    def remove(self, value):
        # Missing values raise KeyError.
        self._map.remove(value)

    def discard(self, value):
        # Missing values are allowed.
        if self._map.contains(value):
            self._map.remove(value)

    def values(self):
        return self._map.keys()
```

```python
seen = IntegerHashSet()

seen.add(4)
seen.add(4)
seen.add(12)

assert len(seen) == 2
assert seen.contains(4) == True

seen.remove(4)

assert seen.contains(4) == False
```

### Costs

Let n be the entry count and B the bucket count.

| Operation | With well-distributed keys and controlled load | Worst case |
| --- | --- | --- |
| Lookup or membership | O(1) expected | O(n) |
| Insert or update | O(1) expected amortized | O(n) |
| Remove | O(1) expected | O(n) |
| Produce all keys in this implementation | O(B + n) | O(B + n) |

Storage is O(B + n).

This implementation does not shrink after deletions. Its bucket count can reflect an earlier larger table.

### When to use a map

Use a map for:

- Frequencies.
- Value-to-position lookup.
- Grouping related items.
- Remembering previously computed results.
- Associating identifiers with records.

### When to use a set

Use a set for:

- Duplicate detection.
- Membership.
- Tracking visited items.
- Distinct-value counting.

### Common mistakes

- Assuming collisions cannot occur.
- Forgetting to redistribute entries after resizing.
- Treating average constant-time lookup as a worst-case guarantee.
- Using an object as a key when its equality or hash behavior can change incompatibly.
- Using a set when counts are required.

### Chapter practice

1. Guided: With eight buckets, which bucket receives keys 2, 10, and 18?
2. Why must resizing recompute bucket positions?
3. Which structure fits “count each word”: a set or a map?
4. What happens if every key goes into one bucket?

#### Answers and explanations

1. All go to bucket 2: 2 % 8 = 2, 10 % 8 = 2, 18 % 8 = 2.

2. The expression uses the bucket count: key % bucket_count. Changing that count can change the correct destination.

3. A map, because each word needs an associated frequency.

4. The bucket becomes a collection that may require scanning all entries. Lookup can become O(n).

## Chapter 4.5: Linked lists

### Analogy: a chain of directions

Imagine finding a location by following instructions:

- The first note tells you where the second note is.
- The second tells you where the third is.
- The final note says there is no next note.

A linked list stores elements through connected nodes.

A node is an object containing a value and one or more references to other nodes.

A singly linked list gives each node a reference to the next node.

The head refers to the first node.

The tail refers to the last node.

### Memory structure

Nodes need not be adjacent in memory.

Each arrow between nodes represents a stored next reference.

Unlike array indexing, accessing the third node requires following links from the head.

### The node class

```python
class Node:
    def __init__(self, value):
        self.value = value
        self.next = None
```

### The list class

```python
class SinglyLinkedList:
    def __init__(self):
        self.head = None
        self.tail = None
        self._size = 0

    def __len__(self):
        return self._size

    def prepend(self, value):
        node = Node(value)

        # The old first node follows the new first node.
        node.next = self.head
        self.head = node

        # An empty list also needs a tail.
        if self.tail is None:
            self.tail = node

        self._size = self._size + 1

    def append(self, value):
        node = Node(value)

        if self.tail is None:
            # The new node is both first and last.
            self.head = node
            self.tail = node
        else:
            # Attach after the old tail.
            self.tail.next = node
            self.tail = node

        self._size = self._size + 1

    def get(self, index):
        if index < 0 or index >= self._size:
            raise IndexError("Invalid linked-list index")

        current = self.head

        # Follow one link for each position passed.
        for step in range(index):
            current = current.next

        return current.value

    def pop_front(self):
        if self.head is None:
            raise IndexError("Cannot remove from an empty list")

        removed = self.head
        self.head = removed.next

        # Removing the only node empties both ends.
        if self.head is None:
            self.tail = None

        removed.next = None
        self._size = self._size - 1

        return removed.value

    def remove_first(self, value):
        previous = None
        current = self.head

        while current is not None:
            if current.value == value:
                if previous is None:
                    # Remove the head.
                    self.head = current.next
                else:
                    # Bypass the current node.
                    previous.next = current.next

                if current is self.tail:
                    self.tail = previous

                current.next = None
                self._size = self._size - 1
                return True

            previous = current
            current = current.next

        return False

    def to_list(self):
        result = []
        current = self.head

        while current is not None:
            result.append(current.value)
            current = current.next

        return result
```

### Worked deletion

Starting values: 10, 20, 30. Remove the first 20.

At the matching node:

| Name | Refers to |
| --- | --- |
| previous | Node containing 10 |
| current | Node containing 20 |
| current.next | Node containing 30 |

The key instruction is previous.next = current.next.

The node containing 10 now leads directly to the node containing 30.

```python
linked = SinglyLinkedList()

linked.append(10)
linked.append(20)
linked.append(30)

assert linked.remove_first(20) == True
assert linked.to_list() == [10, 30]

linked.prepend(5)

assert linked.pop_front() == 5
assert linked.get(1) == 30
```

### Costs

| Operation | Cost |
| --- | --- |
| Read head or tail value when present | O(1) |
| Prepend | O(1) |
| Append with a stored tail | O(1) |
| Remove head | O(1) |
| Access index i | O(i + 1) |
| Search by value | O(n) |
| Remove by value, including search | O(n) |
| Traverse all nodes | O(n) |

Storage is O(n), with additional per-node reference and object overhead.

### The deletion qualification

“Linked-list deletion is constant time” is incomplete.

Rewiring a known node’s predecessor is constant time.

Finding that predecessor may take linear time.

### Doubly linked lists

A doubly linked list stores both next, pointing forward, and previous, pointing backward.

That allows constant-time removal of a known node when the list’s endpoints are updated correctly.

We will implement this structure as a deque in Chapter 4.8.

### When to use linked lists

They are useful when:

- You already hold references to the relevant nodes.
- You need frequent local link changes.
- The problem itself provides linked nodes.
- You are building structures that need stable node references.

In ordinary Python applications, a built-in list or deque is often more convenient and has lower overhead. Linked lists remain important for learning reference manipulation and solving linked-list problems.

### Common mistakes

- Losing the rest of the list by overwriting a link too early.
- Forgetting to update the tail after deleting the final node.
- Treating a node’s value as the node itself.
- Forgetting to advance current.
- Accidentally creating a cycle.

### Chapter practice

1. Guided: Build 3 → 6 → 9, then remove 6.
2. Why is index access slower than in an array?
3. What must happen to both head and tail when the only node is removed?

#### Answers and explanations

1.

```python
linked = SinglyLinkedList()

for value in [3, 6, 9]:
    linked.append(value)

linked.remove_first(6)

assert linked.to_list() == [3, 9]
```

2. A linked list does not calculate a node’s location from its index. It must follow links through earlier nodes.

3. Both must become None. Otherwise, one endpoint would incorrectly retain a node that is no longer in the list.
