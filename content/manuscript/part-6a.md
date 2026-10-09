# Part 6: How to Think Like a Coder

Knowing what a hash map does is different from recognizing when a problem needs one. Knowing how to write a loop is different from deciding what the loop should maintain.

This part teaches that missing connection: how to move from an unfamiliar problem statement to a solution you can explain, implement, test, and improve.

We will use two main problems:

1. Find the longest consecutive section of a list whose numbers add up to a target.
2. Find the longest consecutive section of a binary list containing at most a given number of zeros.

They look similar. Their efficient solutions depend on different properties. Understanding that distinction is more useful than memorizing either solution.

The complete implementations used here were executed and checked through 16,198 comparisons against exhaustive solutions on small inputs, plus the main worked examples. Testing provides evidence; the explanations below also establish why the algorithms work.

## 6.1 — A Repeatable Problem-Solving Process

### The difference between activity and progress

Imagine assembling a piece of furniture.

You could immediately start attaching whichever pieces fit together. You would be busy, but you might build something that prevents the remaining pieces from fitting.

A better process is to identify the intended result, examine the parts, plan an assembly order, and check your work as you go.

Programming has the same distinction.

Writing code is an activity. Making a correct decision about the problem is progress.

Sometimes the most useful next action is writing a loop. Sometimes it is discovering that the problem allows negative numbers.

### Pólya’s four broad phases

The mathematician George Pólya organized problem solving around four phases: understand the problem, devise a plan, carry out the plan, and examine the result. Our programming framework expands those phases into concrete actions. Document1

Here is the ten-step framework we will use.

| Step | Your task | Something concrete you should produce |
| --- | --- | --- |
| 1 | Restate the problem and clarify inputs, outputs, and constraints | A short, precise description of the required behavior |
| 2 | Work through examples by hand | Small examples with justified answers |
| 3 | Find a brute-force solution | A correct method that checks enough possibilities |
| 4 | Identify the bottleneck | A specific explanation of repeated or expensive work |
| 5 | Map the problem to a pattern or data structure | A candidate technique and the conditions that justify it |
| 6 | Plan in plain English or pseudocode | Ordered steps, variable meanings, and a correctness argument |
| 7 | Write the code | An implementation that follows the plan |
| 8 | Test edge cases | Tests designed to expose particular mistakes |
| 9 | Analyze complexity | Time and space costs with reasons |
| 10 | Optimize when necessary | A justified improvement or a reason to stop |

Pseudocode means an algorithm written in structured, language-independent instructions. It is more precise than a vague description but does not need to obey Python syntax.

For example:

```
For each number, add it to the running total.
If the total is larger than the best total seen so far, update the best total.
```

That is pseudocode.

### The steps are a loop, not a rigid ceremony

You will sometimes revisit an earlier step.

For example:

- A failed test may reveal that you misunderstood the output.
- Complexity analysis may reveal that your planned approach is too slow.
- A counterexample may invalidate your chosen pattern.
- Implementing a variable may reveal that its meaning was never clear.

A counterexample is a valid input on which a proposed claim or algorithm fails.

Returning to an earlier step is part of the process.

### What to write before coding

For a new problem, prepare this short worksheet:

```
Input:
Output:
Important constraints:
Small example:
Brute-force approach:
Repeated work:
Candidate improvement:
Why the improvement is safe:
Time:
Space:
```

You do not need polished prose. You need enough precision to expose uncertainty.

Consider these two notes:

“Use a dictionary.”

and:

“For each running total, store its earliest position so that a later matching total gives the longest possible section.”

The second note tells you what the dictionary means and why it helps.

### Worked example: detecting duplicates

Problem:

Given a list of integers, return whether any integer appears more than once.

A useful worksheet is:

```
Input:
A list of integers.

Output:
True if two different positions contain the same value.
Otherwise False.

Important constraints:
Values may be negative.
The list may be empty.
Original order does not affect the answer.

Small example:
[4, 7, 4] -> True

Brute-force approach:
Compare every pair of different positions.

Repeated work:
Each new value is compared with many earlier values.

Candidate improvement:
Keep a set of values already encountered.

Why safe:
A value is a duplicate exactly when it is already in that set.

Time:
Expected O(n).

Space:
O(n) in the worst case.
```

Notice that the set follows from a question:

“Have I seen this value before?”

The structure was chosen to support a needed operation.

### Guided example

Suppose the output changes:

Return how many times each integer appears.

Ask:

1. Does a set preserve counts?
2. What information must be associated with each value?
3. Which structure supports that association?

A set preserves membership, but it does not preserve a separate count for every value. A dictionary mapping each value to its count does.

### Common misconception

“Good programmers recognize the complete solution immediately.”

Experienced programmers often recognize a useful first direction. They still need to check assumptions, resolve details, and verify correctness.

