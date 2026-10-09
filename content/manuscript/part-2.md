# From Zero to LeetCode Hard

# Part 2: How a Computer Actually Thinks

Part 1 introduced the instructions you can write. Part 2 explains what happens when those instructions execute.

The central skill is learning to answer:

At this exact point in the program, what exists, what does each name refer to, and what instruction happens next?

A computer does not infer your intention. It follows the rules of the language. When your mental prediction differs from the result, either your understanding of those rules or your implementation needs correction.

By the end of this part, you will be able to:

- Explain the relationship between variables, objects, and memory.
- Predict how shared lists behave.
- Distinguish changing an object from reassigning a variable.
- Trace function calls and returns.
- Trace loops without skipping intermediate steps.
- Investigate a bug using a specific hypothesis.
- Design tests that expose incorrect assumptions.
- Use assertions to check your functions.
- Explain why passing a few tests does not establish correctness.

The examples include expected results and checks you can run. As noted earlier, this session does not provide a Python runner, so they have been checked by hand rather than claiming execution testing.

## Chapter 2.1: Memory, stored information, and program state

### Start with a workbench analogy

Imagine a workbench containing:

- Cards holding information.
- Labels attached to those cards.
- A sheet of instructions.
- A marker showing the next instruction.

This is a useful first model of a running Python program.

| Workbench item | Programming concept |
| --- | --- |
| Cards holding information | Objects |
| Labels referring to cards | Variable names |
| Written instructions | Code |
| Current arrangement of labels and cards | Part of the program’s state |
| Marker showing where to continue | Execution position |

The analogy has limits. Real memory uses electronic representations, and Python manages additional information. Nevertheless, this model explains many beginner mistakes accurately.

### What memory means

Memory is storage a computer uses to hold information while working.

RAM, short for random-access memory, is the working memory used by running programs. Ordinary RAM does not preserve its contents when power is removed.

Persistent storage, such as an SSD, retains saved information after the program ends and normally after power is removed.

An SSD, or solid-state drive, is a common device used for persistent storage.

Saving lesson.py stores your source code as a file. Running it creates a running program with its own working information.

These are different activities:

```python
# This instruction creates a value during execution.
score = 10
```

Saving the file does not execute the assignment. Running the file does.

### Bits and bytes

A bit is a unit with two possible states, conventionally written 0 and 1.

A byte is a group of eight bits.

The computer represents information using patterns of bits. Different rules determine whether a pattern represents a number, text, an instruction, or something else.

For example, decimal 5 can be represented in binary as:

```
101
```

Binary is a number system using powers of two instead of powers of ten:

| Position value | 4 | 2 | 1 |
| --- | --- | --- | --- |
| Binary digit | 1 | 0 | 1 |
| Contribution | 4 | 0 | 1 |

Total:

4 + 0 + 1 = 5

You do not need to manipulate binary representations to write ordinary Python programs. We introduce them to explain what “stored information” means.

Also, a Python integer object containing 5 occupies more than three bits. Its representation includes information beyond the mathematical value, such as information needed by Python to manage the object.

Do not confuse:

- The number of bits needed to express a mathematical value.
- The total memory used by a Python object representing that value.

### Objects and references

An object is a value represented during Python execution, with a type and associated behavior.

A reference is a connection through which code can access an object.

Consider:

```python
# Make score refer to an integer object representing 10.
score = 10
```

The variable name score refers to the integer object.

For tracing, we can write:

| Name | Refers to |
| --- | --- |
| score | Integer value 10 |

Now execute:

```python
# Reassign score to the result of this expression.
score = score + 5
```

Python:

1. Reads the object referred to by score.
2. Uses its value, 10, in the addition.
3. Produces the result, 15.
4. Makes score refer to the result.

Afterward:

| Name | Refers to |
| --- | --- |
| score | Integer value 15 |

The integer 10 was not edited into 15. Integers are immutable.

### Program state

The state of a program is the information needed to describe its current situation.

For our traces, we will track:

- Variable names and their current values or references.
- Contents of mutable objects.
- Active function calls.
- The current execution position.
- Relevant output produced so far.

A larger real program has additional state, such as open files and network connections.

### Worked example: state changes

```python
# Create two names with initial values.
price = 4
quantity = 3

# Calculate a result using the current values.
total = price * quantity

# Change one input afterward.
quantity = 5

# Display the existing total.
print(total)
```

| After instruction | price | quantity | total | Output so far |
| --- | --- | --- | --- | --- |
| price = 4 | 4 | Not assigned | Not assigned | None |
| quantity = 3 | 4 | 3 | Not assigned | None |
| total = price * quantity | 4 | 3 | 12 | None |
| quantity = 5 | 4 | 5 | 12 | None |
| print(total) | 4 | 5 | 12 | 12 |

Changing quantity does not automatically recalculate total.

If you want an updated total, you must execute the calculation again:

```python
# Recalculate using the current quantity.
total = price * quantity

print(total)  # 20
```

### Common misconception

A variable assignment does not usually create a live formula.

`total = price * quantity` calculates a result at that moment. It does not install a permanent relationship between the three names.

### Guided example

Predict the final values before reading the explanation:

```python
# Store an initial value.
a = 6

# Calculate b using a's current value.
b = a * 2

# Reassign a.
a = 1

# Display both names.
print(a, b)
```

The result is:

```
1 12
```

b received 12 before a changed.

### Chapter practice

1. Explain the difference between saving a Python file and running it.
2. Trace the program below, recording both variables after each assignment.
3. Explain why the final printed value is not 30.

```python
# Practice problem 2.
x = 3
y = x + 4
x = y * 2
y = x - 1

print(x, y)
```

```python
# Practice problem 3.
price = 5
quantity = 2
total = price * quantity

quantity = 6

print(total)
```

