# From Zero to LeetCode Hard

# Part 3: Big-O and Complexity Analysis

In Part 2, you learned to ask:

What does this program do, step by step?

Now we add another question:

How does the amount of work change when the input gets larger?

Two correct programs can behave very differently on large inputs. One might finish after examining each item once. Another might compare every item with every other item.

On a list of ten items, both may feel fast. On a list of one hundred thousand items, the difference can determine whether the program is usable.

This part develops a precise way to reason about that difference.

By the end, you will be able to:

- Count the important operations in a program.
- Distinguish exact operation counts from growth rates.
- Explain common complexity classes.
- Analyze sequential, nested, and dependent loops.
- Account for work hidden inside Python operations.
- Distinguish worst-case, average-case, and amortized analysis.
- Count additional memory, including recursive calls and temporary objects.
- Use input constraints to reject impractical approaches.
- Write a justified complexity explanation for your solution.

The code examples below include expected results or checks. They have been checked by hand, not executed in this session.

## Chapter 3.1: Complexity begins with counting work

### An analogy: checking names on a list

Suppose someone gives you a printed list of names and asks whether “Saket” appears.

One approach is to read names from the beginning until you find it.

If Saket is first, you check one name.

If Saket is last, you check every name.

If Saket is absent, you also check every name.

Now suppose you must identify whether any name appears twice.

A direct approach compares:

- The first name with every later name.
- The second name with every later name.
- The third name with every later name.
- And so on.

The second task involves many more comparisons than one scan.

### Time complexity

Time complexity describes how an algorithm’s amount of work grows as its input size grows.

It usually does not give an exact number of seconds.

Actual time depends on factors such as:

- The computer.
- The programming language and implementation.
- The operations being performed.
- The input’s contents.
- Other activity on the machine.

Complexity analysis removes many of those details so we can compare growth.

### Input size

The input size is a quantity describing how much information the algorithm must process.

We often name it n.

| Input | A useful size variable |
| --- | --- |
| A list | n = len(numbers) |
| A string | n = len(text) |
| Two independent lists | n = len(first), m = len(second) |
| A rectangular grid | r rows and c columns |
| A collection of strings | Number of strings and possibly their total characters |

Always define your size variables.

Saying “the complexity is linear” is incomplete if the reader does not know what quantity it is linear in.

### An operation

An operation is an action we choose to count, such as:

- Comparing two ordinary integers.
- Accessing a list element.
- Adding two ordinary integers.
- Assigning a reference to a name.

We need a cost model, meaning a set of assumptions about what counts as one unit of work.

For most early examples, use this model:

- Ordinary-size integer arithmetic costs a constant amount.
- Comparing ordinary-size integers costs a constant amount.
- Accessing a valid list position costs a constant amount.
- Assigning an object reference to a name costs a constant amount.

A constant amount means the amount does not grow with the input size being analyzed.

These are modeling assumptions. Python’s arbitrarily large integers require a more detailed analysis when their size becomes relevant. We will address that later in this part.

### Worked example: count comparisons in a search

```python
# Search for target while counting equality comparisons.
def search_with_count(numbers, target):
    comparisons = 0

    for number in numbers:
        # Count the comparison about to happen.
        comparisons = comparisons + 1

        if number == target:
            return True, comparisons

    return False, comparisons
```

Examples:

```python
# The first value matches.
print(search_with_count([8, 3, 5, 9], 8))

# The final value matches.
print(search_with_count([8, 3, 5, 9], 9))

# No value matches.
print(search_with_count([8, 3, 5, 9], 7))
```

Expected output:

```
(True, 1)
(True, 4)
(False, 4)
```

We counted equality comparisons, not every underlying machine instruction.

That is useful because the comparisons represent the main repeated work.

### Counting iterations is not always enough

Consider:

```python
# Examine every value once.
for number in numbers:
    print(number)
```

There are n iterations.

However, the cost of printing depends on how much text is produced and on the output system.

For early complexity exercises, avoid treating arbitrary output as a guaranteed one-step operation. We will generally analyze computations that return an answer.

### Worked example: summing a list

```python
# Add every value in the input.
def total(numbers):
    result = 0

    for number in numbers:
        result = result + number

    return result
```

For n elements:

- Initialization happens once.
- The loop body executes n times.
- Each iteration performs a fixed amount of work under our cost model.
- Returning the result happens once.

