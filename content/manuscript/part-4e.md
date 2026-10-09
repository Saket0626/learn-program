# Part 4 continued: Chapters 4.12–4.15, review, glossary, and readiness

## Chapter 4.12: Tries

A trie, often pronounced “try,” stores sequences through shared prefixes.

A prefix is an initial portion of a sequence.

For example:

- "ca" is a prefix of "cat".
- "ca" is a prefix of "car".
- "at" is not a prefix of "cat".

### Analogy: choosing a word one letter at a time

Instead of storing every word as an unrelated key, organize choices by their next character.

The words "car" and "cat" share the path for c, then a, before branching.

```
root
 └── c
      └── a
           ├── r  (word ends)
           └── t  (word ends)
```

### Node contents

Each trie node stores:

- A mapping from next characters to child nodes.
- A Boolean indicating whether a full word ends there.

The ending flag matters because a prefix can exist without being a complete stored word.

### Memory structure

A dictionary-based trie uses many node objects, each with its own dictionary.

Alternative implementations use fixed arrays of children for a fixed alphabet.

An alphabet is the set of symbols allowed in the sequences.

A fixed 26-child array can make sense for lowercase English letters. It may waste memory when most nodes have few children or when the alphabet is large.

### Implementation

```python
class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_word = False


class Trie:
    def __init__(self):
        self.root = TrieNode()

    def insert(self, word):
        current = self.root

        for character in word:
            if character not in current.children:
                current.children[character] = TrieNode()

            current = current.children[character]

        # Mark the endpoint, including the root for the empty word.
        current.is_word = True

    def _walk(self, text):
        current = self.root

        for character in text:
            if character not in current.children:
                return None

            current = current.children[character]

        return current

    def contains(self, word):
        node = self._walk(word)

        return node is not None and node.is_word

    def starts_with(self, prefix):
        # Reaching a node is enough for a prefix.
        return self._walk(prefix) is not None

    def remove(self, word):
        current = self.root
        path = []

        for character in word:
            if character not in current.children:
                return False

            # Remember how to return to the parent.
            path.append((current, character))
            current = current.children[character]

        if not current.is_word:
            return False

        current.is_word = False

        # Remove unused nodes from the endpoint backward.
        for parent, character in reversed(path):
            child = parent.children[character]

            # A remaining word or child still needs this node.
            if child.is_word or len(child.children) > 0:
                break

            del parent.children[character]

        return True
```

reversed(path) iterates over the list from last to first.

del mapping[key] removes an entry from a dictionary.

### Worked trace

Insert "car" and "cat".

| Query | Result | Reason |
| --- | --- | --- |
| Contains "car" | True | Path exists and endpoint is marked |
| Contains "ca" | False | Path exists but endpoint is not a word |
| Starts with "ca" | True | Prefix path exists |
| Contains "cap" | False | No p child after ca |

```python
trie = Trie()

trie.insert("car")
trie.insert("cat")

assert trie.contains("car") == True
assert trie.contains("ca") == False
assert trie.starts_with("ca") == True

assert trie.remove("car") == True
assert trie.contains("car") == False
assert trie.contains("cat") == True
```

### Why deletion must preserve shared prefixes

Deleting "car" must not delete the shared c → a path while "cat" still needs it.

The backward cleanup stops when it reaches a node still needed by another word or prefix.

### Costs

Let L be the input word or prefix length.

With average constant-time child-dictionary operations:

| Operation | Time |
| --- | --- |
| Insert | O(L) average |
| Exact lookup | O(L) average |
| Prefix lookup | O(L) average |
| Remove | O(L) average |

Insertion can allocate up to L new nodes.

If S is the total number of characters across inserted words, node count is at most S + 1, with shared prefixes potentially reducing it.

A trie’s search follows characters rather than comparing entire keys at each tree level. This prefix-oriented organization is the central distinction.

### When to use a trie

Use it when prefix relationships are central:

- Prefix existence.
- Word dictionaries for backtracking.
- Autocomplete.
- Searching many related words.
- Character-by-character branching.

