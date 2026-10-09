## Chapter 5.18: State definition and transitions with coin problems

Similar-looking problems can require different states and transitions.

We will compare:

1. Minimum number of coins.
2. Number of unordered coin combinations.

Assume denominations are distinct positive integers and each denomination is available in unlimited quantity.

### Problem A: minimum coins

Given amount A, return the smallest number of coins summing to exactly A.

Return -1 if impossible.

### Intuition

For amount 6, imagine choosing the final coin.

If it is 1, first solve amount 5.

If it is 3, first solve amount 3.

If it is 4, first solve amount 2.

Choose the best valid possibility.

### State

\[
dp[a]=\text{minimum coins needed to make exactly amount }a
\]

### Transition

For each coin c ≤ a:

\[
dp[a]=\min(dp[a],dp[a-c]+1)
\]

The +1 counts the final coin.

### Base and impossible states

\[
dp[0]=0
\]

Zero coins make zero amount.

Use A + 1 as an impossible marker. With positive integer denominations, any valid representation of amount A uses at most A coins.

### Trace

Coins:

`[1,3,4]`

| Amount | Best construction | Minimum count |
| --- | --- | --- |
| 0 | Empty | 0 |
| 1 | 1 | 1 |
| 2 | 1+1 | 2 |
| 3 | 3 | 1 |
| 4 | 4 | 1 |
| 5 | 4+1 | 2 |
| 6 | 3+3 | 2 |

```python
def minimum_coins(coins, amount):
    impossible = amount + 1
    dp = [impossible] * (amount + 1)
    dp[0] = 0
    for total in range(1, amount + 1):
        for coin in coins:
            if coin <= total:
                dp[total] = min(
                    dp[total],
                    dp[total - coin] + 1,
                )
    if dp[amount] == impossible:
        return -1
    return dp[amount]
```

If k is the number of denominations:

- Time: \(O(Ak)\).
- Space: \(O(A)\).

This is pseudopolynomial in the amount, as discussed in Part 3.

### Problem B: number of combinations

Now count ways to make the amount, treating coin order as irrelevant.

For coins [1,2], amount 3:

1+1+1

1+2

There are two combinations.

2+1 is not a new combination.

### The danger of counting by final coin

If you process totals first and sum all possible final coins, you naturally count ordered sequences.

For amount 3, that gives:

1+1+1

1+2

2+1

That answers a different question.

### A state meaning that controls duplication

Process denominations one at a time.

After processing a denomination, let:

dp[a] count combinations making amount a using only denominations processed so far.

Within the current denomination, increasing totals allow repeated use of that denomination.

```python
def coin_combinations(coins, amount):
    dp = [0] * (amount + 1)
    # One empty combination makes zero.
    dp[0] = 1
    for coin in coins:
        for total in range(coin, amount + 1):
            dp[total] += dp[total - coin]
    return dp[amount]
```

### Trace

Coins [1,2], amount 3:

| Stage | dp |
| --- | --- |
| Initial | [1,0,0,0] |
| After coin 1 | [1,1,1,1] |
| After coin 2 | [1,1,2,2] |

By introducing denominations in a fixed order, the algorithm does not distinguish permutations of the same combination.

### Complexity

- Time: \(O(Ak)\) arithmetic operations.
- Space: \(O(A)\).

### Recognition clues

When a problem says “ways,” determine:

- Do arrangements with different orders count separately?
- Can an item be reused?
- Must the total be exact?
- Is the goal a count, a minimum, or feasibility?

Those questions change the DP.

### Common mistakes

- Using zero for impossible minimum states.
- Using zero instead of one for the empty counting solution.
- Reusing an item that should be available once.
- Counting ordered sequences when combinations are required.

### Practice

1. Guided: What is the minimum count for coins [2], amount 3?
2. How many unordered combinations make amount 4 using [1,2]?
3. Why do duplicate denominations need removal or a different interpretation before using the combination code?

#### Answers and explanations

1. -1. The amount is impossible.

2. Three: 1+1+1+1, 1+1+2, and 2+2.

3. Processing the same denomination as two separate coin types can count the same value combination more than once.


## Chapter 5.19: Two-dimensional DP and sequence matching

Some subproblems need two independent coordinates.

Two dimensions are not chosen because a problem looks difficult. They are chosen because one coordinate does not describe the state completely.

