# From Zero to LeetCode Hard

A Python study paper for someone starting with no programming experience.

This installment contains the complete table of contents and Part 1 only.

The parts stay consistently numbered so they can become one manuscript. The examples have been checked by hand and against Python’s documented behavior. Expected results are included so you can check them as you work. The final PDF will require file-generation access when that stage is reached.

## How to read the difficulty estimates

The scale below describes difficulty within this course. It does not predict how quickly you will learn.

| Level | Meaning |
| --- | --- |
| 1/5 | No programming background required. |
| 2/5 | Combines several basic ideas. |
| 3/5 | Requires reasoning about efficiency and multiple moving parts. |
| 4/5 | Requires selecting and adapting an algorithm. |
| 5/5 | Requires combining techniques, proving key properties, or discovering a difficult insight. |

A program is a set of instructions a computer can execute. An algorithm is a precise method for solving a problem. A program can implement an algorithm.

## Complete table of contents

| Part | Difficulty | Detailed contents | What you will be able to do afterward |
| --- | --- | --- | --- |
| 1. Programming Foundations | 1–2/5 | Running Python; variables; values and types; arithmetic and comparisons; conditionals; loops; functions; lists; strings; dictionaries; sets; error messages; a combined practice project; running glossary. | Write small programs from a blank file, process collections of information, and explain what each line does. |
| 2. How a Computer Actually Thinks | 2/5 | Memory and stored objects; names and references; execution order; function calls; the call stack; mutable and immutable objects; shared references; copying; tracing tables; debugging; expected results; edge cases; automated checks. | Predict program behavior, locate the cause of an error, and design tests that expose incorrect assumptions. |
| 3. Big-O and Complexity Analysis | 2–3/5 | Counting operations; input size; growth rates; time and space complexity; constant, logarithmic, linear, linearithmic, quadratic, exponential, and factorial growth; nested loops; recursive algorithms; auxiliary space; amortized cost; Python operation costs; interpreting input constraints. | Estimate whether an approach is practical and justify its time and memory requirements. |
| 4. Core Data Structures | 2–4/5 | Arrays and Python lists; strings; hash maps and sets; linked lists; stacks; queues; deques; heaps and priority queues; binary trees; binary search trees; tries; graphs using adjacency lists and matrices; union-find. A short introduction to Python classes will precede structures that need custom objects. | Choose a suitable structure, implement its core behavior, explain its memory organization, and compare operation costs. |
| 5. Core Algorithms and Patterns | 3–5/5 | Recursion; sorting; binary search; binary search on the answer; two pointers; sliding windows; prefix sums; intervals; depth-first and breadth-first search; backtracking; greedy algorithms; topological sorting; Dijkstra’s algorithm; bit manipulation; monotonic stacks; dynamic programming in depth. | Recognize common problem structures, trace standard algorithms, and adapt them to unfamiliar questions. |
| 6. How to Think Like a Coder | 3–5/5 | A ten-step problem-solving process; examples and counterexamples; brute force; bottlenecks; choosing structures and patterns; pseudocode; correctness arguments; testing; complexity; optimization; a recognition cheat sheet; a procedure for getting unstuck. | Turn an unfamiliar statement into a reasoned solution without relying on a memorized answer. |
| 7. Fully Worked LeetCode Problems | 2–5/5 | Four Easy, six Medium, and four Hard problems. Every problem includes manual examples, an initial approach, its limitations, the key improvement, trace tables, commented code, complexity, mistakes, edge cases, and related practice. Hard problems include progressively stronger approaches. | Follow the complete process from an initial idea to a justified solution, then reproduce that process independently. |
| 8. The Training Plan | Progressive | A week-by-week plan at roughly 1.5 hours per day; approximately 120 curated problems; practice by pattern followed by mixed practice; error logs; spaced review; spoken explanations; readiness checks for Hard problems; free supplementary resources. | Organize sustained practice, measure actual understanding, and identify what to study next. |

## The internal order of Part 5

This is the longest instructional part. Its chapters will follow this sequence:

| Chapter | Topic | Why it appears here |
| --- | --- | --- |
| 5.1 | Recursion | Establishes how a function can solve a smaller version of its own problem. |
| 5.2 | Sorting | Introduces order as a useful property and applies recursion where appropriate. |
| 5.3 | Binary search | Uses ordered information to discard possibilities. |
| 5.4 | Two pointers | Coordinates two positions within a sequence. |
| 5.5 | Sliding windows | Maintains information about a changing consecutive region. |
| 5.6 | Prefix sums | Reuses totals already computed. |
| 5.7 | Intervals | Combines sorting with reasoning about overlapping ranges. |
| 5.8 | DFS and BFS | Explores connected structures using previously learned stacks and queues. |
| 5.9 | Backtracking | Extends recursion into systematic exploration of choices. |
| 5.10 | Greedy algorithms | Studies when a locally chosen action can lead to a globally correct result. |
| 5.11 | Topological sorting | Handles tasks with prerequisites. |
| 5.12 | Dijkstra’s algorithm | Combines graph exploration, greedy reasoning, and a priority queue. |
| 5.13 | Binary search on the answer | Searches possible answers using a yes-or-no feasibility test. |
| 5.14 | Bit manipulation | Works directly with binary representations of integers. |
| 5.15 | Monotonic stacks | Maintains a useful order while processing a sequence. |
| 5.16 | Dynamic programming foundations | Moves from repeated recursive work to stored answers. |
| 5.17 | Memoization and tabulation | Compares remembering recursive results with building a table directly. |
| 5.18 | State definitions and transitions | Teaches how to specify exactly what each stored answer means. |
| 5.19 | One-dimensional and two-dimensional DP | Handles decisions described by one or two changing quantities. |
| 5.20 | Knapsack and sequence DP | Develops recurring families of decision and matching problems. |
| 5.21 | Space optimization and reconstruction | Reduces storage and, when needed, recovers the choices behind an answer. |

You do not need to understand those terms yet. Each will be defined before use.

## Planned worked problems for Part 7

The suggested progression is retained, including all four suggested Hard problems.

| Stage | Problems | Main purpose |
| --- | --- | --- |
| Easy | Two Sum; Valid Parentheses; Best Time to Buy and Sell Stock; Merge Two Sorted Lists | Introduce lookup tables, stacks, maintaining useful information, and linked-list manipulation. |
| Medium | Longest Substring Without Repeating Characters; Number of Islands; Coin Change; Course Schedule; Top K Frequent Elements; Word Search | Develop windows, graph exploration, dynamic programming, dependencies, frequency selection, and backtracking. |
| Hard | Trapping Rain Water; Merge k Sorted Lists; Word Ladder; Median of Two Sorted Arrays | Combine techniques and study why more efficient approaches are correct. |

The course will prepare you to work toward independent Hard solutions. Completing a fixed number of weeks or problems does not guarantee mastery of every Hard problem.

# Part 1: Programming Foundations

## What you will build toward

By the end of this part, you will be able to write a function that examines a sentence and reports:

- How many words it contains.
- How many different words appear.
- How often each word appears.
- Which word appears first among those tied for the highest frequency.

That requires the foundations in this part. We will introduce each one before combining them.

## How the teaching sequence works

Programming makes you manage several kinds of difficulty at once: unfamiliar notation, changing values, and decisions about how to solve a problem. We will separate those difficulties where possible.

Each chapter follows this sequence:

1. Worked example: Read a complete example with explanations.
2. Guided example: Fill in a small missing decision.
3. Independent practice: Solve a nearby problem without copying.
4. Feedback: Compare your answer with the explanation.
5. Later retrieval: Recreate the idea after a delay.

Retrieval practice means trying to recall or produce an answer before looking it up. Spaced practice means returning to material across separate sessions. Faded practice means gradually removing support, moving from complete examples to partial examples to independent work.

The Institute of Education Sciences recommends spacing learning, alternating worked examples with problem solving, and using active retrieval. Those recommendations inform this course’s structure. They do not establish one universal schedule for every learner. Source: ies.ed.gov

