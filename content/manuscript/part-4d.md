# Part 4 continued: Chapters 4.9–4.11

## Chapter 4.9: Heaps and priority queues

### Analogy: repeatedly taking the most urgent task

A normal queue chooses by arrival time.

A priority queue chooses by priority.

A priority queue is an ADT that supports inserting items and removing an item with the most important priority.

A heap is a common implementation of a priority queue.

We will implement a min-heap, which provides the smallest value first.

### Two heap properties

A binary heap maintains a shape property and an ordering property.

A binary tree gives each node at most two children.

A complete binary tree fills every level before the last, with the last level filled from left to right.

The min-heap ordering rule is: every parent value is less than or equal to each of its children.

This does not require siblings to be sorted relative to each other.

### An example heap

```
        2
      /   \
     5     3
    / \
   9   8
```

Its level-order array is [2, 5, 3, 9, 8].

Level order means reading one tree level at a time, from top to bottom and left to right.

Notice that the array is not globally sorted.

### Array positions replace explicit links

For a zero-based array and node position i:

- left child = 2i + 1
- right child = 2i + 2
- for i > 0, parent = ⌊(i − 1) / 2⌋

The complete shape makes these formulas possible.

### Insertion: move upward

1. Append the new value at the end.
2. Compare it with its parent.
3. Swap when the parent is larger.
4. Repeat until the ordering property holds.

This is called sifting up.

### Removing the minimum: move downward

1. Save the root value.
2. Remove the final array value.
3. Put that final value at the root.
4. Repeatedly swap it with its smaller child while necessary.

This is called sifting down.

### Implementation

The source manuscript stopped in the middle of the swap inside push. The class below finishes that swap and the rest of the operations described in this chapter: sift down, pop, and bottom-up construction.

```python
class MinHeap:
    def __init__(self, values=None):
        self._data = []

        if values is not None:
            for value in values:
                self._data.append(value)

            # Leaves already satisfy the heap rule.
            # Repair internal nodes from the bottom upward.
            last_parent = len(self._data) // 2 - 1

            for index in range(last_parent, -1, -1):
                self._sift_down(index)

    def __len__(self):
        return len(self._data)

    def peek(self):
        if len(self._data) == 0:
            raise IndexError("Cannot inspect an empty heap")

        return self._data[0]

    def push(self, value):
        self._data.append(value)
        index = len(self._data) - 1

        while index > 0:
            parent = (index - 1) // 2

            if self._data[parent] <= self._data[index]:
                break

            # Swap the child and parent.
            # Python evaluates the right-hand values before assigning them.
            self._data[parent], self._data[index] = (
                self._data[index],
                self._data[parent],
            )
            index = parent

    def _sift_down(self, index):
        size = len(self._data)

        while True:
            left = 2 * index + 1
            right = 2 * index + 2
            smallest = index

            if left < size and self._data[left] < self._data[smallest]:
                smallest = left

            if right < size and self._data[right] < self._data[smallest]:
                smallest = right

            if smallest == index:
                return

            self._data[index], self._data[smallest] = (
                self._data[smallest],
                self._data[index],
            )
            index = smallest

    def pop(self):
        if len(self._data) == 0:
            raise IndexError("Cannot pop an empty heap")

        minimum = self._data[0]
        last = self._data.pop()

        if len(self._data) > 0:
            self._data[0] = last
            self._sift_down(0)

        return minimum
```

### Worked insertion

Start with [2, 5, 3, 9, 8]. Insert 1.

| Step | Array |
| --- | --- |
| Append 1 | [2, 5, 3, 9, 8, 1] |
| Compare with parent 3, then swap | [2, 5, 1, 9, 8, 3] |
| Compare with parent 2, then swap | [1, 5, 2, 9, 8, 3] |

The new minimum is at position 0.

```python
heap = MinHeap([5, 2, 8, 1])

assert heap.peek() == 1
assert heap.pop() == 1

heap.push(0)

assert heap.pop() == 0
assert heap.pop() == 2
assert heap.pop() == 5
assert heap.pop() == 8
```

