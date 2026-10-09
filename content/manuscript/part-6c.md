## 6.9 — Steps 9 and 10: Analyze Complexity and Optimize with a Purpose

Complexity analysis should explain where the work comes from.

Do not stop at:

“It has one loop, so it is linear.”

A loop body can contain sorting, slicing, recursion, or another operation whose cost grows with the input.

### Analyze the target-sum solution

Let \(n\) be the number of input elements.

The loop runs \(n\) times.

Each iteration performs:

- An addition.
- A subtraction.
- A dictionary membership test.
- Possibly a dictionary lookup.
- Possibly a dictionary insertion.
- A few comparisons and assignments.

Under the usual model of constant-cost integer operations and average constant-time hash-table operations:

\[
\text{Time}=O(n)\text{ expected}.
\]

The dictionary can contain at most one entry for each distinct prefix sum. There are \(n+1\) prefix boundaries.

Therefore:

\[
\text{Auxiliary space}=O(n).
\]

The output is one integer.

### Precision about assumptions

Python integers can grow beyond a fixed machine word. Operations on extremely large integers cost more than operations on small integers.

Hash tables also have pathological worst cases.

For typical algorithm analysis, we state the standard assumptions and use expected \(O(n)\) time. We should not silently turn that into an unconditional worst-case guarantee.

### Compare the three approaches

| Approach | Main idea | Time | Auxiliary space |
| --- | --- | --- | --- |
| Slice and sum every candidate | Recompute each subarray sum | \(\Theta(n^3)\) | \(O(n)\) |
| Extend a running sum from each start | Reuse work within a starting position | \(\Theta(n^2)\) | \(O(1)\) |
| Prefix sums with earliest positions | Replace starting-position search with lookup | Expected \(O(n)\) | \(O(n)\) |

The fastest solution uses more auxiliary memory than the quadratic one.

That is a time-space tradeoff: using additional memory to reduce computation, or doing more computation to reduce memory.

### Use constraints as filters

Suppose the maximum input length is roughly \(100{,}000\).

A quadratic algorithm may examine around:

\[
\frac{100{,}000 \times 100{,}001}{2}
\]

subarrays—about five billion candidates.

That is a strong reason to seek a better approach.

However:

“\(n \le 100{,}000\), therefore the solution must be \(O(n\log n)\)” is not a proof.

Input constraints suggest feasible growth rates. Actual performance also depends on:

- The time limit.
- The language.
- The work per operation.
- Other input dimensions.
- The number of test cases.
- The structure of the data.

### When are you finished optimizing?

Ask:

1. Is the algorithm correct?
2. Does it meet the expected input limits?
3. Is there a known unnecessary cost?
4. Would another optimization make the code harder to verify?
5. Is the requested task actually asking for the most efficient approach?

Avoid changing a clear, adequate algorithm merely to reduce a minor constant.

### Can this problem be solved in sublinear time?

In the usual setting, an algorithm must inspect every input position in the worst case.

Consider target 1.

- An all-zero list has answer 0.
- If one uninspected position contains 1, the entire list sums to 1, so the answer is the full length.

An algorithm that never inspects that position cannot distinguish those inputs.

Therefore, a worst-case linear amount of input inspection is necessary.

The expected linear-time hash-map approach matches that scale under the standard model.

This argument does not prove that its \(O(n)\) auxiliary memory is necessary.

Time optimality and space optimality are separate claims.

### Optimize the dominant work

Suppose you have an \(O(n^2)\) algorithm.

Changing:

`best = max(best, candidate)`

to:

```python
if candidate > best:
    best = candidate
```

does not remove the quadratic search.

You may change a constant factor, but you have not addressed the bottleneck.

Useful optimization asks:

“Can I avoid doing this family of operations?”

rather than only:

“Can I write this operation differently?”

### Guided example

You have:

```python
for value in numbers:
    if value in another_list:
        ...
```

Let:

- numbers contain \(n\) elements.
- another_list contain \(m\) elements.

List membership can take \(O(m)\), so total time can be \(O(nm)\).

If membership is the only needed operation, building a set from another_list may change the total expected cost to \(O(n+m)\), using \(O(m)\) additional space.

The improvement comes from the operation supported by the data structure.

### Practice

1. Why is “one loop” insufficient evidence for \(O(n)\) time?
2. Does proving a solution’s running time is optimal also prove its memory usage is optimal?
3. A solution passes all small tests but takes quadratic time for \(n=100{,}000\). Which step of the framework should you revisit?

#### Answers and explanations

1. Each iteration may perform nonconstant work, such as a linear search or sorting.

2. No. Time and space require separate analysis and separate lower-bound arguments.

3. Revisit the bottleneck and pattern-selection steps, using the complexity analysis to identify which work must be reduced.


