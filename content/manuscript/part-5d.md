## Chapter 5.14: Bit manipulation

### Intuition: an integer can represent a row of on/off choices

Binary digits are bits.

For example:

13 = 8 + 4 + 1

Its binary representation is:

1101

Bit positions count from zero at the right:

| Position | Value represented |
| --- | --- |
| 0 | 1 |
| 1 | 2 |
| 2 | 4 |
| 3 | 8 |

### Core operators

The source table’s bitwise OR row was swallowed by the `|` character. It is restored here. The truth table below still includes OR.

| Python operator | Meaning |
| --- | --- |
| `&` | Bitwise AND |
| `\|` | Bitwise OR |
| `^` | Bitwise XOR |
| `~` | Bitwise complement |
| `<<` | Shift left |
| `>>` | Shift right |

For one bit:

| First | Second | AND | OR | XOR |
| --- | --- | --- | --- | --- |
| 0 | 0 | 0 | 0 | 0 |
| 0 | 1 | 0 | 1 | 1 |
| 1 | 0 | 0 | 1 | 1 |
| 1 | 1 | 1 | 1 | 0 |

XOR means exclusive OR: the result is one when the bits differ.

### Masks

A bit mask is an integer whose bits identify positions of interest.

To refer to bit k:

`mask = 1 << k`

For k = 3, the mask is binary 1000.

Common operations:

```python
# Read whether bit k is set.
is_set = (number & (1 << k)) != 0
# Set bit k.
number = number | (1 << k)
# Clear bit k.
number = number & ~(1 << k)
# Toggle bit k.
number = number ^ (1 << k)
```

### Worked pattern: remove the lowest set bit

For a positive integer:

`number & (number - 1)`

clears its lowest set bit.

Why?

Subtracting one:

- Changes the lowest set bit from 1 to 0.
- Changes lower zeros into ones.
- Leaves higher bits unchanged.

AND with the original removes that lowest set bit.

### Trace: count set bits in 13

| Number | Binary | After n & (n - 1) |
| --- | --- | --- |
| 13 | 1101 | 12 |
| 12 | 1100 | 8 |
| 8 | 1000 | 0 |

Three set bits.

```python
def count_set_bits(number):
    if number < 0:
        raise ValueError("Require a nonnegative integer")
    count = 0
    while number:
        number = number & (number - 1)
        count += 1
    return count
```

If k bits are set, the loop performs k iterations.

Under a fixed-width word model, this is \(O(k)\) time and \(O(1)\) extra words. For arbitrarily large Python integers, each bit operation can itself depend on bit length.

### Worked pattern: paired values cancel under XOR

Useful identities:

\[
x\oplus x=0
\]

\[
x\oplus0=x
\]

XOR is associative and commutative, so order does not affect the result.

If every integer appears exactly twice except one:

```python
def single_unpaired(numbers):
    answer = 0
    for number in numbers:
        answer ^= number
    return answer
```

For [4,1,2,1,2], paired 1s and 2s cancel, leaving 4.

Time: \(O(n)\) fixed-width operations. Extra space: \(O(1)\) words.

### Python complement caution

Python integers do not automatically wrap to a fixed number of bits.

For example:

`~5 == -6`

If a problem asks for an 8-bit complement, explicitly constrain the width:

`eight_bit_complement = (~number) & 255`

Here, 255 has eight low bits set.

### Recognition clues

Look for:

- A small fixed set of yes/no states.
- Subset encoding.
- Parity or paired cancellation.
- Powers of two.
- Bit-count or bit-position questions.

### Common mistakes

- Confusing and with &.
- Confusing exponentiation ** with XOR ^.
- Applying the paired-XOR trick when frequencies do not satisfy its contract.
- Ignoring fixed-width versus Python integer behavior.

### Practice

1. Guided: What is 1 << 4?
2. What is 6 ^ 6 ^ 9?
3. How many set bits are in binary 10110?

#### Answers and explanations

1. 16

2. 9, because the two 6s cancel.

3. Three.


## Chapter 5.15: Monotonic stacks

A monotonic stack maintains values in a consistently increasing or decreasing order.

The stack often stores unresolved candidates.

### Worked problem

For every value, find the first strictly greater value to its right.

If none exists, return None for that position.

Input:

`[2,1,2,4,3]`

Answer:

`[4,2,4,None,None]`

### Intuition: keep questions waiting until a value answers them

When reading a new value, it can answer earlier smaller values that have not yet found a greater value.

Store their indices on a stack.

The unresolved values will be nonincreasing from bottom to top.