We can describe the total work using:

T(n) = an + b

Here:

- T(n) means the amount of work for size n.
- a represents the fixed work associated with each item.
- b represents fixed setup and finishing work.

We usually do not need the exact values of a and b.

The important fact is that the work grows proportionally to n.

### Guided comparison

Suppose one algorithm performs 5n + 10 units of work, while another performs n².

For n = 10:

- First: 60.
- Second: 100.

For n = 1,000:

- First: 5,010.
- Second: 1,000,000.

The difference becomes much larger as n increases.

### Common misconception

“A computer is fast, so a few extra loops do not matter.”

Whether they matter depends on how the work grows. Comparing every pair among one hundred thousand items involves billions of pairs.

### Chapter practice

1. Guided: How many equality comparisons does a left-to-right search make when the target is absent from a list of length 7?
2. How many times does the loop body below execute?
3. A program performs 3n + 8 operations. Calculate the count for n = 10 and n = 100.
4. Explain why n should not automatically mean the largest numeric value in a list.

```python
# Problem 2.
count = 0

for number in range(2, 8):
    count = count + 1
```

#### Answers and explanations

1. Seven comparisons. Every element must be checked.

2. Six times. The values are 2, 3, 4, 5, 6, 7.

3. For n = 10: 3(10) + 8 = 38. For n = 100: 3(100) + 8 = 308.

4. For many list algorithms, work depends mainly on how many elements exist. [1, 2, 3] and [1000, 2000, 3000] both contain three elements. Numeric magnitude becomes relevant if the algorithm performs work proportional to those values or if large-integer representation costs matter.

## Chapter 3.2: Growth rates before notation

A growth rate describes how a quantity changes as the input size increases.

Before introducing formal Big-O notation, we will examine the main shapes.

### Constant growth

Suppose you retrieve the first element of a nonempty list:

```python
# Input requirement: numbers is nonempty.
def first_value(numbers):
    return numbers[0]
```

The function accesses one position.

It does not scan the other elements.

Whether the list has 10 elements or 100,000 elements, the number of list accesses is one.

This is constant time.

Constant time does not mean zero time. It means the work does not increase with n.

### Linear growth

Linear growth means work proportional to the input size.

```python
# Count values greater than zero.
def count_positive(numbers):
    count = 0

    for number in numbers:
        if number > 0:
            count = count + 1

    return count
```

Every element is examined once.

Doubling the input roughly doubles the repeated work.

### Quadratic growth

Quadratic growth means work proportional to the square of the input size.

```python
# Count all ordered pairs of positions.
def count_ordered_pairs(numbers):
    count = 0

    for first in range(len(numbers)):
        for second in range(len(numbers)):
            count = count + 1

    return count
```

For n positions:

- The outer loop executes n times.
- Each outer iteration executes the inner body n times.
- Total: n × n = n².

An ordered pair distinguishes (first, second) from (second, first).

For three positions, there are nine ordered pairs, including pairs that use the same position twice.

### Cubic growth

Cubic growth means work proportional to n³.

Three full loops over the same input size can produce n × n × n = n³.

Doubling n multiplies this work by eight: (2n)³ = 8n³.

We will rarely accept cubic algorithms for large inputs.

### Logarithmic growth

A logarithm answers:

How many times must a base be multiplied by itself to reach a value?

For base 2: 2³ = 8. Therefore log₂ 8 = 3.

You can also understand log₂ n as approximately the number of halvings needed to reduce n to 1.

| Starting amount | Halving sequence | Halvings to reach 1 |
| --- | --- | --- |
| 8 | 8, 4, 2, 1 | 3 |
| 16 | 16, 8, 4, 2, 1 | 4 |
| 32 | 32, 16, 8, 4, 2, 1 | 5 |

Each doubling of the input adds only one halving step.

That is logarithmic growth.

### Worked example: repeated halving

```python
# Count how many halvings occur before a positive integer becomes zero.
def halving_steps(number):
    steps = 0

    while number > 0:
        number = number // 2
        steps = steps + 1

    return steps
```

For number = 16:

| Iteration | Value before | Value after |
| --- | --- | --- |
| 1 | 16 | 8 |
| 2 | 8 | 4 |
| 3 | 4 | 2 |
| 4 | 2 | 1 |
| 5 | 1 | 0 |

There are five iterations.

