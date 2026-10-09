# Part 3 continued: Chapters 3.4–3.6

## Chapter 3.4: Estimating complexity from loops

The main rule is:

Count how often the work happens. Do not classify a program by its visual indentation alone.

### Sequential loops add

Sequential means one operation or block executes after another.

```python
# Make two separate scans.
def two_totals(numbers):
    first_total = 0

    for number in numbers:
        first_total = first_total + number

    second_total = 0

    for number in numbers:
        second_total = second_total + number

    return first_total + second_total
```

Each loop visits n elements.

Total visits: n + n = 2n.

Therefore O(n).

The loops are not nested, so their counts do not multiply.

### Two independent inputs

```python
# Sum values from two separate lists.
def combined_total(first, second):
    result = 0

    for number in first:
        result = result + number

    for number in second:
        result = result + number

    return result
```

Define n = len(first) and m = len(second).

The total work is O(n + m).

Do not collapse this to O(n) unless you define n as the combined input size or have a known relationship between the two lengths.

### Full nested loops multiply

```python
# Count all cross-list pairs.
def cross_pair_count(first, second):
    count = 0

    for first_value in first:
        for second_value in second:
            count = count + 1

    return count
```

There are n outer iterations and m inner iterations for each.

Total: n·m. Complexity: O(nm).

If both lists have length n, this becomes O(n²).

### A fixed inner loop does not create quadratic growth

```python
# Perform three fixed checks per input value.
def three_checks(numbers):
    count = 0

    for number in numbers:
        for repetition in range(3):
            count = count + 1

    return count
```

Total inner-body executions: 3n.

Complexity: O(n).

The number of nested loops is not sufficient information.

### Dependent loop bounds

A dependent bound changes based on another variable, such as the outer loop’s current position.

```python
# Count pairs of different positions without reversing duplicates.
def unordered_pair_count(numbers):
    count = 0
    n = len(numbers)

    for first in range(n):
        for second in range(first + 1, n):
            count = count + 1

    return count
```

For n = 5:

| first | Inner iterations |
| --- | --- |
| 0 | 4 |
| 1 | 3 |
| 2 | 2 |
| 3 | 1 |
| 4 | 0 |

Total: 4 + 3 + 2 + 1 + 0 = 10.

For general n: (n − 1) + (n − 2) + ⋯ + 1 + 0 = n(n − 1) / 2.

Expanding: (n² − n) / 2.

The dominant term is n².

Therefore O(n²).

Doing roughly half as many pair checks is a useful improvement in constants, but it does not change the quadratic growth class.

### A doubling loop

```python
# Count powers-of-two positions below n.
def doubling_steps(n):
    position = 1
    steps = 0

    while position < n:
        position = position * 2
        steps = steps + 1

    return steps
```

For n = 16: 1 → 2 → 4 → 8 → 16. Four iterations.

For n ≥ 1, the count is ⌈log₂ n⌉.

The ceiling symbol, ⌈x⌉, means round up to the nearest integer.

Complexity: O(log n).

### A linear loop containing a logarithmic loop

```python
# Perform a halving process once for each input element.
def repeated_halving(numbers):
    n = len(numbers)
    count = 0

    for number in numbers:
        remaining = n

        while remaining > 0:
            remaining = remaining // 2
            count = count + 1

    return count
```

For positive n:

- Outer loop: n iterations.
- Inner loop: approximately log₂ n iterations each time.
- Total: O(n log n).

The inner variable is reset to n during every outer iteration. That detail matters.

### Nested loops that are still linear

```python
# Demonstrate a shared index that never resets.
def shared_index_work(numbers):
    n = len(numbers)
    index = 0
    count = 0

    for outer in range(n):
        # Across the entire function, index advances only n times.
        while index < n:
            index = index + 1
            count = count + 1

    return count
```

At the first outer iteration, the while loop advances index from 0 to n.

Afterward, the while condition is false for every remaining outer iteration.

Work:

- Outer-loop overhead: proportional to n.
- Total successful inner iterations across the whole function: n.
- Total: O(n).

This example is deliberately mechanical. Later, two-pointer and sliding-window algorithms use the same counting principle in useful ways.

### A geometric series hidden inside nested loops

Consider:

```python
# Process groups whose sizes double.
def doubling_groups(n):
    size = 1
    count = 0

    while size <= n:
        for item in range(size):
            count = count + 1

        size = size * 2

    return count
```