## 6.10 — A Second Complete Walkthrough: When Sliding Window Is Justified

Now we will apply the full process to a similar-looking problem.

### Problem

Given a list containing only 0 and 1, and a nonnegative integer budget, return the length of the longest consecutive section containing at most budget zeros.

You can also interpret this as:

Find the longest section that could become all ones by changing at most budget zeros to ones.

We only return a length. We do not need to modify the list.

### Step 1: Restate the contract

Input:

- A list of zeros and ones.
- A nonnegative integer budget.

Output:

- The maximum length of a subarray containing at most budget zeros.
- 0 for an empty input.

Important details:

- “At most” allows fewer zeros than the budget.
- Consecutiveness matters.
- The budget may be zero.
- The budget may exceed the number of zeros in the entire list.

### Step 2: Work through an example

```
bits = [1, 0, 1, 0, 0, 1, 1]
budget = 1
```

A valid section is:

`[1, 0, 1]`

Length 3, containing one zero.

Another is:

`[0, 1, 1]`

Also length 3.

Every section of length 4 contains at least two zeros:

| Section | Number of zeros |
| --- | --- |
| [1, 0, 1, 0] | 2 |
| [0, 1, 0, 0] | 3 |
| [1, 0, 0, 1] | 2 |
| [0, 0, 1, 1] | 2 |

Therefore, the answer is 3.

### Step 3: Build brute force

```python
def longest_block_brute(bits, budget):
    # Track the largest valid subarray length.
    best = 0
    # Try every possible starting position.
    for start in range(len(bits)):
        zeros = 0
        # Extend this starting position to every possible end.
        for end in range(start, len(bits)):
            # Update the zero count for the new element.
            if bits[end] == 0:
                zeros += 1
            # This candidate is valid when it stays within budget.
            if zeros <= budget:
                candidate_length = end - start + 1
                best = max(best, candidate_length)
    return best
```

This takes \(O(n^2)\) time and \(O(1)\) auxiliary space.

We could stop a particular inner loop after it exceeds the budget, because extending that fixed start cannot remove zeros. Its worst-case running time would still be quadratic.

### Step 4: Identify repeated work

Neighboring candidate subarrays share most of their elements.

We repeatedly count zeros in overlapping sections.

We would like to maintain one section and update its zero count when boundaries move.

### Step 5: Check whether sliding window is safe

Here is the property we need:

- Adding an element to the right never decreases the number of zeros.
- Removing an element from the left never increases the number of zeros.

Therefore:

- If a window is invalid because it contains too many zeros, extending it cannot repair it.
- Moving its left boundary rightward can repair it.
- A starting position discarded because it had too many zeros cannot become valid later merely by extending the right boundary further.

This property justifies the window movements.

Compare that with arbitrary integer sums:

- Adding a negative number can reduce a sum.
- Removing a negative number can increase a sum.

The useful monotonic behavior exists for zero counts but not for arbitrary sums.

### Step 6: Plan in plain English

1. Begin with an empty window.
2. Move the right boundary one step at a time.
3. Count a newly included zero.
4. While the window has too many zeros, remove its leftmost element.
5. Once the window is valid, compare its length with the best length.
6. Continue until every element has been processed.

Variable meanings:

| Variable | Meaning |
| --- | --- |
| left | First included index in the current window |
| right | Last included index in the current window |
| zeros | Number of zeros currently inside the window |
| best | Largest valid window length found so far |

### Step 7: Implement

The pasted source stopped after computing `current_length`. The update to `best` and the `return` follow the plan in this section: measure the window only after it satisfies the budget, then return the best length. The trace records those updates.

```python
def longest_block_with_zero_budget(bits, budget):
    # The current window begins at this index.
    left = 0
    # Number of zeros inside the current window.
    zeros = 0
    # Largest valid window length found so far.
    best = 0
    # Extend the window one element at a time.
    for right, value in enumerate(bits):
        # Account for the newly included element.
        if value == 0:
            zeros += 1
        # An invalid window must shrink until it fits the budget.
        #
        # Use while because removing one element may not be enough.
        while zeros > budget:
            # Remove the leftmost element from our zero count.
            if bits[left] == 0:
                zeros -= 1
            # Move the left boundary past that removed element.
            left += 1
        # Both boundaries are included indices, so use +1.
        #
        # If the valid window is empty, left == right + 1,
        # and this formula correctly gives 0.
        current_length = right - left + 1
        # Every window measured here satisfies the zero budget.
        best = max(best, current_length)
    return best
```

### Trace the algorithm

Input:

```
bits = [1, 0, 1, 0, 0, 1, 1]
budget = 1
```

The table shows the state after any necessary shrinking.