### Practice

1. Why is “use two pointers” an incomplete plan?
2. A test fails because you returned values when the problem asked for indices. Which framework step needs attention?
3. For duplicate detection, explain why the set should be checked before adding the current value.

#### Answers and explanations

1. It does not identify what the pointers mean, how they move, why those moves are safe, or when the algorithm stops.

2. Step 1: clarify the required output. Testing exposed a misunderstanding of the contract.

3. If you add the current value first, it will always be present when you check. Checking first asks whether an earlier occurrence exists.


## 6.2 — Step 1: Turn the Statement into a Precise Contract

A contract describes what inputs a function accepts and what result it promises for those inputs.

A contract has two useful parts:

- A precondition is something the input must satisfy.
- A postcondition is something the output must satisfy after the function finishes.

For example:

Precondition: the input list is sorted in ascending order.

Postcondition: return the index of the target if present, otherwise return -1.

The sorted-input requirement is not decoration. It is part of what makes ordinary binary search valid.

### Our first main problem

Given a list of integers and a target integer, return the length of the longest nonempty consecutive section whose sum equals the target. Return 0 if no such section exists.

A consecutive section of an array is called a subarray.

For:

`numbers = [8, 3, 5, 2]`

these are subarrays:

`[8]`

`[3, 5]`

`[8, 3, 5, 2]`

This is not a subarray:

`[8, 5]`

It skips the 3.

A subsequence may skip elements while preserving their relative order. A subarray may not skip elements.

That one-word distinction can change the entire solution.

### Write the contract explicitly

For this teaching problem:

| Question | Answer |
| --- | --- |
| What is the input? | A list of integers and an integer target |
| Can numbers be negative? | Yes |
| Can numbers be zero? | Yes |
| Can the list be empty? | Yes |
| Must selected elements be consecutive? | Yes |
| What do we return? | A length, not the elements or their indices |
| Is the required sum exact? | Yes |
| What if several sections have the longest length? | Return that length; their identities do not matter |
| What if no nonempty section works? | Return 0 |
| Can we rearrange the list? | No; adjacency in the original list matters |
| May we modify the input? | Our implementation will leave it unchanged |

These answers remove several plausible but incorrect interpretations.

### Why constraints matter

A constraint is a limit or condition on valid inputs.

Examples include:

- The list contains at most \(100{,}000\) elements.
- Every number is positive.
- The graph has no cycles.
- The string contains only lowercase English letters.
- There is exactly one valid answer.

Constraints serve two purposes.

First, they help determine whether an approach is fast enough.

Second, they may make an otherwise invalid technique correct.

For example:

“Every number is positive” gives us useful control over how a sum changes when a window grows or shrinks.

If negative numbers are allowed, that control disappears.

### Questions that prevent wasted work

Before choosing an algorithm, check these distinctions.

| Distinction | Why it matters |
| --- | --- |
| Values versus indices | Sorting may lose original positions unless you preserve them |
| Subarray versus subsequence | Consecutiveness changes the search space |
| Exactly \(k\) versus at most \(k\) | A candidate with fewer than \(k\) items may or may not qualify |
| One answer versus all answers | Generating all answers can require much more work |
| Count versus maximum | The same states may need different stored information |
| Strictly increasing versus nondecreasing | Equality changes comparisons |
| Directed versus undirected edges | Reachability and cycle rules differ |
| Distinct values versus duplicates allowed | Sets, tie handling, and counting behavior differ |
| Positive versus arbitrary integers | Some sliding-window arguments require positivity or nonnegativity |
| Empty input allowed versus forbidden | Initialization and return behavior may differ |

### Worked example: a dangerous assumption

Suppose you read:

“Find the longest subarray whose sum is the target.”

You decide:

“I will sort the numbers first because sorted arrays are easier.”

Take:

```
numbers = [2, -1, 2]
target = 3
```

The entire original list sums to 3, so the answer is 3.

Sorting changes the list to:

`[-1, 2, 2]`

In this particular case the full sum still matches, but the adjacency relationships have changed. Other subarray sums can change.

For a clearer failure, use:

```
numbers = [2, 100, 1]
target = 3
```

No original subarray sums to 3.

After sorting:

`[1, 2, 100]`

the first two elements sum to 3.

Sorting created a candidate that did not exist in the original problem.

A transformation is useful only if it preserves the information the answer depends on.

### Guided example

Problem:

Return two positions whose values sum to a target.

Before solving, write down:

- Can the same position be used twice?
- Is there guaranteed to be a solution?
- If several pairs work, may any pair be returned?
- Do the returned positions refer to the original list?

These are not implementation details. They define correctness.

### What beginners often get wrong

They solve the version of the problem they expected to see instead of the version actually written.

### Practice