For n = 8, inner work is 1 + 2 + 4 + 8 = 15.

For a power of two n: 1 + 2 + 4 + ⋯ + n = 2n − 1.

This is a geometric series, a sum where each successive term is obtained by multiplying by a fixed ratio.

Total complexity: O(n).

It is not O(n log n).

Although there are logarithmically many outer iterations, they do not each perform n work.

### A useful summation preview

The notation Σ from i = 1 to n of i means:

Add the values of i as i runs from 1 through n.

Thus Σ i = 1 + 2 + ⋯ + n = n(n + 1) / 2.

A summation is a compact way to express repeated addition.

You do not need advanced calculus to analyze the loops in this chapter.

### What beginners often get wrong

“Nested loops mean O(n²).”

Sometimes. But fixed bounds, shrinking bounds, growing bounds, and shared variables can change the answer. Count total executions.

### Chapter practice

1. Guided: What is the complexity of a loop over n values with an inner loop that always runs 5 times?
2. Two separate loops process lengths n and m. What is the complexity?
3. An outer loop runs n times. Each inner loop runs n − first times. What is the growth class?
4. A while loop divides a positive integer by 3 each time. What is its complexity in the integer’s value?
5. Analyze the following code. Pay attention to where index is initialized.

```python
# Problem 5.
index = 0

for outer in range(n):
    while index < n:
        index = index + 1
```

#### Answers and explanations

1. O(n). The body executes 5n times.

2. O(n + m). Sequential work adds.

3. O(n²). The inner counts form a sum such as n + (n − 1) + ⋯ + 1.

4. O(log n). Repeated division by any fixed factor greater than one produces logarithmic iteration growth.

5. O(n). The inner variable is not reset. Its total number of increments is n, and the outer loop also contributes linear work.

## Chapter 3.5: Work hidden inside Python operations

A short line can perform a large amount of work.

The number of source-code lines is not an operation count.

### A useful reference table

These are standard costs for common operations in CPython, the widely used Python implementation. Assume ordinary-size values and ordinary hashing behavior where relevant.

Let n be the collection size and k the number of items copied or added.

| Operation | Typical analysis |
| --- | --- |
| len(items) | O(1) |
| items[index] | O(1) |
| items[index] = value | O(1) |
| items.append(value) | Amortized O(1) |
| items.pop() | Amortized O(1) |
| items.pop(0) | O(n) |
| items.insert(0, value) | O(n) |
| value in items for a list | O(n) worst case |
| items.copy() | O(n) |
| items[start:stop] | O(k) |
| items.extend(other) | O(k) |
| min(items) or max(items) | O(n) |
| Dictionary/set lookup | Average O(1), worst case O(n) |
| List sorting | O(n log n) worst case |

The Python complexity reference distinguishes average, amortized, and worst-case costs. Those labels are part of the claim, not optional details.

We will define amortized analysis in the next chapter.

### Why list membership can scan

```python
# Ask whether target appears somewhere in the list.
target in numbers
```

For a list, Python may need to compare the target against every item.

Therefore:

```python
# Check every query against the full list.
def count_present(numbers, queries):
    count = 0

    for query in queries:
        if query in numbers:
            count = count + 1

    return count
```

Let n = len(numbers) and m = len(queries).

There are m membership checks.

Each may scan n items.

Worst-case time: O(mn).

Only one loop is visible, but the membership operation performs another scan internally.

### Preprocessing can change the repeated work

Preprocessing means doing preparation before answering the main queries.

```python
# Prepare a membership structure once.
def count_present(numbers, queries):
    available = set(numbers)
    count = 0

    for query in queries:
        if query in available:
            count = count + 1

    return count
```

For ordinary integer keys under the standard average-case hashing assumption:

- Build the set: O(n).
- Check m queries: O(m).
- Total average time: O(n + m).

Additional storage can hold up to n distinct values.

We improved repeated lookup work by using extra memory.

This is a time-space tradeoff: changing memory use to improve time, or vice versa.

### Copying inside a loop

```python
# Count the total number of elements in all copied prefixes.
def copied_prefix_sizes(numbers):
    total = 0

    for stop in range(1, len(numbers) + 1):
        prefix = numbers[:stop]
        total = total + len(prefix)

    return total
```

The copies contain 1, 2, 3, …, n elements.

Total copied references: 1 + 2 + ⋯ + n = n(n + 1) / 2.

