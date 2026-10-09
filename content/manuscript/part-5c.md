## Chapter 5.9: Backtracking

### Intuition: choose, explore, undo

Suppose you are generating possible selections from a set of items.

You make one choice, explore everything that follows from it, then undo the choice before trying an alternative.

Backtracking is systematic exploration of choices while restoring the state needed for other branches.

It often uses DFS over an implicit search tree, whose nodes represent partial decisions rather than stored graph objects.

### Worked problem: generate all subsets

For [1,2], the choices are:

- Exclude or include 1.
- Exclude or include 2.

We use a list named path for the current selection.

### Trace

| Decision path | Selection when complete |
| --- | --- |
| Exclude 1, exclude 2 | [] |
| Exclude 1, include 2 | [2] |
| Include 1, exclude 2 | [1] |
| Include 1, include 2 | [1,2] |

```python
def all_subsets(numbers):
    # Contract: input values are distinct.
    result = []
    path = []

    def choose(index):
        if index == len(numbers):
            # Save a snapshot of the current selection.
            result.append(path.copy())
            return
        # Choice 1: exclude this element.
        choose(index + 1)
        # Choice 2: include this element.
        path.append(numbers[index])
        choose(index + 1)
        # Restore the state before returning to the caller.
        path.pop()

    choose(0)
    return result
```

### Why the copy matters

Every recursive call shares the same mutable path.

If you store:

`result.append(path)`

each result entry refers to that same list. Later changes alter what all those references observe.

You need snapshots of completed answers.

### Pruning

Pruning skips a branch once you can prove it cannot produce a needed answer.

Example: if choosing exactly three items, a branch with four chosen items is already invalid.

Pruning must be justified. Discarding a branch because it “looks unlikely” can remove valid solutions.

### Complexity

There are \(2^n\) subsets.

Copying each subset costs its length. Total output size is \(O(n2^n)\).

Therefore:

- Time including output construction: \(O(n2^n)\).
- Auxiliary path and stack space: \(O(n)\).
- Returned-output space: \(O(n2^n)\).

### Recognition clues

Look for:

- Generate all combinations, subsets, or arrangements.
- Find a valid configuration under several constraints.
- Search a board while temporarily marking chosen positions.
- Enumerate solutions where choices affect later choices.

### Common mistakes

- Failing to undo a mutation.
- Recording a shared mutable object instead of a copy.
- Generating duplicate solutions when input values repeat.
- Pruning without a proof that the branch is impossible.

### Practice

1. Guided: List all subsets of [5].
2. Why does the empty input have one subset?
3. What goes wrong if path.pop() is omitted?

#### Answers and explanations

1. [], [5]

2. There is one selection: choose nothing. Thus the result is [[]], not [].

3. A choice from an earlier branch remains in path, contaminating later branches with items they did not choose.


## Chapter 5.10: Greedy algorithms

A greedy algorithm makes a locally selected choice and commits to it without exploring every alternative.

The difficult part is proving the local choice can belong to an optimal global answer.

### Intuition: finish early to preserve future options

Problem:

Select the maximum number of nonoverlapping meetings.

Assume:

- Each meeting has equal value.
- Meetings are half-open intervals [start, end).
- Every meeting has start < end.
- A meeting ending at time 3 is compatible with one starting at time 3.

The greedy rule is:

Among available meetings, select the one that finishes earliest.

### A tempting failed rule

“Choose the meeting that starts earliest.”

Counterexample:

[0,6), [1,2), [2,4), [4,6)

Choosing [0,6) gives one meeting.

Choosing the other three gives three.

### Trace using earliest finish

Sorted by end:

[1,2), [2,4), [0,6), [4,6)

| Meeting | Compatible with last selection? | Action |
| --- | --- | --- |
| [1,2) | Yes | Select |
| [2,4) | Yes | Select |
| [0,6) | No | Skip |
| [4,6) | Yes | Select |

