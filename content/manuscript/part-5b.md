## Chapter 5.5: Sliding windows

A window is a consecutive region of a sequence.

A sliding-window algorithm maintains information about that region while moving its boundaries.

The important opportunity is reuse: neighboring windows overlap heavily.

### Fixed-size windows

Problem:

Find the largest sum of exactly k consecutive values.

The direct approach recomputes each sum from scratch.

Instead:

- Add the newly entering value.
- Subtract the value leaving the window.

### Trace

Input:

`[2, 1, 5, 1, 3]`, k = 3

| Window | Calculation | Sum | Best |
| --- | --- | --- | --- |
| [2, 1, 5] | Initial sum | 8 | 8 |
| [1, 5, 1] | 8 - 2 + 1 | 7 | 8 |
| [5, 1, 3] | 7 - 1 + 3 | 9 | 9 |

```python
def max_fixed_window(numbers, k):
    if k < 1 or k > len(numbers):
        raise ValueError("Require 1 <= k <= input length")
    total = 0
    # Build the first complete window.
    for index in range(k):
        total += numbers[index]
    best = total
    for right in range(k, len(numbers)):
        total += numbers[right]
        total -= numbers[right - k]
        best = max(best, total)
    return best
```

Time: \(O(n)\). Auxiliary space: \(O(1)\).

This fixed-size sum update works even when values are negative.

### Variable-size windows

Now consider:

Find the shortest consecutive region whose sum is at least a positive target.

For the following algorithm, all input values must be positive.

Expand the right boundary until the window qualifies. Then shrink the left boundary while it continues to qualify.

### Why positivity matters

- Adding a positive value increases the sum.
- Removing a positive value decreases the sum.

These predictable changes justify moving boundaries in one direction.

### Trace

Input:

`[2, 3, 1, 2, 4, 3]`, target = 7

| Right index | Added | Sum before shrinking | Qualifying windows examined | Best length |
| --- | --- | --- | --- | --- |
| 0 | 2 | 2 | None | — |
| 1 | 3 | 5 | None | — |
| 2 | 1 | 6 | None | — |
| 3 | 2 | 8 | [2,3,1,2] | 4 |
| 4 | 4 | 10 | [3,1,2,4], [1,2,4] | 3 |
| 5 | 3 | 9 | [2,4,3], [4,3] | 2 |

```python
def min_positive_window(numbers, target):
    # Contract: target and every input value are positive.
    left = 0
    total = 0
    best = len(numbers) + 1
    for right in range(len(numbers)):
        total += numbers[right]
        # Remove left values while the current window still qualifies.
        while total >= target:
            best = min(best, right - left + 1)
            total -= numbers[left]
            left += 1
    if best == len(numbers) + 1:
        return 0
    return best
```

### Why nested loops are still linear

The right pointer advances at most n times.

The left pointer also advances at most n times across the entire function.

It does not reset for each right position.

Time: \(O(n)\). Auxiliary space: \(O(1)\).

### A counterexample when negatives are allowed

Input:

`[1, -1, 5]`, target = 5

A valid shortest answer is [5], length 1.

The positivity-based shrinking logic can stop after removing the first 1, because the sum falls below the target. It then fails to remove -1, which would increase the sum.

The missing monotonic behavior invalidates the method.

### Recognition clues

Look for:

- A substring or subarray, meaning consecutive positions.
- A fixed window length.
- A longest or shortest valid consecutive region.
- A condition that can be maintained as endpoints move.

### Common mistakes

- Using if when repeated shrinking requires while.
- Forgetting to remove a departing item’s contribution.
- Initializing the maximum sum to zero when all windows may be negative.
- Applying a positivity-dependent sum window to arbitrary integers.

### Practice

1. Guided: Find the maximum size-2 window sum in [4, -1, 2, 3].
2. Why is the variable-size algorithm linear despite its nested loop?
3. Give a reason ordinary sum-based shrinking can fail with negative values.

#### Answers and explanations

1. Window sums: 3, 1, 5. Answer: 5.

2. Each endpoint moves forward at most n times.

3. Removing a negative value increases the sum. Therefore, falling below the target does not mean further left-boundary movement cannot restore validity.


## Chapter 5.6: Prefix sums and prefix-frequency maps

### Intuition: save totals so you can subtract earlier work

Suppose you know the total through position 8 and the total through position 3.

Their difference gives the sum of the region between them.

A prefix sum records the sum of an initial portion of a sequence.

Use this definition:

\[
prefix[i]=\text{sum of the first }i\text{ elements}
\]

Therefore:

\[
prefix[0]=0
\]

### Trace

For:

`[3, -1, 4, 2]`

| i | First i values | prefix[i] |
| --- | --- | --- |
| 0 | None | 0 |
| 1 | [3] | 3 |
| 2 | [3,-1] | 2 |
| 3 | [3,-1,4] | 6 |
| 4 | All values | 8 |

```python
def build_prefix(numbers):
    prefix = [0]
    for number in numbers:
        prefix.append(prefix[-1] + number)
    return prefix
```

