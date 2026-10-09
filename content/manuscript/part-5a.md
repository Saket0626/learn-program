# Part 5: Core Algorithms and Patterns

Parts 1–4 established the language, execution model, complexity analysis, and data structures. This part teaches how to organize those tools into solutions.

An algorithmic pattern is a reusable way of organizing a solution. Examples include moving two positions through a sequence, maintaining information about a changing window, or remembering answers to repeated subproblems.

Recognizing a pattern is only the beginning. You must also establish:

1. Why its assumptions hold.
2. What each variable means.
3. Why each update is correct.
4. Why the algorithm eventually finishes.
5. What work and memory it requires.

This part follows the planned 21-chapter sequence. Dynamic programming receives six chapters.

Tested code companion: `part5_algorithms.py`

I executed the companion’s examples and 16,810 additional checks, including exhaustive small inputs and seeded randomized comparisons with reference solutions. Testing provides evidence of correctness. The explanations below establish why the algorithms work.

Unless stated otherwise, complexity uses the ordinary-size arithmetic model from Part 3. Python can represent larger integers, but operations on very large values require additional bit-level work.

## Chapter 5.1: Recursion

### Intuition: delegate a smaller version of the same job

Suppose you need to add:

3 + 1 + 4

You can separate the work into:

3 + the sum of [1, 4]

Then:

1 + the sum of [4]

Then:

4 + the sum of []

The empty list contributes zero.

This is recursion: solving a problem using the answer to a smaller problem of the same kind.

### Three required ingredients

A recursive function needs:

- A contract describing what one call returns.
- A base case handled without another recursive call.
- A progress rule that moves recursive calls toward a base case.

For summing a suffix:

`recursive_sum(numbers, index)` returns the sum of the elements from index through the end.

A suffix is the portion of a sequence beginning at some position and continuing to the end.

### Worked trace before code

Input:

`numbers = [3, 1, 4]`

Calls move downward:

| Call | Work waiting for the smaller call |
| --- | --- |
| sum from index 0 | 3 + answer from index 1 |
| sum from index 1 | 1 + answer from index 2 |
| sum from index 2 | 4 + answer from index 3 |
| sum from index 3 | Return 0 |

Returns move upward:

| Returning call | Calculation | Returned value |
| --- | --- | --- |
| Index 3 | Empty suffix | 0 |
| Index 2 | 4 + 0 | 4 |
| Index 1 | 1 + 4 | 5 |
| Index 0 | 3 + 5 | 8 |

The caller waits while the smaller call runs. It then resumes with the returned value.

### Implementation

```python
def recursive_sum(numbers, index=0):
    # The empty suffix contributes zero.
    if index == len(numbers):
        return 0
    # Add the current value to the sum of the remaining suffix.
    return numbers[index] + recursive_sum(numbers, index + 1)


assert recursive_sum([3, 1, 4]) == 8
assert recursive_sum([]) == 0
```

### Why this works

Assume the smaller call correctly returns the sum after the current position.

Adding the current element then gives the sum beginning at the current position.

At the end, the empty suffix contributes zero, so the chain has a valid stopping point.

This style of reasoning is closely related to mathematical induction, a method that proves a base case and then proves how a smaller valid case supports a larger one.

### Why use an index instead of slicing?

This version passes the original list and changes only an index.

Writing:

`recursive_sum(numbers[1:])`

would create a new slice at every level.

Those copies can add:

\[
n+(n-1)+\cdots+1=O(n^2)
\]

work.

The index-based version avoids that repeated copying.

### Complexity

For n elements:

- One call per element, plus the base call.
- Constant work per call under the numeric model.
- Time: \(O(n)\).
- Maximum active calls: \(O(n)\).
- Auxiliary stack space: \(O(n)\).

An iterative sum can use \(O(1)\) auxiliary space. Recursion is useful when the problem’s structure benefits from it, not automatically for every loop.

### Recognition clues

Consider recursion when:

- A structure contains smaller structures of the same kind.
- A tree problem depends on child-subtree answers.
- A problem branches into choices.
- A problem splits into smaller independent regions.

### Common mistakes

- No base case.
- A recursive call that does not make progress.
- Forgetting to return the recursive result.
- Assuming local variables are shared across all calls.
- Ignoring Python’s recursion-depth limit.

### Practice

1. Guided: Trace recursive_sum([2, 5]).
2. What happens if the recursive call uses index instead of index + 1?
3. How would you define a recursive product of a list? What should the empty product be?

#### Answers and explanations

1. The base returns 0. Then: 5 + 0 = 5, and 2 + 5 = 7.

2. The problem does not get smaller. For nonempty input, the calls continue until Python raises a recursion-depth error.

3. The current value multiplies the product of the remaining suffix. The empty product is 1, because multiplying by one preserves the accumulated product. Using zero would make every result zero.


## Chapter 5.2: Sorting

### Intuition: establish an order that makes later work easier

An unsorted collection gives little information about where a value might be.

After sorting:

- Equal values become adjacent.
- Smaller and larger values occupy predictable regions.
- Two-pointer scans become possible.
- Binary search becomes possible.

Sorting can be part of a solution even when the final output is not itself a sorted list.

We will study two algorithms with different educational purposes.

### Insertion sort: maintain a sorted prefix

Imagine organizing cards in your hand.

Each new card is inserted into its correct position among the cards already organized.

The invariant is:

Before processing position index, the positions before it are sorted.

### Trace

Input:

`[4, 1, 3, 2]`

| Current value | Action | Array afterward |
| --- | --- | --- |
| 1 | Shift 4 right, insert 1 | [1, 4, 3, 2] |
| 3 | Shift 4 right, insert 3 | [1, 3, 4, 2] |
| 2 | Shift 4 and 3 right, insert 2 | [1, 2, 3, 4] |

```python
def insertion_sort(numbers):
    # Preserve the caller's list.
    result = numbers.copy()
    for index in range(1, len(result)):
        # Save the value before shifting over its original position.
        current = result[index]
        position = index - 1
        # Shift larger values one position to the right.
        while position >= 0 and result[position] > current:
            result[position + 1] = result[position]
            position -= 1
        # Insert into the gap.
        result[position + 1] = current
    return result
```

### Costs

- Already sorted input: \(O(n)\) time.
- Reverse-sorted input: \(O(n^2)\) time.
- This version copies the input, so auxiliary space is \(O(n)\).
- The shifting process itself needs only constant additional workspace.

### Merge sort: split, solve, combine

A divide-and-conquer algorithm:

1. Divides a problem into smaller problems.
2. Solves those problems.
3. Combines their answers.

Merge sort divides a list into halves, sorts each half, then merges the two sorted results.

### Trace

Start:

`[4, 1, 3, 2]`

The two halves eventually become:

left = [1, 4]

right = [2, 3]

Merge them:

| Left candidate | Right candidate | Chosen value | Result |
| --- | --- | --- | --- |
| 1 | 2 | 1 | [1] |
| 4 | 2 | 2 | [1, 2] |
| 4 | 3 | 3 | [1, 2, 3] |
| 4 | No remaining right value | 4 | [1, 2, 3, 4] |

### Why can you choose the smaller front value?

Because each half is sorted. Nothing behind that half’s front can be smaller than its front.

```python
def merge_sort(numbers):
    # Empty and one-element lists are already sorted.
    if len(numbers) <= 1:
        return numbers.copy()
    middle = len(numbers) // 2
    # Sort the two halves.
    left = merge_sort(numbers[:middle])
    right = merge_sort(numbers[middle:])
    result = []
    i = 0
    j = 0
    # Repeatedly take the smaller unused front value.
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1
    # At most one side still has unused elements.
    result.extend(left[i:])
    result.extend(right[j:])
    return result
```

### Stability

A sorting algorithm is stable if equal-key records preserve their original relative order.

Choosing the left element on equality helps preserve stability during merging.

