# From Zero to LeetCode Hard

# Part 4: Core Data Structures

A data structure is a way to organize information so particular operations can be performed efficiently.

A list, dictionary, and set can all contain information about the same values. They make different questions easy to answer:

- A list makes “What is at position 5?” easy.
- A dictionary makes “What information belongs to this key?” easy.
- A set makes “Have I seen this value?” easy.

The goal is not to memorize a catalog of structures. It is to connect:

- The question you must answer.
- The information you need to maintain.
- The operations you will perform repeatedly.
- The structure that supports those operations.

This part covers every structure in the original plan:

- Arrays and dynamic arrays.
- Strings.
- Hash maps and hash sets.
- Linked lists.
- Stacks.
- Queues.
- Deques.
- Heaps and priority queues.
- Binary trees.
- Binary search trees.
- Tries.
- Graphs.
- Union-find.

We begin with the Python classes needed to build them.

## Implementation conventions

The implementations are educational. They expose the important mechanics rather than reproduce every feature of Python’s built-in types.

“From scratch” here means implementing the structure’s organization and operations using simpler Python components. Python code still relies on Python’s memory allocation, object references, and basic containers.

For example, our dynamic array will use a Python list as a fixed-capacity backing store. We will implement resizing and shifting ourselves. This demonstrates the algorithm without claiming to recreate Python’s underlying memory allocator.

Unless stated otherwise:

- Numeric values and indices are ordinary-size integers.
- Hash-table bounds assume ordinary-size keys.
- Empty removal operations raise an exception.
- Implementations do not support concurrent mutation.

Code examples have been reviewed by hand, not execution-tested in this session.

Run each chapter’s definitions before its examples.

Hash maps are covered in depth in Chapter 4.4.

## Chapter 4.1: Classes, objects, and interfaces

### Why we need classes

Suppose a structure needs to remember:

- Its first node.
- Its last node.
- Its number of elements.

It also needs operations that update those pieces together.

A class lets us package the state and operations in one place.

A class defines a kind of object.

An instance is a particular object created from that class.

An attribute is a named piece of information accessed through an object, such as counter.value.

A method is a function accessed through an object.

Python’s class system groups state and behavior in this way. An instance can have its own attributes, while methods describe operations on those instances.

### A first class

```python
# Define a new kind of object.
class Counter:
    def __init__(self, starting_value=0):
        # Give this particular object its own value.
        self.value = starting_value

    def increase(self):
        # Change this object's stored value.
        self.value = self.value + 1

    def read(self):
        # Return this object's current value.
        return self.value
```

Use it:

```python
# Create two independent instances.
first = Counter(5)
second = Counter(20)

# Change only the first instance.
first.increase()

print(first.read())   # 6
print(second.read())  # 20
```

### What self means

self is the conventional name for the instance receiving the method call.

When you write first.increase(), Python supplies first as the method’s self argument.

Inside that call, self.value refers to the attribute belonging to first.

The name self is a convention, not a special keyword. Use the convention consistently.

### What __init__ means

__init__ is a special method Python calls to initialize a newly created instance.

In first = Counter(5), the initialization method receives:

- The new instance as self.
- 5 as starting_value.

__init__ should not return a result other than None.

### Special methods

A special method has a name Python recognizes for a particular language operation.

For example, defining __len__ lets an object work with len.

```python
class Bag:
    def __init__(self):
        # Each Bag receives a separate list.
        self._items = []

    def add(self, value):
        self._items.append(value)

    def __len__(self):
        return len(self._items)


bag = Bag()
bag.add(10)
bag.add(20)

print(len(bag))  # 2
```

A leading underscore, as in _items, conventionally means: this is an implementation detail. Use the class’s public operations instead.

It does not make the attribute inaccessible.

### Interfaces and implementations

An interface describes the operations a structure provides and their promised behavior.

An implementation is the code and internal organization that fulfill that interface.

A stack interface might promise:

- Add an item to the top.
- Remove the top item.
- Read the top item.
- Report the size.