Autocomplete still needs to enumerate matching descendants. Prefix lookup being O(L) does not make returning thousands of matches constant time.

### Common mistakes

- Confusing “path exists” with “whole word exists.”
- Deleting nodes shared by another word.
- Ignoring per-node memory overhead.
- Assuming a trie is automatically better than a set for exact-word membership.

### Chapter practice

1. Guided: Insert "app" and "apple". Is "app" a full word and a prefix?
2. After removing "app", should "apple" remain?
3. Why is an endpoint flag necessary?
4. What does inserting the empty string do in this implementation?

#### Answers and explanations

1. Yes to both.

2. Yes. Removing the shorter word clears its endpoint flag but preserves nodes needed by "apple".

3. Without it, the trie could not distinguish a stored word from a prefix that exists only because of a longer word.

4. It marks the root as a word endpoint. Therefore, contains("") becomes True.

## Chapter 4.13: Graphs and their representations

A graph represents objects and relationships.

Its objects are called vertices, or nodes.

Its relationships are called edges.

| Situation | Vertices | Edges |
| --- | --- | --- |
| Road network | Locations | Roads |
| Course prerequisites | Courses | Prerequisite relationships |
| Social network | People | Connections |
| Grid movement | Cells | Allowed moves |

### Directed and undirected graphs

An undirected edge connects both ways.

A directed edge has an orientation, such as A → B.

A weighted edge has an associated value, such as distance, time, or cost.

A path is a sequence of vertices connected by edges.

A cycle returns to a starting vertex through edges without treating immediate repeated traversal of one undirected edge as a new simple cycle.

A connected component in an undirected graph is a maximal group of vertices mutually reachable by paths.

### Example

Vertices 0–3 form a connected group, and vertex 4 is isolated, meaning it has no incident edges.

There are two connected components: {0, 1, 2, 3} and {4}.

Edges in the worked example: 0—1, 0—2, 1—3, 2—3.

### Representation 1: adjacency list

An adjacency list stores each vertex’s neighbors.

| Vertex | Neighbors |
| --- | --- |
| 0 | [1, 2] |
| 1 | [0, 3] |
| 2 | [0, 3] |
| 3 | [1, 2] |
| 4 | [] |

The degree of a vertex in a simple undirected graph is its number of incident edges. For the loop-free examples here, it equals the neighbor-list length.

Our implementation uses integer vertex identifiers from 0 through vertex_count − 1.

It rejects self-edges and suppresses duplicate edges.

A self-edge connects a vertex to itself.

```python
class AdjacencyListGraph:
    def __init__(self, vertex_count, directed=False):
        if vertex_count < 0:
            raise ValueError("Vertex count cannot be negative")

        self.directed = directed
        self.adjacency = []

        for vertex in range(vertex_count):
            self.adjacency.append([])

    def _check_vertex(self, vertex):
        if vertex < 0 or vertex >= len(self.adjacency):
            raise IndexError("Unknown vertex")

    def add_edge(self, first, second):
        self._check_vertex(first)
        self._check_vertex(second)

        if first == second:
            raise ValueError("This graph does not allow self-edges")

        # Membership checks suppress duplicate edges.
        if second not in self.adjacency[first]:
            self.adjacency[first].append(second)

        if not self.directed:
            if first not in self.adjacency[second]:
                self.adjacency[second].append(first)

    def has_edge(self, first, second):
        self._check_vertex(first)
        self._check_vertex(second)

        return second in self.adjacency[first]

    def neighbors(self, vertex):
        self._check_vertex(vertex)
        return list(self.adjacency[vertex])
```

### Representation 2: adjacency matrix

An adjacency matrix is a two-dimensional table.

Entry [u][v] records whether edge u → v exists.

For an undirected graph, the matrix is symmetric across its diagonal.

The source manuscript stopped at the start of remove_edge. The method below finishes that removal using the same directed/undirected rule as add_edge.