For this course, deliberate practice means selecting a specific weakness, attempting a task that exposes it, checking the result, and correcting your approach. “Do more problems” is too vague. “Practice choosing the correct starting value for a running total or maximum” is specific.

We will also use a beginner version of Pólya’s problem-solving framework:

1. Understand the problem.
2. Make a plan.
3. Carry out the plan.
4. Check the result and what you learned.

Part 6 will expand this into the requested ten-step process.

For now, do not attempt to memorize every page. Predict what a program will do, run it, and explain any difference between your prediction and the result.

## Chapter 1.1: What code is and how to run it

### The basic model

Imagine writing instructions for a person who follows them literally but cannot infer missing steps.

“Calculate my total” is incomplete. The person needs to know:

- Which numbers to use.
- Which calculation to perform.
- Where to put the result.

Programming requires that precision.

Code is the written form of instructions in a programming language.

A programming language is a system of notation with rules for expressing computations.

Python is the programming language we will use.

An interpreter is software that executes Python programs. Python’s internal execution process has additional steps, which we will examine later. For now, your working model is that the interpreter carries out your instructions.

### Why Python fits this goal

Python is a good first language for algorithm practice because:

- Basic programs require little setup or surrounding code.
- Common operations use readable notation.
- It includes useful collection types.
- You can test small ideas interactively.
- You can express an algorithm without spending as much effort on low-level memory management.

Python does not remove the need to understand algorithms. A poor approach can still take too long, even if its code is short.

### A free setup

Use Thonny, a Python editor designed for beginners. Its official site provides installation options and describes its beginner-focused interface and debugging features. Source: thonny.org

An editor is a program for writing and changing text files.

An IDE, short for integrated development environment, combines an editor with tools for running and inspecting programs. Thonny is an IDE.

Set it up as follows:

1. Open the official Thonny website.
2. Select the installation option for your operating system.
3. Install and open Thonny.
4. Create a new file.
5. Type the program below.
6. Save the file as lesson_01.py.
7. Use Run → Run current script.

A file extension is the ending of a filename. The .py extension identifies a Python source file.

A script is a file containing a program that you run.

### Your first program

```python
# Display a message.
print("Hello, Saket!")

# Calculate a number and display the result.
print(2 + 3)
```

Expected output:

```
Hello, Saket!
5
```

Output is information a program produces. Here, the output appears in Thonny’s Shell area.

A comment explains code to a human reader. In these examples, a comment starts with # and continues to the end of the line. Python does not execute the comment.

print is a function, a named operation you can ask Python to perform.

A function call asks a function to run. In print(2 + 3), the parentheses contain what we give the function.

An argument is a value supplied to a function call. Here, Python calculates 2 + 3, then supplies the resulting value, 5, to print.

The quotation marks in "Hello, Saket!" identify text. They do not appear in the printed output.

### Instructions versus results

Write this in your editor:

```python
# This is an instruction.
print(2 + 3)
```

Do not also type the expected output 5 underneath it merely because the textbook shows it.

Likewise, if you see >>> in another Python tutorial, that is usually an interactive prompt. It is not part of the code to paste into a script.

### A small vocabulary distinction

An expression is code that produces a value.

Examples:

```python
2 + 3
"hello"
```

A statement is an instruction Python executes. Assignment, which we learn next, is one kind of statement.

In a script, writing an expression alone usually does not display it:

```python
# Calculate 5, but do not display it.
2 + 3

# Calculate 5 and display it.
print(2 + 3)
```

### Common misconception

“If Python calculated something, I should see it.”

A calculation and displaying its result are different actions. An interactive shell may display an expression automatically. A script usually requires print.

### Practice

1. Guided: Write one line that displays I am learning Python.
2. Independent: Display the result of 8 + 4.
3. Prediction: What does this program display?

```python
# One argument is text. The other is an arithmetic expression.
print("8 + 4")
print(8 + 4)
```

#### Answers and explanations

1.

```python
# Display the text inside the quotation marks.
print("I am learning Python")
```

2.