#### Answers and explanations

1. Saving stores the source code in a file. Running asks Python to execute that code, creating and changing program state.

2.

| Assignment | x afterward | y afterward |
| --- | --- | --- |
| x = 3 | 3 | Not assigned |
| y = x + 4 | 3 | 7 |
| x = y * 2 | 14 | 7 |
| y = x - 1 | 14 | 13 |

Output:

```
14 13
```

3. total was calculated when quantity was 2. The stored result is 10. To calculate 30, execute:

```python
# Recalculate after changing quantity.
total = price * quantity

print(total)  # 30
```

## Chapter 2.2: Execution order and evaluating expressions

A useful first rule is:

Follow the next instruction Python actually executes, not the next line your eyes happen to notice.

Execution normally moves through statements in order, but conditionals, loops, and function calls change the path.

### Expressions have intermediate results

Consider:

```python
# Calculate a combined expression.
answer = 2 + 3 * 4
```

The right side groups as:

```
2 + (3 * 4)
```

The intermediate results are:

| Step | Expression being evaluated | Result |
| --- | --- | --- |
| 1 | 3 * 4 | 12 |
| 2 | 2 + 12 | 14 |
| 3 | Assign result to answer | answer refers to 14 |

Parentheses change grouping:

```python
# Add first because the parentheses require it.
answer = (2 + 3) * 4

print(answer)  # 20
```

### Precedence and evaluation order are related but different

Precedence determines how operators group.

Evaluation order determines when the parts of an expression are evaluated.

For ordinary Python expressions such as the following, function calls are evaluated from left to right:

```python
# Return the supplied number after displaying it.
def show(number):
    print("Evaluating:", number)
    return number


# Call show(2), then show(3), then add the returned values.
answer = show(2) + show(3)

print("Answer:", answer)
```

Expected output:

```
Evaluating: 2
Evaluating: 3
Answer: 5
```

Breaking a complicated expression into smaller assignments often makes it easier to understand:

```python
# Make the intermediate results explicit.
first = show(2)
second = show(3)
answer = first + second

print("Answer:", answer)
```

For this example, the sequence of printed messages is the same.

### Conditional execution skips instructions

```python
# Store a value.
number = 4

# Exactly one branch will execute.
if number > 10:
    result = 100
else:
    result = 200

# Continue after the conditional.
print(result)
```

The instruction `result = 100` is not executed.

A trace should not pretend every line ran.

| Event | Outcome |
| --- | --- |
| Assign number | 4 |
| Evaluate number > 10 | False |
| Execute if body | Skipped |
| Execute else body | result becomes 200 |
| Print result | 200 |

### A variable might never receive a value

```python
# Intentionally incomplete program.
score = 40

# This assignment happens only for passing scores.
if score >= 60:
    message = "Pass"

# No value was assigned to message on this path.
print(message)
```

In a fresh execution, this raises NameError.

The issue is not that Python forgot the variable. The assignment was skipped.

One correction is to handle both branches:

```python
# Store a score.
score = 40

# Assign message on every possible path.
if score >= 60:
    message = "Pass"
else:
    message = "Try again"

print(message)
```

### Short-circuiting changes execution order

Recall:

```python
# Avoid division when the denominator is zero.
denominator = 0

safe_and_large = denominator != 0 and 10 / denominator > 2
```

The division is skipped.

For a list, this can protect an index access:

```python
# An empty list has no first element.
numbers = []

# Check nonemptiness before accessing index 0.
starts_positive = len(numbers) > 0 and numbers[0] > 0

print(starts_positive)  # False
```

Reversing the conditions is unsafe:

```python
# Intentionally incorrect order for an empty list.
numbers = []

# Python tries numbers[0] before learning that the list is empty.
starts_positive = numbers[0] > 0 and len(numbers) > 0
```

This raises IndexError.

The two conditions may look mathematically interchangeable, but executing them can have different consequences.

### What beginners often get wrong

A condition can contain operations that fail.

Before accessing `numbers[index]`, establish that the position exists. A later check cannot undo an earlier invalid access.

### Assignment happens after the right side finishes

```python
# Begin with an integer.
number = 5

# The right side fails before a new assignment can finish.
# Run this separately if you want to inspect the exception.
number = 10 / 0
```

The division raises ZeroDivisionError. The assignment does not successfully replace number.

An unhandled exception stops the current execution path, so a later print in the same script would not run.

### Guided example

What happens here?

```python
# Store one value.
number = 0

# The left condition decides the result.
result = number == 0 or 10 / number > 1

print(result)
```

The result is True.

Because the first condition is true, `or` skips the division.

### Chapter practice

1. What does the first program print, and why?
2. Fix the second program so message is assigned on every path.
3. Explain why the third expression is safe for an empty list.
4. Rewrite `answer = (a + b) * (c - d)` using two intermediate variables.

```python
# Problem 1.
x = 3

if x > 5:
    x = x + 10
else:
    x = x * 2

print(x)
```

```python
# Problem 2.
temperature = 15

if temperature > 30:
    message = "Hot"

print(message)
```

```python
# Problem 3.
numbers = []

result = len(numbers) == 0 or numbers[0] == 7
```

#### Answers and explanations

1. It prints 6. `3 > 5` is false, so the else branch doubles x.

2.

```python
# Store the temperature.
temperature = 15

# Cover both possible outcomes.
if temperature > 30:
    message = "Hot"
else:
    message = "Not hot"

print(message)
```

3. `len(numbers) == 0` is true. `or` therefore skips `numbers[0] == 7`, avoiding an invalid access. The final value of result is True.

4.

```python
# Assume a, b, c, and d already have numeric values.
first_result = a + b
second_result = c - d

answer = first_result * second_result
```

The intermediate names expose the two grouped calculations.