```python
class AdjacencyMatrixGraph:
    def __init__(self, vertex_count, directed=False):
        if vertex_count < 0:
            raise ValueError("Vertex count cannot be negative")

        self.directed = directed
        self.matrix = []

        # Allocate independent rows.
        for row in range(vertex_count):
            self.matrix.append([False] * vertex_count)

    def _check_vertex(self, vertex):
        if vertex < 0 or vertex >= len(self.matrix):
            raise IndexError("Unknown vertex")

    def add_edge(self, first, second):
        self._check_vertex(first)
        self._check_vertex(second)

        if first == second:
            raise ValueError("This graph does not allow self-edges")

        self.matrix[first][second] = True

        if not self.directed:
            self.matrix[second][first] = True

    def has_edge(self, first, second):
        self._check_vertex(first)
        self._check_vertex(second)

        return self.matrix[first][second]

    def remove_edge(self, first, second):
        self._check_vertex(first)
        self._check_vertex(second)

        self.matrix[first][second] = False

        if not self.directed:
            self.matrix[second][first] = False
```

### Example checks

```python
graph = AdjacencyListGraph(5)

graph.add_edge(0, 1)
graph.add_edge(0, 2)
graph.add_edge(1, 3)
graph.add_edge(2, 3)

assert graph.neighbors(0) == [1, 2]
assert graph.has_edge(1, 0) == True
assert graph.neighbors(4) == []

directed = AdjacencyMatrixGraph(3, directed=True)
directed.add_edge(0, 1)

assert directed.has_edge(0, 1) == True
assert directed.has_edge(1, 0) == False
```

### Memory comparison

Let V be the number of vertices, E the number of edges, and d(u) the number of stored neighbors of vertex u.

| Operation or property | List of neighbor lists | Matrix |
| --- | --- | --- |
| Storage | O(V + E) | O(V²) |
| Check edge u → v | O(d(u)) | O(1) |
| Enumerate neighbors of u | O(d(u)) | O(V) |
| Add edge in our duplicate-checking implementation | O(d(u)), plus reverse check if undirected | O(1) |
| Initialize empty representation | O(V) | O(V²) |

For an undirected adjacency list, each edge is normally stored twice. That constant factor does not change O(V + E).

If you use sets instead of lists for neighbors, average membership and insertion costs improve, with different storage overhead and iteration-order behavior.

### Sparse versus dense

A sparse graph has relatively few edges compared with the possible number.

A dense graph has many of the possible edges.

Adjacency lists are usually attractive for sparse graphs.

Matrices can be attractive when the graph is dense, the vertex count is manageable, and frequent direct edge tests matter.

### Weighted representations

For a weighted adjacency list: neighbors[u] = [(v, weight), ...].

For a weighted matrix, use a distinct “no edge” marker such as None.

Do not automatically use zero for “no edge,” because a legitimate edge can have weight zero.

### When to use a graph

Use a graph when relationships are not restricted to a simple sequence or one-parent hierarchy.

A tree is a special kind of graph. General graphs can contain cycles, multiple routes, and disconnected regions.

### Common mistakes

- Forgetting the reverse edge in an undirected graph.
- Adding the reverse edge in a directed graph.
- Allocating a huge matrix for a sparse graph.
- Sharing matrix rows with [[False] * V] * V.
- Forgetting visited-state tracking when traversing cyclic graphs.
- Confusing a missing edge with a zero-weight edge.

### Chapter practice

1. Guided: Represent an undirected graph with edges (0, 1) and (1, 2) as neighbor lists.
2. How much matrix storage does a graph with V vertices require?
3. Why does enumerating matrix neighbors require scanning an entire row?
4. Why must graph traversal handle cycles explicitly?

#### Answers and explanations

1.

```
0: [1]
1: [0, 2]
2: [1]
```

2. O(V²). There is a slot for every ordered pair of vertices.

3. A row contains the possible edge status for every vertex. Without another index, each position must be checked to find all neighbors.

4. Following edges without remembering visited vertices can revisit the same vertices indefinitely or perform unnecessary repeated work.

## Chapter 4.14: Union-find

A union-find structure maintains groups of connected items.

It is also called a disjoint-set union, abbreviated DSU.

Disjoint sets are groups that do not overlap: each item belongs to exactly one group.

