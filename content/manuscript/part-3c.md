# Part 3 continued: Chapters 3.7–3.9

## Chapter 3.7: Space complexity and peak memory

Space complexity describes how memory requirements grow with input size.

The main question is:

How much information must exist at the same time?

Time counts work over the execution. Space usually counts the peak amount of simultaneously needed storage.

### Input space, auxiliary space, and output space

These distinctions prevent ambiguous claims.

| Term | Meaning |
| --- | --- |
| Input space | Storage for the supplied input |
| Auxiliary space | Additional working storage used by the algorithm |
| Output space | Storage for the produced result |
| Total space | Input, working storage, and output under the stated convention |

In many algorithm discussions, “space complexity” means auxiliary space.

However, whether returned output is included varies. State your convention when it affects the answer.

### Constant auxiliary space

```python
# Return a scalar total.
def total(numbers):
    result = 0

    for number in numbers:
        result = result + number

    return result
```

Under the ordinary-size numeric cost model, the function stores:

- A running result.
- The current element reference.
- Fixed loop machinery.

It does not create a collection proportional to n.

Auxiliary space: O(1).

The input list still uses memory, but it already existed when the function was called.

### Linear output space

```python
# Return a new list containing doubled values.
def doubled_copy(numbers):
    result = []

    for number in numbers:
        result.append(number * 2)

    return result
```

The output list contains n values.

Therefore:

- Output storage: O(n).
- Additional working storage excluding the output: O(1).
- Extra storage including the output: O(n).

Do not give O(1) without explaining that you excluded the returned list.

### Storage depends on distinct values

```python
# Count occurrences.
def frequencies(numbers):
    counts = {}

    for number in numbers:
        counts[number] = counts.get(number, 0) + 1

    return counts
```

Let n be the number of input values and u be the number of distinct values.

The dictionary has u entries.

Its size is O(u).

Since u ≤ n, the worst-case bound is O(n).

Using u gives a more informative description.

### Peak memory is not total allocation over time

```python
# Repeatedly create a full list copy.
def repeated_copy_work(numbers):
    result = 0

    for number in numbers:
        copied = numbers.copy()
        result = result + len(copied)

    return result
```

Time: n copies. Each copy takes O(n). Total: O(n²).

Peak extra space: a constant number of full-size copies may coexist during reassignment. Earlier discarded copies do not all remain logically needed. Peak grows proportionally to n.

Therefore O(n) auxiliary space, under the usual live-working-storage analysis.

The program can perform quadratic copying work without retaining quadratic storage.

Actual process memory can also reflect Python’s allocator and runtime overhead. Algorithmic space analysis normally focuses on storage the computation needs, rather than exact operating-system measurements.

### Retaining every copy changes the answer

```python
# Keep every full copy.
def store_copies(numbers):
    copies = []

    for number in numbers:
        copies.append(numbers.copy())

    return copies
```

There are n lists, each with n element references.

Output storage: O(n²).

The difference is whether previous copies are retained.

### Nested grids

A grid with r independent rows and c values per row requires O(rc) element storage.

If both dimensions equal n: O(n²).

Do not call every grid O(n²) without defining n. If n means the total number of cells, the same grid contains O(n) cells.

### Sorting space

sorted(numbers) creates another list, so its extra space is at least linear in the number of output references.

numbers.sort() modifies the original list, but “in place” at the interface does not guarantee constant auxiliary memory internally. CPython’s sorting algorithm can use linear temporary storage.

For ordinary interview analysis:

- sorted(numbers): O(n) extra space.
- numbers.sort(): up to O(n) auxiliary space in CPython.

This is a useful reminder that mutation behavior and workspace complexity are separate properties.

### Measuring bytes is a different task

Python’s sys.getsizeof reports memory directly associated with an object. It does not automatically include all objects referenced by a container. Therefore, applying it only to an outer list does not measure the full memory of a nested structure.

Exact memory measurement is useful, but it requires care beyond counting elements.

