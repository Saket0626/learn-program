## 6.5 — Steps 4 and 5: Find the Bottleneck and Derive an Improvement

A bottleneck is the part of a computation that dominates its cost.

For the improved brute force, the bottleneck is now:

For every ending position, we effectively consider many possible starting positions.

Can we avoid searching through those starting positions?

### Change the question

Instead of asking:

“What is the sum of every possible subarray?”

ask:

“If a subarray ends here, what must be true about its starting boundary?”

This is a common problem-solving move: fix one part of a candidate and solve for the other part.

### Introduce prefix sums

Let:

\[
P[i]=\text{sum of the first }i\text{ elements}.
\]

Then:

\[
P[0]=0.
\]

For:

`numbers = [1, -1, 5, -2, 3]`

the prefix sums are:

| Boundary position \(i\) | Elements before that boundary | \(P[i]\) |
| --- | --- | --- |
| 0 | [] | 0 |
| 1 | [1] | 1 |
| 2 | [1, -1] | 0 |
| 3 | [1, -1, 5] | 5 |
| 4 | [1, -1, 5, -2] | 3 |
| 5 | [1, -1, 5, -2, 3] | 6 |

For a subarray beginning at boundary start and ending at boundary end:

\[
\text{subarray sum}=P[end]-P[start].
\]

We want:

\[
P[end]-P[start]=target.
\]

Rearrange:

\[
P[start]=P[end]-target.
\]

Now the problem has become a lookup:

“Have I previously encountered the prefix sum current_prefix_sum - target?”

That is a hash-map question.

### A dictionary must store the right information

Suppose the same prefix sum appears at several boundaries.

Which boundary should we keep?

For a fixed ending boundary:

\[
\text{length}=end-start.
\]

A smaller start gives a larger length.

Therefore:

For each prefix sum, keep its earliest boundary position.

This is the key decision.

A dictionary is not enough by itself. Its values must preserve the information needed by the objective.

### Why later occurrences can be discarded

Suppose:

\[
P[a]=P[b]
\quad\text{and}\quad
a<b.
\]

For any future ending boundary \(r>b\):

\[
P[r]-P[a]=P[r]-P[b].
\]

The two candidate subarrays have the same sum.

But:

\[
r-a>r-b.
\]

The earlier boundary produces a longer subarray.

Thus, for the objective “maximize length,” the later boundary is never better.

This is a dominance argument: one candidate is at least as useful as another for all relevant future decisions.

Dominance arguments justify discarding information.

### Why we store the empty prefix

Before reading any numbers, we have already seen prefix sum 0 at boundary 0.

So the dictionary begins as:

`first_position = {0: 0}`

This allows a valid subarray to begin at the first element.

For example:

```
numbers = [2, 1]
target = 3
```

At ending boundary 2:

```
current prefix sum = 3
needed earlier prefix sum = 3 - 3 = 0
earliest boundary for 0 = 0
length = 2 - 0 = 2
```

Without the initial zero prefix, this candidate would be missed.

### Why a sliding window is not justified here

A tempting thought is:

“The answer is a subarray, so I should use a sliding window.”

But “subarray” describes the answer’s shape. It does not prove that a sliding-window rule is safe.

If numbers can be negative:

- Extending the window can decrease its sum.
- Removing its leftmost element can increase its sum.

For example:

```
numbers = [4, -1]
target = 3
```

Discarding 4 because the current sum is too large destroys the answer.

The prefix-sum equation works regardless of whether the numbers are positive, negative, or zero.

### The same equation, different stored information

Suppose the equation remains:

\[
P[start]=P[end]-target.
\]

The dictionary’s contents depend on the requested output.

| Goal | Information to store for each prefix sum |
| --- | --- |
| Determine whether a valid nonempty subarray exists | Whether that sum appeared earlier |
| Count valid subarrays | Number of earlier appearances |
| Find the longest valid subarray | Earliest earlier boundary |
| Find the shortest valid nonempty subarray | Latest earlier boundary |

For the shortest version, query earlier boundaries before recording the current boundary. Otherwise, when the target is zero, you may accidentally select an empty section.

This is a powerful general lesson:

Choose stored information by working backward from the output you need.

### Guided example

At ending boundary 8, the current prefix sum is 14 and the target is 6.

1. Which earlier prefix sum do we need?
2. Suppose it appeared at boundaries 2 and 5. Which should we use for the longest answer?
3. What candidate length results?

The needed sum is 8. Use boundary 2, giving length 8 - 2 = 6.