Its core operations are:

- find(x): identify the representative of x’s group.
- union(a, b): merge the groups containing a and b.
- connected(a, b): test whether they are already in the same group.

### Analogy: merging teams

Initially, every person is their own team.

When two people’s teams merge, everyone in both teams belongs to one combined team.

You want to answer team-membership questions without rewriting every person’s record after each merge.

### Parent forests

A forest is a collection of trees.

Union-find represents groups as parent-linked trees.

Each item stores a parent identifier.

A root is its own parent.

Following parent links reaches a representative.

| Item | Parent |
| --- | --- |
| 0 | 0 |
| 1 | 0 |
| 2 | 2 |
| 3 | 2 |
| 4 | 4 |

Groups: {0, 1}, {2, 3}, {4}.

Representatives happen to be 0, 2, and 4. Their numeric values have no inherent importance.

### Union by size

Union by size attaches the smaller tree beneath the larger tree.

This prevents repeatedly attaching a large group beneath a tiny one and creating unnecessarily long paths.

### Path compression

Path compression shortens parent chains during find.

Our implementation uses path halving: while moving toward the root, make the current node point to its grandparent.

A grandparent is the parent of a node’s parent.

### Implementation

The source manuscript stopped after finding the two roots inside union. The rest of union, plus component_size, follows the rules in this chapter: link roots by size, do not decrease the component count when the roots already match, and read size only at a root.

```python
class UnionFind:
    def __init__(self, n):
        if n < 0:
            raise ValueError("Item count cannot be negative")

        # Every item initially represents its own group.
        self.parent = list(range(n))

        # Only root entries have meaningful current component sizes.
        self.size = [1] * n

        self.components = n

    def _check_item(self, item):
        if item < 0 or item >= len(self.parent):
            raise IndexError("Unknown item")

    def find(self, item):
        self._check_item(item)

        while self.parent[item] != item:
            # Skip one level in the parent chain.
            self.parent[item] = self.parent[self.parent[item]]

            # Continue from the shortened parent link.
            item = self.parent[item]

        return item

    def connected(self, first, second):
        return self.find(first) == self.find(second)

    def union(self, first, second):
        root_first = self.find(first)
        root_second = self.find(second)

        if root_first == root_second:
            return False

        # Attach the smaller tree beneath the larger tree.
        if self.size[root_first] < self.size[root_second]:
            root_first, root_second = root_second, root_first

        self.parent[root_second] = root_first
        self.size[root_first] = self.size[root_first] + self.size[root_second]
        self.components = self.components - 1
        return True

    def component_size(self, item):
        root = self.find(item)
        return self.size[root]
```

### Worked trace

Start with five items.

| Operation | Groups | Component count |
| --- | --- | --- |
| Initialization | {0}, {1}, {2}, {3}, {4} | 5 |
| union(0, 1) | {0, 1}, {2}, {3}, {4} | 4 |
| union(2, 3) | {0, 1}, {2, 3}, {4} | 3 |
| union(1, 3) | {0, 1, 2, 3}, {4} | 2 |
| union(0, 2) | Unchanged | 2 |

The final union returns False because both items already belong to the same group.

```python
groups = UnionFind(5)

assert groups.union(0, 1) == True
assert groups.union(2, 3) == True
assert groups.connected(0, 3) == False

assert groups.union(1, 3) == True

assert groups.connected(0, 3) == True
assert groups.component_size(0) == 4
assert groups.components == 2

assert groups.union(0, 2) == False
assert groups.components == 2
```

### Why joining roots matters

The operation is intended to combine two whole groups.

If you reassign an arbitrary internal node’s parent instead of linking roots, you can detach or reorganize only part of a represented group and break the intended membership structure.

Find the roots first.

### Costs

Union by size limits tree growth. Combining it with path compression gives an amortized bound involving the inverse Ackermann function, written α(n).

This function grows so slowly that it remains tiny for practical input sizes. It is not mathematically identical to a constant.