For positive integer n, the exact count is floor(log₂ n) + 1.

The floor symbol, ⌊x⌋, means round down to the nearest integer.

The extra final step from 1 to 0 explains the +1.

The growth rate is still logarithmic.

### Linearithmic growth

Linearithmic growth means proportional to n log n.

The name combines “linear” and “logarithmic.”

This pattern often appears when:

- There are logarithmically many levels of processing.
- Each level performs total work proportional to n.

Effective comparison-based sorting algorithms often have this growth rate.

We will derive a sorting example later rather than asking you to memorize that connection without explanation.

### Exponential growth

Exponential growth occurs when increasing the problem size by one multiplies the work by a fixed factor greater than one.

An important example is 2ⁿ.

If every item presents two independent choices, such as “include” or “exclude,” then n items have 2ⁿ possible choice combinations.

For three items:

- First item: 2 possibilities.
- Second item: 2 possibilities for each previous choice.
- Third item: 2 possibilities for each previous combination.
- Total: 2 × 2 × 2 = 8.

A subset is a selection of zero or more elements from a collection. A collection of n distinct elements has 2ⁿ subsets.

### Factorial growth

The factorial of a nonnegative integer n, written n!, is:

n! = n(n − 1)(n − 2)⋯2·1

Also: 0! = 1.

A permutation is an ordering of items.

For n distinct items:

- There are n choices for the first position.
- Then n − 1 for the second.
- Then n − 2.
- And so on.

Therefore, there are n! permutations.

| n | 2ⁿ | n! |
| --- | --- | --- |
| 5 | 32 | 120 |
| 10 | 1,024 | 3,628,800 |
| 15 | 32,768 | 1,307,674,368,000 |
| 20 | 1,048,576 | 2,432,902,008,176,640,000 |

Generating or checking every ordering becomes impractical quickly.

### Compare the growth rates

The following table shows mathematical quantities, not predicted runtimes:

| n | log₂ n, approximately | n | n log₂ n, approximately | n² | n³ |
| --- | --- | --- | --- | --- | --- |
| 10 | 3.32 | 10 | 33 | 100 | 1,000 |
| 100 | 6.64 | 100 | 664 | 10,000 | 1,000,000 |
| 1,000 | 9.97 | 1,000 | 9,966 | 1,000,000 | 1,000,000,000 |
| 100,000 | 16.61 | 100,000 | 1,660,964 | 10,000,000,000 | 1,000,000,000,000,000 |

### What happens when the input doubles?

| Growth | Effect of changing n to 2n |
| --- | --- |
| Constant | Approximately unchanged |
| Logarithmic | Adds a constant amount of work |
| Linear | Approximately doubles |
| Linearithmic | Slightly more than doubles |
| Quadratic | Multiplies by 4 |
| Cubic | Multiplies by 8 |

For exponential 2ⁿ, increasing n by one already doubles the work.

### Common misconception

2n and 2ⁿ are very different.

2n means twice the input size.

2ⁿ means multiplying 2 by itself n times.

### Chapter practice

1. Guided: If a quadratic algorithm’s input grows from 100 to 200, approximately how does its main work change?
2. How many halvings reduce 64 to 1?
3. Which is larger at n = 20: n² or 2ⁿ?
4. Why does examining every subset require considering 2ⁿ possibilities?
5. If an algorithm examines exactly the first 10 items whenever they exist, does its work grow with a very large list length?

#### Answers and explanations

1. It multiplies by approximately four: 200² / 100² = 4.

2. Six: 64 → 32 → 16 → 8 → 4 → 2 → 1.

3. 20² = 400. 2²⁰ = 1,048,576. The exponential quantity is much larger.

4. Each item has two choices: included or excluded. Multiplying two choices across n items gives 2ⁿ.

5. No. The number examined is bounded by 10. That is constant work with respect to the list length.

## Chapter 3.3: What Big-O means

We now attach notation to growth rates.

### Big-O notation

Big-O notation describes an asymptotic upper bound.

Asymptotic means concerned with behavior as the input size becomes sufficiently large.

An upper bound is a limit that a quantity does not exceed under the stated conditions.

Informally: T(n) = O(g(n)) means that, for sufficiently large inputs, the work is at most a constant multiple of g(n).

Read O(n) aloud as “big O of n.”

