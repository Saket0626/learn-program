# Part 8: The Training Plan

This plan turns Parts 1–7 into a sequence of daily work.

It contains:

- A **40-week roadmap** built around approximately 90 minutes a day.
- **120 unique LeetCode problems**, grouped by technique and ordered for learning.
- A review schedule that revisits material after increasing delays.
- A system for diagnosing mistakes.
- Exercises for explaining solutions aloud.
- Readiness checks for attempting unfamiliar Hard problems.
- Free supplementary resources.

The core list contains **41 Easy, 71 Medium, and 8 Hard problems**. Four additional Hard problems appear later as optional assessments.

Forty weeks is a planning estimate, not a deadline or a guarantee. Some weeks may take two weeks. The goal is to develop independent problem-solving ability, not to finish a numbered list on schedule.

Reading the previous parts does not automatically mean you should skip the early weeks. Use the readiness checks to decide where to begin.

---

## 8.1 — What Effective Practice Actually Looks Like

### Separate familiarity from ability

Consider two situations.

In the first, you read a solution and every line makes sense.

In the second, you begin with an empty editor and produce a correct solution without seeing the technique or code.

Those are different levels of knowledge.

**Familiarity** means something feels recognizable.

**Retrieval** means you can bring the needed information to mind without looking at it.

**Transfer** means you can apply an understood idea to a different problem.

Your training should develop all three, with increasing emphasis on retrieval and transfer.

### The learning cycle

For each new technique, use this sequence:

1. Study one worked example.
2. Explain its important decisions.
3. Complete a partly guided example.
4. Solve a related problem independently.
5. Return after a delay.
6. Apply the idea to a variation.

This is **faded practice**: support gradually decreases as your ability increases.

For example, when learning a sliding window:

| Stage | What you receive | What you must produce |
|---|---|---|
| Worked example | Complete explanation, trace, and code | Explain the window’s meaning and updates |
| Guided example | Problem plus questions about validity | Derive the movement rules |
| Independent example | Problem statement only | Choose and justify the technique |
| Delayed review | Previously studied problem | Reconstruct the solution without notes |
| Transfer | A changed condition | Explain whether the same technique still applies |

### Why delayed recall belongs in the plan