### Why construction can be linear

Heapify means rearranging an existing collection into heap order.

Repeatedly inserting n values gives an O(n log n) upper bound.

Bottom-up heap construction is O(n).

Why?

- Roughly half the nodes are leaves and require no downward movement.
- Roughly a quarter can move at most one level.
- Roughly an eighth can move at most two.
- Very few can move many levels.

The aggregate work is bounded by a linear quantity.

### Costs

| Operation | Time |
| --- | --- |
| Peek minimum | O(1) |
| Push | O(log n) heap work; amortized accounting for array growth |
| Pop minimum | O(log n) |
| Bottom-up heapify | O(n) |
| Find an arbitrary value | O(n) worst case |
| Storage | O(n) |

### Python’s heapq

Python provides heap operations over a list:

```python
import heapq

heap = [5, 2, 8]
heapq.heapify(heap)

heapq.heappush(heap, 1)

assert heapq.heappop(heap) == 1
assert heap[0] == 2
```

heapq uses a zero-based min-heap convention. Its documentation describes the heap invariant and the functions for maintaining it.

### Priority ties

If entries are tuples, Python compares them lexicographically, meaning it compares the first differing position.

A useful entry format is (priority, insertion_number, task).

The unique insertion number breaks priority ties before Python needs to compare task objects.

This also preserves arrival order among tied priorities when insertion numbers increase.

### When to use a heap

Use a heap when you repeatedly need the smallest or largest current item:

- Merge sorted streams.
- Keep the best k candidates.
- Process events by time.
- Select the next closest graph-search candidate.

### Common mistakes

- Assuming every heap position is sorted.
- Swapping with the larger child in a min-heap.
- Changing an internal priority without restoring heap order.
- Forgetting that finding an arbitrary item can still be linear.

### Chapter practice

1. Guided: What is the parent index of index 6?
2. Is [1, 4, 2, 8, 5] a valid min-heap?
3. Why does repeatedly popping a min-heap produce sorted output?
4. Why does efficient minimum access not imply efficient arbitrary search?

#### Answers and explanations

1. (6 − 1) // 2 = 2.

2. Yes. 1 is no larger than 4 and 2. 4 is no larger than 8 and 5.

3. Each removal returns the smallest remaining value, then restores the heap invariant.

4. The heap only orders parents relative to descendants. It does not provide the global left-versus-right ordering needed to direct an arbitrary search.

## Chapter 4.10: Binary trees

### Analogy: a branching hierarchy

A tree organizes information through parent-child relationships.

A rooted tree has one designated root, and every other node has exactly one parent within the tree.

A child is directly below a parent.

A leaf has no children.

A subtree consists of a node and all its descendants.

A descendant is reachable by repeatedly following child references.

A binary tree allows at most two children, conventionally called left and right.

A binary tree is not automatically ordered by value. The example below is a valid binary tree. It is not a binary search tree, because the values do not follow the ordering rule introduced in the next chapter.

```
        8
      /   \
    20     3
   /        \
  1          15
```

### Depth and height

We will count edges:

- The root has depth 0.
- A child of the root has depth 1.
- A node’s depth is the number of edges from the root.
- A tree’s height is the greatest node depth.
- A one-node tree has height 0.

An edge is a connection between nodes.

We will describe operations as O(h + 1) when necessary so the one-node case remains explicit.

### Memory representation

```python
class TreeNode:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None
```

Build a tree:

```python
root = TreeNode(8)

root.left = TreeNode(20)
root.right = TreeNode(3)

root.left.left = TreeNode(1)
root.right.right = TreeNode(15)
```

Each node stores two references. A missing child is None.

### Traversal

A traversal visits the nodes of a structure in a specified order.

| Traversal | Order |
| --- | --- |
| Preorder | Node, left subtree, right subtree |
| Inorder | Left subtree, node, right subtree |
| Postorder | Left subtree, right subtree, node |
| Level order | Level by level from the root |

Part 5 will teach recursive and iterative traversal patterns in depth.

Here is an iterative preorder implementation:

```python
def preorder(root):
    result = []

    if root is None:
        return result

    # A list is used as a stack.
    pending = [root]

    while len(pending) > 0:
        node = pending.pop()
        result.append(node.value)

        # Push right first so left is removed and visited first.
        if node.right is not None:
            pending.append(node.right)

        if node.left is not None:
            pending.append(node.left)

    return result
```

For the example:

```python
assert preorder(root) == [8, 20, 1, 3, 15]
```

### Why push right first?

A stack removes the most recent item.

After pushing right and then left, left is on top.

This is an example of choosing insertion order to create the desired removal order.

### A general-tree search

Without an ordering rule, you may need to inspect every node:

```python
def tree_contains(root, target):
    if root is None:
        return False

    pending = [root]

    while len(pending) > 0:
        node = pending.pop()

        if node.value == target:
            return True

        if node.left is not None:
            pending.append(node.left)

        if node.right is not None:
            pending.append(node.right)

    return False
```

### Costs

Let n be the node count and h the height.

| Operation | Cost |
| --- | --- |
| Read a known node’s child | O(1) |
| Attach a new child to a known empty child position | O(1) |
| Search without an ordering rule | O(n) worst case |
| Visit every node | O(n) |
| Linked-node storage | O(n) |

The explicit preorder stack uses O(h + 1) auxiliary space in the worst case for this binary-tree traversal. Returning the traversal list adds O(n) output storage.

### When to use trees

Use tree representations for hierarchies, expression structures, recursive decompositions, problems supplied as tree nodes, and situations where each non-root item has one parent.

### Common mistakes

- Assuming all binary trees are search trees.
- Confusing height with node count.
- Forgetting empty-tree handling.
- Accidentally sharing one child node under multiple parents when a true tree is required.
- Creating a cycle by linking a descendant back to an ancestor.

### Chapter practice

1. Guided: What is the height of a root with two leaf children?
2. Give the preorder traversal of a root 5, left child 2, and right child 9.
3. Why is finding an arbitrary value in a general binary tree O(n) in the worst case?

#### Answers and explanations

1. Height 1, because the longest root-to-leaf path contains one edge.

2. 5, 2, 9.

3. Without a value-ordering rule, the value could be anywhere or absent. You may need to inspect every node.

## Chapter 4.11: Binary search trees

A binary search tree, or BST, adds an ordering invariant to a binary tree.

For this implementation:

- Every value in a node’s left subtree is smaller than the node’s value.
- Every value in its right subtree is larger.
- Duplicate values are ignored.

Other BST designs can store duplicate counts. The policy must be explicit.

### Example

```
        8
      /   \
     3     12
    / \   /  \
   1   6 10   14
```

To search for 6:

- 6 < 8, so go left.
- 6 > 3, so go right.
- Find 6.

At each step, the invariant tells you which subtree can contain the target.

### Important: the rule applies to whole subtrees

Checking only immediate children is insufficient.

For example, a value 9 anywhere in the left subtree of 8 violates the BST rule, even if it is larger than its immediate parent.

### Implementation

This class uses TreeNode from the preceding chapter.

The source manuscript stopped inside insert. The methods below finish insert and add the deletion cases, minimum, inorder, and remove described in this chapter.