### Example A: paths through a grid

Given a rectangular grid:

- 0 means open.
- 1 means blocked.
- Start at the upper-left cell.
- Move only right or down.
- Count paths to the lower-right cell.

### Intuition

Every path entering a cell comes from:

- The cell above.
- The cell to its left.

Those arrival groups are distinct.

### State

\[
dp[r][c]=\text{number of valid paths reaching cell }(r,c)
\]

### Transition

For an open non-start cell:

\[
dp[r][c]=dp[r-1][c]+dp[r][c-1]
\]

A missing neighbor contributes zero.

A blocked cell contributes zero.

### Trace

Grid:

```
0 0 0
0 1 0
0 0 0
```

DP table:

| Row / column | 0 | 1 | 2 |
| --- | --- | --- | --- |
| 0 | 1 | 1 | 1 |
| 1 | 1 | 0 | 1 |
| 2 | 1 | 1 | 2 |

```python
def grid_paths(grid):
    if not grid or not grid[0]:
        return 0
    rows = len(grid)
    columns = len(grid[0])
    dp = []
    for row in range(rows):
        dp.append([0] * columns)
    for row in range(rows):
        for column in range(columns):
            if grid[row][column] == 1:
                continue
            if row == 0 and column == 0:
                dp[row][column] = 1
            else:
                if row > 0:
                    dp[row][column] += dp[row - 1][column]
                if column > 0:
                    dp[row][column] += dp[row][column - 1]
    return dp[-1][-1]
```

- Time: \(O(RC)\) arithmetic operations.
- Space: \(O(RC)\).

### Why this is not ordinary graph traversal

We are counting routes, not merely marking reachable cells.

The movement rules form an acyclic dependency structure: each move increases a coordinate.

A visited Boolean would lose the number of different ways to reach a cell.

### Example B: longest common subsequence

A common subsequence appears in both sequences while preserving order, possibly skipping positions.

The longest common subsequence, or LCS, has the greatest possible length.

Example:

"abcde"

"ace"

LCS: "ace", length 3.

### State

\[
dp[i][j]=\text{LCS length of the first }i\text{ characters of the first string}
\]

\[
\text{and the first }j\text{ characters of the second string}
\]

The prefix lengths can be zero.

### Transition when final characters match

If:

`first[i - 1] == second[j - 1]`

there exists an optimal alignment using that matching pair. Extend the best answer for the shorter prefixes:

\[
dp[i][j]=dp[i-1][j-1]+1
\]

### Transition when final characters differ

They cannot be matched to each other.

An optimal answer must omit at least one of those two final positions.

Try both possibilities:

\[
dp[i][j]=\max(dp[i-1][j],dp[i][j-1])
\]

### Trace for "abc" and "ac"

| First prefix / second prefix | Empty | a | ac |
| --- | --- | --- | --- |
| Empty | 0 | 0 | 0 |
| a | 0 | 1 | 1 |
| ab | 0 | 1 | 1 |
| abc | 0 | 1 | 2 |

```python
def lcs_table(first, second):
    dp = []
    for i in range(len(first) + 1):
        dp.append([0] * (len(second) + 1))
    for i in range(1, len(first) + 1):
        for j in range(1, len(second) + 1):
            if first[i - 1] == second[j - 1]:
                dp[i][j] = dp[i - 1][j - 1] + 1
            else:
                dp[i][j] = max(
                    dp[i - 1][j],
                    dp[i][j - 1],
                )
    return dp
```

Usage:

```python
table = lcs_table("abcde", "ace")
assert table[-1][-1] == 3
```

For nonempty lengths m and n:

- Time: \(O(mn)\).
- Space: \(O(mn)\).

Including boundary rows, table dimensions are (m + 1) × (n + 1).

### Recognition clues

Look for:

- A grid location plus movement dependencies.
- Comparing two sequences.
- A state requiring two prefix lengths.
- Match/skip decisions.

### Common mistakes

- Confusing substring with subsequence.
- Using character indices where the state is defined by prefix lengths.
- Sharing rows with repeated-list multiplication.
- Failing to handle empty prefixes.
- Resetting LCS to zero on a mismatch, which belongs to a different contiguous-matching problem.

### Practice