1. Explain the difference between “a subarray of length exactly three” and “a subsequence of length exactly three.”
2. Why might sorting be safe for duplicate detection but unsafe for finding the longest consecutive section with a target sum?
3. If a statement guarantees a nonempty input, must your solution invent behavior for an empty input?

#### Answers and explanations

1. A subarray uses three adjacent elements. A subsequence uses three elements in their original relative order but may skip elements.

2. Rearranging values does not change whether a duplicate exists. It can change which values are adjacent, so it can change valid subarrays.

3. No. Correctness is required for inputs satisfying the stated contract. You may support additional inputs, but doing so is a separate design choice.


## 6.3 — Step 2: Work Through Examples That Reveal Structure

Examples are not only for checking finished code. They are tools for discovering the algorithm.

A useful example is small enough to inspect completely and varied enough to challenge your assumptions.

### Start smaller than you think you need

For our target-sum problem, begin with:

```
numbers = [2, -1, 2]
target = 3
```

There are six nonempty subarrays.

| Start index | End index, inclusive | Subarray | Sum | Length | Valid? |
| --- | --- | --- | --- | --- | --- |
| 0 | 0 | [2] | 2 | 1 | No |
| 0 | 1 | [2, -1] | 1 | 2 | No |
| 0 | 2 | [2, -1, 2] | 3 | 3 | Yes |
| 1 | 1 | [-1] | -1 | 1 | No |
| 1 | 2 | [-1, 2] | 1 | 2 | No |
| 2 | 2 | [2] | 2 | 1 | No |

The answer is 3.

This table also suggests a brute-force strategy:

Try every starting position and every ending position.

The example has helped generate an algorithm.

### Use examples with different jobs

Do not collect five examples that all behave the same way.

Give each example a purpose.

| Input and target | Expected answer | What it checks |
| --- | --- | --- |
| [], target 3 | 0 | Empty input |
| [3], target 3 | 1 | One valid element |
| [4], target 3 | 0 | No solution |
| [0, 0], target 0 | 2 | Repeated sums and zeros |
| [-2, -1, -3], target -3 | 2 | Negative values and target |
| [1, -1, 5, -2, 3], target 3 | 4 | A longer answer that begins at the start |
| [9, 1, 2], target 3 | 2 | An answer at the end |

A list of expected answers is not enough. You should be able to justify each one.

For:

`[-2, -1, -3]`

with target -3, the valid subarrays include:

```
[-2, -1]  # Length 2
[-3]      # Length 1
```

Therefore, the longest length is 2.

### Distinguish observation from proof

Suppose you observe:

“On my three examples, when the sum became too large, removing an element from the left helped.”

That is evidence about those examples.

It is not yet a general rule.

Consider:

```
numbers = [4, -1]
target = 3
```

If you discard 4 immediately because it exceeds the target, you lose the valid subarray [4, -1].

The later negative number reduces the sum.

A few successful examples cannot establish that a move is always safe.

### Construct counterexamples deliberately

A strong habit is to ask:

“What input would make my reason for this step stop being true?”

If your reasoning depends on:

“Adding an element increases the sum,”

try adding a negative number.

If your reasoning depends on:

“Each value appears once,”

try duplicates.

If your reasoning depends on:

“There is a next element,”

try a one-element input.

If your reasoning depends on:

“The graph is connected,”

try an isolated vertex.

### Guided example: strictness

Suppose you are finding a strictly increasing sequence and your code uses:

```python
if numbers[j] <= numbers[i]:
```

What tiny example can challenge the comparison?

Use:

`[2, 2]`

A strictly increasing sequence cannot contain both values. Equality must not qualify as an increase.

A two-element example has exposed a logical error.

### Common misconception

“A large random test is always more useful than a small test.”

A tiny, carefully chosen test often identifies the exact assumption that failed. Large tests are useful too, especially after you have a reference implementation.

### Practice

1. Give a small example showing that a large positive sum can later become a smaller sum after extending a subarray.
2. Why is [0, 0] with target 0 useful for testing the longest-target-sum problem?
3. A proposed algorithm returns the first valid section it finds. Give an input where that is not the longest valid section.

#### Answers and explanations

1. [7, -5]: the first element sums to 7, but the full subarray sums to 2.

2. Several prefix positions have the same sum. It can reveal whether the algorithm preserves the earliest useful position and whether it handles zero correctly.

3. [3, 0, 0] with target 3. The first valid section [3] has length 1; the full list has length 3.


## 6.4 — Step 3: Build a Correct Brute-Force Solution

A brute-force algorithm solves a problem by directly checking a broad collection of possible answers, often all of them.

Brute force is useful because it gives you:

- A concrete starting point.
- A way to understand the search space.
- A correct reference for testing faster approaches.
- Something specific to improve.

The search space is the collection of candidates your algorithm may need to consider.

