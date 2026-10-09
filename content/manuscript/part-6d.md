## 6.12 — Practice the Process Until You Can Use It Independently

Solving problems independently means making the important decisions yourself.

It does not require inventing every algorithm from scratch. It requires understanding which known ideas apply and why.

### Use worked examples, then remove support

A useful progression is:

Worked example: Read a complete solution and follow every state change.

Guided example: Solve a similar problem with prompts but without the full algorithm.

Independent problem: Solve a related problem without prompts, then compare your reasoning with a reference.

The support should gradually decrease.

If you always see the pattern name before beginning, you are practicing implementation after classification. You also need practice doing the classification yourself.

### An example progression

For prefix-sum problems:

1. Read a worked example that computes range sums.
2. Derive the target-sum equation with guidance.
3. Independently decide what to store for the longest version.
4. Solve the counting version.
5. Explain why the longest and counting versions store different information.
6. Revisit both later without notes.

The transfer happens when you can explain the change in stored information.

### Practice explaining a solution aloud

Use this order:

1. Contract: “The input is … and I must return …”
2. Baseline: “A direct approach would …”
3. Cost: “That repeats …, so it costs …”
4. Insight: “The useful relationship is …”
5. State: “I maintain …”
6. Correctness: “This preserves all necessary candidates because …”
7. Complexity: “Each … happens at most … times.”
8. Tests: “I would check … because …”

For our main problem, an effective explanation is:

“I need the longest consecutive section with a target sum, and values may be negative. Trying every start and end takes quadratic time if I maintain running sums. For a section ending at boundary end, its sum is the current prefix sum minus an earlier prefix sum. Therefore, I need an earlier prefix equal to the current prefix minus the target. I store the earliest boundary for each prefix sum because that gives the longest section ending here. Each value is processed once, giving expected linear time and linear auxiliary space.”

This explanation names both the mechanism and the reason for the stored information.

### A self-assessment rubric

Do not judge learning only by whether the final code was accepted.

| Level | Evidence |
| --- | --- |
| 0 | I needed the complete solution and cannot yet explain its key idea |
| 1 | I can explain the solution while looking at it |
| 2 | I can reconstruct it after seeing the main hint |
| 3 | I can solve it independently and justify correctness and complexity |
| 4 | I can solve a related variation and explain which assumptions changed |

The distinction between levels 3 and 4 matters.

Memorized code can sometimes reproduce one solution. Transfer requires understanding.

### A reusable problem-solving worksheet

Use this until the questions become habitual.

```
1. CONTRACT
   What are the inputs?
   What exactly must be returned?
   What conditions are guaranteed?
   What must not change?

2. EXAMPLES
   What is the smallest meaningful example?
   What is the answer, and why?
   What example challenges my first assumption?

3. BRUTE FORCE
   What are the possible candidates?
   How can I examine enough of them to guarantee correctness?

4. BOTTLENECK
   Which operation is repeated?
   What dominates the running time?

5. PATTERN OR STRUCTURE
   What operation do I need to make cheaper?
   Which technique supports it?
   What assumptions does that technique require?

6. PLAN
   What does each variable mean?
   What happens in each iteration or recursive call?
   Why is each discarded candidate safe to discard?
   Why does the algorithm terminate?

7. IMPLEMENT
   Does the code follow the plan?
   Are boundaries and update order consistent?

8. TEST
   What are the smallest valid inputs?
   What cases attack the algorithm's assumptions?
   Can brute force provide expected answers?

9. COMPLEXITY
   How many times can each important operation occur?
   What storage exists simultaneously?

10. IMPROVE AND REVIEW
    Does the solution meet the constraints?
    What was the key insight?
    What mistake should I record?
    What related problem would test transfer?
```

### Independent practice

For these problems, write the worksheet before writing code.

#### Problem 1: Longest section with equal zeros and ones

Given a list containing only zeros and ones, return the length of the longest consecutive section containing the same number of zeros and ones.

Example:

`[0, 1, 0, 1, 1]`

Answer:

4

Questions:

- How could you transform the values so that equality becomes a sum condition?
- Which information should be stored for repeated prefix sums?

#### Problem 2: Longest section with at most two distinct values

Given a list of integers, return the length of the longest consecutive section containing at most two distinct values.

Example:

`[1, 2, 1, 3, 3]`

Answer:

3

Questions:

- What determines whether the current window is valid?
- Why is a set alone inconvenient when removing one occurrence of a value?
- When can a value be removed from the window’s frequency dictionary?

#### Problem 3: Smallest capacity for ordered shipments

Packages have positive integer weights and must be shipped in their given order. Each day, the total shipped weight cannot exceed a fixed capacity.

Find the smallest capacity that ships all packages within a given positive number of days.

Example:

```
weights = [2, 3, 4]
days = 2
```

Answer:

5

Questions:

- How can you test a proposed capacity?
- If capacity c works, must capacity c + 1 work?
- What lower and upper search bounds are guaranteed?

#### Problem 4: Shortest path or cheapest path?

You have a graph representing locations.

- In version A, every edge costs one unit.
- In version B, edges have different nonnegative costs.