### Practice

1. At ending boundary 7, the prefix sum is 10 and the target is 4. What earlier prefix sum is needed?
2. Why does replacing an earlier position with a later position risk breaking the longest-subarray algorithm?
3. For counting valid subarrays, why is storing only the earliest position insufficient?

#### Answers and explanations

1. We need 10 - 4 = 6.

2. The later position produces shorter future subarrays with exactly the same sums. Replacing the earlier position loses potentially better answers.

3. Several earlier boundaries with the needed prefix sum correspond to several different valid subarrays. Counting requires their frequency, not one representative position.


## 6.6 — A Pattern Recognition Cheat Sheet

A problem-solving pattern is a reusable arrangement of ideas that solves a family of problems.

Pattern recognition should work like diagnosis:

1. Observe clues.
2. Generate candidates.
3. Check whether the necessary conditions hold.
4. Reject candidates that fail those conditions.

A clue suggests a technique. It does not prove the technique applies.

### Arrays, strings, and lookup problems

| Problem clue | Candidate technique | Question that must be answered |
| --- | --- | --- |
| “Have I seen this value?” | Set | Do I need membership only, or additional information? |
| “How many times does each value appear?” | Frequency dictionary | What identifies a distinct category? |
| “Find a value matching the current value” | Hash map or set | Can the required partner be expressed directly? |
| Sorted input and a target position | Binary search | Does each comparison safely eliminate a region? |
| Sorted input and a pair relation | Two pointers | Why can one endpoint be discarded? |
| A consecutive block of exactly \(k\) elements | Fixed-size sliding window | Can the window result be updated when one item enters and one leaves? |
| Longest or shortest valid consecutive block | Variable-size sliding window | Does validity change predictably as boundaries move? |
| Many sums over fixed array ranges | Prefix sums | Is the array unchanged between queries? |
| Exact subarray sums, including negative values | Prefix sums with a hash map | Do I need counts, earliest positions, or latest positions? |
| Overlapping ranges or appointments | Sort intervals | Are endpoints inclusive, and do touching intervals overlap? |
| Next greater or smaller element | Monotonic stack | Which unresolved elements become answerable when a new value arrives? |
| A small alphabet or a compact set of flags | Frequency array or bit mask | Is the possible value range small and known? |

A bit mask is an integer whose individual binary digits represent separate yes/no states.

### Graphs, trees, and relationships

| Problem clue | Candidate technique | Question that must be answered |
| --- | --- | --- |
| Reachability or connected regions | BFS or DFS | What are the vertices, and what makes two vertices adjacent? |
| Fewest steps where every move has equal cost | BFS | Does every edge contribute the same cost? |
| Minimum total path cost with nonnegative edge weights | Dijkstra’s algorithm | Are all edge weights nonnegative? |
| Prerequisites or dependency ordering | Topological sort | Is the graph directed, and can it contain a cycle? |
| Repeatedly connect groups and ask whether two items share a group | Union-find | Are the relevant operations merges and connectivity queries? |
| Hierarchical relationships | Tree traversal | What information should flow from parent to child or child to parent? |
| Prefix matching among many words | Trie | Are queries about shared beginnings rather than whole-word equality? |
| Level-by-level processing | BFS | Is distance from the starting point the important organization? |

### Optimization, enumeration, and repeated subproblems

| Problem clue | Candidate technique | Question that must be answered |
| --- | --- | --- |
| Generate every valid arrangement | Backtracking | What choices exist, and when is a partial choice impossible? |
| Repeated smaller versions of the same decision problem | Dynamic programming | What complete state determines the remaining answer? |
| Best result from a sequence of local choices | Greedy, possibly DP | Can the local choice be proved safe? |
| Repeatedly take the smallest or largest current candidate | Heap | Do candidates arrive or change during processing? |
| Keep the best \(k\) candidates | Heap, sorting, or selection | Do I need a fully sorted result, and how large is \(k\)? |
| Minimize the largest allowed value | Binary search on the answer | Can I test feasibility, and is it monotonic? |
| Maximize the smallest allowed value | Binary search on the answer | Does feasibility change in only one direction as the answer changes? |
| Explore choices that repeatedly reach equivalent states | Memoization | Does the state include everything affecting future choices? |
| Need the latest unresolved item first | Stack | Does last-in, first-out order match the dependency? |

A feasibility test answers whether a proposed candidate limit or condition can be satisfied.

A property is monotonic when it changes in only one direction as the relevant parameter increases. For binary search on the answer, this often means:

impossible, impossible, impossible, possible, possible, possible

or the reverse.

### Three dangerous keyword shortcuts

“Minimum” does not automatically mean greedy

Minimum coins is an optimization problem.

With coins:

`[1, 3, 4]`

and amount:

6

choosing the largest available coin first gives:

4 + 1 + 1

Three coins.

But:

3 + 3

uses two.

The objective says what to optimize. It does not justify a local-choice rule.

“Array” does not automatically mean two pointers

Two pointers require a reason that pointer movement preserves all necessary candidates.

Without that reason, pointer movement is guessing.

“Count ways” does not automatically mean dynamic programming

Some counting problems have direct formulas. Others require frequency maps, combinatorics, or enumeration.

Dynamic programming becomes useful when a manageable collection of states captures repeated subproblems.

### Work backward from the operation

Sometimes the structure is easiest to choose by naming the operation you need.

| Needed operation | Likely structure |
| --- | --- |
| Test membership | Set |
| Associate a key with information | Dictionary |
| Retrieve the most recently added unresolved item | Stack |
| Process items in arrival order | Queue |
| Repeatedly retrieve the smallest current item | Min-heap |
| Merge groups and test connectivity | Union-find |
| Follow shared word prefixes | Trie |

This is more reliable than selecting a structure because it appeared in the previous problem you solved.

### Guided example

Problem:

Tasks have prerequisite relationships. Return an order that completes every prerequisite before its dependent task.

Reasoning:

1. A task is a vertex.
2. A prerequisite relationship is a directed edge.
3. The answer must respect all directed dependencies.
4. That is the purpose of a topological ordering.
5. A directed cycle means no such ordering exists.

The technique follows from the relationship the output must satisfy.

### Practice

1. A grid contains open cells and blocked cells. Every legal move costs one step. You need the fewest steps to a destination. Which technique is a strong candidate, and why?
2. A problem asks for the longest subarray with exact sum \(k\), and negative numbers are allowed. Which candidate technique should you investigate?
3. A problem repeatedly asks for the smallest currently available task, while new tasks become available. Why might a heap be useful?

#### Answers and explanations

1. BFS, because it explores reachable positions in order of the number of equal-cost moves from the start.

2. Prefix sums with a dictionary, storing the earliest position for each prefix sum when maximizing length.

3. A heap supports inserting newly available tasks and removing the smallest current task without sorting the entire collection after each change.


## 6.7 — Step 6: Plan the Algorithm and Explain Why It Works

Before coding, define the meaning of every important variable.

A name such as count is not a complete definition.

Compare:

“count is a count.”

with:

“zero_count is the number of zeros inside the current window, including both boundaries.”

The second description lets you check whether each update is correct.

### Variable meanings for the target-sum algorithm

We will use:

| Variable | Meaning |
| --- | --- |
| end | The boundary after the values processed so far |
| prefix_sum | Sum of the first end elements |
| first_position | Earliest known boundary for each previously encountered prefix sum |
| needed | Prefix sum required at the start of a valid section ending here |
| best | Longest valid length found so far |

### Plain-English plan

1. Record that prefix sum 0 occurs at boundary 0.
2. Start the running prefix sum and best length at zero.
3. Process each value from left to right.
4. Update the running prefix sum.
5. Compute the earlier prefix sum needed to make the current section sum to the target.
6. If that sum was seen earlier, calculate the candidate length.
7. Update the best length.
8. Record the current prefix sum only if it has never appeared before.
9. Return the best length.

### Pseudocode

```
first_position contains 0 mapped to boundary 0
prefix_sum is 0
best is 0

for each value, with ending boundary end:
    add value to prefix_sum
    needed is prefix_sum minus target

    if needed has an earlier recorded boundary:
        candidate_length is end minus that boundary
        update best

    if prefix_sum has never been recorded:
        record its current boundary

return best
```

### Use a loop invariant

A loop invariant is a statement that remains true at a specified point during every loop iteration.

It gives the loop a precise promise.

For our algorithm, immediately before processing the next value:

1. prefix_sum equals the sum of all values processed so far.
2. first_position stores the earliest boundary for every prefix sum encountered so far.
3. best is the longest valid subarray ending at any boundary already processed.

To prove a loop correct, check three stages.

### Initialization

Before processing any values:

- The processed sum is 0.
- Prefix sum 0 exists at boundary 0.
- There is no processed nonempty subarray, so the best valid length is 0.

The invariant holds.

### Maintenance

Suppose the invariant holds before an iteration.