| Operation | Cost |
| --- | --- |
| Initialize n items | O(n) |
| Find | O(α(n)) amortized |
| Union | O(α(n)) amortized |
| Connected query | O(α(n)) amortized |
| Storage | O(n) |

A sequence of m operations after initialization has the standard bound O(n + m α(n)).

For this size-weighted structure, a single operation can still take logarithmic time before compression has shortened the relevant path.

### When to use union-find

Use it when:

- Groups repeatedly merge.
- You need many connectivity queries.
- You process undirected edges and want to detect redundant connections.
- You need the number or sizes of connected components.
- You build algorithms such as Kruskal’s minimum spanning tree.

A spanning tree connects all vertices of a connected undirected graph without cycles. A minimum spanning tree minimizes total edge weight among such trees. We mention it here as a use case, not as an algorithm you must already know.

### What union-find does not provide

It does not automatically provide:

- The actual path between two items.
- Shortest paths.
- Directed reachability.
- Efficient arbitrary splitting of groups.
- Efficient deletion of previously added connections.

Connectivity membership is less information than a complete graph representation.

### Common mistakes

- Treating the representative as a permanent semantic identifier.
- Reading size[item] without first finding the root.
- Decreasing the component count when a union joins an already-connected pair.
- Assuming the parent links are the original graph’s edges.
- Calling the bound worst-case constant time.

### Chapter practice

1. Guided: Starting with four items, perform union(0, 1) and union(1, 2). How many components remain?
2. Why should component_size(2) use find(2)?
3. Can union-find tell you the shortest route between two connected graph vertices?
4. What should union(a, b) do when both have the same root?

#### Answers and explanations

1. Two: {0, 1, 2}, {3}.

2. Only a root’s size entry represents the current full component size. Non-root entries can be stale.

3. No. It records group membership, not path information or distances.

4. Leave the structure’s component count unchanged and report that no merge occurred. Our implementation returns False.

## Chapter 4.15: Choosing the structure from the required operation

A problem often becomes easier when you translate its wording into operations.

Do not begin with: Which data structure looks familiar?

Begin with: What question must I answer repeatedly?

### Selection table

| Repeated need | Likely starting structure | Why |
| --- | --- | --- |
| Access an item by position | Array/list | Direct indexing |
| Keep an ordered sequence with end appends | Dynamic array/list | Efficient indexing and amortized append |
| Map identifiers to information | Hash map | Efficient average lookup by key |
| Check whether a value appeared | Hash set | Efficient average membership |
| Rewire known neighboring nodes | Linked list | Local link updates |
| Handle the most recent unfinished item | Stack | LIFO order |
| Handle the oldest pending item | Queue | FIFO order |
| Add and remove at both ends | Deque | Efficient endpoint operations |
| Repeatedly extract the smallest current item | Min-heap | Root access and logarithmic updates |
| Maintain a hierarchy | Tree | Parent-child organization |
| Maintain searchable sorted keys | Balanced search tree | Ordering with logarithmic height |
| Search by shared prefixes | Trie | Character-by-character prefix paths |
| Represent arbitrary relationships | Graph | Vertices and edges |
| Merge groups and query connectivity | Union-find | Efficient component maintenance |

### Worked choice 1: count words

Required operation: given a word, find and update its count.

A dictionary is a natural choice.

A set would lose frequencies.

A list of pairs could work, but locating the right pair might require a scan for every word.

### Worked choice 2: process tasks by arrival

Required operation: remove the earliest task that has not been processed.

Use a queue.

A stack would process the most recent task instead.

A heap would introduce a priority rule the problem did not request.

### Worked choice 3: process tasks by urgency

Required operation: remove the currently smallest priority value.

Use a min-heap.

A sorted list also supports reading the smallest value, but maintaining sorted order during frequent insertions can require shifting many elements.

### Worked choice 4: autocomplete

Required operations: follow a typed prefix, and enumerate words beneath that prefix.

A trie organizes exactly that relationship.

A hash set supports exact-word checks but does not directly organize words by shared prefixes.

### Worked choice 5: evolving connectivity

Required operations: add an undirected connection, and ask whether two vertices are now connected.