| Notation | Name |
| --- | --- |
| O(1) | Constant |
| O(log n) | Logarithmic |
| O(n) | Linear |
| O(n log n) | Linearithmic |
| O(n²) | Quadratic |
| O(n³) | Cubic |
| O(2ⁿ) | Exponential |
| O(n!) | Factorial |

### The formal definition

For nonnegative work functions, T(n) = O(g(n)) if there are constants c > 0 and n₀ such that:

T(n) ≤ c · g(n)

for every n ≥ n₀.

The constants mean:

- c: an allowed fixed multiplier.
- n₀: a starting point after which the bound holds.

You do not need to calculate these constants for every interview explanation. The definition explains why we simplify expressions.

### Worked example: prove a linear upper bound

Suppose T(n) = 3n + 7.

For n ≥ 1: 7 ≤ 7n.

Therefore: 3n + 7 ≤ 3n + 7n = 10n.

We can choose c = 10, n₀ = 1.

Therefore T(n) = O(n).

The proof does not say the program performs exactly n operations.

It says a constant multiple of n eventually bounds the work.

### Why constant factors disappear

Both n and 100n grow linearly.

Their ratio is always 100.

That difference can matter in actual runtime, but it does not change their growth category.

Thus O(100n) = O(n).

Likewise O(n/2) = O(n).

### Why lower-order terms disappear

A term is one component of an expression joined by addition or subtraction.

A dominant term is the term whose growth eventually outweighs the others.

For T(n) = 2n² + 5n + 8, the n² term dominates as n grows.

Therefore T(n) = O(n²).

We are not claiming the other work vanishes. We are classifying the overall growth.

### Common simplifications

| Work expression | Standard tight growth description |
| --- | --- |
| 4n + 20 | O(n) |
| n² + n | O(n²) |
| 7n log n + 3n | O(n log n) |
| n/4 + 1000 | O(n) |
| 12 | O(1) |
| 2ⁿ + n³ | O(2ⁿ) |

### An important precision: Big-O is not automatically tight

A tight bound matches the growth rate from both above and below, up to constant factors.

If an algorithm takes linear time, it is technically also O(n²).

Why?

For sufficiently large n, a quadratic function is an upper bound on a linear function.

But calling a linear algorithm O(n²) hides useful information.

In normal algorithm discussions, people usually expect the tightest standard bound you can justify.

### Big-Theta and Big-Omega

Two related notations make the distinction explicit.

| Notation | Meaning |
| --- | --- |
| O(g(n)) | Asymptotic upper bound |
| Ω(g(n)) | Asymptotic lower bound |
| Θ(g(n)) | Matching upper and lower bounds |

The Greek letters are pronounced: Ω omega, Θ theta.

If T(n) = 3n + 7, then T(n) = Θ(n), because the function grows linearly from both directions.

### Common misconception

Big-O does not mean “worst case,” and Big-Omega does not mean “best case.”

You can apply upper or lower bounds to a best-case function, a worst-case function, or an average-case function.

We will distinguish those cases in Chapter 3.6.

### Why logarithm bases usually disappear

For any fixed bases greater than one:

log_a n = log_b n / log_b a

The denominator is a constant.

Therefore O(log₂ n) = O(log₁₀ n) = O(log n).

We may use base 2 when counting actual halvings, then omit the base when giving a growth class.

### Big-O does not guarantee which program is faster on one small input

Suppose:

- Algorithm A performs approximately 1000n operations.
- Algorithm B performs approximately n² operations.

At n = 10: A is 10,000; B is 100.

At n = 10,000: A is 10,000,000; B is 100,000,000.

The linear algorithm eventually has the advantage, but constants can matter for smaller inputs.

### Chapter practice

1. Guided: Simplify 8n + 30.
2. Simplify 4n² + 9n + 12.
3. Is a linear-time algorithm technically O(n²)?
4. Explain why O(log₂ n) and O(log₁₀ n) describe the same growth class.
5. Does O(1) mean “exactly one instruction”?

#### Answers and explanations

1. O(n).

2. O(n²).

3. Yes. Big-O provides an upper bound. However, O(n), or more precisely Θ(n) when justified, communicates its growth more accurately.

4. The two logarithms differ only by a fixed multiplier. Big-O ignores fixed positive multipliers.

5. No. It means the work is bounded independently of the input size being analyzed. Ten operations or one thousand fixed operations can both be O(1).