```python
# Add the numbers before displaying the result.
print(8 + 4)
```

Output:

```
12
```

3.

```
8 + 4
12
```

Quotation marks make the first argument text. Python does not perform arithmetic inside an ordinary quoted string.

## Chapter 1.2: Variables and assignment

### Analogy first

Think of a variable as a label attached to a value.

You can attach the label score to the value 10. Later, you can move that label to the value 15.

In Python, this label analogy is more accurate than imagining that every variable is a separate box holding a private copy. Part 2 will explain why that matters.

A value is a piece of information, such as 10 or "Saket".

A variable is a name that refers to a value.

### Creating a variable

```python
# Make the name score refer to the integer 10.
score = 10

# Read the value associated with score and display it.
print(score)
```

Output:

```
10
```

The = symbol performs assignment: it makes a name refer to the result of an expression.

Read:

```python
score = 10
```

as:

Assign the value 10 to the name score.

Do not read it as a mathematical claim that must remain true forever.

### The right side is evaluated first

To evaluate an expression means to determine its value.

```python
# Begin with 10 points.
score = 10

# Read the old score, add 5, then assign the result to score.
score = score + 5

# Display the updated score.
print(score)
```

Output:

```
15
```

The middle line works in this order:

1. Find the current value of score: 10.
2. Calculate 10 + 5: 15.
3. Make score refer to 15.

This is why score = score + 5 makes sense in programming even though it would not be a valid ordinary algebraic equation.

### Worked trace

A trace is a step-by-step record of execution.

```python
# Start with three items.
items = 3

# Add two items.
items = items + 2

# Double the current number of items.
items = items * 2

# Display the final amount.
print(items)
```

| Executed instruction | Calculation | items afterward |
| --- | --- | --- |
| items = 3 | Use 3 | 3 |
| items = items + 2 | 3 + 2 | 5 |
| items = items * 2 | 5 * 2 | 10 |
| print(items) | Display current value | 10 |

The * symbol means multiplication.

### One assignment does not establish a permanent relationship

```python
# Assign an initial value.
a = 4

# Make b refer to the current value of a.
b = a

# Reassign a.
a = 9

# Display both values, separated by a space.
print(a, b)
```

Output:

```
9 4
```

b = a does not mean “keep b synchronized with a forever.”

print can accept several arguments separated by commas. By default, it displays them separated by spaces.

### Naming variables

Use names that describe meaning:

```python
# Clear names explain what the values represent.
student_count = 30
maximum_score = 100
user_name = "Saket"
```

For now, follow these rules:

- Start names with a letter.
- Use letters, digits, and underscores afterward.
- Do not use spaces.
- Capitalization matters: score and Score are different names.
- Do not use language words such as if or for.
- Avoid naming variables print, list, or str, because those names already have useful meanings.

A keyword is a word reserved by the language for a particular purpose. if and for are keywords.

student_count follows snake_case, a naming style that separates words with underscores.

### A shorter update

```python
# Start with 10 points.
score = 10

# For this numeric example, this means score = score + 5.
score += 5

# Display 15.
print(score)
```

You will also see -=, *=, and other update operators.

We will use the longer form when it makes learning easier.

### What beginners often get wrong

Using a variable before assigning it:

print(points) cannot work unless points has already been assigned in the current execution context.

### Practice

1. Guided: Start coins at 7, add 3, then print it.
2. Prediction: What does the following program print?
3. Independent: A rectangle has width 6 and height 4. Store both values, calculate its area, and print the area.

```python
# Values change one instruction at a time.
x = 2
y = x + 3
x = 10

# Display the current values.
print(x, y)
```

#### Answers and explanations

1.

```python
# Start with seven coins.
coins = 7

# Add three to the current amount.
coins = coins + 3

# Display the new amount.
print(coins)
```

Output: 10.

2.

```
10 5
```

y receives the result of 2 + 3. Reassigning x afterward does not recalculate y.

3.

```python
# Store the dimensions.
width = 6
height = 4

# Multiply the dimensions.
area = width * height

# Display the calculated area.
print(area)
```

Output: 24.