Union-find is a strong candidate.

If you must also return the actual route, maintain additional graph information.

### Combining structures

Real solutions often use more than one structure.

| Problem need | Combined structures |
| --- | --- |
| Count frequencies, then select the largest counts | Hash map + heap |
| Search a graph while avoiding revisits | Adjacency list + stack or queue + set |
| Preserve first-occurrence order while removing duplicates | List + set |
| Explore words on a board | Grid + trie + visited-state tracking |
| Maintain a cache with fast lookup and recency updates | Hash map + doubly linked list |

A cache stores previously obtained information for faster reuse.

These combinations work because each structure has a distinct job.

### Avoid unnecessary complexity

If all you need is one maximum value from a fixed list, one scan is enough.

You do not need a heap merely because the word “maximum” appears.

If you need repeated minimum extraction while values are inserted, the heap becomes more relevant.

Pattern recognition must account for the full sequence of operations.

### Chapter practice

Choose a structure and explain the repeated operation.

1. Guided: A program must undo the most recent action.
2. A program repeatedly asks whether an integer has appeared before.
3. A program repeatedly removes the smallest pending distance.
4. A program merges groups and asks whether two people are in the same group.
5. A program must retain the order of first appearances while removing duplicates.

#### Answers and explanations

1. Stack. The most recent action is handled first.

2. Hash set. The repeated operation is membership.

3. Min-heap. The repeated operation is minimum extraction with updates to pending values.

4. Union-find. The operations are group merging and component membership.

5. List plus set. The list preserves output order. The set tracks whether a value has already appeared.

## Part 4 implementation review

The structures above deliberately make their invariants visible.

| Structure | Central invariant |
| --- | --- |
| Dynamic array | Logical items occupy the first size positions |
| Text sequence | The public operations do not modify existing text |
| Chained hash map | Each key is stored in the bucket determined by the current bucket count |
| Singly linked list | Following next from head reaches each logical node in order |
| Stack | The top is the most recently pushed remaining item |
| Queue | The front is the earliest enqueued remaining item |
| Doubly linked deque | Forward and backward links agree, with correct endpoints |
| Min-heap | Every parent is no larger than either child |
| Binary tree | Nodes form a rooted, acyclic parent-child hierarchy |
| BST | Every left-subtree value is smaller and every right-subtree value is larger |
| Trie | A path spells a prefix, and endpoint flags identify stored words |
| Graph representation | Stored edges match the intended directed or undirected relationships |
| Union-find | Following parents reaches a root representing the entire component |

When an implementation fails, inspect the invariant that should have survived the last operation.

Examples:

- A deque removal fails because the backward link was not updated.
- A heap pop fails because the replacement root was not sifted downward.
- A hash lookup fails because resizing did not redistribute entries.
- A BST removal fails because the replacement value violates subtree ordering.
- A union-find count fails because a redundant union still decreased the count.

This is more precise than treating each bug as an unrelated accident.

## Running glossary: additions from Part 4