For the longest-target-sum problem, the candidates are all nonempty subarrays.

### Count the candidates

For a list of length \(n\):

- There are \(n\) subarrays starting at index 0.
- There are \(n-1\) starting at index 1.
- There are \(n-2\) starting at index 2.
- There is one starting at index n - 1.

Therefore, the number of nonempty subarrays is:

\[
n+(n-1)+\cdots+1=\frac{n(n+1)}{2}.
\]

This is \(\Theta(n^2)\).

Remember:

- \(O(n^2)\) gives an upper bound on the growth rate.
- \(\Theta(n^2)\) states that the growth rate is quadratic both above and below, up to constant factors.

### First implementation: generate and sum every subarray

We will use half-open boundaries: a subarray begins at start and stops before end.

Thus:

`numbers[start:end]`

has length:

`end - start`

Here is the direct implementation:

```python
def longest_target_sum_slow(numbers, target):
    # A length of 0 means that no valid nonempty subarray
    # has been found yet.
    best = 0
    # Choose the first index of the subarray.
    for start in range(len(numbers)):
        # Choose the boundary immediately after the subarray.
        # Starting at start + 1 makes every candidate nonempty.
        for end in range(start + 1, len(numbers) + 1):
            # Slicing creates the candidate subarray.
            # sum() adds all values in that candidate.
            candidate_sum = sum(numbers[start:end])
            # Only candidates with the exact target sum qualify.
            if candidate_sum == target:
                candidate_length = end - start
                # Keep the largest valid length found so far.
                best = max(best, candidate_length)
    return best
```

### Why it is correct

There are two obligations.

Coverage: Does it consider every possible answer?

Every nonempty subarray has a starting index and an ending boundary. The two loops visit every valid pair.

Selection: Does it choose the right result among those candidates?

It considers only candidates whose sum equals the target, and it keeps the maximum length.

If no candidate qualifies, best remains 0, as required.

### Why it is slow

There are \(\Theta(n^2)\) candidates.

For each candidate:

- Slicing copies its elements.
- sum() visits its elements.

A candidate may contain \(O(n)\) elements.

The total running time is \(\Theta(n^3)\).

Its peak auxiliary space is \(O(n)\), because a slice can contain the entire input. The slices are temporary; we do not retain all of them simultaneously.

### Improve the brute force without changing its search space

Fix a starting position.

Suppose we have already computed:

sum of numbers[start : end]

To extend the section by one element, we do not need to sum everything again.

We can add the newly included value.

For:

`numbers = [2, -1, 2]`

and start = 0:

| Newly included index | Newly included value | Running sum |
| --- | --- | --- |
| 0 | 2 | 2 |
| 1 | -1 | 1 |
| 2 | 2 | 3 |

The revised algorithm is:

```python
def longest_target_sum_brute(numbers, target):
    # Track the largest valid length.
    best = 0
    # Try every possible starting index.
    for start in range(len(numbers)):
        # This sum belongs only to the current starting index.
        running_sum = 0
        # Extend the subarray one element at a time.
        for end in range(start, len(numbers)):
            running_sum += numbers[end]
            # Here end is an included index, so the length
            # requires +1.
            if running_sum == target:
                candidate_length = end - start + 1
                best = max(best, candidate_length)
    return best
```

This version still examines every subarray, but each extension requires constant work under our usual integer-operation model.

Its complexity is:

- Time: \(\Theta(n^2)\).
- Auxiliary space: \(O(1)\).

### The important discovery

We did not begin by naming a famous pattern.

We asked:

“What work am I repeating?”

The answer was:

“I keep adding numbers that were already added for the previous candidate.”

That question produced an improvement.

### Guided example

Suppose you are checking every pair of elements to find whether two values sum to a target.

Your brute-force structure is:

```
For each first position:
    For each later second position:
        Check their sum.
```

The search space contains pairs, not subarrays.

Before optimizing, identify:

- What question is asked repeatedly?
- Can some structure answer that question without scanning all later values?

The repeated question can be reframed as:

“Does a value equal to target - current_value exist among the relevant other positions?”

That wording points toward membership lookup.

### What beginners often get wrong

They abandon brute force before making it correct. Then they have neither a reliable starting point nor a reference implementation.

### Practice

1. Why does the first algorithm take cubic time despite having only two explicit loops?
2. Why must running_sum = 0 be inside the outer loop in the improved brute force?
3. If a valid subarray is found, why can we not immediately stop the inner loop?

#### Answers and explanations

1. The slice and sum() perform additional work proportional to the candidate’s length. That hidden linear work occurs for quadratically many candidates.

2. Each starting position defines a new family of subarrays. Its first running sum must begin at zero; otherwise values from the previous family contaminate it.

3. A longer subarray with the same starting position may also have the target sum. This is especially clear with zeros or positive and negative values that cancel.