Time: O(n²).

The call to len(prefix) is constant time. The slice creation is the expensive operation.

### Calling sum repeatedly

For ordinary-size numbers, sum(numbers) must process the values being added.

```python
# Recompute the same total n times.
def repeated_total(numbers):
    result = 0

    for number in numbers:
        result = sum(numbers)

    return result
```

There are n calls to an operation that scans n values.

Time: O(n²).

If the input never changes, compute the sum once.

### List front removal

A Python list stores its element references in an indexed arrangement. Removing the first item requires shifting the later references toward the front.

Consider repeatedly removing the first item:

```python
# Consume a list from the front.
def remove_everything(numbers):
    while len(numbers) > 0:
        numbers.pop(0)
```

The amount shifted is approximately (n − 1) + (n − 2) + ⋯ + 1 + 0.

Time: O(n²).

A deque, pronounced “deck,” is a double-ended queue designed for efficient additions and removals at both ends. Python documents approximately constant-time end operations for collections.deque, while list front removals require linear movement. We will implement and use queues and deques in Part 4.

### String construction

Strings are immutable, so repeatedly building longer strings can repeatedly copy existing text.

```python
# Build reversed text by repeatedly prepending one character.
def reverse_by_prepending(text):
    result = ""

    for character in text:
        result = character + result

    return result
```

The constructed strings have lengths 1, 2, 3, …, n.

The total character-copying work grows quadratically.

A safer general construction pattern is to collect pieces and join them once. Python’s documentation specifically cautions about repeated concatenation of immutable sequences and recommends alternatives such as collecting strings and joining them.

```python
# Build the reversed character sequence, then join once.
def reverse_with_parts(text):
    parts = []

    # Visit valid character positions from last to first.
    for index in range(len(text) - 1, -1, -1):
        parts.append(text[index])

    # Create one final string from all pieces.
    return "".join(parts)
```

For a string of n characters:

- Append n one-character pieces: O(n) total amortized work.
- Join n characters: O(n).
- Total: O(n).

There is also additional storage for the pieces and returned string.

Python has optimizations for some concatenation situations. Do not base an algorithm’s general complexity claim on assuming every repeated concatenation is optimized.

### String comparisons are not always constant

Comparing two long strings can require examining many characters.

```python
first == second
```

If the strings have the same length and agree until near the end, comparison may examine nearly the entire string.

If each comparison can inspect L characters, a loop performing n such comparisons may take O(nL).

Similarly, hashing a newly encountered long string requires processing its contents. Some implementations cache string hashes, which can reduce later repeated hashing work for the same string object.

The important habit is to identify whether keys or compared objects can themselves be large.

### Sorting is work, even when it is one line

```python
ordered = sorted(numbers)
```

For n ordinary integers, the standard worst-case time bound is O(n log n).

A later linear scan does not dominate that sorting step:

O(n log n + n) = O(n log n).

Python’s sorting implementation can exploit existing ordered runs, so favorable inputs may require less work than the worst-case bound. Its sorting guide also distinguishes sorted, which creates a new list, from list.sort, which changes the existing list.

### What beginners often get wrong

“It is a built-in, so it is constant time.”

A built-in may be implemented efficiently, but it still must perform the work required by its operation.

### Chapter practice

1. Guided: A loop runs n times and calls max(numbers) each time. What is the time complexity?
2. A function creates one list copy and then scans that copy once. What is its time complexity?
3. A loop checks n integers for membership in a list of length m. What is the worst-case complexity?
4. Why can repeated list front removal be quadratic?
5. Explain why sorting followed by a scan is generally O(n log n), not O(n²).

#### Answers and explanations

1. O(n²). Each maximum calculation scans n values.

2. O(n). Copying and scanning are sequential: O(n) + O(n) = O(n).

3. O(nm). There are n queries, each potentially scanning m items.

4. Each removal may shift almost all remaining items. The total shifts form a triangular sum (n − 1) + (n − 2) + ⋯ + 1, which is quadratic.

5. The phases happen one after another, so their costs add: O(n log n) + O(n). They do not multiply.

## Chapter 3.6: Best case, worst case, average case, and amortized cost

These terms answer different questions.

### Best-case analysis

The best case is the least work among inputs of the specified size.

For a search in a nonempty list, the target may be first.

The search can return after one comparison: Θ(1).

### Worst-case analysis