| Term | Meaning |
| --- | --- |
| Abstract data type | A behavior specification independent of a particular implementation |
| Adjacency list | A graph representation storing each vertex’s neighbors |
| Adjacency matrix | A graph representation with a slot for every ordered vertex pair |
| Alphabet | The allowed symbols in a collection of sequences |
| Array | An indexed arrangement of elements |
| Attribute | Information accessed through an object’s named member |
| Balanced search tree | A search tree that maintains logarithmic height |
| Binary heap | A complete binary tree satisfying a heap-order rule |
| Binary search tree | A binary tree with an ordering rule over entire subtrees |
| Binary tree | A tree where each node has at most two children |
| Bucket | A hash-table location containing entries assigned to it |
| Child | A node directly below a parent |
| Circular buffer | Array-based storage whose positions wrap around |
| Class | A definition of a kind of object |
| Complete binary tree | A binary tree filled level by level, with the final level filled left to right |
| Connected component | A maximal mutually reachable group in an undirected graph |
| Contiguous | Adjacent in a storage arrangement |
| Data structure | An organization of information supporting particular operations |
| Degree | Number of incident edges, with details depending on graph conventions |
| Dense graph | A graph with many of the possible edges |
| Deque | A queue supporting additions and removals at both ends |
| Dequeue | Remove the front queue item |
| Descendant | A node reachable by following child references |
| Directed edge | An edge with an orientation |
| Disjoint sets | Nonoverlapping groups |
| Doubly linked list | A list whose nodes store both previous and next references |
| Edge | A relationship or connection between vertices |
| Enqueue | Add an item to the back of a queue |
| FIFO | First in, first out |
| Forest | A collection of trees |
| Graph | A collection of vertices and edges |
| Hash map | A key-value mapping implemented using hashing |
| Hash set | A membership collection implemented using hashing |
| Head | Reference to the first linked-list node |
| Heapify | Rearrange a collection into heap order |
| Height | Maximum root-to-node edge distance under this course’s convention |
| Implementation | The internal code and organization fulfilling an interface |
| Inorder | Left subtree, node, right subtree |
| Inorder successor | The next larger item in a BST’s sorted order |
| Instance | A particular object created from a class |
| Interface | The operations and behavior a structure promises |
| Isolated vertex | A vertex with no incident edges |
| Leaf | A tree node with no children |
| Level order | Visiting tree levels from top to bottom |
| Lexicographic comparison | Comparing sequences at their first differing position |
| LIFO | Last in, first out |
| Linked list | A sequence represented by connected nodes |
| Load factor | Number of hash-table entries divided by bucket count |
| Memory address | A location identifier in memory |
| Min-heap | A heap whose parent values do not exceed child values |
| Node | An object storing a value and structural references |
| Parent | The node directly above a child |
| Path | A sequence of vertices joined by edges |
| Path compression | Shortening union-find parent chains during lookup |
| Path halving | Making visited nodes point to their grandparents while walking toward a root |
| Peek | Inspect the next removable item without removing it |
| Pop | Remove an item according to a structure’s policy |
| Postorder | Left subtree, right subtree, node |
| Prefix | An initial portion of a sequence |
| Preorder | Node, left subtree, right subtree |
| Priority queue | An ADT that removes items according to priority |
| Push | Add an item to a stack or heap, according to that structure’s operation |
| Queue | A FIFO collection |
| Root | The designated top node of a rooted tree |
| Rotation | A local search-tree restructuring preserving sorted order |
| Self-edge | An edge from a vertex to itself |
| Separate chaining | Resolving hash collisions with per-bucket collections |
| Sift down | Restore heap order by moving a value toward descendants |
| Sift up | Restore heap order by moving a value toward ancestors |
| Singly linked list | A list whose nodes store next references |
| Sparse graph | A graph with relatively few edges |
| Special method | A method Python recognizes for a language operation |
| Stack | A LIFO collection |
| Subsequence | An order-preserving selection that may skip positions |
| Subtree | A node together with its descendants |
| Tail | Reference to the final linked-list node |
| Traversal | Visiting a structure’s elements in a specified order |
| Trie | A structure organizing sequences through shared prefixes |
| Undirected edge | A connection usable in both directions |
| Union by size | Attaching the smaller union-find tree beneath the larger |
| Union-find | A structure for merging disjoint groups and querying membership |
| Vertex | An object represented in a graph |
| Weighted edge | An edge with an associated cost or other numeric value |

## Part 4 readiness check

Before moving to algorithms, you should be able to:

- Explain why array indexing is fast but front insertion is not.
- Explain how two different keys survive a hash collision.
- Rewire a linked list without losing the remaining nodes.
- Distinguish stack, queue, and priority-queue removal rules.
- Explain why a heap is not a sorted array.
- Distinguish a binary tree from a binary search tree.
- Explain why an unbalanced BST can become linear.
- Distinguish a stored trie word from a prefix.
- Choose between adjacency lists and a matrix.
- Explain what union-find remembers and what it does not.
- State the invariant of a structure before changing it.
- Choose a structure based on repeated operations, rather than a keyword alone.

End of Part 4. Next: Part 5, Core Algorithms and Patterns.