After adding the next value:

- prefix_sum is correct for the new ending boundary.
- Any valid subarray ending here must begin at a boundary whose prefix sum is prefix_sum - target.
- If such boundaries exist, the earliest gives the longest candidate.
- Comparing that candidate with best accounts for all valid sections ending here.
- Recording a previously unseen prefix sum preserves earliest positions.

The invariant holds for the next iteration.

### Termination

Eventually, every value has been processed.

The invariant then says that best covers valid subarrays ending at every possible ending boundary.

Every nonempty subarray has one of those boundaries, so best is the required answer.

### Correctness also requires progress

A correct-looking invariant does not prove that an algorithm stops.

A termination argument explains why execution must finish.

Here, the for loop processes a finite list once.

For a while loop, you may need a more explicit measure:

- The search interval gets shorter.
- The number of unprocessed items decreases.
- A pointer advances toward a fixed boundary.

If nothing is guaranteed to change toward completion, an infinite loop may be possible.

### Proof templates worth recognizing

You do not need advanced mathematics for many algorithm proofs. You need a suitable structure.

| Technique | Typical correctness question |
| --- | --- |
| Exhaustive search | Did we examine every legal candidate? |
| Binary search | Why can the discarded region contain no needed answer? |
| Two pointers | Why is moving this endpoint safe? |
| Sliding window | Why can discarded starting positions never become useful again? |
| Greedy | Can an optimal solution be adjusted to make this local choice without becoming worse? |
| Dynamic programming | Does every solution fall into one of the transitions from smaller states? |
| BFS | Why are positions reached in increasing distance order? |
| Hash-map summary | Does the stored information preserve everything needed for future decisions? |

### Common misconception

“A correctness explanation is just a description of the code.”

“The loop increments left” describes behavior.

“The discarded start cannot produce any future valid window” justifies behavior.

### Guided example

Suppose a duplicate-detection loop uses a set named seen.

A useful invariant is:

Before processing the current value, seen contains exactly the distinct values at earlier positions.

This explains:

- Why membership means a duplicate exists.
- Why adding the current value prepares the set for the next iteration.

### Practice

1. In the target-sum algorithm, what property would fail if repeated prefix sums overwrote their earlier positions?
2. Why is “the pointer moves” weaker than a full termination argument?
3. For a loop finding the maximum element, state a useful invariant after processing the first \(i\) elements.

#### Answers and explanations

1. The dictionary would no longer store the earliest boundary for each prefix sum, so it could miss the longest candidate.

2. A pointer could move back and forth forever. You must show progress toward a finite stopping condition, such as increasing without passing a fixed limit.

3. For \(i \ge 1\), the tracked maximum equals the largest value among the first \(i\) elements.


## 6.8 — Steps 7 and 8: Implement, Trace, and Test

Now the algorithm has:

- A contract.
- A derivation.
- Defined state.
- An ordered plan.
- A correctness argument.

Writing Python is the next step.

### Final implementation

The pasted source stopped after `candidate_length = end - start`. The three lines that update `best`, record a new prefix only when it is unseen, and return `best` are the plan from this chapter’s pseudocode. The trace below depends on them.

```python
def longest_target_sum(numbers, target):
    # Prefix sum 0 exists before we process any elements.
    #
    # Dictionary meaning:
    # prefix sum -> earliest boundary with that prefix sum
    first_position = {0: 0}
    # Sum of all values processed so far.
    prefix_sum = 0
    # Length of the longest valid nonempty subarray found.
    # If no such subarray exists, this remains 0.
    best = 0
    # enumerate(..., start=1) labels ending boundaries:
    #
    # After processing numbers[0], end is 1.
    # After processing numbers[1], end is 2.
    #
    # Therefore, prefix_sum represents numbers[0:end].
    for end, value in enumerate(numbers, start=1):
        prefix_sum += value
        # We need:
        #
        # prefix_sum - earlier_prefix_sum == target
        #
        # Rearranging gives:
        needed = prefix_sum - target
        # Check earlier boundaries before recording this boundary.
        if needed in first_position:
            start = first_position[needed]
            # Boundaries are half-open, so no +1 is needed.
            candidate_length = end - start
            best = max(best, candidate_length)
        if prefix_sum not in first_position:
            first_position[prefix_sum] = end
    return best
```

### Trace the complete state changes

Input:

```
numbers = [1, -1, 5, -2, 3]
target = 3
```

Initial state:

```
first_position = {0: 0}
prefix_sum = 0
best = 0
```