The implementation could use an array or linked nodes.

An abstract data type, often abbreviated ADT, describes behavior independently of a particular implementation.

Stacks, queues, and priority queues are commonly discussed as ADTs.

### Raising an exception

We previously handled exceptions. Now we will deliberately report invalid operations.

The raise statement raises an exception:

```python
# Report an invalid operation explicitly.
raise IndexError("Cannot remove from an empty structure")
```

This line is not meant to run successfully. It tells the caller the operation cannot be completed.

We will use:

- IndexError for invalid positions or empty indexed structures.
- KeyError for missing keys.
- ValueError for invalid argument values where appropriate.

### Chapter practice

1. Guided: Add a decrease method to Counter.
2. Why do first and second keep different values?
3. What is the difference between a stack interface and a stack implementation?

#### Answers and explanations

1. Place this method inside Counter:

```python
def decrease(self):
    # Update the instance receiving this call.
    self.value = self.value - 1
```

2. Each call to Counter(...) creates a separate instance. Each instance has its own value attribute.

3. The interface describes behavior, such as removing the most recently added item. The implementation explains how that behavior is achieved, such as using the end of an array or the head of a linked list.

## Chapter 4.2: Arrays and dynamic arrays

### Analogy: numbered lockers

An array resembles a row of numbered lockers.

If you know the locker number, you can go directly to it.

If you need to insert a locker in the middle while preserving the numbering and order, later contents may need to move.

An array stores elements in indexed positions.

A fixed-size array has a fixed number of positions.

A dynamic array can grow by replacing its backing storage with a larger one.

### How arrays work in memory

For a traditional array of equal-width entries, the location of element i can be calculated as:

base address + i × entry width

A memory address identifies a location in memory.

Because the position can be calculated, indexing does not require examining earlier elements.

A Python list is a dynamic array of references to objects. The reference slots are arranged contiguously, meaning next to one another in the backing storage. The referenced objects themselves need not be next to one another.

| Slot | Stored reference points to |
| --- | --- |
| 0 | Integer object representing 10 |
| 1 | String object representing "cat" |
| 2 | Another list object |

This helps explain why Python lists can contain mixed types.

Python also provides array.array for compact storage of values constrained by a chosen numeric type code. That differs from a general list of object references.

### Length versus capacity

- Length: number of logical elements currently stored.
- Capacity: number of available slots before expansion.

Example:

| Property | Value |
| --- | --- |
| Logical elements | [10, 20, 30] |
| Length | 3 |
| Capacity | 4 |
| Unused slots | 1 |

Adding one more item fits. Adding a fifth item requires expansion in our implementation.

### Invariant

Our dynamic array maintains 0 ≤ size ≤ capacity.

The logical elements occupy positions 0 through size − 1.

Unused positions are outside the logical sequence, even if they contain None.

### Implementation

This version supports nonnegative indices only.

```python
class DynamicArray:
    def __init__(self):
        # Start with four available slots.
        self._capacity = 4

        # No logical elements have been inserted yet.
        self._size = 0

        # Treat this list as fixed-capacity backing storage.
        self._data = [None] * self._capacity

    def __len__(self):
        return self._size

    def _check_index(self, index):
        # Existing elements occupy positions 0 through size - 1.
        if index < 0 or index >= self._size:
            raise IndexError("Index outside the logical array")

    def get(self, index):
        self._check_index(index)
        return self._data[index]

    def set(self, index, value):
        self._check_index(index)
        self._data[index] = value

    def _grow(self):
        # Doubling leaves room for many later appends.
        new_capacity = self._capacity * 2
        new_data = [None] * new_capacity

        # Copy existing element references.
        for index in range(self._size):
            new_data[index] = self._data[index]

        # Replace the backing storage.
        self._data = new_data
        self._capacity = new_capacity

    def append(self, value):
        # Expand only when every slot is occupied.
        if self._size == self._capacity:
            self._grow()

        # Write into the first unused logical position.
        self._data[self._size] = value
        self._size = self._size + 1

    def insert(self, index, value):
        # Insertion at size means insertion at the end.
        if index < 0 or index > self._size:
            raise IndexError("Invalid insertion position")

        if self._size == self._capacity:
            self._grow()

        # Shift from right to left so values are not overwritten.
        position = self._size

        while position > index:
            self._data[position] = self._data[position - 1]
            position = position - 1

        self._data[index] = value
        self._size = self._size + 1

    def remove_at(self, index):
        self._check_index(index)

        # Preserve the value being removed.
        removed = self._data[index]

        # Close the gap by shifting later elements left.
        for position in range(index, self._size - 1):
            self._data[position] = self._data[position + 1]

        self._size = self._size - 1

        # Release the reference in the now-unused final slot.
        self._data[self._size] = None

        return removed

    def pop(self):
        if self._size == 0:
            raise IndexError("Cannot pop an empty array")

        return self.remove_at(self._size - 1)

    def to_list(self):
        # Return a separate list of logical elements.
        result = []

        for index in range(self._size):
            result.append(self._data[index])

        return result
```