### Fixed names can still reference growing objects

This code has one main variable:

```python
# Build an increasingly large list.
result = []

for number in range(n):
    result.append(number)
```

It uses O(n) storage.

Counting variable names is not a space analysis.

### What beginners often get wrong

“There are only three variables, so the space is constant.”

A variable can refer to a list, dictionary, string, or other structure whose size grows with the input.

### Chapter practice

1. Guided: What is the auxiliary space of a function that tracks only a maximum value and a loop index?
2. A function builds a set containing all distinct input integers. Express its space using u, then give its worst-case bound in n.
3. A function creates and discards a length-n list during each of n iterations. What are its time and peak extra-space bounds?
4. A function retains all those lists. What changes?
5. Why does returning a new list of n values require O(n) output storage?

#### Answers and explanations

1. O(1) under the ordinary-size value model.

2. O(u). Since u ≤ n, the worst case is O(n).

3. Time: O(n²). Peak extra space: O(n), assuming old lists are not retained.

4. Retaining n lists of n references requires O(n²) storage.

5. The output must hold n entries simultaneously. Even if the function uses only a few other variables, the output itself grows with n.

## Chapter 3.8: A first look at recursive complexity

Part 5 will teach recursion as a problem-solving technique. Here, we need enough of it to count work and memory.

### Recursion

Recursion occurs when a function calls itself, directly or indirectly.

A base case is a situation the function handles without another recursive call.

A recursive case reduces or transforms the problem and makes another call.

### Worked example: countdown

```python
# Count down through recursive calls.
# Input requirement: n is a nonnegative integer.
def countdown(n):
    # Stop creating calls at zero.
    if n == 0:
        return

    # Continue with a smaller value.
    countdown(n - 1)
```

For countdown(3), the calls are countdown(3), countdown(2), countdown(1), countdown(0).

There are four total calls.

The deepest moment has four active call frames.

For general n:

- Total calls: n + 1.
- Maximum simultaneous calls: n + 1.

Therefore, under the standard operation model:

- Time: O(n).
- Call-stack space: O(n).

The call-stack storage is auxiliary space.

### A recurrence

A recurrence expresses the cost of a problem in terms of the cost of smaller problems.

For countdown: T(n) = T(n − 1) + O(1).

Read it as: the work for size n is the work for size n − 1, plus a constant amount.

Expanding: T(n) = T(n − 2) + O(1) + O(1).

Continue until the base case.

There are linearly many constant contributions: T(n) = O(n).

### Halving recursion

```python
# Repeatedly halve a positive integer.
def recursive_halving(n):
    # Stop once the value is at most one.
    if n <= 1:
        return

    recursive_halving(n // 2)
```

The number of active calls is logarithmic: n, n/2, n/4, …

Time: O(log n).

Stack space: O(log n).

This assumes each call does only constant work beyond the recursive call under our numeric model.

### Two recursive branches

```python
# Explore two choices at each level.
# Input requirement: remaining is a nonnegative integer.
def explore_two_choices(remaining):
    if remaining == 0:
        return

    # Explore the first choice.
    explore_two_choices(remaining - 1)

    # Explore the second choice.
    explore_two_choices(remaining - 1)
```

For remaining = 3:

| Depth | Number of calls at that depth |
| --- | --- |
| 0 | 1 |
| 1 | 2 |
| 2 | 4 |
| 3 | 8 |

Total calls: 1 + 2 + 4 + 8 = 15.

For general n: 1 + 2 + ⋯ + 2ⁿ = 2ⁿ⁺¹ − 1.

Time: O(2ⁿ).

### But the stack is not exponential

The two recursive calls execute one after another.

Python finishes the first branch before entering the second branch.

At the deepest point, only one path is active.

Maximum call depth: n + 1.

Stack space: O(n).

This distinction is essential:

- Time depends on all calls executed.
- Stack space depends on the maximum number active together.

If the function stored every generated result, output space could be much larger. This example stores no such results.

