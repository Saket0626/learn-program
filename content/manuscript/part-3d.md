# Part 3 continued: Chapters 3.10–3.11, glossary, and readiness

## Chapter 3.10: Complete comparison of three correct approaches

We will analyze three solutions to the same problem.

### Problem

Given a list of integers, determine whether any value appears at least twice.

Return True if a duplicate exists. Return False otherwise.

Assume the input must remain unchanged.

### Approach A: compare every pair

This is a brute-force approach: a direct method that checks all relevant possibilities without using a more selective structure.

```python
# Check every pair of distinct positions.
def has_duplicate_pairs(numbers):
    n = len(numbers)

    for first in range(n):
        for second in range(first + 1, n):
            if numbers[first] == numbers[second]:
                return True

    return False
```

Trace on [4, 1, 4]:

| first | second | Values compared | Equal? |
| --- | --- | --- | --- |
| 0 | 1 | 4 and 1 | No |
| 0 | 2 | 4 and 4 | Yes |

The function returns True.

Worst-case time: if every value is distinct, the function checks n(n − 1) / 2 pairs. Therefore O(n²).

Best-case time: for inputs of length at least two, the first pair might match. Then it returns after one comparison: O(1).

Auxiliary space: only a fixed number of variables are used: O(1).

Why improve it? When processing a value, the algorithm repeatedly asks about its relationship with many other values. A better organization of the values can reduce those repeated comparisons.

### Approach B: sort a copy, then check neighbors

Key observation: if equal values are sorted together, any duplicate creates an equal neighboring pair.

For example:

```
Original: [4, 1, 4, 2]
Sorted:   [1, 2, 4, 4]
```

We no longer need to compare every possible pair.

```python
# Sort a copy so the original input remains unchanged.
def has_duplicate_sorted(numbers):
    ordered = sorted(numbers)

    # Equal values must be adjacent somewhere in sorted order.
    for index in range(1, len(ordered)):
        if ordered[index] == ordered[index - 1]:
            return True

    return False
```

Trace on [4, 1, 4]. Sorted copy: [1, 4, 4].

| Index | Previous value | Current value | Equal? |
| --- | --- | --- | --- |
| 1 | 1 | 4 | No |
| 2 | 4 | 4 | Yes |

Time: sorting O(n log n), scanning O(n). Combined worst-case time O(n log n + n) = O(n log n).

Space: the copied list and sorting workspace require O(n) extra space.

Tradeoff compared with pair checking:

- Better worst-case growth.
- More memory.
- Still correct without relying on average-case hash lookup.

The scan’s early return does not eliminate the preceding sort.

### Approach C: remember values in a set

Key observation: when a value appears, ask whether it appeared earlier.

We do not need its position or frequency. We need membership information.

```python
# Remember values encountered earlier.
def has_duplicate_set(numbers):
    seen = set()

    for number in numbers:
        # A previous occurrence establishes a duplicate.
        if number in seen:
            return True

        # Record this value for later checks.
        seen.add(number)

    return False
```

Trace on [4, 1, 4]:

| Current value | Already present? | Action | Set contents afterward |
| --- | --- | --- | --- |
| 4 | No | Add 4 | {4} |
| 1 | No | Add 1 | {1, 4} |
| 4 | Yes | Return True | No further change |

Time: under average-case constant-time hashing for ordinary integer keys, at most n membership checks and at most n insertions. Average time O(n).

The theoretical hash-table worst case can be O(n²) across the full sequence.

That does not invalidate the standard average-case analysis. It tells us what assumption supports it.

Space: at most n distinct values are stored: O(n).

### Comparison

| Approach | Time | Extra space | Preserves input? |
| --- | --- | --- | --- |
| Compare pairs | O(n²) worst case | O(1) | Yes |
| Sort a copy | O(n log n) worst case | O(n) | Yes |
| Track a set | O(n) average case | O(n) | Yes |

### How a beginner can discover the improvement

Start by identifying the repeated question: Have I already encountered this value?

Then ask what information would answer it directly.

- A list of previous values still requires a scan.
- A set is designed for membership queries.
- Sorting is another way to make equal values easier to locate.

The improvement comes from changing how information is organized, not from shortening variable names or combining lines.