1. Guided: How many right/down paths exist in an open 2×2 grid?
2. What is the LCS length of "ab" and "ba"?
3. Why must an empty-prefix row contain zeros?

#### Answers and explanations

1. Two: right then down, and down then right.

2. One. Either "a" or "b" can be chosen, but not both in the required order.

3. An empty sequence contains no nonempty subsequence.


## Chapter 5.20: Knapsack and increasing subsequences

This chapter studies two recurring DP meanings:

- “Best answer using the first i items under a resource limit.”
- “Best answer ending exactly at position i.”

Those meanings are different and should not be mixed.

### 0/1 knapsack

Given items with weights and values, choose a subset whose total weight is at most a capacity.

Each item may be used at most once.

The name 0/1 means each item is either excluded or included once.

### Intuition

For the current item:

- Skip it.
- Or take it and solve the remaining-capacity problem using earlier items.

### State

\[
dp[i][c]=\text{maximum value using the first }i\text{ items with capacity }c
\]

Assume:

- Positive integer weights.
- Nonnegative values.
- Nonnegative integer capacity.
- Corresponding weight/value lists of equal length.

### Transition

Skip:

\[
dp[i-1][c]
\]

Take, if weight fits:

\[
value[i-1]+dp[i-1][c-weight[i-1]]
\]

Choose the larger.

The previous row in both choices ensures the current item cannot be reused.

### Trace

Items:

| Item | Weight | Value |
| --- | --- | --- |
| A | 2 | 4 |
| B | 3 | 5 |
| C | 4 | 7 |

Capacity: 5.

| Items available / capacity | 0 | 1 | 2 | 3 | 4 | 5 |
| --- | --- | --- | --- | --- | --- | --- |
| None | 0 | 0 | 0 | 0 | 0 | 0 |
| A | 0 | 0 | 4 | 4 | 4 | 4 |
| A, B | 0 | 0 | 4 | 5 | 5 | 9 |
| A, B, C | 0 | 0 | 4 | 5 | 7 | 9 |

The best value is 9, using A and B.

```python
def knapsack_table(weights, values, capacity):
    dp = []
    for i in range(len(weights) + 1):
        dp.append([0] * (capacity + 1))
    for i in range(1, len(weights) + 1):
        weight = weights[i - 1]
        value = values[i - 1]
        for space in range(capacity + 1):
            # Option 1: skip the current item.
            dp[i][space] = dp[i - 1][space]
            if weight <= space:
                # Option 2: take it once.
                dp[i][space] = max(
                    dp[i][space],
                    value + dp[i - 1][space - weight],
                )
    return dp[-1][-1]
```

For n items and capacity W:

- Time: \(O(nW)\).
- Space: \(O(nW)\), including boundary dimensions.
- This is pseudopolynomial in W.

### Why a value-to-weight greedy rule is insufficient

With indivisible items, taking the best ratio first can prevent a better combination.

Greedy ratio selection solves a different version where fractions of items may be taken. It does not generally solve 0/1 knapsack.

### Longest increasing subsequence

An increasing subsequence preserves original order and has strictly increasing values. It may skip elements.

Example:

`[3,1,2,5,4]`

One longest increasing subsequence is:

`[1,2,5]`

Length: 3.

### State

\[
dp[i]=\text{length of the longest increasing subsequence ending exactly at }i
\]

Every individual value forms a length-one subsequence.

For an earlier index j, if:

\[
numbers[j]<numbers[i]
\]

then a subsequence ending at j can be extended with numbers[i].

### Transition

\[
dp[i]=\max(dp[i],dp[j]+1)
\]

for valid earlier j.

### Trace

| Index | Value | Useful earlier endings | dp[i] |
| --- | --- | --- | --- |
| 0 | 3 | None | 1 |
| 1 | 1 | None | 1 |
| 2 | 2 | Value 1 | 2 |
| 3 | 5 | Values 3, 1, 2 | 3 |
| 4 | 4 | Values 3, 1, 2 | 3 |

```python
def lis_length(numbers):
    if not numbers:
        return 0
    # dp[i] is the best increasing subsequence ending exactly at i.
    dp = [1] * len(numbers)
    for i in range(len(numbers)):
        for j in range(i):
            if numbers[j] < numbers[i]:
                dp[i] = max(dp[i], dp[j] + 1)
    return max(dp)
```