### Balanced splitting with linear work per level

Suppose an algorithm:

- Splits a problem into two halves.
- Solves both halves.
- Performs work proportional to the current problem size to combine them.

A balanced split produces subproblems of approximately equal size.

For powers of two, the recurrence is T(n) = 2T(n/2) + O(n).

| Depth | Subproblems | Size of each | Combined nonrecursive work |
| --- | --- | --- | --- |
| 0 | 1 | n | O(n) |
| 1 | 2 | n/2 | O(n) |
| 2 | 4 | n/4 | O(n) |
| 3 | 8 | n/8 | O(n) |

There are approximately log₂ n splitting levels.

Linear work per level times logarithmically many levels gives O(n log n).

This is the counting structure behind merge sort, which we will implement in Part 5.

### Space must include local collections

A logarithmic call depth does not automatically imply logarithmic total auxiliary space.

If each active call holds a newly copied subarray, those arrays also consume memory.

You must account for:

- Call frames.
- Local collections.
- Temporaries.
- Retained output.

### Python recursion depth

Python has a recursion limit to help prevent uncontrolled stack growth. A theoretically linear recursive algorithm can still fail on a deeply nested input.

Changing the recursion limit is not a general solution to an unsuitable implementation. Often, an iterative algorithm is more appropriate.

We will revisit this when implementing graph traversal and backtracking.

### Common misconception

“Two recursive calls mean O(2ⁿ).”

Not necessarily.

Two calls on size n − 1 behave very differently from two calls on size n / 2. Count both the branching and the reduction in problem size.

### Chapter practice

1. Guided: A recursive function decreases n by one and makes one recursive call. Each call performs constant additional work. What are its time and stack-space bounds?
2. A function makes one recursive call on n // 2. What are the corresponding bounds?
3. Why does the two-choice example take exponential time but linear stack space?
4. Explain why two half-size calls plus linear combining work gives O(n log n).
5. Can call depth alone determine total memory use?

#### Answers and explanations

1. Time O(n). Stack space O(n).

2. Time O(log n). Stack space O(log n), assuming constant work and storage per call beyond the recursive call.

3. There are exponentially many calls across all branches, but only one branch is active at a time. A path contains at most linearly many calls.

4. The splitting creates logarithmically many levels. Across each level, the subproblem sizes add to n, so the combined work per level is linear.

5. No. The calls may also allocate lists, dictionaries, strings, or other structures. Their simultaneous storage must be included.

## Chapter 3.9: Using input constraints to choose an approach

A constraint is a stated limit or requirement on valid inputs.

Examples:

- 1 ≤ len(numbers) ≤ 100,000
- −1,000,000 ≤ numbers[i] ≤ 1,000,000
- The input is already sorted.
- There are at most 20 items.

Constraints provide clues about feasible algorithms.

They do not uniquely identify the solution.

### Start with the maximum input

Suppose n ≤ 100,000.

An algorithm that compares every pair of distinct positions may perform n(n − 1) / 2 comparisons.

At n = 100,000: 100,000 × 99,999 / 2 = 4,999,950,000.

That is about five billion comparisons.

A one-pass algorithm examines about one hundred thousand values.

A sorting-based algorithm has a growth scale near 100,000 log₂(100,000) ≈ 1.66 million.

These counts strongly suggest that the quadratic approach is unsuitable for an ordinary time-limited Python solution.

### A practical screening table

This is a rough guide for selecting candidates, not a guarantee of acceptance.

| Maximum size | Approaches worth investigating |
| --- | --- |
| Around 8–10 items | Enumerating permutations may be possible if per-order work is small |
| Around 20 items | Some 2ⁿ subset approaches may be possible |
| Around 100 items | Some cubic approaches may be possible |
| Around 1,000 items | Quadratic approaches are often plausible |
| Around 100,000 items | Look strongly toward O(n log n), O(n), or better |
| Around 1,000,000 items | Linear scans and careful memory use become especially important |
| Numeric range around 10⁹ | Iterating through every value is usually unsuitable; logarithmic or mathematical reasoning may help |