For ordinary integers, equal values look identical. Stability matters more when sorting records by one field.

### Complexity

At each splitting level, merging handles a total of \(O(n)\) elements.

There are \(O(\log n)\) levels.

Therefore:

\[
O(n\log n)
\]

time.

This slicing-based implementation uses \(O(n)\) peak auxiliary storage, including copied lists and merge results, plus a logarithmic-depth call stack. The combined bound remains \(O(n)\).

### Practical Python

Use `sorted(values)` or `values.sort()` in ordinary solutions unless the problem requires implementing sorting.

Knowing the algorithms helps you reason about behavior and complexity. It does not mean you should rewrite sorting every time.

### Recognition clues

Sorting is promising when:

- Equal values should become neighbors.
- You need to process events by position or time.
- You need to compare extremes.
- An unordered problem becomes easier after imposing order.

### Common mistakes

- Sorting when original positions are required, then losing those positions.
- Forgetting whether the chosen operation mutates the input.
- Assuming sorting is free because it is one line.
- Using insertion sort for large arbitrary inputs.

### Practice

1. Guided: Perform insertion sort’s first insertion on [3, 1, 2].
2. Merge [1, 5] and [2, 4, 6].
3. Why does insertion sort shift values from right to left?

#### Answers and explanations

1. Insert 1 into the sorted prefix [3]. Result: [1, 3, 2].

2. Choose 1, 2, 4, 5, then 6. Result: [1, 2, 4, 5, 6].

3. Moving rightmost values first avoids overwriting a value before it has been moved.


## Chapter 5.3: Binary search

### Intuition: discard a region that cannot contain the answer

Suppose a sorted list’s middle value is 20.

If you seek 30, everything at or before that middle position is too small.

You can discard half the remaining positions with one comparison.

Binary search requires an ordering property that justifies the discarded region.

### Exact search contract

Input: a list sorted in nondecreasing order.

Output: an index containing the target, or -1 if absent.

If duplicates exist, this version may return any matching index.

### Trace

Search for 9 in:

`[2, 4, 7, 9, 12]`

| left | right | middle | Middle value | Action |
| --- | --- | --- | --- | --- |
| 0 | 4 | 2 | 7 | Discard indices 0–2 |
| 3 | 4 | 3 | 9 | Return 3 |

```python
def binary_search(numbers, target):
    # Candidate indices form a closed interval [left, right].
    left = 0
    right = len(numbers) - 1
    while left <= right:
        middle = left + (right - left) // 2
        if numbers[middle] == target:
            return middle
        if numbers[middle] < target:
            # The middle and everything before it are too small.
            left = middle + 1
        else:
            # The middle and everything after it are too large.
            right = middle - 1
    return -1
```

### Invariant

If the target exists in the remaining search, it lies between left and right, inclusive.

Each unsuccessful iteration removes middle and at least part of the interval.

### Boundary search: first value at least the target

Many problems need a boundary rather than an arbitrary exact match.

A lower bound here is the first position whose value is at least the target.

If no such value exists, return the list length.

```python
def lower_bound(numbers, target):
    # Search for a boundary in the half-open interval [left, right).
    left = 0
    right = len(numbers)
    while left < right:
        middle = (left + right) // 2
        if numbers[middle] < target:
            left = middle + 1
        else:
            # Middle might be the first qualifying position.
            right = middle
    return left
```

For [1, 2, 2, 5] and target 2:

| left | right | middle | Value | Update |
| --- | --- | --- | --- | --- |
| 0 | 4 | 2 | 2 | right = 2 |
| 0 | 2 | 1 | 2 | right = 1 |
| 0 | 1 | 0 | 1 | left = 1 |

Return 1.

Python’s `bisect_left` provides this insertion-boundary behavior. Finding the boundary is logarithmic, but inserting into a Python list afterward can still require linear shifting. Python 3.14.8 documentation

### Complexity

- Time: \(O(\log n)\).
- Auxiliary space: \(O(1)\).

### Recognition clues