| right | New value | Shrinking action | left | zeros | Valid window | Length | best |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 0 | 1 | None | 0 | 0 | [1] | 1 | 1 |
| 1 | 0 | None | 0 | 1 | [1, 0] | 2 | 2 |
| 2 | 1 | None | 0 | 1 | [1, 0, 1] | 3 | 3 |
| 3 | 0 | Remove indices 0 and 1 | 2 | 1 | [1, 0] | 2 | 3 |
| 4 | 0 | Remove indices 2 and 3 | 4 | 1 | [0] | 1 | 3 |
| 5 | 1 | None | 4 | 1 | [0, 1] | 2 | 3 |
| 6 | 1 | None | 4 | 1 | [0, 1, 1] | 3 | 3 |

### Why it finds the longest answer

For each ending position:

1. We extend the current window.
2. If it becomes invalid, we discard starts until it becomes valid.
3. Every discarded start contains too many zeros for this ending position.
4. Those starts cannot become valid for any later ending position, because extending cannot reduce their zero count.
5. The remaining left is the earliest valid start for this ending position.

An earlier start gives a longer window, so we evaluate the longest valid window ending at each position.

Taking the maximum over all ending positions gives the overall answer.

### Step 8: Test edge cases

```python
# Empty list.
assert longest_block_with_zero_budget([], 1) == 0
# No changes are needed.
assert longest_block_with_zero_budget([1, 1, 1], 0) == 3
# No zero is permitted.
assert longest_block_with_zero_budget([0, 0], 0) == 0
# Only one of the two zeros can be included.
assert longest_block_with_zero_budget([0, 0], 1) == 1
# The budget covers every zero.
assert longest_block_with_zero_budget([0, 0], 2) == 2
# Main example.
assert longest_block_with_zero_budget(
    [1, 0, 1, 0, 0, 1, 1],
    1,
) == 3
```

### Step 9: Analyze complexity

The outer loop moves right through the list once.

The inner loop moves left only forward.

Across the entire execution:

- right advances \(n\) times.
- left advances at most \(n\) times.

Therefore:

\[
\text{Time}=O(n).
\]

The nested loop does not imply quadratic time because the total number of left-boundary moves is bounded by \(n\).

The algorithm stores a fixed number of variables:

\[
\text{Auxiliary space}=O(1).
\]

### Step 10: Decide whether further optimization is needed

The algorithm already processes the input in linear time and uses constant auxiliary space under the usual model.

There is no repeated scan to remove.

Making the code more complicated to avoid a few arithmetic operations would not improve its growth rate.

### Guided example

Trace:

```
bits = [1, 0, 0, 1]
budget = 1
```

At the second zero:

- The window temporarily contains two zeros.
- Removing the first 1 does not reduce the zero count.
- Removing the next 0 does.
- Therefore, shrinking must continue for more than one step.

That is why this implementation uses while, not if.

### What beginners often get wrong

They update best before repairing an invalid window. That can record a length that violates the problem’s constraint.

### Practice

1. Trace [0, 1, 1, 0, 1] with budget 1. What is the answer?
2. Why is removing only one leftmost element sometimes insufficient?
3. Explain precisely why this sliding-window argument works for zero counts but fails for arbitrary signed sums.

#### Answers and explanations

1. The answer is 4, from [1, 1, 0, 1].

2. The removed element may be a 1, leaving the zero count unchanged. Several elements may need to leave before a zero is removed.

3. Extending a window cannot decrease its zero count, so an invalid start remains invalid for future ends. With signed sums, a newly added negative number can change an oversized sum into a valid one, so discarding the start may lose a future answer.


## 6.11 — What to Do When You Are Completely Stuck

“Stuck” is not one condition.

You may be stuck because you:

- Do not understand the statement.
- Cannot generate candidates.
- Have a correct but slow method.
- Suspect a pattern but cannot justify it.
- Know the algorithm but cannot express its state.
- Have code that fails.

Each blockage requires a different action.

### Diagnose the blockage

| What you can currently do | What is missing | Useful next action |
| --- | --- | --- |
| Repeat the story, but cannot predict outputs | Understanding | Solve a tiny example manually |
| Predict outputs, but cannot describe any algorithm | Candidate generation | List all possible answers on a tiny input |
| Describe a correct slow algorithm | Efficiency | Identify repeated work |
| Name a likely pattern | Justification | State its assumptions and seek a counterexample |
| Explain the algorithm but struggle to code | State design | Define each variable and write pseudocode |
| Run code, but get wrong answers | Debugging | Find the first incorrect state |
| Get correct answers on small cases, but time out | Complexity | Count dominant operations and inspect hidden costs |

### A concrete stuck procedure

1. Rewrite the output requirement

Complete this sentence:

“For this input, I must return _____.”

Be exact.

Not:

“Find something about the array.”

Instead:

“Return the largest length among consecutive sections whose sum is exactly the target.”