The worst case is the greatest work among allowed inputs of the specified size.

For a left-to-right search, the target may be absent or last.

Then all n elements are examined: Θ(n).

### Average-case analysis

The average case is the expected work under a stated distribution of inputs.

A distribution describes how likely different inputs are.

An expected value is a probability-weighted average.

For a simple example, assume:

- The target appears exactly once.
- Every position is equally likely.

The comparison counts are 1, 2, 3, …, n.

Their average is (1 + 2 + ⋯ + n) / n.

Using the sum formula: (n(n + 1) / 2) / n = (n + 1) / 2.

Therefore, average search time under these assumptions is Θ(n).

Checking about half the list on average is still linear.

### “Average” requires assumptions

If targets are usually first, the average differs.

If targets are usually absent, the average differs.

Do not say “average case” without understanding what is being averaged.

### Early return does not remove the worst case

```python
# Return early when possible.
def contains_zero(numbers):
    for number in numbers:
        if number == 0:
            return True

    return False
```

Best case for nonempty input: O(1).

Worst case: O(n).

The existence of an early return does not guarantee it will happen early.

### Amortized analysis

Amortized analysis bounds the total cost of a sequence of operations, then spreads that total across the sequence.

It does not require a probability distribution over inputs.

Think of occasionally replacing a storage container:

- Most additions fit in the existing container.
- Sometimes the container fills.
- You acquire a larger container and move the existing contents.
- That addition is expensive.
- Many later additions are cheap.

### A model dynamic array

A dynamic array is an indexed sequence that can grow by allocating a larger backing storage area when needed.

Its capacity is the number of elements it can hold before another expansion is needed.

For an illustrative implementation, suppose capacity doubles: 1, 2, 4, 8, 16, ...

This is a teaching model, not a claim that Python uses that exact growth sequence.

When expanding:

- From 1 to 2, copy 1 existing reference.
- From 2 to 4, copy 2.
- From 4 to 8, copy 4.
- From 8 to 16, copy 8.

The total references copied across many expansions form 1 + 2 + 4 + 8 + ⋯.

Up to n appended elements, this total is proportional to n.

There are also n ordinary writes for the newly appended elements.

Therefore, n appends cost O(n) in total.

The cost per append, amortized across the sequence, is O(n) / n = O(1).

### An individual append can still be expensive

If expansion requires copying the current n references, that particular append can take O(n).

This does not contradict amortized constant time.

The claims refer to different things:

| Claim | What it describes |
| --- | --- |
| One append can cost O(n) | A single expensive event |
| Append is amortized O(1) | Cost spread across a sequence |
| n appends take O(n) total | Aggregate sequence cost |

### Average and amortized are different

| Analysis | Main question |
| --- | --- |
| Worst case | How expensive can this input or operation be? |
| Average case | What is the expected cost under an input distribution? |
| Amortized | How expensive is a whole sequence, spread across its operations? |

### Dictionary and set claims

For dictionary and set operations, the usual efficient lookup claim depends on hash-table behavior.

A hash table organizes entries using numeric hash information so that a key can often be located without scanning every entry.

A collision occurs when different keys compete for the same hash-based location or search path.

We will study implementation in Part 4.

For now:

- Average-case lookup is commonly treated as O(1) for ordinary-size keys.
- Collisions can make worst-case lookup much more expensive.
- Insertions may also involve resizing.
- Hashing or comparing a large key can add its own cost.

When you analyze a set-based algorithm, state the average-case hashing assumption.

### Common misconception

“Amortized constant time means every operation is constant time.”

It means expensive operations are sufficiently infrequent that the total sequence cost remains linear in the number of operations.

### Chapter practice

1. Guided: A search finds its target first. What is its best-case complexity?
2. Under the equally likely successful-position assumption, why is average search still linear?
3. Can one list append be linear while a sequence of appends has constant amortized cost?
4. Does amortized analysis require random inputs?
5. A function returns immediately for a special input but scans the entire list otherwise. What should its worst-case analysis include?

#### Answers and explanations

1. O(1) for a nonempty list with the target first.

2. The expected comparisons are (n + 1) / 2. That grows proportionally to n.

3. Yes. A resize can require copying many references, but the total resizing work across the sequence can still be linear.

4. No. Amortized analysis studies aggregate cost across operations. It does not depend on averaging over random inputs.

5. The full scan: O(n). A favorable special case does not remove a slower allowed case.