```python
class BinarySearchTree:
    def __init__(self):
        self.root = None
        self._size = 0

    def __len__(self):
        return self._size

    def contains(self, value):
        current = self.root

        while current is not None:
            if value == current.value:
                return True

            if value < current.value:
                current = current.left
            else:
                current = current.right

        return False

    def insert(self, value):
        if self.root is None:
            self.root = TreeNode(value)
            self._size = 1
            return True

        current = self.root

        while True:
            if value == current.value:
                # Our policy ignores duplicates.
                return False

            if value < current.value:
                if current.left is None:
                    current.left = TreeNode(value)
                    self._size = self._size + 1
                    return True

                current = current.left
            else:
                if current.right is None:
                    current.right = TreeNode(value)
                    self._size = self._size + 1
                    return True

                current = current.right

    def minimum(self):
        if self.root is None:
            raise IndexError("Cannot read the minimum of an empty tree")

        current = self.root

        while current.left is not None:
            current = current.left

        return current.value

    def inorder(self):
        result = []

        def walk(node):
            if node is None:
                return

            walk(node.left)
            result.append(node.value)
            walk(node.right)

        walk(self.root)
        return result

    def _minimum_node(self, node):
        while node.left is not None:
            node = node.left

        return node

    def remove(self, value):
        self.root, removed = self._remove(self.root, value)

        if removed:
            self._size = self._size - 1

        return removed

    def _remove(self, node, value):
        if node is None:
            return None, False

        if value < node.value:
            node.left, removed = self._remove(node.left, value)
            return node, removed

        if value > node.value:
            node.right, removed = self._remove(node.right, value)
            return node, removed

        # No children, or only a right child.
        if node.left is None:
            return node.right, True

        # Only a left child.
        if node.right is None:
            return node.left, True

        # Two children: copy the inorder successor, then remove that successor.
        successor = self._minimum_node(node.right)
        node.value = successor.value
        node.right, _removed = self._remove(node.right, successor.value)
        return node, True
```

### Deletion’s three cases

| Node being removed | Action |
| --- | --- |
| No children | Disconnect it |
| One child | Connect its parent directly to its child |
| Two children | Replace its value with its inorder successor, then remove that successor |

The inorder successor is the next larger value in the BST’s sorted order.

For a node with a right subtree, its successor is the smallest node in that right subtree.

That successor cannot have a left child. Otherwise, it would not be the smallest.

### Worked example

```python
tree = BinarySearchTree()

for value in [8, 3, 12, 1, 6, 10, 14]:
    tree.insert(value)

assert tree.contains(6) == True
assert tree.contains(7) == False
assert tree.minimum() == 1

assert tree.inorder() == [1, 3, 6, 8, 10, 12, 14]

tree.remove(8)

assert tree.inorder() == [1, 3, 6, 10, 12, 14]
assert len(tree) == 6
```

Removing root 8:

- Its successor is 10.
- Replace the root’s value with 10.
- Remove the old node containing 10.

### Height controls performance

If the tree stays balanced, its height is logarithmic.

If you insert sorted values into this unbalanced implementation, 1, 2, 3, 4, 5, it becomes a chain of right children.

Then its height is linear.

BST operation costs depend on height; logarithmic search is not guaranteed by the BST ordering rule alone.

| Operation | General bound | Balanced height |
| --- | --- | --- |
| Search | O(h + 1) | O(log n) |
| Insert | O(h + 1) | O(log n) |
| Remove | O(h + 1) | O(log n) |
| Minimum | O(h + 1) | O(log n) |
| Full inorder traversal | O(n) | O(n) |

Our implementation does not rebalance.

### Balanced search trees

A balanced search tree maintains rules that keep height logarithmic.

Examples include AVL trees and red-black trees. Their rotations and balancing policies are beyond this first implementation.

A rotation is a local restructuring that changes tree shape while preserving sorted order.

### When to use a BST

A balanced ordered structure is useful for:

- Maintaining sorted keys while updating them.
- Finding nearest smaller or larger keys.
- Ordered traversal.
- Range queries.

A basic hash map is often better for plain membership when ordering is unnecessary.

### Common mistakes

- Claiming every BST search is O(log n).
- Forgetting the duplicate policy.
- Checking only immediate children when validating the invariant.
- Deleting a two-child node without preserving subtree ordering.

### Chapter practice

1. Guided: Insert 5, 2, 8, 1, 3. What is the inorder result?
2. Why does inserting sorted values harm this implementation?
3. Why can the inorder successor have no left child?
4. What is the maximum number of children a BST node can have?

#### Answers and explanations

1. 1, 2, 3, 5, 8.

2. Each larger value attaches to the right of the previous one, creating a chain instead of a shallow tree.

3. A left child would contain a smaller value in the right subtree, contradicting the successor’s choice as that subtree’s minimum.

4. Two. A BST is a binary tree with an additional ordering rule.