### Worked trace: insertion

Start: [10, 20, 30]. Insert 99 at index 1.

| Step | Logical movement |
| --- | --- |
| Make room at the end | A slot is available at position 3 |
| Move position 2 to 3 | Move 30 |
| Move position 1 to 2 | Move 20 |
| Write position 1 | Insert 99 |

Result: [10, 99, 20, 30].

Shifting left to right would overwrite a value before copying it.

### Example checks

```python
values = DynamicArray()

values.append(10)
values.append(20)
values.append(30)
values.insert(1, 99)

assert values.to_list() == [10, 99, 20, 30]
assert values.remove_at(2) == 20
assert values.pop() == 30
assert values.to_list() == [10, 99]
assert len(values) == 2
```

### Operation costs

Let n be the logical length.

| Operation | Time |
| --- | --- |
| Read or replace by valid index | O(1) |
| Append | Amortized O(1), individual resize O(n) |
| Remove final element in this implementation | O(1) |
| Insert near the beginning | O(n) |
| Remove near the beginning | O(n) |
| Search an unsorted array | O(n) |
| Copy all elements | O(n) |

This implementation does not shrink. Its allocated storage is O(C), where C is capacity. After many deletions, capacity can remain much larger than the current length.

### When to use it

Use an array-like structure when you need:

- Fast indexing.
- Ordered storage.
- Sequential scans.
- Frequent appends.
- Compact storage of references relative to separately allocated linked nodes.

### Common mistakes

- Confusing capacity with length.
- Assuming middle insertion is constant time.
- Forgetting that list slicing copies references.
- Assuming a copied list deeply copies its elements.
- Depending on indices after inserting or deleting earlier elements.

### Chapter practice

1. Guided: Starting with [4, 8, 12], insert 6 at index 1.
2. Why is accessing index 900 not slower than accessing index 3 in an array?
3. Why does this implementation clear the unused final slot after removal?

#### Answers and explanations

1.

```python
values = DynamicArray()

for number in [4, 8, 12]:
    values.append(number)

values.insert(1, 6)

assert values.to_list() == [4, 6, 8, 12]
```

2. The slot location is calculated from the index. Earlier elements do not need to be traversed.

3. Otherwise, the backing storage would retain an unnecessary reference to an object that is no longer part of the logical array.

## Chapter 4.3: Strings as structured text

### Analogy: a printed sentence

You can point to a character in a printed sentence. You can copy a portion of it. But changing the printed sentence requires producing different text.

Python strings are immutable sequences of Unicode code points.

A code point is a numbered unit in Unicode’s text representation system.

A visible symbol can contain multiple code points. Our introductory examples use ordinary English letters so one visible letter corresponds to one indexed element.

### Memory model

A Python string stores encoded character information and metadata such as its length. It is not a Python list containing a separately referenced one-character string at each position.

The exact representation is an implementation detail.

For algorithm analysis, remember:

- Indexing retrieves a position.
- A nontrivial copied substring requires storage proportional to its length.
- Strings cannot be edited in place.
- Repeated reconstruction can dominate the runtime.

### Operations rather than another copy of Python’s str

We will implement a small text-sequence interface over a tuple of characters.

This is a learning model. It is not Python’s actual string representation.

The interface offers no mutation methods. The underscore attribute remains a Python implementation detail, so this class does not enforce the same intrinsic immutability as a built-in string.

```python
class TextSequence:
    def __init__(self, characters):
        # Store an ordered, immutable tuple of characters.
        self._characters = tuple(characters)

    def __len__(self):
        return len(self._characters)

    def character_at(self, index):
        if index < 0 or index >= len(self):
            raise IndexError("Character index outside the text")

        return self._characters[index]

    def substring(self, start, stop):
        # This teaching interface uses nonnegative bounds.
        if start < 0 or stop < start or stop > len(self):
            raise IndexError("Invalid substring boundaries")

        selected = []

        for index in range(start, stop):
            selected.append(self._characters[index])

        # Return a new text object.
        return TextSequence(selected)

    def concatenate(self, other):
        combined = []

        # Copy this object's characters.
        for character in self._characters:
            combined.append(character)

        # Copy the other object's characters.
        for character in other._characters:
            combined.append(character)

        return TextSequence(combined)

    def find(self, pattern):
        # Return the first matching start position, or -1.
        n = len(self)
        m = len(pattern)

        # The empty pattern matches at the beginning.
        if m == 0:
            return 0

        # Try every start position where the pattern could fit.
        for start in range(n - m + 1):
            matches = True

            for offset in range(m):
                if self._characters[start + offset] != pattern[offset]:
                    matches = False
                    break

            if matches:
                return start

        return -1

    def to_string(self):
        return "".join(self._characters)
```

### Worked search

Search for "ana" in "banana".

| Candidate start | Characters examined | Result |
| --- | --- | --- |
| 0 | b versus a | Reject |
| 1 | a versus a, n versus n, a versus a | Match |

Return 1.

```python
text = TextSequence("banana")

assert text.character_at(0) == "b"
assert text.substring(1, 4).to_string() == "ana"
assert text.find("ana") == 1
assert text.find("xyz") == -1
assert text.find("") == 0

combined = text.concatenate(TextSequence(" split"))
assert combined.to_string() == "banana split"
```

### Costs

Let n be text length, m be pattern or second-text length, and k be selected substring length.

| Operation in this implementation | Time | New result storage |
| --- | --- | --- |
| Character access | O(1) | O(1) |
| Substring | O(k) | O(k) |
| Concatenation | O(n + m) | O(n + m) |
| Naive pattern search | O(nm) worst-case bound | O(1) auxiliary |
| Convert to a built-in string | O(n) | O(n) |

The search bound describes our naive implementation. Do not infer that Python’s built-in substring search uses this exact algorithm.

### When to use text-specific structures

Use strings when the information is text and you need:

- Character comparisons.
- Substrings.
- Parsing, meaning interpreting text according to rules.
- Pattern matching.
- Text transformations.

Use a list of pieces when building a large result incrementally, then join those pieces.

### Common mistakes

- Treating a string as mutable.
- Assuming all visible symbols occupy one indexed position.
- Rebuilding a long string repeatedly.
- Confusing a substring with a subsequence.

A subsequence preserves order but may skip positions. A substring cannot skip positions.

### Chapter practice

1. Guided: Extract "code" from "leetcode" using start and stop indices.
2. Why does naive pattern matching have an O(nm) worst-case bound?
3. Is "ace" a substring or subsequence of "abcde"?

#### Answers and explanations

1.

```python
text = TextSequence("leetcode")
assert text.substring(4, 8).to_string() == "code"
```

2. There can be O(n) candidate starts. At each one, the algorithm may compare O(m) pattern characters.

3. It is a subsequence. It skips b and d. It is not a substring because its characters are not consecutive.