Look for:

- Sorted input.
- A first or last qualifying position.
- A condition that changes once across an ordered domain.
- A numeric answer whose feasibility can be checked.

The last case returns in Chapter 5.13.

### Common mistakes

- Mixing closed and half-open interval rules.
- Updating left = middle when this may repeat the same interval.
- Discarding middle when it might still be the boundary.
- Applying binary search without a monotonic condition.

### Practice

1. Guided: What does lower_bound([1, 3, 3, 7], 3) return?
2. What does it return for target 8?
3. How would you change the condition to find the first value strictly greater than the target?

#### Answers and explanations

1. Index 1.

2. Index 4, the length of the list.

3. Discard values less than or equal to the target:

```python
if numbers[middle] <= target:
    left = middle + 1
else:
    right = middle
```

This is an upper-bound search.


## Chapter 5.4: Two pointers

A pointer in this context is an index or reference tracking a position. It does not mean you are manually manipulating machine addresses.

The two-pointer pattern coordinates two positions so each movement eliminates work or maintains an invariant.

### Opposite ends: pair sum in sorted input

Problem:

Find two distinct positions whose values sum to a target.

Assume the list is sorted.

Start with:

- left at the smallest value.
- right at the largest value.

If the sum is too small, move left.

If it is too large, move right.

### Why those moves are safe

Suppose:

`numbers[left] + numbers[right] < target`

`numbers[right]` is the largest remaining partner.

Even that partner is insufficient for `numbers[left]`.

Therefore, `numbers[left]` cannot participate in a valid remaining pair. Discard it.

The too-large case is symmetric: the smallest available partner is already too large when paired with `numbers[right]`.

### Trace

Input:

`[1, 2, 4, 7, 11]`, target = 9

| Left value | Right value | Sum | Action |
| --- | --- | --- | --- |
| 1 | 11 | 12 | Move right leftward |
| 1 | 7 | 8 | Move left rightward |
| 2 | 7 | 9 | Return positions |

```python
def sorted_pair_sum(numbers, target):
    left = 0
    right = len(numbers) - 1
    while left < right:
        total = numbers[left] + numbers[right]
        if total == target:
            return left, right
        if total < target:
            left += 1
        else:
            right -= 1
    return None
```

### Complexity

Each iteration moves at least one pointer inward.

- Time: \(O(n)\).
- Auxiliary space: \(O(1)\).

If you sort first, include the sorting cost and preserve original indices if the problem requires them.

### Same direction: read and write positions

Another two-pointer arrangement separates:

- Where you read input.
- Where you write accepted output.

Example: move zeros to the end while preserving nonzero order.

```python
def move_zeros(numbers):
    write = 0
    for read in range(len(numbers)):
        if numbers[read] != 0:
            # Write the next retained value.
            numbers[write] = numbers[read]
            write += 1
    # Fill the unused suffix with zeros.
    for index in range(write, len(numbers)):
        numbers[index] = 0
```

For:

`[0, 1, 0, 3, 12]`

the nonzero values are written as:

1, 3, 12

Then the remaining two positions become zero.

Time is \(O(n)\), with \(O(1)\) auxiliary space.

### Recognition clues

Look for:

- Sorted pairs or comparisons between extremes.
- In-place filtering or compaction.
- Comparing two sequences from their ends.
- Positions that can move only forward or inward.

### Common misconception

Two pointers are not justified merely because a problem involves two values.

You need a reason that moving a pointer cannot discard a needed answer.

### Practice

1. Guided: Find a target-10 pair in [1, 3, 4, 6, 8].
2. Why must the pair-search loop use left < right?
3. What should move_zeros([0, 0, 5, 0, 2]) produce?

#### Answers and explanations

1. 1 + 8 = 9, move left. 3 + 8 = 11, move right. 3 + 6 = 9, move left. 4 + 6 = 10. Return positions (2, 3).

2. The problem requires two distinct positions. Equality would use one element twice.

3. [5, 2, 0, 0, 0].