Experiments on learning from prose found that practicing retrieval improved delayed retention compared with repeatedly studying the material, even when repeated study increased confidence. That supports testing what you can produce without notes. It does not establish that any particular LeetCode schedule is optimal. [PubMed](https://pubmed.ncbi.nlm.nih.gov/16507066/?utm_source=chatgpt.com)

Research on distributed practice also supports spreading learning over time. The useful spacing depends partly on how long you need to retain the material. The specific review intervals in this plan are practical starting points, not scientifically exact deadlines. [PubMed](https://pubmed.ncbi.nlm.nih.gov/16719566/?utm_source=chatgpt.com)

### Deliberate practice needs a narrow target

**Deliberate practice** means working on a specific weakness, receiving useful feedback, and adjusting what you do.

Compare these goals:

> “Do more binary search.”

and:

> “Practice defining whether the right boundary is included, then trace inputs of lengths zero, one, and two.”

The second goal identifies a behavior you can inspect and improve.

Examples:

| Weakness | Focused practice |
|---|---|
| Off-by-one errors | Trace boundaries on very small inputs |
| Choosing the wrong pattern | Compare similar problems with different assumptions |
| Incomplete DP state | Explain what information affects future decisions |
| Incorrect complexity claims | Count operations across the whole execution |
| Difficulty writing recursion | State the function’s promise before writing its body |
| Forgetting backtracking cleanup | Trace the path before and after every recursive return |

### Use four learning labels

Record one of these labels for each problem:

| Label | Meaning |
|---|---|
| **Studied** | You understand a worked solution while examining it |
| **Rebuilt** | You reconstructed it after learning the key idea |
| **Retained** | You reconstructed and explained it after a meaningful delay |
| **Transferred** | You applied the idea to a related problem without being told the technique |

A problem can have an accepted submission and still be only **Studied**.

That label is useful information. It tells you what kind of practice comes next.

### Worked example

You read the Two Sum solution, then immediately type it from memory.

Record:

```text
Status: Rebuilt

What I can explain:
The needed partner is target - current value.
The dictionary stores earlier positions.
Checking before insertion prevents reusing a position.

What is still untested:
Whether I can reconstruct the idea next week.
Whether I can adapt the dictionary's contents for a different output.
```

### Guided example

You solve a prefix-sum counting problem after being told:

> “Store the frequency of each earlier prefix sum.”

Your implementation may be correct, but the central choice was supplied.

Record that help. Later, test whether you can independently choose between storing:

- Existence.
- Frequency.
- Earliest position.
- Latest position.

### Practice

1. You watched a solution yesterday and can recognize its code today. Which learning label is justified?
2. Why is “I completed five problems” an incomplete measure of progress?
3. Turn “I am bad at graphs” into a narrow practice objective.

<details>
<summary>Answers and explanations</summary>

1. At least **Studied**. Recognition alone does not establish that you can reconstruct it.
2. It does not show how much help you used, whether you can explain correctness, or whether you retained the technique.
3. One useful objective is: “Given five graph problems, define the vertices and edges, then decide whether the task is reachability, shortest path, connectivity, or dependency ordering.”

</details>

---

## 8.2 — How to Use Your 90 Minutes

A session needs both a learning target and a stopping point.

You do not need to finish a new problem every day. A difficult problem may occupy several sessions.

### The standard session

| Time | Activity | Concrete result |
|---|---|---|
| 0–15 minutes | Retrieve earlier material | A short explanation, trace, or small implementation without notes |
| 15–25 minutes | Read the new problem and work examples | Contract, constraints, and hand-checked examples |
| 25–50 minutes | Develop a solution | Brute force, bottleneck, and candidate improvement |
| 50–75 minutes | Implement and test | Working code or a clearly isolated remaining issue |
| 75–85 minutes | Explain correctness and complexity | A short spoken or written explanation |
| 85–90 minutes | Record the lesson | Mistake entry and next review date |

This is a default allocation. Move time between activities when the problem requires it.

If your reasoning is incomplete at minute 50, continue reasoning. Do not force yourself to code an unjustified idea because the table says “implement.”

### A session for learning a completely new technique

Use a different allocation when the technique itself is unfamiliar:

| Time | Activity |
|---|---|
| 0–10 minutes | Recall the prerequisite concepts |
| 10–30 minutes | Study a small worked example |
| 30–45 minutes | Trace it without looking at the supplied trace |
| 45–70 minutes | Reconstruct the implementation |
| 70–85 minutes | Solve a guided variation |
| 85–90 minutes | Record the invariant and one failure case |

For example, your first heap session should include tracing heap operations. Starting with a difficult heap application before understanding the structure creates avoidable confusion.

### A session for a Hard problem

A Hard problem often needs more planning time.

| Time | Activity |
|---|---|
| 0–10 minutes | Retrieve relevant prerequisites |
| 10–25 minutes | Clarify the statement and enumerate small cases |
| 25–50 minutes | Derive brute force and investigate improvements |
| 50–65 minutes | Prove or disprove candidate ideas |
| 65–80 minutes | Implement the justified portion |
| 80–90 minutes | Record progress, tests, and the precise next question |

If the session ends without a complete solution, leave a useful note:

```text
Current approach:
BFS is correct.

Current bottleneck:
Finding neighbors compares each word with the entire dictionary.

Next question:
Can I generate possible neighbors directly?
```

That is a productive stopping point.

### The weekly rhythm

A normal week can use:

| Day | Main purpose |
|---|---|
| Monday | Learn or refresh the week’s technique |
| Tuesday | Solve a related problem with less support |
| Wednesday | Solve independently |
| Thursday | Continue the week’s problems or repair a weakness |
| Friday | Attempt a harder variation |
| Saturday | Mixed review and unfinished work |
| Sunday | Light review, planning, or rest |

Six 90-minute sessions provide nine hours. A light seventh session adds roughly 30–45 minutes.

The roadmap’s weekly problem counts describe **first passes**. Delayed reviews happen inside later sessions.

### What to do when reviews take longer than expected

A full reconstruction is different from a five-minute concept check.

If today’s review needs 35 minutes:

- Use the first 35 minutes for it.
- Reduce the new-problem block.
- Keep the explanation and mistake-log steps.
- Move the new problem to tomorrow if necessary.

Do not continually add review work on top of the original workload.

### During college exam weeks

Use a maintenance schedule:

- Three sessions of 20–30 minutes.
- No new techniques.
- One short explanation.
- One old implementation.
- One mistake-log review.

Then resume the roadmap where you left off.

A missed week changes the calendar. It does not erase the work already learned.

### Worked example: a 90-minute Two Sum session

```text
15 minutes:
Rebuild a frequency dictionary from a small list.

10 minutes:
Clarify that Two Sum returns indices and uses different positions.

25 minutes:
Write pair enumeration, then derive target - current_value.

25 minutes:
Implement the dictionary solution and test duplicate values.

10 minutes:
Explain why checking before insertion matters.

5 minutes:
Record the insight and schedule a delayed review.
```

### Practice

1. Your new problem remains unsolved after 90 minutes, but you have a correct brute force and one disproved optimization. Was the session necessarily unsuccessful?
2. You have 40 minutes of important review due today. What should happen to the new-problem workload?
3. During a busy exam week, what is a better maintenance task than watching three unfamiliar algorithm videos?

<details>
<summary>Answers and explanations</summary>

1. No. You have made concrete progress and can identify the next question.
2. Reduce it. Reviews replace part of the session rather than becoming an unlimited addition.
3. Reconstruct one previously learned solution, explain its invariant, and revisit a recurring mistake.

</details>

---

## 8.3 — The 40-Week Roadmap

The problem numbers in the next table refer to the **training order in Section 8.4**, not LeetCode’s own IDs.

For example:

- Training problem **4** is LeetCode **1: Two Sum**.
- Training problem **120** is LeetCode **4: Median of Two Sorted Arrays**.

### Before choosing your starting week

Attempt these five tasks without following an existing solution:

1. Write a function that counts the occurrences of each value in a list.
2. Trace a loop and show every change to its variables.
3. Explain the difference between returning and printing.
4. Explain why a nested loop might be quadratic, and why some nested loops are linear overall.
5. Write and test a function that finds the longest strictly increasing consecutive run.

If the first three are difficult, begin at Week 1.

If the first three are comfortable but complexity and independent planning are weak, begin around Week 5.

If all five are comfortable, use Week 6 as a diagnostic before starting the problem sequence.

### Weeks 1–6: Build the foundation

| Week | Main work | Required result before advancing |
|---:|---|---|
| 1 | Run Python. Learn values, variables, types, expressions, and input/output. | Write several small programs without copying their structure. |
| 2 | Conditionals, `for`, `while`, and tracing. | Explain each iteration of a loop and fix an off-by-one error. |
| 3 | Functions, lists, strings, indexing, and slicing. | Turn a plain-English task into a function with a return value. |
| 4 | Dictionaries, sets, errors, and small integrated programs. | Build a word-frequency report and explain its data structures. |
| 5 | Parts 2, 3, and 6: execution, debugging, complexity, and problem-solving. | Compare two approaches and justify their costs. |
| 6 | Review Part 4. Implement a linked list, stack, queue, and a small hash table with guidance. Preview recursion and sorting. | Trace references, explain basic operations, and use the Part 6 worksheet. |

Week 6 is an initial pass through structures. Trees, heaps, graphs, and other structures return in detail when the roadmap reaches them.

### Weeks 7–19: Arrays, searching, lists, stacks, and heaps

| Week | Training problems | Main emphasis |
|---:|---|---|
| 7 | 1–4 | Basic array processing, membership, and value-to-index lookup |
| 8 | 5–8 | Frequencies and grouping by a reusable key |
| 9 | 9–12 | Frequency ranking, prefix/suffix products, sets, and grid bookkeeping |
| 10 | 13–18 | Two-pointer movement and safe elimination |
| 11 | 19–24 | Fixed and variable sliding windows |
| 12 | 25–29 | Prefix sums, frequencies, and earliest positions |
| 13 | 30–33 | Binary-search boundaries and invariants |
| 14 | 34–37 | Rotated arrays and binary search on an answer |
| 15 | 38–41 | Linked-list references, reversal, and slow/fast pointers |
| 16 | 42–45 | Multi-step list operations and node mapping |
| 17 | 46–49 | Stack behavior and augmented state |
| 18 | 50–52 | Expression evaluation, monotonic stacks, first Hard stretch problem |
| 19 | 53–58 | Heaps, streaming selection, scheduling, and two-heap balancing |

### Weeks 20–32: Trees, graphs, search, greedy, and bits

| Week | Training problems | Main emphasis |
|---:|---|---|
| 20 | 59–62 | Recursive tree contracts and subtree summaries |
| 21 | 63–65 | Bottom-up tree information, BFS levels, and BST bounds |
| 22 | 66–68 | Ordered traversal, tree construction, and path-state distinctions |
| 23 | 69–71 | Tries, prefixes, and recursive wildcard matching |
| 24 | 72–75 | Grid and graph representations, visitation, and components |
| 25 | 76–79 | Component measurements, graph copying, and multi-source traversal |
| 26 | 80–82 | Topological sorting and union-find |
| 27 | 83–85 | Connectivity counts, group merging, and weighted shortest paths |
| 28 | 86–89 | Backtracking choices, progress, and output construction |
| 29 | 90–93 | Duplicate suppression, partitioning, and path-local visitation |
| 30 | 94–97 | Greedy reasoning and reachable boundaries |
| 31 | 98–100 | Interval order, overlap rules, and exchange arguments |
| 32 | 101–104 | XOR, bit counting, carries, and Python’s integer model |

### Weeks 33–40: Dynamic programming and integration

| Week | Training problems | Main emphasis |
|---:|---|---|
| 33 | 105–108 | Define 1D DP states and derive transitions |
| 34 | 109–112 | Grid DP, prefix states, and sequence states |
| 35 | 113–116 | 2D DP, subset-sum states, editing, and counting subsequences |
| 36 | 117 | Trapping Rain Water: derive brute force, stored maxima, and two pointers |
| 37 | 118 | Merge k Sorted Lists: compare scanning, sorting, heaps, and balanced merging |
| 38 | 119 | Word Ladder: graph modeling, neighbor generation, and two-sided search |
| 39 | 120 | Median of Two Sorted Arrays: derive and justify the partition search |
| 40 | Mixed assessment | Attempt unfamiliar problems, identify remaining gaps, and plan the next cycle |

### How to treat the early Hard problems

Training problems 52, 58, 68, and 116 are **stretch problems**: problems deliberately placed beyond the surrounding difficulty.

Their first attempt may be guided.

The requirement is:

1. Understand the simpler prerequisite problems.
2. Make a serious attempt.
3. Study the missing idea if needed.
4. Reconstruct it.
5. Schedule a delayed review.

They are not requirements to independently solve a Hard before continuing the rest of the course.

### When to repeat a week

Repeat or extend a topic week when:

- You cannot explain what the central state means.
- You repeatedly need the same key hint.
- You cannot reconstruct a representative solution after several days.
- You cannot distinguish the technique from a similar but unsuitable one.
- Your implementations work only after trial-and-error changes you cannot justify.

Do not repeat a whole week because of one minor syntax error.

### Worked example: deciding whether to advance

Suppose Week 11 ends like this:

```text
Fixed windows:
Can implement and explain.

Longest unique substring:
Can implement after a small reminder.

Minimum positive-sum window:
Can implement, but cannot explain why negative numbers break it.

Permutation window:
Copied most of the solution.
```

Spend additional sessions on window validity and frequency updates.

Adding another unfamiliar topic would not repair those gaps.

### Practice

1. You finish Week 14’s submissions but cannot explain why binary search on capacity is valid. Should you treat that topic as retained?
2. A Hard stretch problem takes three sessions and one hint. Does that invalidate the roadmap?
3. Why does the plan revisit data structures when their application topics begin?

<details>
<summary>Answers and explanations</summary>

1. No. You need to explain the monotonic feasibility condition and the search boundaries.
2. No. The schedule allows guided learning and extension.
3. The second pass connects operations and representations to a concrete reason for using them.

</details>

---

## 8.4 — The 120-Problem Practice Sequence

Each problem title links to its official LeetCode page. Difficulty labels were checked against the official pages for this plan.

The **learning target** column describes what to extract from the problem. It is a hint, so cover that column during independent assessments.

The order is instructional. A problem labeled Easy can still expose an unfamiliar concept.

### A. Arrays and hash maps: problems 1–12

Start with direct implementations. For example, a frequency dictionary is a suitable first solution to Majority Element. A more specialized constant-space algorithm can be a later exercise.

| Order | LeetCode problem | Level | Learning target |
|---:|---|---|---|
| 1 | [1929. Concatenation of Array](https://leetcode.com/problems/concatenation-of-array/) | Easy | Build an output list deliberately |
| 2 | [217. Contains Duplicate](https://leetcode.com/problems/contains-duplicate/) | Easy | Membership and sets |
| 3 | [242. Valid Anagram](https://leetcode.com/problems/valid-anagram/) | Easy | Compare character frequencies |
| 4 | [1. Two Sum](https://leetcode.com/problems/two-sum/) | Easy | Store earlier values and indices |
| 5 | [383. Ransom Note](https://leetcode.com/problems/ransom-note/) | Easy | Available counts versus required counts |
| 6 | [169. Majority Element](https://leetcode.com/problems/majority-element/) | Easy | Frequencies and guaranteed properties |
| 7 | [268. Missing Number](https://leetcode.com/problems/missing-number/) | Easy | Compare an expected set with observed values |
| 8 | [49. Group Anagrams](https://leetcode.com/problems/group-anagrams/) | Medium | Build a shared key for equivalent items |
| 9 | [347. Top K Frequent Elements](https://leetcode.com/problems/top-k-frequent-elements/) | Medium | Count, then select by frequency |
| 10 | [238. Product of Array Except Self](https://leetcode.com/problems/product-of-array-except-self/) | Medium | Combine prefix and suffix information |
| 11 | [128. Longest Consecutive Sequence](https://leetcode.com/problems/longest-consecutive-sequence/) | Medium | Avoid repeatedly exploring the same run |
| 12 | [36. Valid Sudoku](https://leetcode.com/problems/valid-sudoku/) | Medium | Track row, column, and box constraints |

The first ten official entries and the two remaining entries establish these names and difficulty labels. [LeetCode](https://leetcode.com/problems/concatenation-of-array/description/?utm_source=chatgpt.com)

**Checkpoint:** explain why a dictionary might store a count in one problem, an index in another, and a collection of grouped values in another.

### B. Two pointers: problems 13–18

| Order | LeetCode problem | Level | Learning target |
|---:|---|---|---|
| 13 | [125. Valid Palindrome](https://leetcode.com/problems/valid-palindrome/) | Easy | Compare inward-moving boundaries |
| 14 | [344. Reverse String](https://leetcode.com/problems/reverse-string/) | Easy | In-place swaps and termination |
| 15 | [283. Move Zeroes](https://leetcode.com/problems/move-zeroes/) | Easy | Read/write pointers and stable order |
| 16 | [167. Two Sum II: Input Array Is Sorted](https://leetcode.com/problems/two-sum-ii-input-array-is-sorted/) | Medium | Use ordering to discard candidates |
| 17 | [11. Container With Most Water](https://leetcode.com/problems/container-with-most-water/) | Medium | Justify moving the limiting side |
| 18 | [15. 3Sum](https://leetcode.com/problems/3sum/) | Medium | Fix one choice and avoid duplicate outputs |

Official problem references: [LeetCode](https://leetcode.com/problems/valid-palindrome/description/?utm_source=chatgpt.com)

**Checkpoint:** for every pointer movement, explain which candidates are discarded and why none is needed.

### C. Sliding windows: problems 19–24

| Order | LeetCode problem | Level | Learning target |
|---:|---|---|---|
| 19 | [643. Maximum Average Subarray I](https://leetcode.com/problems/maximum-average-subarray-i/) | Easy | Update a fixed-size window |
| 20 | [219. Contains Duplicate II](https://leetcode.com/problems/contains-duplicate-ii/) | Easy | Restrict membership to a recent region |
| 21 | [3. Longest Substring Without Repeating Characters](https://leetcode.com/problems/longest-substring-without-repeating-characters/) | Medium | Repair a duplicate-free window |
| 22 | [209. Minimum Size Subarray Sum](https://leetcode.com/problems/minimum-size-subarray-sum/) | Medium | Shrink a qualifying positive-sum window |
| 23 | [424. Longest Repeating Character Replacement](https://leetcode.com/problems/longest-repeating-character-replacement/) | Medium | Express validity using counts |
| 24 | [567. Permutation in String](https://leetcode.com/problems/permutation-in-string/) | Medium | Compare frequencies inside a fixed window |

Official problem references: [LeetCode](https://leetcode.com/problems/maximum-average-subarray-i/description/?utm_source=chatgpt.com)

**Checkpoint:** explain why “the answer is a substring” does not, by itself, justify a sliding window.

### D. Prefix sums: problems 25–29

| Order | LeetCode problem | Level | Learning target |
|---:|---|---|---|
| 25 | [1480. Running Sum of 1d Array](https://leetcode.com/problems/running-sum-of-1d-array/) | Easy | Maintain a cumulative total |
| 26 | [724. Find Pivot Index](https://leetcode.com/problems/find-pivot-index/) | Easy | Relate left, current, and right totals |
| 27 | [303. Range Sum Query: Immutable](https://leetcode.com/problems/range-sum-query-immutable/) | Easy | Answer ranges by prefix subtraction |
| 28 | [560. Subarray Sum Equals K](https://leetcode.com/problems/subarray-sum-equals-k/) | Medium | Count matching earlier prefix sums |
| 29 | [525. Contiguous Array](https://leetcode.com/problems/contiguous-array/) | Medium | Transform a balance condition into a sum |

Official problem references: [LeetCode](https://leetcode.com/problems/running-sum-of-1d-array/description/?utm_source=chatgpt.com)

**Checkpoint:** distinguish storing prefix-sum frequencies from storing earliest prefix positions.

### E. Binary search: problems 30–37

| Order | LeetCode problem | Level | Learning target |
|---:|---|---|---|
| 30 | [704. Binary Search](https://leetcode.com/problems/binary-search/) | Easy | Preserve a search interval |
| 31 | [35. Search Insert Position](https://leetcode.com/problems/search-insert-position/) | Easy | Find a boundary rather than only equality |
| 32 | [278. First Bad Version](https://leetcode.com/problems/first-bad-version/) | Easy | Search a monotonic yes/no property |
| 33 | [74. Search a 2D Matrix](https://leetcode.com/problems/search-a-2d-matrix/) | Medium | Translate between representations |
| 34 | [153. Find Minimum in Rotated Sorted Array](https://leetcode.com/problems/find-minimum-in-rotated-sorted-array/) | Medium | Identify which region contains the break |
| 35 | [33. Search in Rotated Sorted Array](https://leetcode.com/problems/search-in-rotated-sorted-array/) | Medium | Use a sorted half to eliminate candidates |
| 36 | [875. Koko Eating Bananas](https://leetcode.com/problems/koko-eating-bananas/) | Medium | Search a feasible processing rate |
| 37 | [1011. Capacity To Ship Packages Within D Days](https://leetcode.com/problems/capacity-to-ship-packages-within-d-days/) | Medium | Separate feasibility from optimization |

Official problem references: [LeetCode](https://leetcode.com/problems/binary-search/description/?utm_source=chatgpt.com)

**Checkpoint:** state the meaning of both boundaries before writing the loop.

### F. Linked lists: problems 38–45

| Order | LeetCode problem | Level | Learning target |
|---:|---|---|---|
| 38 | [206. Reverse Linked List](https://leetcode.com/problems/reverse-linked-list/) | Easy | Preserve the next reference before rewiring |
| 39 | [21. Merge Two Sorted Lists](https://leetcode.com/problems/merge-two-sorted-lists/) | Easy | Reuse nodes and maintain a tail |
| 40 | [876. Middle of the Linked List](https://leetcode.com/problems/middle-of-the-linked-list/) | Easy | Slow and fast pointer movement |
| 41 | [141. Linked List Cycle](https://leetcode.com/problems/linked-list-cycle/) | Easy | Detect repeated movement through a cycle |
| 42 | [19. Remove Nth Node From End of List](https://leetcode.com/problems/remove-nth-node-from-end-of-list/) | Medium | Maintain a pointer gap |
| 43 | [143. Reorder List](https://leetcode.com/problems/reorder-list/) | Medium | Combine finding, reversing, and merging |
| 44 | [2. Add Two Numbers](https://leetcode.com/problems/add-two-numbers/) | Medium | Carry state through unequal-length inputs |
| 45 | [138. Copy List with Random Pointer](https://leetcode.com/problems/copy-list-with-random-pointer/) | Medium | Map original nodes to copied nodes |

Official problem references: [LeetCode](https://leetcode.com/problems/reverse-linked-list/description/?utm_source=chatgpt.com)

**Checkpoint:** draw or trace node identities. Equal values do not imply that two references identify the same node.

### G. Stacks and monotonic stacks: problems 46–52

| Order | LeetCode problem | Level | Learning target |
|---:|---|---|---|
| 46 | [20. Valid Parentheses](https://leetcode.com/problems/valid-parentheses/) | Easy | Resolve the latest unfinished opener |
| 47 | [232. Implement Queue using Stacks](https://leetcode.com/problems/implement-queue-using-stacks/) | Easy | Reverse order through transfer |
| 48 | [496. Next Greater Element I](https://leetcode.com/problems/next-greater-element-i/) | Easy | Keep unresolved values on a monotonic stack |
| 49 | [155. Min Stack](https://leetcode.com/problems/min-stack/) | Medium | Maintain an additional summary |
| 50 | [150. Evaluate Reverse Polish Notation](https://leetcode.com/problems/evaluate-reverse-polish-notation/) | Medium | Preserve operand order |
| 51 | [739. Daily Temperatures](https://leetcode.com/problems/daily-temperatures/) | Medium | Resolve waiting indices |
| 52 | [84. Largest Rectangle in Histogram](https://leetcode.com/problems/largest-rectangle-in-histogram/) | Hard | Determine maximal spans from boundaries |

Official problem references: [LeetCode](https://leetcode.com/problems/valid-parentheses/description/?utm_source=chatgpt.com)

**Checkpoint:** explain why many pops inside a loop can still produce linear total work.

### H. Heaps and priority queues: problems 53–58

| Order | LeetCode problem | Level | Learning target |
|---:|---|---|---|
| 53 | [1046. Last Stone Weight](https://leetcode.com/problems/last-stone-weight/) | Easy | Repeatedly select the largest values |
| 54 | [703. Kth Largest Element in a Stream](https://leetcode.com/problems/kth-largest-element-in-a-stream/) | Easy | Preserve only the useful candidates |
| 55 | [215. Kth Largest Element in an Array](https://leetcode.com/problems/kth-largest-element-in-an-array/) | Medium | Compare sorting and bounded-heap approaches |
| 56 | [973. K Closest Points to Origin](https://leetcode.com/problems/k-closest-points-to-origin/) | Medium | Rank objects by a derived key |
| 57 | [621. Task Scheduler](https://leetcode.com/problems/task-scheduler/) | Medium | Combine availability, frequency, and cooldown |
| 58 | [295. Find Median from Data Stream](https://leetcode.com/problems/find-median-from-data-stream/) | Hard | Balance lower and upper halves |

Official problem references: [LeetCode](https://leetcode.com/problems/last-stone-weight/description/?utm_source=chatgpt.com)

**Checkpoint:** distinguish a heap’s root guarantee from a fully sorted sequence.

### I. Trees and binary search trees: problems 59–68

| Order | LeetCode problem | Level | Learning target |
|---:|---|---|---|
| 59 | [104. Maximum Depth of Binary Tree](https://leetcode.com/problems/maximum-depth-of-binary-tree/) | Easy | Define a recursive return value |
| 60 | [100. Same Tree](https://leetcode.com/problems/same-tree/) | Easy | Compare structure and values |
| 61 | [226. Invert Binary Tree](https://leetcode.com/problems/invert-binary-tree/) | Easy | Transform subtrees consistently |
| 62 | [543. Diameter of Binary Tree](https://leetcode.com/problems/diameter-of-binary-tree/) | Easy | Separate returned height from best path |
| 63 | [110. Balanced Binary Tree](https://leetcode.com/problems/balanced-binary-tree/) | Easy | Combine validity with subtree information |
| 64 | [102. Binary Tree Level Order Traversal](https://leetcode.com/problems/binary-tree-level-order-traversal/) | Medium | Process one BFS layer at a time |
| 65 | [98. Validate Binary Search Tree](https://leetcode.com/problems/validate-binary-search-tree/) | Medium | Carry bounds from all ancestors |
| 66 | [230. Kth Smallest Element in a BST](https://leetcode.com/problems/kth-smallest-element-in-a-bst/) | Medium | Use ordered traversal |
| 67 | [105. Construct Binary Tree from Preorder and Inorder Traversal](https://leetcode.com/problems/construct-binary-tree-from-preorder-and-inorder-traversal/) | Medium | Divide a reconstruction problem |
| 68 | [124. Binary Tree Maximum Path Sum](https://leetcode.com/problems/binary-tree-maximum-path-sum/) | Hard | Distinguish an extendable path from a completed path |

Official problem references: [LeetCode](https://leetcode.com/problems/maximum-depth-of-binary-tree/description/?utm_source=chatgpt.com)

**Checkpoint:** before writing recursive code, finish this sentence:

> “For a subtree rooted at this node, my function returns…”

For maximum-path problems, the value returned to a parent may differ from the best answer found inside the subtree.

### J. Tries: problems 69–71

| Order | LeetCode problem | Level | Learning target |
|---:|---|---|---|
| 69 | [208. Implement Trie](https://leetcode.com/problems/implement-trie-prefix-tree/) | Medium | Store shared prefixes and word endings |
| 70 | [648. Replace Words](https://leetcode.com/problems/replace-words/) | Medium | Stop at the appropriate matching prefix |
| 71 | [211. Design Add and Search Words Data Structure](https://leetcode.com/problems/design-add-and-search-words-data-structure/) | Medium | Branch when a wildcard permits alternatives |

Official problem references: [LeetCode](https://leetcode.com/problems/implement-trie-prefix-tree/description/?utm_source=chatgpt.com)

**Checkpoint:** explain why reaching a trie node does not necessarily mean a complete stored word ends there.

### K. Basic graph traversal: problems 72–79

| Order | LeetCode problem | Level | Learning target |
|---:|---|---|---|
| 72 | [733. Flood Fill](https://leetcode.com/problems/flood-fill/) | Easy | Traverse a connected region |
| 73 | [463. Island Perimeter](https://leetcode.com/problems/island-perimeter/) | Easy | Count boundaries without double counting |
| 74 | [1971. Find if Path Exists in Graph](https://leetcode.com/problems/find-if-path-exists-in-graph/) | Easy | Build adjacency and test reachability |
| 75 | [200. Number of Islands](https://leetcode.com/problems/number-of-islands/) | Medium | Count connected components |
| 76 | [695. Max Area of Island](https://leetcode.com/problems/max-area-of-island/) | Medium | Aggregate information during traversal |
| 77 | [133. Clone Graph](https://leetcode.com/problems/clone-graph/) | Medium | Preserve identity and cycles while copying |
| 78 | [994. Rotting Oranges](https://leetcode.com/problems/rotting-oranges/) | Medium | Start BFS from multiple sources |
| 79 | [417. Pacific Atlantic Water Flow](https://leetcode.com/problems/pacific-atlantic-water-flow/) | Medium | Reverse the direction of the question |

Official problem references: [LeetCode](https://leetcode.com/problems/flood-fill/description/?utm_source=chatgpt.com)

**Checkpoint:** define the graph before selecting the traversal. A grid is a representation, not a separate category of algorithm.

### L. Dependencies, union-find, and shortest paths: problems 80–85

| Order | LeetCode problem | Level | Learning target |
|---:|---|---|---|
| 80 | [207. Course Schedule](https://leetcode.com/problems/course-schedule/) | Medium | Detect impossible dependency cycles |
| 81 | [210. Course Schedule II](https://leetcode.com/problems/course-schedule-ii/) | Medium | Construct a valid dependency order |
| 82 | [684. Redundant Connection](https://leetcode.com/problems/redundant-connection/) | Medium | Detect an edge joining an existing component |
| 83 | [1319. Number of Operations to Make Network Connected](https://leetcode.com/problems/number-of-operations-to-make-network-connected/) | Medium | Relate spare connections and component counts |
| 84 | [721. Accounts Merge](https://leetcode.com/problems/accounts-merge/) | Medium | Join groups through shared identifiers |
| 85 | [743. Network Delay Time](https://leetcode.com/problems/network-delay-time/) | Medium | Use weighted shortest paths |

Official problem references: [LeetCode](https://leetcode.com/problems/course-schedule/description/?utm_source=chatgpt.com)

**Checkpoint:** explain when BFS, Dijkstra, topological sorting, and union-find answer different questions.

### M. Backtracking: problems 86–93

| Order | LeetCode problem | Level | Learning target |
|---:|---|---|---|
| 86 | [78. Subsets](https://leetcode.com/problems/subsets/) | Medium | Enumerate include/exclude choices |
| 87 | [46. Permutations](https://leetcode.com/problems/permutations/) | Medium | Track used choices |
| 88 | [77. Combinations](https://leetcode.com/problems/combinations/) | Medium | Avoid counting order as a new selection |
| 89 | [39. Combination Sum](https://leetcode.com/problems/combination-sum/) | Medium | Allow controlled reuse |
| 90 | [90. Subsets II](https://leetcode.com/problems/subsets-ii/) | Medium | Avoid duplicate results |
| 91 | [40. Combination Sum II](https://leetcode.com/problems/combination-sum-ii/) | Medium | Combine one-use choices with duplicate handling |
| 92 | [131. Palindrome Partitioning](https://leetcode.com/problems/palindrome-partitioning/) | Medium | Generate valid partitions |
| 93 | [79. Word Search](https://leetcode.com/problems/word-search/) | Medium | Maintain and undo path-local visitation |

Official problem references: [LeetCode](https://leetcode.com/problems/subsets/description/?utm_source=chatgpt.com)

**Checkpoint:** distinguish “this choice cannot work” from “this choice has not worked yet.” Pruning requires a reason.

### N. Greedy algorithms and intervals: problems 94–100

| Order | LeetCode problem | Level | Learning target |
|---:|---|---|---|
| 94 | [121. Best Time to Buy and Sell Stock](https://leetcode.com/problems/best-time-to-buy-and-sell-stock/) | Easy | Preserve the best earlier purchase |
| 95 | [455. Assign Cookies](https://leetcode.com/problems/assign-cookies/) | Easy | Justify a locally economical assignment |
| 96 | [55. Jump Game](https://leetcode.com/problems/jump-game/) | Medium | Maintain the reachable boundary |
| 97 | [45. Jump Game II](https://leetcode.com/problems/jump-game-ii/) | Medium | Group progress into minimum-step layers |
| 98 | [56. Merge Intervals](https://leetcode.com/problems/merge-intervals/) | Medium | Sort and combine overlaps |
| 99 | [57. Insert Interval](https://leetcode.com/problems/insert-interval/) | Medium | Separate before, overlapping, and after regions |
| 100 | [435. Non-overlapping Intervals](https://leetcode.com/problems/non-overlapping-intervals/) | Medium | Connect removal to compatible selection |

Official problem references: [LeetCode](https://leetcode.com/problems/best-time-to-buy-and-sell-stock/description/?utm_source=chatgpt.com)

**Checkpoint:** give an exchange argument or another correctness argument for the greedy choice.

### O. Bit manipulation: problems 101–104

| Order | LeetCode problem | Level | Learning target |
|---:|---|---|---|
| 101 | [136. Single Number](https://leetcode.com/problems/single-number/) | Easy | Use XOR cancellation |
| 102 | [191. Number of 1 Bits](https://leetcode.com/problems/number-of-1-bits/) | Easy | Inspect or remove set bits |
| 103 | [338. Counting Bits](https://leetcode.com/problems/counting-bits/) | Easy | Reuse a smaller integer’s bit count |
| 104 | [371. Sum of Two Integers](https://leetcode.com/problems/sum-of-two-integers/) | Medium | Separate sum bits from carry bits |

Official problem references: [LeetCode](https://leetcode.com/problems/single-number/description/?utm_source=chatgpt.com)

**Checkpoint:** before solving problem 104 with negative inputs in Python, revisit fixed-width masks and signed interpretation. Python integers do not automatically overflow like fixed-width integers.

### P. Dynamic programming: problems 105–116

| Order | LeetCode problem | Level | Learning target |
|---:|---|---|---|
| 105 | [70. Climbing Stairs](https://leetcode.com/problems/climbing-stairs/) | Easy | Derive a recurrence from the last move |
| 106 | [198. House Robber](https://leetcode.com/problems/house-robber/) | Medium | Compare taking and skipping |
| 107 | [213. House Robber II](https://leetcode.com/problems/house-robber-ii/) | Medium | Reduce a circular constraint to cases |
| 108 | [322. Coin Change](https://leetcode.com/problems/coin-change/) | Medium | Optimize over possible final coins |
| 109 | [62. Unique Paths](https://leetcode.com/problems/unique-paths/) | Medium | Combine incoming counts |
| 110 | [64. Minimum Path Sum](https://leetcode.com/problems/minimum-path-sum/) | Medium | Change counting into cost minimization |
| 111 | [139. Word Break](https://leetcode.com/problems/word-break/) | Medium | Define a solvable-prefix state |
| 112 | [300. Longest Increasing Subsequence](https://leetcode.com/problems/longest-increasing-subsequence/) | Medium | Define a sequence ending at an index |
| 113 | [1143. Longest Common Subsequence](https://leetcode.com/problems/longest-common-subsequence/) | Medium | Use a two-prefix state |
| 114 | [416. Partition Equal Subset Sum](https://leetcode.com/problems/partition-equal-subset-sum/) | Medium | Form a 0/1 subset-sum state |
| 115 | [72. Edit Distance](https://leetcode.com/problems/edit-distance/) | Medium | Model operations as state transitions |
| 116 | [115. Distinct Subsequences](https://leetcode.com/problems/distinct-subsequences/) | Hard | Count ways to match two prefixes |

Official problem references: [LeetCode](https://leetcode.com/problems/climbing-stairs/description/?utm_source=chatgpt.com)

**Checkpoint:** for every DP solution, write:

1. State definition.
2. Base cases.
3. Transition.
4. Evaluation order.
5. Location of the final answer.
6. Time and space complexity.

For Longest Increasing Subsequence, learn the quadratic DP first. Then study the faster method as a separate improvement.

### Q. Hard capstones: problems 117–120

| Order | LeetCode problem | Level | Learning target |
|---:|---|---|---|
| 117 | [42. Trapping Rain Water](https://leetcode.com/problems/trapping-rain-water/) | Hard | Derive and compare multiple approaches |
| 118 | [23. Merge k Sorted Lists](https://leetcode.com/problems/merge-k-sorted-lists/) | Hard | Combine sorted structure with efficient selection |
| 119 | [127. Word Ladder](https://leetcode.com/problems/word-ladder/) | Hard | Improve a graph representation and its search |
| 120 | [4. Median of Two Sorted Arrays](https://leetcode.com/problems/median-of-two-sorted-arrays/) | Hard | Search an answer-defining partition |

Official problem references: [LeetCode](https://leetcode.com/problems/trapping-rain-water/description/?utm_source=chatgpt.com)

These four were fully explained in Part 7. Here, they are **reconstruction and explanation tasks**. They cannot serve as evidence that you independently discovered an unfamiliar Hard solution.

### Practice

1. Why should you cover the learning-target column during a mixed assessment?
2. You solved Two Sum in Part 7. How should you use it when reaching training problem 4?
3. Why is it reasonable to revisit Missing Number after studying XOR?

<details>
<summary>Answers and explanations</summary>

1. The column reveals useful techniques and removes part of the recognition task.
2. Reconstruct it without notes, explain the operation order, and test it. Record it as a review rather than a first discovery.
3. A new technique can produce a different solution. Comparing approaches helps you understand their assumptions and tradeoffs.

</details>

---

## 8.5 — The Spaced-Repetition System

**Spaced repetition** means revisiting material after delays instead of concentrating every repetition into one sitting.

The goal is not to reread every solution on a fixed calendar. The goal is to retrieve the important decisions before checking your notes.

### A starting schedule

Let **Day 0** be the day you first understand and reconstruct a solution.

The following dates are measured from Day 0.

| Review | When | What to do |
|---|---|---|
| Initial reconstruction | Day 0 | Close the explanation and rebuild the key steps |
| Review 1 | Day 1 | Explain the idea and trace a small example |
| Review 2 | Day 3 | Reconstruct the state and important updates |
| Review 3 | Day 7 | Write a complete solution from a blank editor |
| Review 4 | Day 14 | Solve a variation or reconstruct the proof |
| Review 5 | Day 30 | Complete a cold reconstruction |
| Review 6 | Day 60 | Use it in mixed practice or solve a related problem |

A **cold reconstruction** means starting without first reviewing the solution, notes, or pattern label.

These are target intervals. If a review falls during exams or a busy day, move it. A small delay is preferable to abandoning the system.

### What counts as a successful review?

For a quick review, you should be able to state:

- The key representation.
- The meaning of the state.
- The central update.
- Why that update is correct.
- One important edge case.
- The complexity.

For a full coding review, also produce working code and test it.

Do not count “I remembered that the answer uses a dictionary” as a successful review.

### Adapt the schedule to the result

| Result | Next action |
|---|---|
| Correct explanation and implementation without help | Move to a longer interval |
| Correct idea, small syntax issue | Repair it and keep the general schedule |
| Forgot a central invariant or transition | Review the concept and retry after 1–3 days |
| Remembered code but could not explain it | Return to derivation and counterexamples |
| Needed the complete solution again | Mark as Studied or Rebuilt and restart with shorter delays |
| Solved a related variation independently | Mark evidence of transfer |

A conceptual failure deserves more attention than a forgotten method name.

### Prevent the review queue from growing without limit

If every problem receives six long recoding sessions, the workload becomes excessive.

Use three review sizes:

| Size | Typical duration | Purpose |
|---|---:|---|
| Concept review | 3–5 minutes | Retrieve the invariant, recurrence, or decision rule |
| Trace review | 5–10 minutes | Follow state changes on a revealing input |
| Full reconstruction | 20–45 minutes or more | Rebuild and test the implementation |

Reserve full reconstructions for:

- Problems that taught an important pattern.
- Problems where you needed substantial help.
- Problems with recurring implementation errors.
- Problems whose logic you can no longer explain.

For several easy problems that teach the same idea, a representative reconstruction plus shorter reviews may be enough.

### Worked example: reviewing Two Sum

**Day 1**

Without notes, explain:

```text
For current value x, the partner must be target - x.
The dictionary maps earlier values to positions.
Check before insertion.
```

**Day 3**

Trace:

```python
nums = [3, 3]
target = 6
```

Explain why the two positions are different.

**Day 7**

Write the function from a blank editor and test it.

**Day 14**

Consider a variation:

> Return whether any pair exists, rather than its indices.

Explain why a set can now be sufficient.

**Day 30**

Reconstruct Two Sum without being told that it is a hash-map problem.

### Guided example: a failed review

You revisit longest target-sum subarray and remember the prefix-sum equation, but you store the most recent position instead of the earliest.

That is a conceptual error about the optimization objective.

Your corrective review should compare:

```text
For the same ending boundary:
earlier start -> longer section
later start -> shorter section
```

Then trace `[0, 0]`, target `0`.

### Practice

1. Are Days 1, 3, 7, and 14 intervals added to one another or dates measured from Day 0?
2. You remember the algorithm but forget whether Python uses `append` or `push` for a list. Should the whole concept restart at Day 0?
3. You have 15 reviews due. How should you avoid turning the day into several hours of mandatory recoding?

<details>
<summary>Answers and explanations</summary>

1. In this plan, they are dates measured from Day 0.
2. Usually no. Check the syntax and distinguish that issue from forgetting the algorithm.
3. Use short concept reviews, prioritize weak and important problems, and select a small number for full reconstruction. Reduce new work when necessary.

</details>

---

## 8.6 — Keep a Mistake Log That Changes Your Practice

A mistake log should identify causes.

This entry is too vague:

```text
Binary search was hard.
```

This entry is actionable:

```text
I mixed an included right boundary with an excluded right boundary.
The two-element case exposed the error.
I need to state the interval convention before writing the loop.
```

### Classify the mistake

| Category | What failed | Appropriate repair |
|---|---|---|
| Contract | You solved the wrong requested behavior | Restate inputs, outputs, and constraints |
| Representation | You modeled the problem poorly | Identify the actual objects and relationships |
| Pattern selection | You chose an unjustified technique | Check assumptions and build counterexamples |
| State definition | Variables or DP states omitted necessary information | Define each state precisely |
| Transition | The update did not match the state | Derive the update again |
| Implementation | Correct plan, incorrect code | Find the first incorrect state |
| Complexity | The method performs too much work | Identify the dominant operation |
| Testing | Important cases were never checked | Build tests from assumptions |
| Explanation | You could not justify the method | Write a correctness argument |
| Retention | Previously learned reasoning was unavailable | Shorten the next retrieval interval |

### The mistake-log template

```text
Problem:
Date:
Attempt type:
Help used:

Expected behavior:
What my solution did:

First incorrect assumption or state:
Smallest revealing example:

Root cause:
Correct principle:

Repair exercise:
Next review:
```

**Root cause** means the underlying reason the mistake occurred.

The final wrong answer is an outcome. The root cause might be an incorrect boundary convention or an incomplete state.

### Worked entry

```text
Problem:
Longest Substring Without Repeating Characters

Attempt type:
Independent review

Help used:
A failing example supplied by the judge

Expected behavior:
"abba" should produce 2.

What my solution did:
Returned 3.

First incorrect state:
At the final "a", left moved backward from 2 to 1.

Smallest revealing example:
"abba"

Root cause:
I treated every previous occurrence as if it were inside the window.

Correct principle:
The left boundary must never move backward.

Repair exercise:
Trace "abba", "tmmzuxt", and a string with all unique characters.

Next review:
Explain and implement again in three days.
```

### Convert repeated errors into targeted drills

If the same category appears repeatedly, pause new problems and practice that category.

Examples:

**Repeated boundary mistakes**

Trace these cases for the relevant algorithm:

- Empty input, if allowed.
- One element.
- Two elements.
- Target before all values.
- Target after all values.
- Duplicate boundary values.

**Repeated recursion mistakes**

For each function, write:

```text
Input meaning:
Return meaning:
Base case:
Smaller subproblem:
How recursive results combine:
```

**Repeated DP mistakes**

Write the state in a complete sentence before writing the recurrence.

Poor:

```text
dp[i] is the answer.
```

Better:

```text
dp[i] is the fewest coins needed to form amount i.
```

**Repeated graph mistakes**

Before coding, identify:

```text
Vertices:
Edges:
Directed or undirected:
Weighted or unweighted:
What visited means:
When a vertex becomes visited:
```

### Track independence separately from correctness

Use these help codes:

| Code | Help received |
|---|---|
| H0 | No solution or pattern hints |
| H1 | Syntax or documentation lookup |
| H2 | Small conceptual hint |
| H3 | The main technique or recurrence was supplied |
| H4 | Full explanation or implementation was studied |

An H4 solution can be a valuable learning session. It should not be reported as an independent solve.

For strict assessments, use H0. For ordinary learning, record help honestly and continue.

### Review the log weekly

At the end of each week, identify:

1. The most frequent error category.
2. One error that no longer recurs.
3. One concept that needs another worked example.
4. One targeted drill for the next week.

You do not need to reread every historical entry.

### Practice

1. “I forgot to remove a cell from the path set during backtracking.” Which category best fits if your written plan correctly included cleanup?
2. You used sliding window on arbitrary signed sums without checking whether shrinking was safe. Which category fits?
3. Why record the smallest revealing example?

<details>
<summary>Answers and explanations</summary>

1. Implementation. The plan was correct, but the code omitted an operation.
2. Pattern selection, caused by an unchecked assumption.
3. A small example makes the failure easy to trace and becomes a focused regression test.

</details>

---

## 8.7 — Practice Explaining Solutions Aloud

An explanation should make the algorithm’s decisions understandable.

Listing code statements is not enough.

Compare:

> “I make a dictionary, run a loop, and update the answer.”

with:

> “For each ending boundary, I need an earlier prefix sum equal to the current sum minus the target. I store the earliest position for each prefix sum because it gives the longest possible section ending here.”

The second explanation connects state to purpose.

### The seven-part explanation

Use this order:

1. **Contract:** what is given and what must be returned.
2. **Baseline:** the direct correct approach.
3. **Bottleneck:** the repeated work.
4. **Insight:** the relationship that removes it.
5. **State and updates:** what is maintained and how it changes.
6. **Correctness:** why the method covers the needed possibilities.
7. **Complexity and tests:** what the work costs and what might break.

### Start with two-minute explanations

You do not need to explain every line aloud.

For Two Sum:

```text
The input is a list and a target. I must return two different indices.

The direct approach checks every pair, which takes quadratic time.

For a current value x, the required partner is target - x.

I keep a dictionary of earlier values and their positions.

I check for the partner before adding the current value, so a match
must come from an earlier position.

When the later member of the valid pair appears, the earlier member
is already available.

The expected time is linear and the extra space is linear.

I would test equal values at different positions, negative numbers,
and a pair near the end.
```

### Then add a trace

Choose one input that exposes an important decision.

For longest unique substring, `"abba"` is more useful than `"abcd"` because it demonstrates why the left boundary must not move backward.

For Coin Change, `[1, 3, 4]` with amount `6` demonstrates why the greedy choice fails.

For Word Search, a failed branch demonstrates why cleanup matters.

### Score the explanation

Give each category:

- `0`: missing or incorrect.
- `1`: partly correct but vague.
- `2`: precise and correct.

| Category | Maximum score |
|---|---:|
| Contract | 2 |
| Brute force and bottleneck | 2 |
| State meaning | 2 |
| Update rule | 2 |
| Correctness | 2 |
| Complexity | 2 |
| Edge cases | 2 |

A score is a diagnostic, not a certificate.

If your weakest category is correctness, the next session should include proof practice. Another implementation alone may not fix it.

### Useful follow-up questions

After your explanation, ask:

- Why is this information sufficient?
- What input assumption makes this move safe?
- What changes if duplicates are allowed?
- What changes if numbers can be negative?
- Why does the algorithm terminate?
- Can the same state occur through different histories?
- Is the output itself large enough to determine a lower bound on time?

### Practice speaking without narrating every keystroke

During a coding session:

1. Explain the plan before coding.
2. State the meaning of important variables.
3. Explain significant decisions.
4. Pause briefly when concentrating on syntax.
5. Return to explanation when testing or revising.

You do not need continuous commentary to demonstrate understanding.

### Guided example

You say:

> “This is \(O(n)\) because it has one loop.”

Improve it:

> “The right pointer visits each position once. The left pointer only moves forward and advances at most \(n\) times across the entire run. The total number of pointer moves is linear.”

That explanation also handles the inner `while` loop.

### Practice

1. Improve: “BFS works because it uses a queue.”
2. Improve: “The DP transition takes the minimum.”
3. Why is a revealing counterexample useful in a spoken explanation?

<details>
<summary>Answers and explanations</summary>

1. “BFS processes vertices in increasing numbers of edges from the start. Because each move has the same cost, first discovery gives a shortest distance.”
2. “Every construction has a final choice. I examine each allowed final choice and combine it with the best solution for the remaining state, then select the smallest valid total.”
3. It shows which assumption matters and why a tempting alternative fails.

</details>

---

## 8.8 — How to Tell When You Are Ready for Hard Problems

There are two different goals:

1. Be ready to **learn from** a Hard problem.
2. Be ready to **solve an unfamiliar Hard independently**.

You can begin learning from Hards before you consistently solve them independently.

### Readiness is specific to a topic

You might be ready for a heap-based Hard while still needing guidance on a medium DP problem.

Use prerequisite relationships.

| Hard problem | Useful prerequisites |
|---|---|
| Largest Rectangle in Histogram | Stack behavior, next-greater/smaller reasoning, boundary widths |
| Find Median from Data Stream | Min-heaps, max-heaps, balancing two groups |
| Binary Tree Maximum Path Sum | Recursive return contracts, subtree summaries, negative-value cases |
| Distinct Subsequences | Two-dimensional prefix states and counting transitions |
| Trapping Rain Water | Running maxima, two pointers, safe elimination |
| Merge k Sorted Lists | Merge two lists, heap selection, tie-breaking |
| Word Ladder | BFS distances, sets, graph modeling |
| Median of Two Sorted Arrays | Binary-search invariants and boundary reasoning |

Do not wait until you know every topic before trying the Hard associated with one well-understood topic.

### A practical gate for independent attempts

For the relevant topic, aim to demonstrate:

- Two representative Medium solutions reconstructed after a delay.
- At least one related problem solved without being told the pattern.
- A correct brute-force approach when an optimized solution is unclear.
- A precise definition of the state.
- An explanation of the invariant or recurrence.
- Correct handling of small and unusual inputs.
- A justified complexity analysis.

These are my training criteria, not a validated universal threshold.

### What a useful Hard attempt looks like

A useful attempt may produce:

```text
Correct problem model.
Correct brute force.
A clear bottleneck.
A failed idea with a counterexample.
A promising representation.
An unresolved proof obligation.
```

That is more valuable than an unexplained implementation that happens to pass.

However, it is still different from an independent solution. Record the distinction.

### A three-session approach for your first Hards

**Session 1: Derive**

- Restate the problem.
- Enumerate small cases.
- Build brute force.
- Identify repeated work.
- Try to disprove candidate improvements.

**Session 2: Resolve**

- Review the exact unresolved question.
- Take the smallest useful hint if necessary.
- Write the invariant or recurrence.
- Implement and test.

**Session 3: Reconstruct**

After a delay:

- Start with a blank editor.
- Explain the solution before coding.
- Rebuild it.
- Compare at least two approaches.
- Change one condition and discuss the effect.

### Measure independent performance on unfamiliar problems

The four Hard capstones from Part 7 are familiar. Rebuilding them measures retention.

For unfamiliar assessment, choose a problem whose explanation and code you have not studied. Avoid reading its topic tags first.

Possible later assessments include:

| Problem | Official level |
|---|---|
| [76. Minimum Window Substring](https://leetcode.com/problems/minimum-window-substring/) | Hard |
| [85. Maximal Rectangle](https://leetcode.com/problems/maximal-rectangle/) | Hard |
| [297. Serialize and Deserialize Binary Tree](https://leetcode.com/problems/serialize-and-deserialize-binary-tree/) | Hard |
| [329. Longest Increasing Path in a Matrix](https://leetcode.com/problems/longest-increasing-path-in-a-matrix/) | Hard |

These four are separate from the core 120. [LeetCode](https://leetcode.com/problems/minimum-window-substring/description/?utm_source=chatgpt.com)

If you already know a listed solution, select another unfamiliar problem.

### What counts as an independent solve?

For this plan:

1. You did not read a solution or receive the central technique.
2. You developed the important state and transitions yourself.
3. Your implementation passes relevant tests.
4. You can justify correctness.
5. You can justify complexity.
6. You can explain why at least one tempting alternative fails or is less suitable.

A solution reached over two honest sessions can still be independent. Independence does not require a 30-minute timer.

### Do not turn “Hard” into a promise about every Hard

The label includes many different kinds of difficulty:

- Combining familiar techniques.
- Finding an unusual representation.
- Designing a subtle DP state.
- Proving a greedy choice.
- Managing a complex implementation.
- Knowing a specialized algorithm outside this course.

The intended outcome is the ability to solve a growing range of unfamiliar Hards and to investigate the rest systematically.

### Practice

1. You can reproduce Median of Two Sorted Arrays after reading Part 7. Does that demonstrate independent discovery?
2. You solve a new Hard in two sessions without hints and can justify it. Does taking two sessions disqualify it?
3. You struggle with an unfamiliar specialized algorithm. Does that show all your previous progress was ineffective?

<details>
<summary>Answers and explanations</summary>

1. No. It demonstrates reconstruction or retention, depending on the delay and help used.
2. No. The independence criterion concerns the source of the reasoning, not an arbitrary timer.
3. No. Identify the missing prerequisite and learn it. Hard problems do not all require the same knowledge.

</details>

---

## 8.9 — Avoid the Traps That Produce Lots of Activity and Little Learning

### Trap 1: Memorizing complete implementations

Symptoms:

- You can type the remembered code.
- You cannot explain a boundary update.
- A changed condition makes the solution collapse.

Correction:

- Re-derive the state.
- Trace a counterexample.
- Change the requested output.
- Explain which stored information must change.

For example:

```text
Count target-sum subarrays:
Store prefix frequencies.

Longest target-sum subarray:
Store earliest prefix positions.
```

The difference must make sense without memorizing two separate templates.

### Trap 2: Watching several explanations before trying

A worked example can be useful. Repeated passive exposure can also hide what you cannot yet produce.

Use this rule:

> After one explanation, close it and produce something.

That might be:

- A trace.
- Pseudocode.
- A correctness argument.
- A complete implementation.
- A counterexample to a wrong approach.

If you cannot produce anything, identify the specific missing concept before watching more.

### Trap 3: Reading the pattern label first

During early learning, a labeled topic helps.

During assessment, the label removes part of the task.

Alternate between:

- Topic-focused practice.
- Mixed practice with the category hidden.

This mixture is called **interleaving**: combining different kinds of problems so you must decide which approach applies.

Begin with a small mixed set. Do not randomize your entire learning sequence before understanding any technique.

### Trap 4: Chasing submission speed too early

A timer can help reveal how you spend time, but speed is not the first objective.

First establish:

1. Correct interpretation.
2. Correct reasoning.
3. Correct implementation.
4. Reliable testing.
5. Clear explanation.

Then improve speed by reducing repeated confusion.

### Trap 5: Treating every failure as a reason to change patterns

If your code fails one test, inspect the first incorrect state.

The technique may be correct while the implementation has a boundary error.

Randomly replacing the algorithm prevents you from learning the cause.

### Trap 6: Skipping brute force

Without a baseline, you may not know:

- What candidates exist.
- What work must be avoided.
- How to generate expected answers for small tests.

A correct slow solution is often the best starting point for an efficient one.

### Trap 7: Optimizing before defining the state

Especially in DP, begin with a clear table.

Only reduce memory after you know:

- Which earlier states are required.
- In what order they must be available.
- Whether overwriting a value changes the meaning of later updates.

A one-array implementation is not an improvement if you cannot explain why it is correct.

### Trap 8: Using AI to make the central decisions

AI can help teach, review, and generate tests. It can also remove the very decisions you need to practice.

Useful prompts:

```text
Do not give me the solution.
Ask me one question that will help me identify the repeated work.
```

```text
Here is my invariant.
Find a small input that would disprove it if it is wrong.
```

```text
Review my complexity explanation.
Point out hidden operations I failed to count.
```

```text
I understand the solution.
Give me one variation that tests whether I understand its assumptions.
Do not include the answer yet.
```

During an independent assessment, keep solution-generating assistance closed. If you use it, record the help level.

### Trap 9: Practicing only comfortable problems

Comfortable reviews help retention, but they should not consume every session.

Use the mistake log to select one manageable weakness at a time.

Avoid the opposite extreme too: repeatedly attempting problems for which you lack several prerequisites.

### Trap 10: Maintaining a streak at the expense of the plan

A daily streak counts days with activity. It does not measure understanding.

A short maintenance session can be useful during a busy week. Submitting an already memorized one-line answer solely to preserve a counter does not repair a weak concept.

### Worked example

You have completed ten sliding-window problems but fail a prefix-sum problem because you keep trying to shrink when a signed sum becomes too large.

The repair is not another ten ordinary windows.

Compare:

- Positive-sum windows.
- Arbitrary signed sums.
- Prefix-sum equations.

Write the condition that makes each method valid.

### Practice

1. Why can constant access to topic tags hide a weakness?
2. What should you do after one complete solution video?
3. When is an AI hint compatible with productive learning?

<details>
<summary>Answers and explanations</summary>

1. The tags choose a candidate technique for you. You may become good at implementing a named pattern without learning to recognize it.
2. Close it and reconstruct a concrete part of the solution without looking.
3. When it addresses a specific blockage, preserves as much reasoning as possible, and is recorded honestly rather than counted as independent discovery.

</details>

---

## 8.10 — Free Resources and Exactly When to Use Them

Use one main learning sequence. Supplement it when you identify a particular gap.

Starting several complete courses at once can consume the time intended for solving and review.

### 1. CS50’s Introduction to Programming with Python

[CS50P](https://cs50.harvard.edu/python/)

The course is designed for learners with or without programming experience. Its free OpenCourseWare includes Python instruction and exercises covering fundamentals, exceptions, testing, and other topics. [cs50.harvard.edu](https://cs50.harvard.edu/python/?utm_source=chatgpt.com)

**Use it when:** Weeks 1–4 reveal gaps in basic Python.

**How to use it:**

- Choose the lesson matching your current gap.
- Complete the associated exercises.
- Return to this roadmap after you can write the relevant constructs independently.

You do not need to finish all of CS50P before solving the first Easy problems.

### 2. University of Helsinki’s Python Programming MOOC

[Python Programming MOOC 2026](https://programming-26.mooc.fi/)

The University of Helsinki provides introductory material in Parts 1–7 and advanced material in Parts 8–14, with programming exercises throughout the course structure. [Python Programming MOOC 2026](https://programming-26.mooc.fi/?utm_source=chatgpt.com)

**Use it when:** you need more small programming exercises before algorithm problems.

**How to use it:**

- Work through an appropriate exercise sequence.
- Type your own solution.
- Use failures to identify a missing language concept.

Choose this or CS50P as your main supplementary fundamentals course. You do not need both in full.

### 3. Python Tutor

[Python Tutor](https://pythontutor.com/)

Python Tutor visualizes code execution, variables, objects, references, and stack frames in the browser. Its core visualization tool is free. [Python Online Compiler with Visual Debugger](https://pythontutor.com/?utm_source=chatgpt.com)

**Use it when:** you are confused about what the program does at a particular step.

Useful targets:

- Two names referring to one list.
- List mutation.
- Linked-list rewiring.
- Function calls.
- Recursive returns.

**How to use it:**

1. Predict the next state.
2. Advance one step.
3. Compare your prediction with the actual state.
4. Explain the difference.

Do not only watch the animation.

### 4. VisuAlgo

[VisuAlgo](https://visualgo.net/en)

VisuAlgo provides interactive visualizations for data structures and algorithms, including graph traversal and heaps. It supports experimenting with inputs in its visualization tools. [VisuAlgo](https://visualgo.net/en?utm_source=chatgpt.com)

**Use it when:** you understand the operations verbally but need to see their structural effect.

**How to use it:**

- Choose a small custom input.
- Predict the next operation.
- Run the step.
- Reproduce the same trace on paper or in a table.

### 5. MIT OpenCourseWare 6.006

[Introduction to Algorithms](https://ocw.mit.edu/courses/6-006-introduction-to-algorithms-fall-2011/)

This course provides lecture videos, notes, assignments, and exams covering algorithm design and analysis. The materials are freely available through MIT OpenCourseWare. [MIT OpenCourseWare](https://ocw.mit.edu/courses/6-006-introduction-to-algorithms-fall-2011/?utm_source=chatgpt.com)

**Use it when:** you already know basic Python and want deeper explanations of algorithms, correctness, and complexity.

**How to use it:**

- Select a lecture matching the current roadmap topic.
- Work a related exercise afterward.
- Translate any older Python syntax into the Python 3 conventions used in this paper.

Do not treat a university lecture sequence as a substitute for your own implementation practice.

### 6. Official Python documentation

[Python tutorial and reference](https://docs.python.org/3/tutorial/)

The official tutorial explicitly assumes general programming knowledge. Use it as a reference after learning the basics, rather than as your only introduction from zero. [Python 3.14.8 documentation](https://docs.python.org/3/tutorial/?utm_source=chatgpt.com)

**Use it when:** you need the exact behavior of an operation.

Examples:

- Does a method mutate the object?
- What does the method return?
- What happens when a key is absent?
- Which arguments does a library function accept?

### A resource-selection rule

| Current blockage | Best first action |
|---|---|
| You cannot write a loop or function | Fundamentals lesson and small exercises |
| You cannot follow changing references | Python Tutor |
| You cannot picture heap or graph operations | VisuAlgo |
| You need deeper correctness or analysis | MIT material |
| You forgot a Python method’s behavior | Official documentation |
| You cannot recognize a familiar pattern | Mixed problem practice and comparison |
| You keep repeating one mistake | Targeted drill from the mistake log |

More resources are not automatically better. The resource should answer a specific question.

### Practice

1. You understand recursion verbally but cannot follow the call stack. Which resource is a strong fit?
2. You repeatedly forget whether a list method changes the list or returns a new one. What should you consult?
3. Why should you avoid starting three full beginner courses at once?

<details>
<summary>Answers and explanations</summary>

1. Python Tutor, used with predictions before each step.
2. Official Python documentation, followed by a tiny experiment.
3. The overlap can consume practice time without addressing the particular weaknesses that need work.

</details>

---

## 8.11 — Your Final Assessment and the Next Training Cycle

Finishing the core list is a useful milestone. It does not end the learning process.

The next decision should depend on evidence from your work.

### Week 40 assessment

Use several sessions rather than one exhausting test.

| Session | Task |
|---|---|
| 1 | Cold reconstruction of one earlier Easy and one earlier Medium |
| 2 | An unfamiliar Medium with topic labels hidden |
| 3 | Another unfamiliar Medium from a different area |
| 4 | Begin an unfamiliar Hard |
| 5 | Continue that Hard without solution assistance, or record the precise missing idea |
| 6 | Review results, explain solutions aloud, and classify weaknesses |
| 7 | Plan the next cycle or take a light review day |

Choose unfamiliar assessment problems from techniques you have actually studied. A test of an unlearned specialized algorithm measures a different gap.

### Record more than pass or fail

For each assessment, record:

```text
Did I understand the contract correctly?
Did I produce a correct brute force?
Did I identify the bottleneck?
Did I select the technique independently?
Did I define the state precisely?
Could I explain correctness?
Did I implement the plan?
Did my tests expose important cases?
Was my complexity analysis accurate?
What help did I use?
```

### Interpret the result

| Result | Next training focus |
|---|---|
| Good reasoning, frequent syntax trouble | Short implementation drills |
| Good implementation after hints, weak recognition | Mixed unlabeled problems |
| Correct approach, recurring boundary bugs | Small-case traces and invariants |
| Strong familiar solutions, weak variations | Transfer exercises |
| Good immediate performance, poor delayed recall | More retrieval and fewer new problems |
| Strong Medium performance, weak Hard decomposition | Multi-session Hard attempts and bottleneck analysis |
| Weak DP states | Return to smaller state-definition exercises |
| Weak graph modeling | Practice defining vertices, edges, and objectives |

### A four-week continuation cycle

After the initial roadmap, use a focused cycle.

| Week | Work |
|---:|---|
| 1 | Repair the weakest concept with two representative problems and targeted drills |
| 2 | Solve three or four related variations with decreasing support |
| 3 | Mix those problems with other topics, hiding labels |
| 4 | Attempt one unfamiliar Hard and perform delayed reviews |

Then evaluate again.

Do not respond to every weakness by downloading a new list of 200 problems.

### A weekly dashboard

Keep the record small enough that you will actually use it.

```text
Week:
Topic:
Study sessions completed:

New problems attempted:
Problems rebuilt:
Delayed reviews passed:
Unfamiliar problems solved without central hints:

Most common error:
Most useful counterexample:
Concept needing repair:

Next week's main objective:
```

A useful weekly objective is:

> “Explain why each binary-search boundary update preserves the answer.”

Another is:

> “Define complete DP states before writing recurrences.”

“Become better at coding” is too broad to guide the next session.

### Worked example: choosing the next cycle

Suppose your results show:

```text
Arrays and hashing:
Strong.

Trees:
Can solve familiar recursion problems.

Graphs:
Often choose DFS without checking whether the problem asks for
shortest distance.

DP:
Can implement a recurrence once it is supplied.

Retention:
Generally good after one week.
```

Your next cycle should emphasize:

1. Graph objective recognition.
2. DP state and transition derivation.
3. A small amount of tree review.

Repeating many easy hash-map problems would not address the observed gaps.

### Final independent exercises

1. Build your first seven-day schedule. Give every session a concrete output.
2. Choose three problems from the catalog and assign an initial help level and review plan.
3. Write a mistake-log entry for a real or hypothetical off-by-one error.
4. Explain one familiar solution aloud using the seven-part structure.
5. Define the evidence you will require before labeling a solution “Retained.”

<details>
<summary>Example answers and evaluation criteria</summary>

**1. Seven-day schedule**

An acceptable first week might include:

- Run a Python file and evaluate expressions.
- Write a program using variables and input conversion.
- Use conditionals to classify values.
- Trace a `for` loop.
- Trace and repair a `while` loop.
- Write two short functions without copying.
- Review errors and identify the next weak concept.

If you are starting later, replace these with the appropriate topic tasks.

**2. Problems and reviews**

For a new problem:

- Record the help actually used.
- Reconstruct on Day 0.
- Explain on Day 1.
- Trace on Day 3.
- Recode on Day 7.

Adjust later reviews according to performance.

**3. Mistake-log entry**

The entry should identify:

- The intended boundary meaning.
- The incorrect update.
- A small failing input.
- The corrected rule.
- A future test or drill.

**4. Spoken explanation**

Check whether it includes:

- Contract.
- Baseline.
- Bottleneck.
- Insight.
- State and updates.
- Correctness.
- Complexity and tests.

**5. Retained**

A useful criterion is:

> “After a meaningful delay, I can reconstruct the solution without reviewing it first, explain its central reasoning, and test important edge cases.”

Immediate repetition alone is insufficient.

</details>

---

## Running Glossary — Part 8 Additions

| Term | Meaning |
|---|---|
| Familiarity | Recognizing material when you see it |
| Retrieval | Producing remembered information without looking at it |
| Transfer | Applying an understood idea to a different problem |
| Faded practice | Gradually reducing guidance |
| Deliberate practice | Targeted work on a weakness with feedback and adjustment |
| Spaced repetition | Revisiting material after delays |
| Cold reconstruction | Rebuilding a solution without first reviewing it |
| Interleaving | Mixing problem types so you must select the approach |
| Stretch problem | A problem deliberately beyond the surrounding difficulty |
| Root cause | The underlying reason an error occurred |
| Rubric | A set of criteria used to assess work |
| Maintenance session | A short session intended to preserve existing knowledge |
| Independent solve | A solution whose central reasoning you developed without solution hints |

---

## Final Course Readiness Checklist

You have reached the intended outcome when you can repeatedly demonstrate these behaviors:

- Translate an unfamiliar statement into a precise contract.
- Work through small examples before coding.
- Produce a correct brute-force approach.
- Identify repeated work or another bottleneck.
- Select a data structure because of the operations it supports.
- Check the assumptions behind a pattern.
- Define state precisely.
- Explain why the algorithm is correct.
- Implement it in Python.
- Test cases designed to challenge its assumptions.
- Analyze time and space honestly.
- Learn from a failed attempt without immediately copying a solution.
- Reconstruct important ideas after a delay.
- Solve related variations.
- Independently solve an increasing range of unfamiliar Hard problems.

**End of Part 8. This completes the eight-part text of “From Zero to LeetCode Hard.”**