### Checks for all three functions

```python
# Use cases with and without duplicates.
cases = [
    ([], False),
    ([5], False),
    ([1, 2, 3], False),
    ([1, 1], True),
    ([4, 1, 4], True),
    ([-2, 0, -2], True),
]

for numbers, expected in cases:
    before = numbers.copy()

    assert has_duplicate_pairs(numbers) == expected
    assert has_duplicate_sorted(numbers) == expected
    assert has_duplicate_set(numbers) == expected

    # None of the three implementations should mutate the input.
    assert numbers == before

print("Duplicate checks passed")
```

### Chapter practice

1. Guided: Why is the pair-checking approach quadratic even though it avoids reversed pairs?
2. Why does the sorting approach need only neighboring comparisons?
3. If the input is already sorted, what time and extra space does a neighboring scan require?
4. If you store previously seen values in a list instead of a set, what is the worst-case time?
5. Explain the assumptions behind the set approach’s linear-time claim.

#### Answers and explanations

1. The pair count is n(n − 1) / 2. Dropping a constant factor does not remove the quadratic dominant term.

2. All equal values occur together in sorted order. If a value appears more than once, at least two occurrences are adjacent.

3. Time O(n). Extra space O(1). No sorting copy is needed.

4. O(n²). Each membership query can scan all earlier values. The scan lengths can grow as 0 + 1 + 2 + ⋯ + (n − 1).

5. It assumes ordinary-size keys and average-case efficient hash-table operations. Large key-processing costs or pathological collisions can change the detailed analysis.

## Chapter 3.11: A repeatable complexity-analysis procedure

You now have enough tools to analyze small programs systematically.

### Step 1: define the size variables

Write n = number of input elements, or:

- n = length of the first string
- m = length of the second string

Do not reuse n for several unrelated quantities.

### Step 2: state the case and assumptions

Examples:

- Worst-case time, ordinary-size integer operations.
- Average-case time, assuming efficient hash-table operations.
- Auxiliary space excludes the returned output.

These statements prevent accidental overclaiming.

### Step 3: identify the repeated work

Look for loops, function calls inside loops, recursion, sorting, membership checks, slices and copies, string construction, and large outputs.

### Step 4: count total executions

For each important operation, ask:

- How many times can it run?
- Does its cost change as the input grows?
- Is a variable reset or shared across iterations?
- Does an early return remove all large cases or only some?

### Step 5: combine costs

- Sequential phases usually add.
- Independent full nested repetitions multiply.
- Dependent bounds require a sum.
- Recursive calls require counting the resulting subproblems.

### Step 6: simplify

Remove constant multipliers and lower-order terms when reporting the growth class.

Preserve independent parameters unless a relationship is stated.

For example, O(n + m) does not generally become O(n).

### Step 7: count simultaneous storage

Include created collections, copied slices, temporary buffers, active recursive frames, stored intermediate answers, and output, with your convention stated.

### Step 8: compare against constraints

Use the largest allowed input to evaluate the scale of the work and storage.

### Step 9: check whether the algorithm can do less work

Ask:

- Am I recomputing an unchanged value?
- Can I store a previous result?
- Can I use a structure with a better operation cost?
- Can I exploit sorting, a limited value range, or another input property?
- Is the requested output itself already large?

### Output size creates a lower bound

If a problem asks you to return n separate elements, explicitly constructing that output requires at least linear work and storage for those elements.

If it asks for every pair, the output itself may contain quadratic many entries.

If it asks for every permutation as a full length-n sequence, the output contains n × n! element positions.

No algorithm can explicitly write that entire output in constant time.

An output-sensitive analysis includes the size of the produced output in the complexity description.

### Numeric-size caveat

Python integers can grow beyond ordinary machine-sized values.

For a b-bit integer:

- Storing it requires space proportional to b.
- Adding large integers can require processing their digits or bits.
- Multiplication is not generally constant time.

For example:

```python
# Repeatedly double a growing integer.
value = 1

for step in range(n):
    value = value * 2
```

After n doublings, the integer is 2ⁿ.

Its binary representation needs n + 1 bits.

So “one variable” does not imply constant space if the numeric value’s representation grows without bound.