For a half-open range [left, right):

\[
\text{range sum}=prefix[right]-prefix[left]
\]

Example: indices 1 through 2, represented by [1, 3):

\[
prefix[3]-prefix[1]=6-3=3
\]

That matches:

-1 + 4 = 3

### Costs

- Build: \(O(n)\) time and space.
- Each range-sum query: \(O(1)\).

This is especially useful when many queries refer to an unchanged input.

If values change, the old prefix sums can become invalid. Later data structures such as Fenwick trees address efficient updates, but they are outside this core part.

### Count subarrays with a target sum

Suppose a subarray ends at the current position.

Let its ending prefix sum be current.

We want an earlier prefix previous satisfying:

\[
current-previous=target
\]

Rearrange:

\[
previous=current-target
\]

Now the question becomes:

How many earlier prefix sums equal current - target?

A frequency dictionary answers that.

### Trace

Input:

`[1, -1, 1]`, target = 1

Initialize:

`counts = {0: 1}`

The empty prefix is a valid earlier prefix.

| Current value | Current prefix | Needed earlier prefix | Earlier occurrences | Answer |
| --- | --- | --- | --- | --- |
| 1 | 1 | 0 | 1 | 1 |
| -1 | 0 | -1 | 0 | 1 |
| 1 | 1 | 0 | 2 | 3 |

The qualifying subarrays are:

- The first [1].
- The final [1].
- The entire [1, -1, 1].

```python
def count_target_subarrays(numbers, target):
    counts = {0: 1}
    prefix = 0
    answer = 0
    for number in numbers:
        prefix += number
        # Count earlier prefixes before recording the current prefix.
        answer += counts.get(prefix - target, 0)
        counts[prefix] = counts.get(prefix, 0) + 1
    return answer
```

### Why lookup comes before insertion

If you insert the current prefix first and target == 0, you can count a zero-length region ending at the current boundary.

The problem asks for nonempty subarrays, so the dictionary must represent earlier boundaries.

### Complexity

Under average-case dictionary operations:

- Time: \(O(n)\).
- Auxiliary space: \(O(n)\) worst case.

Negative values are allowed.

### Recognition clues

Look for:

- Many range-sum queries.
- A subarray sum equal to a target.
- Negative values that break a basic sliding window.
- An equation involving the difference of two cumulative quantities.

### Common mistakes

- Mixing inclusive and exclusive boundaries.
- Omitting the initial zero prefix.
- Storing only membership when repeated prefix values require frequencies.
- Updating the dictionary before counting earlier matches.

### Practice

1. Guided: Build prefix sums for [2, 5, -3].
2. How do you obtain the sum of indices 1 and 2 from that array?
3. How many zero-sum nonempty subarrays does [0, 0] contain?

#### Answers and explanations

1. [0, 2, 7, 4]

2. Use: prefix[3] - prefix[1] = 4 - 2 = 2

3. Three: first zero, second zero, and both zeros. The prefix zero occurs repeatedly, which is why frequency matters.


## Chapter 5.7: Intervals

An interval represents a range between a start and an end.

Endpoint conventions matter:

- A closed interval [a, b] includes both endpoints.
- A half-open interval [a, b) includes a but excludes b.

This chapter merges closed intervals.

### Intuition: process ranges from left to right

After sorting by start:

- The next interval either extends the current merged region.
- Or it begins a new separate region.

You do not need to compare it with every earlier interval.

### Trace

Input:

`[[1,3], [2,6], [8,10], [10,12]]`

| Next interval | Comparison | Merged result |
| --- | --- | --- |
| [1,3] | First interval | [[1,3]] |
| [2,6] | 2 <= 3, overlaps | [[1,6]] |
| [8,10] | 8 > 6, separate | [[1,6], [8,10]] |
| [10,12] | 10 <= 10, touches | [[1,6], [8,12]] |

Because the intervals are closed, sharing endpoint 10 counts as overlap.

```python
def merge_intervals(intervals):
    # Contract: each interval has start <= end.
    ordered = sorted(intervals)
    merged = []
    for start, end in ordered:
        if not merged or start > merged[-1][1]:
            # Start a new merged interval.
            merged.append([start, end])
        else:
            # Extend only if this interval reaches farther.
            merged[-1][1] = max(merged[-1][1], end)
    return merged
```

### Why only the latest merged interval matters

Earlier merged intervals end before the latest merged interval begins.

Since starts are processed in sorted order, a new interval cannot jump backward and overlap a completed earlier region without also overlapping the latest relevant region.

### Nested intervals

Input:

`[[1,10], [2,3]]`

The second interval is contained inside the first.

Using max preserves endpoint 10.

Blindly replacing the endpoint with 3 would incorrectly shrink the merged range.

### Complexity

- Sorting: \(O(n\log n)\).
- Scan: \(O(n)\).
- Extra storage: \(O(n)\), including sorting/output structures.

### Recognition clues

Look for:

- Meetings, ranges, segments, reservations, or occupied time.
- Overlap, merging, coverage, or conflicts.
- A need to process starts or ends in order.