Explain which algorithm you would consider for each version, and construct a tiny example showing why the same ordinary BFS strategy does not solve both.

#### Answers and explanations

Problem 1

Treat:

0 as -1

1 as +1

Then a section with equal zeros and ones has transformed sum zero.

For example:

`[0, 1, 0, 1, 1]`

becomes:

`[-1, 1, -1, 1, 1]`

The first four elements sum to zero.

Use running prefix sums and store the earliest boundary for each sum. Equal prefix sums identify zero-sum sections. Keeping the earliest boundary maximizes length.

Expected time: \(O(n)\). Auxiliary space: \(O(n)\).

You do not need to build a separate transformed list; convert each value as it is processed.

Problem 2

Use a variable-size sliding window with a frequency dictionary.

- Add the rightmost value to its frequency.
- If there are more than two distinct values, remove values from the left.
- Decrease each removed value’s frequency.
- Delete its dictionary entry when its frequency becomes zero.
- Measure the window only after it contains at most two distinct values.

A set alone does not tell you whether another occurrence of a removed value remains inside the window.

The window is justified because extending it cannot reduce its number of distinct values. A start that already contains too many distinct values cannot become valid by extending farther.

Expected time: \(O(n)\).

For this fixed limit of two distinct values, the dictionary contains at most three keys during the add-then-shrink process, so auxiliary space is \(O(1)\). For a general limit \(k\), the corresponding bound is \(O(\min(n,k+1))\) entries.

Problem 3

For a proposed capacity, scan weights in order and place as many consecutive packages as fit on the current day. Start a new day when the next package would exceed the capacity.

For a fixed capacity, taking the longest fitting prefix each day cannot require more days than ending that day earlier: ending earlier leaves at least as much work for later days.

Feasibility is monotonic:

If a capacity works, any larger capacity also works.

Search bounds:

- Lower bound: the maximum package weight.
- Upper bound: the sum of all package weights.

For [2, 3, 4]:

- Capacity 4 requires three days.
- Capacity 5 ships [2, 3] on day one and [4] on day two.

Use binary search on the answer.

If \(R\) is the difference between the initial upper and lower bounds, time is \(O(n\log(R+2))\), with \(O(1)\) auxiliary space under the usual arithmetic model.

Problem 4

Version A: BFS, because the number of edges determines total cost.

Version B: Dijkstra’s algorithm, because edges have nonnegative but potentially different costs.

Counterexample:

- A -> C costs 10.
- A -> B costs 1.
- B -> C costs 1.

BFS prioritizes the one-edge route from A to C. But the two-edge route through B costs only 2.

Fewest edges and smallest total weight are different objectives.


## Running Glossary — Part 6 Additions

| Term | Meaning |
| --- | --- |
| Contract | A precise description of accepted inputs and promised behavior |
| Precondition | A requirement that must hold for the input |
| Postcondition | A requirement that must hold after the function finishes |
| Constraint | A limit or condition on valid inputs |
| Subarray | A consecutive section of an array |
| Subsequence | Elements selected in their original relative order, possibly with gaps |
| Pseudocode | Structured algorithm instructions that need not obey a programming language |
| Counterexample | A valid case that disproves a claim or breaks an algorithm |
| Search space | The collection of candidates an algorithm may consider |
| Brute force | A direct method that examines a broad collection of candidates, often all of them |
| Bottleneck | The operation or phase dominating the computation’s cost |
| Prefix boundary | A position between elements identifying how many elements precede it |
| Dominance argument | A justification that one candidate is never more useful than another for the relevant objective |
| Loop invariant | A statement preserved at a specified point in every iteration |
| Termination argument | An explanation of why an algorithm must eventually stop |
| Feasibility test | A procedure that checks whether a proposed condition or candidate limit can be satisfied |
| Monotonicity | A property changing in only one direction as a parameter changes |
| Test oracle | A source of expected outputs |
| Differential testing | Comparing implementations on the same inputs |
| Test property | A rule that correct outputs must satisfy |
| Time-space tradeoff | Reducing computation by using more memory, or reducing memory by doing more computation |
| Relaxation | An easier problem obtained by weakening a requirement |
| Hint ladder | A progression from small hints to increasingly explicit help |
| Transfer | Applying an understood idea to a new problem or variation |
| Bit mask | An integer whose bits represent separate yes/no states |

## Part 6 Readiness Check

Before moving on, you should be able to:

- Restate a problem without relying on vague terms.
- Separate the required output from your preferred implementation.
- Build a correct brute-force approach.
- Name the repeated work that makes it slow.
- Choose a data structure by the operation it supports.
- Treat pattern clues as hypotheses that require checking.
- Explain why a pointer move or discarded candidate is safe.
- Define each important variable precisely.
- State a useful loop invariant.
- Design tests that challenge assumptions.
- Use brute force to check a faster solution on small inputs.
- Justify complexity by counting total work.
- Explain why negative numbers invalidate some sum-based sliding windows.
- Explain why the longest prefix-sum problem stores earliest positions.
- Identify what kind of help you need when stuck.

End of Part 6.

Next: Part 7 — Fully Worked LeetCode Problems, applying this process to the complete progression from Easy through Hard.