For most introductory list problems, we use the conventional fixed-size-value model. When a problem depends on huge integers, state a bit-based model instead.

### Measuring runtime

A benchmark is a measurement of actual performance under chosen conditions.

Benchmarking can help answer: which of these implementations is faster for the inputs and environment I care about?

It cannot replace the question: how does the algorithm’s work grow?

A useful measurement procedure is:

- Use known input sizes.
- Test several larger sizes.
- Repeat measurements.
- Avoid unrelated printing inside the measured computation.
- Compare results under similar conditions.
- Check that every version computes the same answer.

Do not invent timing results when you have not measured them.

### A hand-counted experiment

You can verify growth without a clock by returning an operation count.

```python
# Count all ordered pairs of n positions.
def pair_iterations(n):
    count = 0

    for first in range(n):
        for second in range(n):
            count = count + 1

    return count

# Expected counts follow directly from the loops.
assert pair_iterations(5) == 25
assert pair_iterations(10) == 100
assert pair_iterations(20) == 400
```

Doubling from 5 to 10 multiplies the count by 4.

Doubling from 10 to 20 multiplies it by 4 again.

This directly demonstrates quadratic growth.

### What a good complexity explanation sounds like

Weak explanation: Time is O(n) because there is one loop.

Better explanation: Let n be the input length. The loop examines each element once. Each iteration performs a constant amount of work under the ordinary-integer model, so worst-case time is O(n). The function keeps only two counters and a current-element reference, so auxiliary space is O(1).

For a set-based function: Let n be the input length and u the number of distinct values encountered. There are at most n lookups and insertions. Under average-case constant-time hashing, total time is O(n). The set stores at most u entries, giving O(u) auxiliary space and O(n) in the worst case.

These explanations identify the source of the bound.

### Chapter practice

1. Guided: Analyze the time and extra space of the first function below.
2. Analyze the second function using separate n and m.
3. Analyze the third function’s time and returned-output space.
4. Explain why the final function is not constant-space merely because it uses one result variable.
5. Write a complete complexity explanation for longest_increasing_run from Part 2.

```python
# Problem 1.
def sorted_total(numbers):
    ordered = sorted(numbers)
    result = 0

    for number in ordered:
        result = result + number

    return result
```

```python
# Problem 2.
def count_equal_pairs(first, second):
    count = 0

    for a in first:
        for b in second:
            if a == b:
                count = count + 1

    return count
```

```python
# Problem 3.
def all_prefixes(numbers):
    prefixes = []

    for stop in range(1, len(numbers) + 1):
        prefixes.append(numbers[:stop])

    return prefixes
```

```python
# Problem 4.
def copy_values(numbers):
    result = []

    for number in numbers:
        result.append(number)

    return result
```

#### Answers and explanations

1. Let n be the input length. Sorting: O(n log n) worst-case time. Scan: O(n). Total: O(n log n). Extra space: O(n) for the copied list and sorting workspace. Also notice that sorting is unnecessary if the only goal is the total. Removing it gives a linear-time, constant-auxiliary-space algorithm under the ordinary numeric model.

2. Let n = len(first) and m = len(second). There are nm equality checks. Time O(nm). Auxiliary space O(1), assuming ordinary-size values and counters.

3. The copied prefix sizes are 1 + 2 + ⋯ + n = n(n + 1) / 2. Time O(n²). Returned-output space O(n²). All copied prefixes are retained.

4. The name result refers to a list that grows to n entries. Output storage is O(n), even though there is only one name for that list.

5. A complete explanation: Let n be the number of input integers. After handling the empty case, the function compares each element after the first with its immediate predecessor. Each iteration performs a fixed number of comparisons and counter updates. Therefore, worst-case time is O(n). It stores only the current run length, the best run length, and a loop index, so auxiliary space is O(1) under the ordinary-size integer model. It does not modify the input.

## Running glossary: additions from Part 3

Retain the glossaries from Parts 1 and 2.

