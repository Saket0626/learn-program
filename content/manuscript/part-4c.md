# Part 4 continued: Chapters 4.6–4.8

## Chapter 4.6: Stacks

### Analogy: a stack of plates

You add a plate to the top.

You remove the plate currently on top.

The most recently added plate is removed first.

A stack follows LIFO, meaning last in, first out.

Operations:

- Push: add an item to the top.
- Pop: remove and return the top item.
- Peek: read the top item without removing it.

### Memory and implementation choices

A stack can use:

- The end of a dynamic array.
- The head of a singly linked list.

We will use linked nodes so the stack mechanics do not rely on list append and pop.

This implementation uses the Node class from Chapter 4.5.

```python
class Stack:
    def __init__(self):
        self._top = None
        self._size = 0

    def __len__(self):
        return self._size

    def push(self, value):
        node = Node(value)

        # The previous top follows the new top.
        node.next = self._top
        self._top = node

        self._size = self._size + 1

    def peek(self):
        if self._top is None:
            raise IndexError("Cannot peek at an empty stack")

        return self._top.value

    def pop(self):
        if self._top is None:
            raise IndexError("Cannot pop an empty stack")

        removed = self._top
        self._top = removed.next

        removed.next = None
        self._size = self._size - 1

        return removed.value

    def is_empty(self):
        return self._size == 0
```

### Worked trace

| Operation | Stack contents, bottom to top | Result |
| --- | --- | --- |
| Push A | [A] | — |
| Push B | [A, B] | — |
| Push C | [A, B, C] | — |
| Pop | [A, B] | C |
| Peek | [A, B] | B |

```python
stack = Stack()

stack.push("A")
stack.push("B")
stack.push("C")

assert stack.pop() == "C"
assert stack.peek() == "B"
assert len(stack) == 2
```

### Costs

For this linked implementation:

| Operation | Time |
| --- | --- |
| Push | O(1) |
| Pop | O(1) |
| Peek | O(1) |
| Length | O(1) |

Storage is O(n).

### When to use a stack

Use one when the most recent unfinished item should be handled next:

- Matching parentheses.
- Undoing recent actions.
- Exploring a path before returning to alternatives.
- Tracking nested function calls.
- Maintaining unresolved values in monotonic-stack problems.

The last two algorithms will be taught later.

### Worked idea: matching parentheses

For the text (()), an opening parenthesis creates an unfinished obligation. A closing parenthesis must match the most recent unmatched opening. This naturally fits a stack.

A full solution appears in Part 7.

### Common mistakes

- Popping before checking whether the stack is empty.
- Using the front of a Python list as the stack top.
- Forgetting that peek must preserve the item.
- Confusing LIFO with FIFO.

### Chapter practice

1. Guided: Push 4, 7, and 2. What are the next two popped values?
2. Why does undo behavior often use a stack?
3. Implement is_empty for this stack.

#### Answers and explanations

1. 2, then 7.

2. The most recent completed action is normally the first action undone.

3. The method included above:

```python
def is_empty(self):
    return self._size == 0
```

## Chapter 4.7: Queues

### Analogy: a checkout line

The first person to join the line is the first person served.

A queue follows FIFO, meaning first in, first out.

Operations:

- Enqueue: add an item at the back.
- Dequeue: remove and return the item at the front.
- Peek: inspect the front item.

### Memory organization

A linked queue maintains a front reference, a back reference, and a node count.

New items attach after the back.

Removal advances the front.

```python
class Queue:
    def __init__(self):
        self._front = None
        self._back = None
        self._size = 0

    def __len__(self):
        return self._size

    def enqueue(self, value):
        node = Node(value)

        if self._back is None:
            # The first node becomes both endpoints.
            self._front = node
            self._back = node
        else:
            self._back.next = node
            self._back = node

        self._size = self._size + 1

    def peek(self):
        if self._front is None:
            raise IndexError("Cannot peek at an empty queue")

        return self._front.value

    def dequeue(self):
        if self._front is None:
            raise IndexError("Cannot dequeue an empty queue")

        removed = self._front
        self._front = removed.next

        # If the front disappeared, the queue is empty.
        if self._front is None:
            self._back = None

        removed.next = None
        self._size = self._size - 1

        return removed.value
```

### Worked trace

| Operation | Front-to-back contents | Returned value |
| --- | --- | --- |
| Enqueue A | [A] | — |
| Enqueue B | [A, B] | — |
| Enqueue C | [A, B, C] | — |
| Dequeue | [B, C] | A |
| Enqueue D | [B, C, D] | — |
| Dequeue | [C, D] | B |

```python
queue = Queue()

queue.enqueue("A")
queue.enqueue("B")

assert queue.dequeue() == "A"

queue.enqueue("C")

assert queue.dequeue() == "B"
assert queue.dequeue() == "C"
assert len(queue) == 0

# Check that the emptied queue can be reused.
queue.enqueue("D")
assert queue.peek() == "D"
```

### Costs

| Operation | Time |
| --- | --- |
| Enqueue | O(1) |
| Dequeue | O(1) |
| Peek | O(1) |
| Length | O(1) |

Storage is O(n).

### A practical Python queue

For algorithm problems, collections.deque is a standard choice:

```python
from collections import deque

queue = deque()

queue.append("A")
queue.append("B")

assert queue.popleft() == "A"
```