```python
def finish_time(interval):
    return interval[1]

def select_meetings(intervals):
    ordered = sorted(intervals, key=finish_time)
    chosen = []
    last_end = None
    for start, end in ordered:
        if last_end is None or start >= last_end:
            chosen.append((start, end))
            last_end = end
    return chosen
```

The key argument tells sorting which value to use when ordering each item.

### Why the rule works: an exchange argument

An exchange argument shows that replacing part of an optimal solution with the greedy choice does not make the solution worse.

Take an optimal schedule.

Let its first meeting be A.

Let the earliest-finishing meeting be G.

Since G ends no later than A, replacing A with G cannot interfere with the later meetings that followed A.

The schedule keeps the same number of meetings.

Therefore, some optimal schedule begins with G.

After selecting G, the same reasoning applies to meetings that start after it ends.

### Complexity

- Sorting: \(O(n\log n)\).
- Scan: \(O(n)\).
- Extra storage including output and sorted copy: \(O(n)\).

### A case where greedy coin selection fails

Coins:

[1,3,4]

Amount:

6

Taking the largest possible coin first gives:

4 + 1 + 1

Three coins.

But:

3 + 3

uses two.

The local largest-coin choice has no general correctness guarantee. We will solve the general problem with dynamic programming.

### Recognition clues

Consider greedy reasoning when:

- A choice can safely remove possibilities.
- Sorting creates a useful order of decisions.
- An exchange argument is available.
- One candidate dominates another in every relevant future situation.

### Common misconception

“This choice seems best now” is not a proof.

Try to construct a small counterexample before trusting a greedy rule.

### Practice

1. Guided: Apply earliest finish to [1,3), [2,4), [3,5).
2. Why does earliest finish help preserve future options?
3. Does this algorithm remain correct if meetings have different rewards?

#### Answers and explanations

1. Choose [1,3), skip [2,4), then choose [3,5). Two meetings.

2. Finishing earlier leaves at least as much remaining time as any later-finishing first choice.

3. Not generally. Maximizing total reward is different from maximizing the number of meetings. Weighted scheduling typically requires a different method, often dynamic programming.


## Chapter 5.11: Topological sorting

A topological ordering places vertices in an order such that every directed edge goes from an earlier vertex to a later one.

Interpret an edge A → B as:

A must come before B.

A directed graph has a topological ordering exactly when it is a directed acyclic graph, abbreviated DAG.

Acyclic means containing no directed cycle.

### Intuition: repeatedly complete tasks with no remaining prerequisites

The indegree of a vertex is the number of incoming edges.

A vertex with indegree zero has no remaining prerequisite in the current graph.

### Kahn’s algorithm

1. Count indegrees.
2. Queue every zero-indegree vertex.
3. Remove one ready vertex.
4. Reduce the indegrees of its outgoing neighbors.
5. Queue any neighbor whose indegree becomes zero.

### Trace

Edges:

0 → 2

1 → 2

2 → 3

Initial indegrees:

[0, 0, 2, 1]

| Removed | Changed indegree | Ready queue afterward | Order |
| --- | --- | --- | --- |
| 0 | Vertex 2: 2→1 | [1] | [0] |
| 1 | Vertex 2: 1→0 | [2] | [0,1] |
| 2 | Vertex 3: 1→0 | [3] | [0,1,2] |
| 3 | None | [] | [0,1,2,3] |

```python
from collections import deque

def topological_order(adjacency):
    indegree = [0] * len(adjacency)
    for neighbors in adjacency:
        for neighbor in neighbors:
            indegree[neighbor] += 1
    ready = deque()
    for vertex in range(len(adjacency)):
        if indegree[vertex] == 0:
            ready.append(vertex)
    order = []
    while ready:
        vertex = ready.popleft()
        order.append(vertex)
        for neighbor in adjacency[vertex]:
            indegree[neighbor] -= 1
            if indegree[neighbor] == 0:
                ready.append(neighbor)
    if len(order) != len(adjacency):
        return None
    return order
```

### Cycle detection

In a cycle, every remaining vertex depends on another remaining vertex.

If the queue empties before all vertices are processed, no topological ordering exists.

Returning None distinguishes failure from the valid empty ordering [] for a graph with no vertices.