### Trace

| Current value | Indices resolved | Pending indices afterward |
| --- | --- | --- |
| 2 at index 0 | None | [0] |
| 1 at index 1 | None | [0,1] |
| 2 at index 2 | Index 1 gets answer 2 | [0,2] |
| 4 at index 3 | Indices 2 and 0 get answer 4 | [3] |
| 3 at index 4 | None | [3,4] |

```python
def next_greater_values(numbers):
    answer = [None] * len(numbers)
    pending = []
    for index in range(len(numbers)):
        while pending and numbers[index] > numbers[pending[-1]]:
            previous = pending.pop()
            answer[previous] = numbers[index]
        pending.append(index)
    return answer
```

### Why is it the first greater value?

A pending index has survived all values between its position and the current position.

None of those earlier scanned values resolved it.

The current value is the first encountered value that is greater.

### Why indices instead of only values?

You must know which answer position to fill.

Repeated values can occur at different positions, so the value alone does not identify the destination.

### Complexity

Every index is:

- Pushed once.
- Popped at most once.

Total time: \(O(n)\).

Auxiliary stack and output: \(O(n)\).

A single iteration may pop many items, but the total number of pops remains linear.

### Recognition clues

Look for:

- Next greater or smaller value.
- Previous greater or smaller value.
- Nearest boundary that defeats a candidate.
- Histogram or temperature-style problems.

### Common mistakes

- Using >= when the problem asks for strictly greater.
- Forgetting unresolved items at the end.
- Storing values when output requires positions or distances.
- Calling the nested loop quadratic without counting total pops.

### Practice

1. Guided: Find next-greater values for [3,1,2].
2. What should [2,2] return under the strictly-greater rule?
3. How would you return distances to the next greater value instead?

#### Answers and explanations

1. [None, 2, None]

2. [None, None]. Equal values do not qualify.

3. When resolving previous at current index, store: answer[previous] = index - previous. Choose the missing-answer marker required by the problem.


## Chapter 5.16: Dynamic programming foundations

### Intuition: solve a subproblem once, then reuse its answer

Suppose a recursive solution repeatedly asks the same question.

If the inputs to that question are identical, the answer is identical.

Instead of recomputing it, store the result.

Dynamic programming, abbreviated DP, organizes a problem into reusable subproblems and computes each needed answer without repeating all the underlying work.

The phrase “dynamic programming” does not mean the program changes its own source code.

### Two important properties

Overlapping subproblems: different branches ask for the same smaller answers.

Optimal substructure: an optimal answer can be constructed from appropriately chosen optimal subproblem answers.

For counting and feasibility problems, we similarly need a correct way to combine smaller answers, even when “optimal” is not the objective.

### Worked problem: climbing stairs

You can climb one or two steps at a time.

How many different ordered step sequences reach exactly n steps?

For n = 3:

1 + 1 + 1

1 + 2

2 + 1

Answer: 3.

Order matters.

### Define a state

A state is the information that identifies a subproblem.

Let:

\[
ways(n)=\text{number of step sequences reaching exactly }n
\]

Consider the final move.

It is either:

- One step, following a sequence reaching n - 1.
- Two steps, following a sequence reaching n - 2.

These groups do not overlap because their final moves differ.

Therefore:

\[
ways(n)=ways(n-1)+ways(n-2)
\]

A transition is the rule deriving one state’s answer from other states.

### Base cases

\[
ways(0)=1
\]

There is one way to make zero progress: take no steps.

\[
ways(1)=1
\]

There is one sequence: [1].

The empty sequence counting as one is crucial when it serves as the completed remainder of a larger sequence.

### Naive recursion

```python
def stairs_recursive(n):
    # Contract: n is a nonnegative integer.
    if n <= 1:
        return 1
    return stairs_recursive(n - 1) + stairs_recursive(n - 2)
```

### Where repeated work appears

Computing ways(5) asks for ways(4) and ways(3).

Computing ways(4) asks for ways(3) again.

The same state is being solved repeatedly.

| State | Answer |
| --- | --- |
| 0 | 1 |
| 1 | 1 |
| 2 | 2 |
| 3 | 3 |
| 4 | 5 |
| 5 | 8 |

### Complexity of naive recursion

The branching recursion has exponential growth.

A valid upper bound is \(O(2^n)\) time.

Maximum call depth is \(O(n)\).

The exact growth is smaller than \(2^n\), but the exponential classification is enough to identify repeated computation as the central problem.

### How to begin a DP solution

Write these before code:

1. What does one state mean?
2. Which smaller states determine it?
3. What are the smallest valid answers?
4. Why does the transition cover all possibilities?
5. Does it count any possibility more than once?
6. In what order can states be evaluated?

MIT’s introductory algorithms materials organize dynamic programming around subproblems, memoization, and applications such as knapsack and sequence problems. MIT OpenCourseWare

### Recognition clues

Consider DP when:

- You seek a count, minimum, maximum, or feasibility answer.
- Choices lead to repeated smaller questions.
- A state can summarize the past information relevant to the future.
- Brute-force recursion repeats substantial work.

### Common misconception

“DP means create a table.”

The table stores answers. The central work is defining what those answers mean and how they depend on one another.

### Practice

1. Guided: List all ways to climb two steps.
2. Why is ways(0) one rather than zero?
3. If moves of size 3 are also allowed, what new term appears in the transition?

#### Answers and explanations

1. 1 + 1, and 2.

2. There is one empty sequence. When a chosen move finishes the climb exactly, its remaining subproblem must contribute one completed possibility.

3. Add ways(n - 3), with appropriate base or out-of-range handling.


## Chapter 5.17: Memoization and tabulation

These are two ways to evaluate the same dependency structure.

### Memoization: start with the requested problem

Memoization stores a function’s result for a state and reuses it when that state appears again.

This is often called top-down DP.

### Trace for ways(5)

A depth-first evaluation computes smaller states first as needed:

| State completed | Calculation | Stored answer |
| --- | --- | --- |
| 2 | ways(1) + ways(0) | 2 |
| 3 | ways(2) + ways(1) | 3 |
| 4 | ways(3) + ways(2) | 5 |
| 5 | ways(4) + ways(3) | 8 |

When ways(3) is requested again, its stored answer is returned.

```python
def stairs_memo(n):
    # Store the known base answers.
    memo = {0: 1, 1: 1}

    def solve(remaining):
        if remaining not in memo:
            memo[remaining] = (
                solve(remaining - 1) + solve(remaining - 2)
            )
        return memo[remaining]

    return solve(n)
```

### Complexity

There are n + 1 possible states.

Each non-base state performs constant work beyond its dependencies.

- Time: \(O(n)\) under the arithmetic and average dictionary model.
- Memo storage: \(O(n)\).
- Recursive stack: \(O(n)\).
- Total auxiliary space: \(O(n)\).

### Tabulation: build from the smallest states

Tabulation fills answers in an order where dependencies are already available.

This is often called bottom-up DP.

```python
def stairs_table(n):
    dp = [0] * (n + 1)
    # One empty sequence reaches zero steps.
    dp[0] = 1
    for step in range(1, n + 1):
        # Sequences whose final move is one step.
        dp[step] = dp[step - 1]
        if step >= 2:
            # Sequences whose final move is two steps.
            dp[step] += dp[step - 2]
    return dp[n]
```

For n = 5:

`dp = [1, 1, 2, 3, 5, 8]`

### Complexity

- Time: \(O(n)\).
- Table space: \(O(n)\).
- No recursive call stack.

### Comparison

| Question | Memoization | Tabulation |
| --- | --- | --- |
| Starting point | Requested state | Base states |
| Evaluation | Recursive, as needed | Explicit dependency order |
| Computes unreachable states? | Often avoids them | May compute them |
| Recursion depth concern | Yes | Usually no |
| Natural fit | Recursive formulation | Regular state table |

Neither is universally superior.

### Cache keys must contain the full state

Suppose the answer depends on both:

- Which items remain.
- How much capacity remains.

Caching only capacity would mix different subproblems.

The stored key must identify all information that affects the answer.

### Counting can create large integers

The number of stair sequences grows rapidly.

The \(O(n)\) time claim counts additions as basic operations. Exact Python integers eventually require multiple machine words, so a bit-level analysis would account for increasing integer size.

### Recognition clues

Use memoization when the recursive state is easy to express.

Use tabulation when dependency order is clear and avoiding recursion is useful.

### Common mistakes

- Creating a new memo dictionary during every recursive call.
- Caching under an incomplete key.
- Returning before storing the result.
- Filling a table before its dependencies are available.

### Practice

1. Guided: What does stairs_table(4) return?
2. Does memoization change the recurrence?
3. Why does bottom-up stair counting proceed from smaller indices to larger ones?

#### Answers and explanations

1. 5

2. No. It changes how results are reused, not the mathematical definition of the answer.

3. State i depends on i - 1 and i - 2, so those values must be ready first.