| Term | Meaning |
| --- | --- |
| Amortized analysis | Analysis of total cost across a sequence of operations, spread across those operations. |
| Asymptotic | Describing behavior as input size becomes sufficiently large. |
| Auxiliary space | Additional working storage beyond the input, with output treatment stated when relevant. |
| Average case | Expected cost under a specified distribution of inputs. |
| Balanced split | Division into subproblems of approximately equal size. |
| Base case | A recursive case handled without another recursive call. |
| Benchmark | A measurement of actual performance under chosen conditions. |
| Best case | Least work among allowed inputs of a specified size. |
| Big-O | Notation for an asymptotic upper bound. |
| Big-Omega | Notation for an asymptotic lower bound. |
| Big-Theta | Notation for a matching asymptotic upper and lower bound. |
| Bit complexity | Analysis that accounts for the number of bits in represented values. |
| Brute force | A direct approach that checks the relevant possibilities without a more selective technique. |
| Capacity | Available storage positions before a dynamic array must expand. |
| Ceiling | Rounding upward to the nearest integer. |
| Collision | Competition between different keys in a hash-based lookup structure. |
| Constant time | Work bounded independently of the input-size parameter. |
| Constraint | A stated limit or requirement on valid input. |
| Cost model | Assumptions about how the work of operations is counted. |
| CPython | A widely used implementation of the Python language. |
| Cubic | Growth proportional to the cube of input size. |
| Dependent bound | A loop or operation limit that changes with another variable. |
| Distribution | A description of the likelihood of different inputs or outcomes. |
| Dominant term | The part of an expression whose growth eventually outweighs the other parts. |
| Dynamic array | An indexed sequence that expands its underlying capacity when needed. |
| Expected value | A probability-weighted average. |
| Exponential growth | Growth that multiplies by a fixed factor when the size increases by one. |
| Factorial | The product n(n − 1)⋯1, written n!. |
| Geometric series | A sum whose successive terms have a fixed multiplicative ratio. |
| Growth rate | How a quantity changes as input size increases. |
| Hash table | A structure using hash information to organize and locate keys. |
| Input size | A defined measure of the amount of input information. |
| Linear | Growth proportional to input size. |
| Linearithmic | Growth proportional to n log n. |
| Logarithm | The exponent needed to reach a value from a specified base. |
| Lower bound | A quantity below which the analyzed cost cannot fall under the stated conditions. |
| Operation | An action chosen as a unit or component of computational work. |
| Output-sensitive analysis | Analysis that includes produced-output size as a parameter. |
| Output space | Storage needed for the produced result. |
| Peak space | Maximum storage simultaneously needed during execution. |
| Permutation | An ordering of items. |
| Preprocessing | Preparatory work performed before the main queries or computation. |
| Pseudopolynomial | Polynomial in numeric input values, but not necessarily in their encoded bit lengths. |
| Quadratic | Growth proportional to the square of input size. |
| Recurrence | An expression describing a problem’s cost using costs of smaller problems. |
| Recursion | A function calling itself directly or indirectly. |
| Sequential | Happening one operation or phase after another. |
| Space complexity | How memory requirements grow with input size. |
| Subset | A selection of zero or more elements from a collection. |
| Summation | A compact expression for repeated addition. |
| Tight bound | A growth description bounded from both above and below by constant multiples. |
| Time complexity | How computational work grows with input size. |
| Time-space tradeoff | An exchange between time requirements and memory requirements. |
| Upper bound | A quantity the analyzed cost does not exceed under stated conditions. |
| Worst case | Greatest work among allowed inputs of a specified size. |

## Part 3 readiness check

Before moving on, you should be able to explain each statement:

- Two separate linear scans are still linear.
- Two nested loops are not automatically quadratic.
- Checking every unordered pair is still quadratic.
- A list membership test can hide a full scan.
- Copying a prefix inside a loop can create quadratic work.
- Logarithmic growth comes from repeatedly reducing possibilities by a fixed factor.
- Big-O is an upper bound, not a synonym for worst case.
- Amortized constant time allows occasional expensive operations.
- Peak space differs from the total amount of memory allocated over time.
- Recursive space depends on active calls and their stored data, not just total call count.
- Input constraints suggest plausible approaches but do not prove which technique is required.
- A complexity explanation must define its input-size variables and relevant assumptions.

End of Part 3. Next: Part 4, Core Data Structures.