“May be possible” depends on:

- The time limit.
- The language.
- The cost per iteration.
- The number of test cases.
- Additional factors hidden in the bound.
- Memory requirements.

For example, n·2ⁿ can be materially more expensive than 2ⁿ.

### Why there is no universal operations-per-second rule

A Python iteration that increments an integer differs from one that:

- Creates a list.
- Hashes a long string.
- Performs a large-integer multiplication.
- Sorts a collection.
- Writes output.

A numerical operation budget can be a rough estimate, but it is not a law.

Use asymptotic analysis to reject large mismatches first. Use measurement later for close practical questions.

### Multiple input dimensions

Suppose a grid has at most 1,000 rows and at most 1,000 columns.

A full scan visits 1,000 × 1,000 = 1,000,000 cells.

Its complexity is O(rc), where r and c are the dimensions.

If the problem instead limits the total number of cells, use that total rather than multiplying unrelated maxima that cannot occur together.

### Multiple test cases

If one case takes O(n²), t cases of that size can take O(tn²).

But some problems constrain the sum of input sizes across cases.

For example: the sum of all list lengths is at most 100,000.

For a linear algorithm, total work across all cases is then linear in that combined size.

Read aggregate constraints carefully.

### Value constraints can matter

Suppose a list has 100,000 values, but each value lies between 0 and 100.

You can potentially count frequencies using 101 counters.

The key parameter is the value range size, which we can call R.

A frequency-table approach may take O(n + R) time and O(R) space.

If R = 101 is fixed, that behaves linearly in n.

If R is one billion, allocating a counter for every possible value is a different proposal.

### Numeric value is not the same as encoded input length

Suppose the input is one integer N.

An algorithm that counts from 1 through N performs O(N) iterations.

However, representing N in binary takes only about log₂ N bits.

Let b be the bit length. Then N can be roughly 2ᵇ.

So work that is linear in the numeric value can be exponential in the number of bits used to write the input.

This distinction becomes important in algorithms whose running time depends on a target sum or capacity.

### Pseudopolynomial time

An algorithm is called pseudopolynomial when its time is polynomial in numeric input values but not necessarily polynomial in their encoded bit lengths.

You will encounter this term when studying dynamic programming problems such as knapsack.

For now, remember:

Always state whether a variable means the number of elements, a numeric target, a value range, or the number of bits.

### Memory constraints also reject approaches

A grid with 10,000 × 10,000 cells contains 100,000,000 cells.

Even before considering Python object overhead, that is an enormous number of entries.

A time-efficient algorithm can still fail because it stores too much.

### Common misconception

“The constraints say n ≤ 100,000, so the solution must be O(n log n).”

The limit is a clue. It does not prove the intended bound or identify the technique. A linear solution may exist, or another parameter may dominate.

### Chapter practice

1. Guided: Roughly how many ordered-pair checks does an n² algorithm make when n = 100,000?
2. Why might an exponential approach be plausible for 18 items but unsuitable for 100 items?
3. A grid has r rows and c columns. State the complexity of visiting each cell once.
4. A function loops from 1 through a numeric input N. Is its work linear in N or necessarily linear in the number of digits used to write N?
5. A problem has 100 cases, each of size 1,000. What is the growth expression for an O(n²) algorithm across the cases?

#### Answers and explanations

1. 100,000² = 10,000,000,000. Ten billion checks.

2. 2¹⁸ = 262,144, while 2¹⁰⁰ ≈ 1.27 × 10³⁰. The second is vastly larger. Per-combination work still matters for the smaller case.

3. O(rc).

4. It is linear in the numeric value N. It is not necessarily linear in the number of digits or bits representing N.

5. O(tn²). For the stated sizes, the basic quadratic quantity across all cases is 100 × 1,000² = 100,000,000, before accounting for the work inside each iteration.