2. Solve a smaller instance completely

Use three or four elements.

List candidates.

This often reveals what a brute-force loop must enumerate.

3. Relax one difficulty

A relaxation is an easier version formed by weakening a requirement.

Examples:

- Find any valid answer before finding the best answer.
- Check one candidate before searching for a candidate.
- Solve for a fixed ending position.
- Handle a tree before a general graph.
- Assume all numbers are positive, then identify what changes with negatives.

The easier version is useful only if you understand what additional work is needed to return to the original problem.

4. Identify repeated questions

Ask:

- Am I repeatedly asking whether a value exists?
- Am I repeatedly summing overlapping regions?
- Am I recomputing the same recursive state?
- Am I repeatedly selecting the smallest candidate?
- Am I repeatedly checking connectivity?
- Am I revisiting positions without marking them?

These questions often point to a data structure or reusable pattern.

5. Change the viewpoint

Useful changes include:

- Fix the ending position instead of the starting position.
- Process from right to left.
- Solve the decision version: “Is answer \(x\) feasible?”
- Work backward from the desired output.
- Track what must be removed rather than what must be kept.
- Represent relationships as a graph.
- Represent a partial solution by a smaller state.

For our target-sum problem, the productive viewpoint change was:

“For this ending boundary, which earlier prefix sum do I need?”

6. Try to break the candidate idea

Do not spend twenty minutes implementing a claim you can disprove in one minute.

Try:

- Empty input.
- One element.
- Duplicates.
- All equal values.
- Zero.
- Negative values.
- An answer at the first or last position.
- No solution.
- Several equally good solutions.

7. Ask for the smallest useful hint

A useful hint request is specific:

“I have an \(O(n^2)\) solution that fixes each start and extends the end. What repeated work should I examine?”

Another:

“I think sliding window applies, but negative numbers make the sum nonmonotonic. What other representation of a subarray sum should I consider?”

These requests preserve more of the discovery process than asking immediately for finished code.

### A hint ladder

Use increasingly strong help only as needed.

| Level | Help requested |
| --- | --- |
| 1 | Clarify a term or requirement |
| 2 | Suggest a revealing example |
| 3 | Point out the repeated work |
| 4 | Name a relevant technique |
| 5 | Explain the key invariant or recurrence |
| 6 | Show pseudocode |
| 7 | Show a complete implementation |

After a hint, stop reading and attempt the next step yourself.

### When to stop unaided struggle

Use progress rather than elapsed time alone.

Productive struggle produces something new:

- A clearer contract.
- A brute-force method.
- A failed hypothesis with a counterexample.
- A useful equation.
- A smaller state.
- A test that isolates a bug.

Unproductive struggle repeats the same vague thought without new evidence.

For a beginning practice session, you might spend about 15–25 focused minutes attempting a problem before taking a small hint. That is a practical starting rule, not a universal threshold. Adjust it to the problem and your current knowledge.

### How to use a full solution without wasting the problem

If you need to read a full solution:

1. Identify the exact idea you were missing.
2. Close the solution.
3. Explain the idea in your own words.
4. Reconstruct the algorithm from a blank editor.
5. Test it.
6. Change one condition and ask whether the technique still applies.
7. Revisit the problem later without looking.

Copying code tests your ability to copy. Reconstructing it tests whether you can generate the necessary decisions.

### Keep a mistake log that records causes

A useful entry is:

```
Problem type:
Longest exact-sum subarray.

My incorrect idea:
Shrink whenever the current sum exceeds the target.

Failed assumption:
I assumed extending the window could only increase the sum.

Counterexample:
[4, -1], target 3.

Correct insight:
With negative numbers, use the difference between prefix sums.

Transfer rule:
Check monotonicity before applying a sum-based sliding window.
```

An unhelpful entry is:

Need to get better at arrays.

It gives you no specific behavior to change.

### Guided example

You have a recursive solution that repeatedly reaches the same situation:

```
current position = 7
remaining amount = 12
```

Ask:

1. Does the answer from that situation depend only on those two values?
2. Or does it also depend on earlier choices?

If those two values completely determine future options, memoization may reuse the answer.

If earlier choices still matter, the state is incomplete.

### Practice

1. You cannot solve a problem efficiently, but you can describe an exhaustive search. What should you do next?
2. You read a solution and understand each line while looking at it. What should you do to check whether you can reproduce the reasoning?
3. Your DP cache uses only the current index, but the future also depends on remaining capacity. What is wrong?

#### Answers and explanations

1. Identify the dominant repeated work, then ask what information or structure could avoid it.

2. Close the solution, explain the key idea, and implement it from a blank editor. Then test it and consider a nearby variation.

3. The cache key does not describe the complete state. Different remaining capacities may have different answers at the same index.