Python documents efficient appends and removals at both ends of a deque. Arbitrary middle indexing is not its strength.

### When to use a queue

Use one when older pending work should be handled first:

- Breadth-first search.
- Processing levels of a tree.
- Handling tasks in arrival order.
- Simulating waiting lines.

### Another implementation: a circular buffer

A circular buffer stores queue items in an array while allowing the front and back positions to wrap around.

For capacity C, the next position after index i is (i + 1) % C.

Wrapping allows reuse of freed positions without shifting every element.

We will not need a separate circular-buffer implementation to solve the upcoming problems, but the representation explains how an array can support an efficient queue.

### Common mistakes

- Using list.pop(0) repeatedly and overlooking its shifting cost.
- Forgetting to clear the back reference when removing the only node.
- Implementing stack behavior when the problem requires queue order.

### Chapter practice

1. Guided: Enqueue 10, 20, 30, dequeue once, then enqueue 40. What are the contents?
2. Why does a queue need a back reference for constant-time linked insertion?
3. In a circular buffer of capacity 5, what index follows index 4?

#### Answers and explanations

1. Front to back: 20, 30, 40.

2. Without a back reference, appending would require following links from the front to find the final node.

3. (4 + 1) mod 5 = 0. The position wraps to index 0.

## Chapter 4.8: Deques and doubly linked lists

A deque is a double-ended queue.

It supports additions and removals at both the front and back.

### Analogy: a train accessible from either end

If items must be added or removed at either end, a queue’s one-direction policy is too restrictive.

We can implement a deque with a doubly linked list.

Each node stores a value, a previous-node reference, and a next-node reference.

### Memory structure

The first node’s previous is None.

The last node’s next is None.

The deque stores references to both endpoints.

```python
class DoubleNode:
    def __init__(self, value):
        self.value = value
        self.previous = None
        self.next = None


class LinkedDeque:
    def __init__(self):
        self._front = None
        self._back = None
        self._size = 0

    def __len__(self):
        return self._size

    def append_left(self, value):
        node = DoubleNode(value)
        node.next = self._front

        if self._front is None:
            self._back = node
        else:
            self._front.previous = node

        self._front = node
        self._size = self._size + 1

    def append_right(self, value):
        node = DoubleNode(value)
        node.previous = self._back

        if self._back is None:
            self._front = node
        else:
            self._back.next = node

        self._back = node
        self._size = self._size + 1

    def peek_left(self):
        if self._front is None:
            raise IndexError("Cannot peek at an empty deque")

        return self._front.value

    def peek_right(self):
        if self._back is None:
            raise IndexError("Cannot peek at an empty deque")

        return self._back.value

    def pop_left(self):
        if self._front is None:
            raise IndexError("Cannot remove from an empty deque")

        removed = self._front
        self._front = removed.next

        if self._front is None:
            self._back = None
        else:
            # The new front must not point backward at the removed node.
            self._front.previous = None

        removed.next = None
        removed.previous = None
        self._size = self._size - 1
        return removed.value

    def pop_right(self):
        if self._back is None:
            raise IndexError("Cannot remove from an empty deque")

        removed = self._back
        self._back = removed.previous

        if self._back is None:
            self._front = None
        else:
            self._back.next = None

        removed.next = None
        removed.previous = None
        self._size = self._size - 1
        return removed.value
```

The source manuscript stopped inside pop_left. The methods above finish that operation and add pop_right, peek_left, and peek_right, using the link-update rules stated in this chapter, so the worked trace can run.

### Worked trace

```python
values = LinkedDeque()

values.append_right(20)  # [20]
values.append_left(10)   # [10, 20]
values.append_right(30)  # [10, 20, 30]

assert values.pop_right() == 30
assert values.pop_left() == 10
assert values.peek_left() == 20
assert values.peek_right() == 20
```

### Why both links must be updated

When removing the front:

1. Move _front to the next node.
2. Clear the new front’s previous.
3. If no nodes remain, clear _back.

Failing step 2 leaves a backward reference to a removed node.

### Costs

| Operation | Time |
| --- | --- |
| Add at either end | O(1) |
| Remove at either end | O(1) |
| Peek at either end | O(1) |
| Find an arbitrary value | O(n) |
| Reach an arbitrary middle position | O(n) worst case |

Storage is O(n).

Our implementation uses individually allocated doubly linked nodes. Python’s collections.deque has a different internal representation built around blocks of references.

### When to use a deque

Use one when:

- Both ends are active.
- Implementing a queue.
- Maintaining a sliding-window candidate structure.
- Some graph-search operations add to the front while others add to the back.

Those last two uses will appear in later algorithm chapters.

### Common mistakes

- Updating only one side of a doubly linked connection.
- Forgetting the one-element case.
- Assuming a deque has array-like constant-time middle indexing.

### Chapter practice

1. Guided: Add 2 right, 1 left, and 3 right. Remove left, then right. What remains?
2. Why can a doubly linked list remove its tail in constant time?
3. What must both endpoints become after removing the final item?

#### Answers and explanations

1. The sequence becomes [1, 2, 3]. Removing left returns 1. Removing right returns 3. The remaining value is 2.

2. The tail stores a reference to its predecessor. There is no need to search from the head.

3. Both become None.