### Why return max(dp)?

The longest subsequence may end before the final position.

The state is “ending exactly here,” not “best anywhere in this prefix.”

### Complexity

- Time: \(O(n^2)\).
- Space: \(O(n)\).

A more advanced \(O(n\log n)\) method maintains minimum possible ending values for subsequences of each length and uses binary search. The quadratic DP is the foundation for understanding what those optimized values represent.

### Recognition clues

Knapsack:

- Choose or skip items.
- Limited capacity, budget, or resource.
- Each item once, or a clearly specified reuse rule.

Sequence DP:

- Preserve order but allow skips.
- The best answer ending at one position depends on earlier compatible endings.
- A last-choice or last-element decomposition is natural.

### Common mistakes

- Forgetting the item index in a 0/1 state.
- Using a current-row result and accidentally reusing an item.
- Treating LIS as a consecutive run.
- Returning dp[-1] when the best subsequence can end earlier.
- Using <= when strict increase is required.

### Practice

1. Guided: With one item of weight 2 and value 5, capacity 4, what is the 0/1 answer?
2. What is the LIS length of [5,4,3]?
3. Why can [1,3] be a subsequence of [1,2,3]?
4. What changes if knapsack requires filling capacity exactly?

#### Answers and explanations

1. 5 The item cannot be used twice.

2. 1

3. A subsequence may skip the value 2 while preserving order.

4. Unused capacity is no longer automatically acceptable. Impossible exact-weight states need an explicit marker rather than all being initialized to value zero.


## Chapter 5.21: Space optimization and reconstructing choices

A full DP table is often the clearest first correct implementation.

Only after understanding its dependencies should you reduce storage.

### Principle

If future states never need an old value again, that storage may be reused.

The important question is:

Which previous states must still be available when I calculate the next state?

### Example A: stairs with two stored answers

The transition is:

\[
ways(n)=ways(n-1)+ways(n-2)
\]

Only two previous values are needed.

### Trace

| Step computed | Previous two | Previous one | New current |
| --- | --- | --- | --- |
| 2 | 1 | 1 | 2 |
| 3 | 1 | 2 | 3 |
| 4 | 2 | 3 | 5 |
| 5 | 3 | 5 | 8 |

```python
def stairs_small_space(n):
    if n <= 1:
        return 1
    previous_two = 1
    previous_one = 1
    for step in range(2, n + 1):
        current = previous_one + previous_two
        # Advance both meanings by one step.
        previous_two = previous_one
        previous_one = current
    return previous_one
```

- Time: \(O(n)\) arithmetic operations.
- Auxiliary space: \(O(1)\) numeric variables.
- Exact bit storage grows with the size of the counts.

Updating previous_two too early without preserving the needed values can corrupt the transition.

### Example B: LCS with two rows

An LCS cell depends on:

- Previous row, same column.
- Current row, previous column.
- Previous row, previous column.

Only the previous and current rows are needed for the length.

```python
def lcs_small_space(first, second):
    # Use the shorter string for the row width.
    if len(second) > len(first):
        first, second = second, first
    previous = [0] * (len(second) + 1)
    for character in first:
        current = [0] * (len(second) + 1)
        for j in range(1, len(second) + 1):
            if character == second[j - 1]:
                current[j] = previous[j - 1] + 1
            else:
                current[j] = max(
                    previous[j],
                    current[j - 1],
                )
        previous = current
    return previous[-1]
```

For nonempty lengths m and n:

- Time: \(O(mn)\).
- Auxiliary space: \(O(\min(m,n))\).

The method still performs all relevant state calculations. It stores fewer of them simultaneously.

### Example C: 0/1 knapsack in one dimension

We can reuse one capacity array, but update direction matters.

```python
def knapsack_small_space(weights, values, capacity):
    dp = [0] * (capacity + 1)
    for i in range(len(weights)):
        # Descend so lower-capacity entries still describe earlier items.
        for space in range(capacity, weights[i] - 1, -1):
            dp[space] = max(
                dp[space],
                values[i] + dp[space - weights[i]],
            )
    return dp[capacity]
```

### Why descending order is necessary

Use one item:

weight = 2

value = 5

capacity = 4

If capacity updates ascend:

1. At capacity 2, set value to 5.
2. At capacity 4, read the newly updated capacity-2 value.
3. Add the same item again.
4. Incorrectly obtain 10.

Descending order processes capacity 4 before capacity 2 is updated for the current item.

Therefore, the source value still describes earlier items.

### Loop direction expresses a reuse rule

| Problem | Typical capacity direction for one item/coin |
| --- | --- |
| 0/1 item, at most once | Descending |
| Unlimited reuse | Ascending |

The direction is not a memorized decoration. It determines which version of a state is being read.

Costs:

- Time: \(O(nW)\).
- Space: \(O(W)\).

### Reconstruction: return the actual choices

An optimal value is not always enough.

Reconstruction recovers the choices that produce a computed answer.

For LCS, we can walk backward through the full table.

At state (i,j):

- If final characters match, record the character and move diagonally.
- Otherwise, move toward a neighboring state preserving the best length.

```python
def lcs_sequence(first, second):
    dp = lcs_table(first, second)
    i = len(first)
    j = len(second)
    result = []
    while i > 0 and j > 0:
        if first[i - 1] == second[j - 1]:
            result.append(first[i - 1])
            i -= 1
            j -= 1
        elif dp[i - 1][j] >= dp[i][j - 1]:
            i -= 1
        else:
            j -= 1
    # Characters were discovered from the end backward.
    result.reverse()
    return "".join(result)
```

### Trace for "abc" and "ac"

| State | Characters | Action | Recorded backward |
| --- | --- | --- | --- |
| (3,2) | c, c | Record c, diagonal | c |
| (2,1) | b, a | Move to (1,1) | c |
| (1,1) | a, a | Record a, diagonal | c,a |

Reverse the collected characters:

"ac"

Different tie choices may return different valid LCS strings with the same maximum length.

### Complexity

- Table construction: \(O(mn)\) time and space.
- Backtracking through the table: \(O(m+n)\) time.
- Output length: at most \(\min(m,n)\).

Our reconstruction deliberately keeps the full table. More advanced reconstruction techniques can save memory, but they require additional reasoning.

### Recognition clues

Optimize space when:

- State dependencies use only nearby rows or a fixed number of previous values.
- The memory constraint matters.
- You can state exactly which old values are still needed.

Keep more information when:

- You need actual choices, not only a score.
- You need to explain or inspect intermediate states.
- Compression would make correctness substantially harder to maintain.

### Common mistakes

- Overwriting a dependency before reading it.
- Changing a two-dimensional table into one dimension without preserving state meaning.
- Accidentally turning 0/1 knapsack into unlimited knapsack.
- Assuming a compressed score table automatically preserves enough information to reconstruct a solution.

### Practice

1. Guided: What happens if 0/1 knapsack updates capacities upward for one item of weight 2, value 5, capacity 4?
2. Why can stair counting use two values?
3. Why does LCS reconstruction reverse the collected characters?
4. Does reducing DP storage necessarily reduce its time complexity?

#### Answers and explanations

1. It can incorrectly reuse the item and report 10 rather than 5.

2. Each state depends only on the two immediately preceding answers.

3. The table walk starts at the ends of the strings, so matching characters are discovered in reverse order.

4. No. Two-row LCS still computes the same number of states, so its time remains \(O(mn)\).


## How the patterns differ

These distinctions are more useful than memorizing labels.

| Pattern | What makes progress safe? | Information maintained |
| --- | --- | --- |
| Binary search | A comparison or predicate rules out a region | Candidate boundaries |
| Two pointers | Ordering or a read/write invariant justifies movement | Two positions |
| Sliding window | Window updates preserve useful information and valid movement rules | Boundaries plus window state |
| Prefix sums | A region can be expressed as a difference of cumulative values | Cumulative totals |
| BFS | Queue order processes increasing unweighted distance | Queue, discovered state, distance |
| DFS | Stack order explores one branch before alternatives | Active exploration and visited state |
| Backtracking | Choices are explored and then undone | Partial solution and constraints |
| Greedy | A proof shows a local choice can belong to an optimal solution | Chosen decisions and remaining feasibility |
| Topological sort | Zero indegree means no remaining prerequisite | Indegrees and ready vertices |
| Dijkstra | Nonnegative weights make the cheapest pending distance safe to finalize | Best distances and a min-heap |
| Monotonic stack | A new value resolves or dominates earlier candidates | Ordered unresolved indices |
| Dynamic programming | Correctly defined states reuse complete subproblem answers | Stored state results |