### Complexity

- Time: \(O(V+E)\).
- Auxiliary space: \(O(V)\), excluding the supplied graph.

### Recognition clues

Look for:

- Prerequisites.
- Build dependencies.
- Tasks that must precede other tasks.
- Detecting whether a dependency system is possible.

### Common mistakes

- Reversing the meaning of the edges.
- Starting with only one zero-indegree vertex.
- Forgetting disconnected components.
- Treating one valid ordering as the only possible ordering.

### Practice

1. Guided: Is [1,0,2,3] also valid for the example?
2. What happens for 0 → 1 and 1 → 0?
3. Why does a zero-indegree vertex belong safely at the next output position?

#### Answers and explanations

1. Yes. Both 0 and 1 must precede 2, but their relative order is unrestricted.

2. Neither vertex is initially ready. The algorithm returns None.

3. No unprocessed vertex is required to precede it, so placing it next violates no remaining dependency.


## Chapter 5.12: Dijkstra’s algorithm

BFS minimizes edge count when all edges have equal cost.

For nonnegative weighted edges, use Dijkstra’s algorithm to find shortest path distances from a starting vertex.

### Intuition: expand the cheapest unfinished route

Maintain the best distance currently known for each vertex.

A min-heap repeatedly selects the smallest pending distance.

A relaxation attempts to improve a neighbor’s distance through the current vertex:

\[
candidate=distance[current]+edge\_weight
\]

If candidate is smaller, update the neighbor.

Dijkstra’s correctness depends on nonnegative edge weights. Princeton’s shortest-path material explains relaxation and this requirement. algs4.cs.princeton.edu

### Example

Edges:

0 → 1, cost 4

0 → 2, cost 1

2 → 1, cost 2

1 → 3, cost 1

2 → 3, cost 5

### Trace

| Heap entry removed | Improvements | Distances [0,1,2,3] |
| --- | --- | --- |
| (0,0) | 1 gets 4, 2 gets 1 | [0,4,1,∞] |
| (1,2) | 1 improves to 3, 3 gets 6 | [0,3,1,6] |
| (3,1) | 3 improves to 4 | [0,3,1,4] |
| (4,1) | Obsolete entry, skip | Unchanged |
| (4,3) | No outgoing improvements | Unchanged |
| (6,3) | Obsolete entry, skip | Unchanged |

The heap can contain old distances. We skip entries that no longer match the current best distance.

```python
import heapq

def dijkstra(adjacency, start):
    # Each adjacency entry contains (neighbor, weight) pairs.
    for neighbors in adjacency:
        for neighbor, weight in neighbors:
            if weight < 0:
                raise ValueError("Dijkstra requires nonnegative weights")
    distance = [float("inf")] * len(adjacency)
    distance[start] = 0
    pending = [(0, start)]
    while pending:
        current_distance, vertex = heapq.heappop(pending)
        if current_distance != distance[vertex]:
            # A later discovery improved this vertex.
            continue
        for neighbor, weight in adjacency[vertex]:
            candidate = current_distance + weight
            if candidate < distance[neighbor]:
                distance[neighbor] = candidate
                heapq.heappush(pending, (candidate, neighbor))
    return distance
```

`float("inf")` represents positive infinity. It marks an unreachable or not-yet-reached distance.

### Why choosing the smallest distance is safe

Suppose the smallest valid pending distance is d.

Any route that first goes through a vertex with distance at least d, then follows nonnegative edges, cannot return with a total smaller than d.

That is the reason the smallest unfinished distance can be finalized.

Negative edges invalidate this reasoning.

### Complexity of this implementation

This version inserts improved entries rather than updating existing heap entries.

- Up to \(O(E)\) entries may enter the heap.
- Time: \(O(V+E\log(E+2))\).
- Auxiliary space: \(O(V+E)\).

For simple graphs, this is commonly expressed as an \(O((V+E)\log V)\) time bound.

Do not claim \(O(V)\) heap storage for this duplicate-entry implementation.

### Recognition clues

Look for:

- Minimum total travel cost.
- Nonnegative weighted graph edges.
- Repeatedly selecting the smallest known unfinished distance.

If negative edges are allowed, consider other algorithms such as Bellman–Ford, or topological processing if the weighted graph is a DAG.

### Common mistakes

- Using Dijkstra with negative weights.
- Marking a vertex finished when first discovered.
- Failing to skip obsolete heap entries.
- Updating a distance without pushing the improved candidate.

### Practice

1. Guided: Why is the shortest distance from 0 to 1 equal to 3 rather than 4?
2. Why is heap entry (4,1) obsolete?
3. Does a zero-weight edge violate the algorithm’s assumptions?

#### Answers and explanations

1. Route 0 → 2 → 1 costs: 1 + 2 = 3

2. The stored best distance for vertex 1 has already improved to 3.

3. No. Zero is nonnegative.


## Chapter 5.13: Binary search on the answer

Sometimes the input is not sorted, but the possible answers have a useful order.

A predicate is a function that returns true or false.

A predicate is monotonic over an ordered domain when its truth value changes in one direction, such as:

False, False, False, True, True, True

Then binary search can find the first true answer.

### Worked problem: minimum shipping capacity

Given positive package weights in a fixed order, find the smallest capacity that ships them within a given number of days.

Rules:

- Do not reorder packages.
- Each package is shipped whole.
- A day’s total weight cannot exceed capacity.

### Feasibility question

For a proposed capacity C:

Can we finish within the allowed days?

If capacity C works, any larger capacity also works.

That establishes monotonicity.

### Bounds

The capacity must be at least:

\[
\max(weights)
\]

Otherwise, the largest package cannot fit.

The capacity need not exceed:

\[
\sum weights
\]

because that ships everything in one day.

### Feasibility implementation

```python
def days_needed(weights, capacity):
    # Contract: capacity is at least the largest weight.
    days = 1
    load = 0
    for weight in weights:
        if load + weight > capacity:
            days += 1
            load = 0
        load += weight
    return days
```

Filling each day until the next package no longer fits minimizes the number of days for that capacity. Ending a day earlier cannot make later ordered packages fit into fewer days.

### Binary search

```python
def minimum_capacity(weights, days):
    # Contract: nonempty positive weights and days >= 1.
    left = max(weights)
    right = sum(weights)
    while left < right:
        middle = (left + right) // 2
        if days_needed(weights, middle) <= days:
            # This capacity works. Search for a smaller working value.
            right = middle
        else:
            # This capacity is too small.
            left = middle + 1
    return left
```

### Trace

Weights:

`[3,2,2,4,1,4]`

Allowed days: 3.

| left | right | Capacity tested | Days needed | Update |
| --- | --- | --- | --- | --- |
| 4 | 16 | 10 | 2 | right = 10 |
| 4 | 10 | 7 | 3 | right = 7 |
| 4 | 7 | 5 | 4 | left = 6 |
| 6 | 7 | 6 | 3 | right = 6 |

Answer: 6.

One valid division is:

[3,2] | [2,4] | [1,4]

### Complexity

Let n be the number of packages and:

\[
R=\sum weights-\max(weights)
\]

Each feasibility check scans n values.

Time:

\[
O(n\log(R+2))
\]

Auxiliary space: \(O(1)\).

### Recognition clues

Look for:

- Minimize the maximum.
- Maximize the minimum.
- Minimum speed, capacity, time, or threshold.
- A yes-or-no feasibility test that becomes easier as the answer moves in one direction.

### Common mistakes

- Assuming feasibility is monotonic without proving it.
- Choosing an upper bound that might not work.
- Returning any feasible value instead of the boundary.
- Mixing “at most” with “exactly.”

### Practice

1. Guided: What is the minimum capacity for weights [2,2,2] in three days?
2. What about one day?
3. Why can you discard every capacity below an infeasible midpoint?

#### Answers and explanations

1. 2

2. 6

3. A smaller capacity cannot ship more packages per day than the tested capacity under the same ordering rules. It cannot fix the infeasibility.