### Common mistakes

- Ignoring endpoint conventions.
- Failing to sort.
- Shrinking a merged interval when processing a contained interval.
- Mutating the original nested lists accidentally.

### Practice

1. Guided: Merge [[1,4], [2,3], [6,8]].
2. Do closed intervals [1,2] and [2,3] overlap?
3. Do half-open intervals [1,2) and [2,3) overlap?

#### Answers and explanations

1. [[1,4], [6,8]]

2. Yes. Both contain 2.

3. No. The first excludes 2. A problem may separately request combining adjacent ranges, so always follow its stated rule.


## Chapter 5.8: Breadth-first search and depth-first search

Both algorithms explore connections. Their difference is the order in which pending work is handled.

### Breadth-first search: expand by distance in edges

Breadth-first search, abbreviated BFS, uses a queue.

It explores:

1. The starting vertex.
2. Vertices one edge away.
3. Vertices two edges away.
4. And so on.

Analogy: a search expands outward one layer at a time.

For an unweighted graph, BFS gives shortest path lengths measured in number of edges.

### Example graph

The source paste included a diagram renderer stylesheet instead of the drawing. The graph it labeled is vertices 0, 1, 2, 3, and an isolated 4:

```
0 — 1
|    |
2 — 3

4   (no edges)
```

Adjacency list:

```python
graph = [
    [1, 2],
    [0, 3],
    [0, 3],
    [1, 2],
    [],
]
```

### Trace from vertex 0

| Removed from queue | Newly discovered | Queue afterward | Known distances |
| --- | --- | --- | --- |
| 0 | 1, 2 | [1,2] | 0→0, 1→1, 2→1 |
| 1 | 3 | [2,3] | Add 3→2 |
| 2 | None | [3] | Unchanged |
| 3 | None | [] | Unchanged |

Vertex 4 remains unreachable.

```python
from collections import deque

def bfs_distances(adjacency, start):
    # Vertices are valid integers from 0 through V - 1.
    distance = [-1] * len(adjacency)
    distance[start] = 0
    pending = deque([start])
    while pending:
        vertex = pending.popleft()
        for neighbor in adjacency[vertex]:
            if distance[neighbor] == -1:
                # Mark immediately when the vertex enters the queue.
                distance[neighbor] = distance[vertex] + 1
                pending.append(neighbor)
    return distance
```

Expected result:

`[0, 1, 1, 2, -1]`

### Why the first discovery gives a shortest path

The queue handles all distance-d vertices before distance-d + 1 vertices.

A newly discovered neighbor receives distance d + 1.

A shorter path would have reached it from an earlier layer, which would already have been processed.

This argument assumes equal-cost edges.

### Depth-first search: follow one branch before returning

Depth-first search, abbreviated DFS, uses a stack, explicitly or through recursion.

Analogy: explore one corridor until you cannot continue, then return to an earlier branching point.

```python
def dfs_order(adjacency, start):
    seen = [False] * len(adjacency)
    order = []

    def visit(vertex):
        # Mark before following edges to prevent cycles from repeating work.
        seen[vertex] = True
        order.append(vertex)
        for neighbor in adjacency[vertex]:
            if not seen[neighbor]:
                visit(neighbor)

    visit(start)
    return order
```

For the graph above, following neighbors in their listed order:

0, 1, 3, 2

### DFS trace

| Active action | Result |
| --- | --- |
| Visit 0 | Follow neighbor 1 |
| Visit 1 | Skip seen 0, follow 3 |
| Visit 3 | Skip seen 1, follow 2 |
| Visit 2 | Both neighbors already seen |
| Return through waiting calls | Exploration completes |

DFS does not generally discover shortest unweighted paths first.

### Complexity

With adjacency lists:

- Time: \(O(V+E)\).
- Auxiliary space: \(O(V)\).

Undirected edges appear twice in adjacency lists, but this changes only a constant factor.

The supplied functions explore only the starting vertex’s reachable component. To process a disconnected graph fully, start a new traversal from every still-unvisited vertex.

### Recognition clues

Use BFS for:

- Shortest paths in unweighted graphs.
- Minimum number of moves where every move costs one.
- Tree levels.
- Expanding layers.

Use DFS for:

- Reachability.
- Connected regions.
- Tree structure.
- Exploring choices.
- Dependency or cycle analyses with additional state.

### Common mistakes

- Forgetting visited information in cyclic graphs.
- Marking BFS vertices too late and enqueuing duplicates.
- Using BFS for arbitrary weighted shortest paths.
- Assuming recursive DFS is safe for arbitrarily deep inputs.

### Practice

1. Guided: What is vertex 3’s BFS distance from 0 in the example?
2. Why does vertex 4 keep distance -1?
3. Why is “first path found by DFS” not generally a shortest-path guarantee?

#### Answers and explanations

1. Two edges.

2. It is disconnected from the starting component.

3. DFS follows a branch deeply even if another unexplored branch reaches the destination in fewer edges.