### A focused DP checklist

Before implementing a new DP problem, write the following:

1. State sentence: “dp[...] means …”
2. Answer location: Which state contains the requested answer?
3. Choices: What can happen first or last?
4. Transition: Which smaller answers follow from each choice?
5. Base cases: What are the smallest complete or empty situations?
6. Impossible states: How are they represented?
7. Order: Are dependencies computed before use?
8. Counting policy: Do different paths represent distinct answers or duplicates?
9. Complexity: Number of states multiplied by work per state.
10. Storage: Which states must coexist, and are choices needed for reconstruction?

For example, saying “use a 2D DP” skips the most important work. Saying “dp[i][c] is the maximum value using the first i items with capacity at most c” gives you something you can verify.

## Running glossary: additions from Part 5

| Term | Meaning |
| --- | --- |
| Backtracking | Exploring choices while restoring state before exploring alternatives |
| Bottom-up DP | Computing subproblems in an explicit dependency order |
| Boundary search | Searching for the first or last position satisfying a condition |
| Breadth-first search | Queue-based exploration by increasing edge distance |
| Closed interval | An interval including both endpoints |
| DAG | Directed acyclic graph |
| Depth-first search | Stack-based exploration that follows a branch before returning |
| Divide and conquer | Divide a problem, solve smaller parts, combine their answers |
| Dynamic programming | Computing reusable subproblem answers without repeated full recomputation |
| Exchange argument | A proof replacing a choice in an optimal solution without worsening it |
| Feasibility | Whether a candidate satisfies the requirements |
| Greedy algorithm | An algorithm committing to locally selected choices supported by a correctness argument |
| Half-open interval | An interval including its start and excluding its end |
| Indegree | Number of incoming directed edges |
| Knapsack | A family of item-selection problems with resource constraints |
| LCS | Longest common subsequence |
| LIS | Longest increasing subsequence |
| Lower bound | First sorted position whose value is at least a target, in this search context |
| Mathematical induction | Proving a base case and a rule extending smaller valid cases |
| Memoization | Caching answers to states requested by a function |
| Monotonic predicate | A true/false condition changing in only one direction over an ordered domain |
| Monotonic stack | A stack maintaining an increasing or decreasing ordering property |
| Optimal substructure | The ability to construct an optimal answer from appropriate optimal subproblem answers |
| Overlapping subproblems | Repeated requests for identical smaller problems |
| Predicate | A function returning true or false |
| Prefix sum | A cumulative total over an initial sequence portion |
| Pruning | Discarding a search branch proven unable to produce a needed answer |
| Reconstruction | Recovering the choices behind a computed answer |
| Relaxation | Attempting to improve a path distance through an edge |
| Search tree | A tree of partial decisions explored by a search process |
| Sliding window | Maintaining information about a moving consecutive region |
| Stable sort | A sort preserving relative order among equal-key records |
| State | Information identifying one DP subproblem |
| Suffix | A sequence portion from a position through the end |
| Tabulation | Storing answers computed in a chosen bottom-up order |
| Top-down DP | Memoized evaluation starting from the requested problem |
| Topological ordering | A vertex order respecting every directed prerequisite edge |
| Transition | A rule deriving a state’s answer from other states |
| Two pointers | Coordinating two positions to eliminate work or maintain an invariant |
| XOR | A bitwise operation producing one where corresponding bits differ |

## Part 5 readiness check

You are ready to move toward independent problem solving when you can:

- Explain why a binary-search update cannot discard the answer.
- Identify the assumptions required by a sliding window.
- Derive a prefix-sum equation before choosing a dictionary.
- Distinguish unweighted BFS from weighted Dijkstra.
- Restore state correctly during backtracking.
- Produce a counterexample to an unjustified greedy rule.
- Explain why every monotonic-stack item is pushed and popped at most once.
- Define a DP state in a complete sentence.
- Derive a transition from choices rather than copying a formula.
- Distinguish combinations from ordered sequences.
- Explain why 0/1 knapsack iterates capacity downward.
- Separate output reconstruction from computing an optimal score.

End of Part 5. Next: Part 6, How to Think Like a Coder.