| end | Value | prefix_sum | needed | Earlier start found | Candidate length | best | Dictionary action |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 1 | 1 | -2 | None | — | 0 | Store 1: 1 |
| 2 | -1 | 0 | -3 | None | — | 0 | Keep existing 0: 0 |
| 3 | 5 | 5 | 2 | None | — | 0 | Store 5: 3 |
| 4 | -2 | 3 | 0 | 0 | 4 | 4 | Store 3: 4 |
| 5 | 3 | 6 | 3 | 4 | 1 | 4 | Store 6: 5 |

Final answer:

4

The winning subarray is:

`[1, -1, 5, -2]`

It sums to 3.

### Build tests from risks

A good test has a reason to exist.

```python
# Empty input: there is no nonempty valid section.
assert longest_target_sum([], 3) == 0
# A single matching element.
assert longest_target_sum([3], 3) == 1
# A single element with no match.
assert longest_target_sum([4], 3) == 0
# Repeated prefix sums must preserve the earliest boundary.
assert longest_target_sum([0, 0], 0) == 2
# Negative values and a negative target are valid.
assert longest_target_sum([-2, -1, -3], -3) == 2
# The longest answer starts at the first element.
assert longest_target_sum([1, -1, 5, -2, 3], 3) == 4
# The longest answer ends at the final element.
assert longest_target_sum([9, 1, 2], 3) == 2
# A zero target does not mean an empty section is the answer.
assert longest_target_sum([4], 0) == 0
```

An assertion checks that a condition is true. If it is false, Python raises an AssertionError.

### Use brute force as a reference

A test oracle is a source of expected answers.

For small inputs, a correct brute-force solution can be an oracle for a faster implementation.

This gives us differential testing: run two implementations on the same input and compare their results.

```python
from itertools import product

# Test lists of lengths 0 through 6.
for length in range(7):
    # product(..., repeat=length) generates every sequence
    # of this length using only -1, 0, and 1.
    for values in product((-1, 0, 1), repeat=length):
        numbers = list(values)
        # Try several negative, zero, and positive targets.
        for target in range(-3, 4):
            # The exhaustive implementation supplies the answer.
            expected = longest_target_sum_slow(numbers, target)
            # The efficient implementation should agree.
            actual = longest_target_sum(numbers, target)
            # Include the failing input if disagreement occurs.
            assert actual == expected, (
                numbers,
                target,
                expected,
                actual,
            )
```

The slow reference is practical here because the generated lists are tiny.

This test does not prove correctness for all possible inputs. It is good at detecting implementation mistakes across many small combinations.

### Test properties when exact answers are inconvenient

A test property is a rule that correct outputs must obey.

For this problem:

\[
0 \le \text{answer} \le n.
\]

Another property:

Reversing the entire list does not change the longest target-sum subarray length.

Why?

Every original subarray corresponds to a reversed subarray with the same values, sum, and length.

For example:

```python
numbers = [1, -1, 5, -2, 3]
assert (
    longest_target_sum(numbers, 3)
    == longest_target_sum(numbers[::-1], 3)
)
```

Such tests are useful, but a wrong algorithm can still satisfy some properties. Use them alongside example tests and a correctness argument.

### Debug the first divergence

Suppose your implementation fails on:

```
numbers = [0, 0]
target = 0
```

Expected answer: 2.

Your answer: 1.

Imagine your code always performs:

`first_position[prefix_sum] = end`

After the first zero, it changes:

`{0: 0}`

into:

`{0: 1}`

That is the first incorrect state change.

The final return value is wrong because the earliest boundary was lost earlier.

A productive debugging question is:

“At what first step does the program’s state stop matching its intended meaning?”

That is more precise than staring at the final answer.

### Guided example

You accidentally write:

`candidate_length = end - start + 1`

Which test exposes this quickly?

```
numbers = [3]
target = 3
```

The correct length is 1, but the incorrect formula produces 2.

The bug comes from mixing an ending boundary with an ending included index.

### Practice

1. Why does this implementation use end - start rather than end - start + 1?
2. What is the benefit of comparing the optimized solution with brute force on many tiny inputs?
3. If a test fails, why should you locate the first incorrect state rather than patch the final result?

#### Answers and explanations

1. end is the boundary after the subarray. The half-open range [start, end) contains end - start elements.

2. Brute force can provide reliable expected answers for many combinations, catching mistakes that a few hand-picked examples miss.

3. The final result is usually a consequence of an earlier broken assumption or update. Fixing that first divergence addresses the cause.

