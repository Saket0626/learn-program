# Part 1 continued: Chapters 1.3–1.6

## Chapter 1.3: Data types, conversion, and input

A data type, or type, describes the kind of a value and the operations that make sense for it.

Compare these two values:

```python
7
"7"
```

The first represents a number. The second represents text containing the character 7.

That distinction affects what Python does.

### The first types to learn

| Python type | Meaning | Examples |
| --- | --- | --- |
| int | Integer: a whole number | 0, 12, -4 |
| float | Floating-point number: a numeric representation that can express fractional values, usually approximately | 3.5, -0.25, 2.0 |
| str | String: a sequence of text characters | "hello", "7", "" |
| bool | Boolean: one of two logical values | True, False |
| NoneType | The type of None, which often represents no result or no value | None |

A character is a unit of text, such as a letter, digit, or punctuation mark. We will refine this definition for Python strings later.

An empty string, written "", contains no characters.

### Looking at a type

The built-in function type tells you a value’s type.

A built-in is something Python supplies without requiring you to define it.

```python
# Store values of different types.
age = 18
price = 2.5
name = "Saket"
is_ready = True
result = None

# Inspect their types.
print(type(age))
print(type(price))
print(type(name))
print(type(is_ready))
print(type(result))
```

Expected output:

```
<class 'int'>
<class 'float'>
<class 'str'>
<class 'bool'>
<class 'NoneType'>
```

For now, read the word inside the quotation marks as the type’s name. We will explain Python classes before implementing custom data structures.

### The same symbol can behave differently

```python
# Add two integers.
print(7 + 2)

# Join two strings.
print("7" + "2")
```

Output:

```
9
72
```

Joining strings is called concatenation.

Python does not assume whether combining a string and an integer should mean arithmetic or text joining:

```python
# Intentionally incorrect: incompatible operands for this operation.
print("7" + 2)
```

This raises a TypeError. An error is a reported problem that prevents an operation from completing as written.

### Type conversion

Conversion means producing a value of one type from a value of another type.

```python
# Convert numeric text into an integer.
number = int("7")

# Perform integer arithmetic.
print(number + 2)

# Convert an integer into text.
message = "Score: " + str(9)

# Display the combined string.
print(message)

# Convert numeric text into a floating-point value.
print(float("2.5"))
```

Output:

```
9
Score: 9
2.5
```

Conversions must make sense.

- int("12") works.
- int("twelve") does not.
- int("3.5") does not directly parse a decimal string as an integer.
- int(3.9) produces 3, discarding the fractional part toward zero.
- int(-3.9) produces -3.

That last behavior differs from floor division, which we will discuss next.

### Reading user input

Input is information supplied to a program.

The input function displays an optional prompt, waits for you to type a line, and returns the entered text as a string.

```python
# Ask for text and store it.
name = input("What is your name? ")

# Display a greeting.
print("Hello,", name)
```

If you enter Saket, the greeting is:

```
Hello, Saket
```

When you need a number, convert the input:

```python
# Read the user's entry as a string.
age_text = input("Enter your age: ")

# Convert the string into an integer.
age = int(age_text)

# Calculate an updated age.
next_age = age + 1

# Display the result.
print("Next year:", next_age)
```

If you enter 18, the result is:

```
Next year: 19
```

For early exercises, fixed values in code are often easier than interactive input. They let you repeat the exact same experiment.

On LeetCode, you will usually receive inputs as function arguments. You generally will not need input for the standard function-based questions.

### Floating-point precision

A computer has finite storage. Many decimal fractions cannot be represented exactly in the usual floating-point format.

For example:

```python
# The stored approximations do not add to an exact decimal 0.3.
print(0.1 + 0.2)
```

A typical Python result is:

```
0.30000000000000004
```

This is not evidence that addition is broken. It reflects the representation used.

Most of our early algorithm exercises will use integers. Later, when decimal comparisons matter, we will discuss suitable comparison methods.

### Common misconception

bool("False") does not interpret the word “False.”

It produces True because the string is nonempty. Converting to a Boolean checks truthiness, a concept introduced in Chapter 1.5.

### Practice

1. Guided: Convert "25" to an integer, add 5, and print the result.
2. Prediction: What are the results of "3" + "4" and 3 + 4?
3. Independent: Ask for a whole-number quantity, convert it to an integer, multiply it by 4, and print the result.

#### Answers and explanations

1.

```python
# Convert text to a number.
number = int("25")

# Add numerically.
print(number + 5)
```

Output: 30.

2.

- "3" + "4" produces the string "34".
- 3 + 4 produces the integer 7.

3.

```python
# Read the entry as text.
quantity_text = input("Enter a whole-number quantity: ")

# Convert the text to an integer.
quantity = int(quantity_text)

# Calculate and display the result.
print(quantity * 4)
```

If the user enters 6, the result is 24.

This version assumes the user enters valid integer text. Chapter 1.12 introduces handling a failed conversion.

## Chapter 1.4: Operators and expressions

An operator is a symbol or word that performs an operation on values.

The values an operator acts on are called operands.

In 8 + 3, + is the operator. 8 and 3 are the operands.

### Arithmetic operators

| Operator | Meaning | Example | Result |
| --- | --- | --- | --- |
| + | Addition | 8 + 3 | 11 |
| - | Subtraction | 8 - 3 | 5 |
| * | Multiplication | 8 * 3 | 24 |
| / | Division | 8 / 2 | 4.0 |
| // | Floor division | 8 // 3 | 2 |
| % | Remainder | 8 % 3 | 2 |
| ** | Exponentiation | 2 ** 3 | 8 |

### Floor division and remainder

Suppose you have 17 objects and put them into groups of 5.

You can form 3 complete groups, with 2 objects left.

```python
# Count complete groups.
print(17 // 5)

# Count leftover objects.
print(17 % 5)
```

Output:

```
3
2
```

For integer values a and nonzero b, Python’s operators satisfy:

```
a = (a // b) * b + (a % b)
```

For the example:

```
17 = 3 * 5 + 2
```

### A negative-number detail

Floor means rounding down toward negative infinity.

Therefore:

```python
# -7 / 3 is approximately -2.333...
# Rounding downward gives -3.
print(-7 // 3)
```

Output:

```
-3
```

Do not define // as “remove everything after the decimal point.” That description fails for negative results.

### Checking evenness

An integer is even when dividing it by 2 leaves remainder 0.

```python
# Produce a Boolean result.
print(8 % 2 == 0)

# Nine leaves a remainder of one.
print(9 % 2 == 0)
```

Output:

```
True
False
```

### Comparison operators

A comparison tests a relationship between values.

| Operator | Meaning |
| --- | --- |
| == | Equal to |
| != | Not equal to |
| < | Less than |
| <= | Less than or equal to |
| > | Greater than |
| >= | Greater than or equal to |

For the basic values used here, these comparisons produce a Boolean.

```python
# Compare integer values.
print(5 == 5)
print(5 != 5)
print(3 < 8)
print(8 <= 8)
```

Output:

```
True
False
True
True
```

### Common misconception

= and == do different jobs.

score = 10 assigns a value.

score == 10 asks whether the current value equals 10.

### Order of operations

Precedence is the rule that determines which operations group together first.

```python
# Multiplication happens before addition.
print(2 + 3 * 4)

# Parentheses make the addition happen first.
print((2 + 3) * 4)
```

Output:

```
14
20
```

For early work:

1. Use parentheses when grouping might be unclear.
2. Remember that multiplication and division precede addition and subtraction.
3. Remember that comparisons occur after the arithmetic expressions they compare.

You do not need to memorize Python’s full precedence table today.

### Boolean operators

Boolean operators combine or change conditions.

| a | b | a and b | a or b |
| --- | --- | --- | --- |
| False | False | False | False |
| False | True | False | True |
| True | False | False | True |
| True | True | True | True |

- and: both conditions must be true.
- or: at least one condition must be true.
- not: reverses a Boolean.

```python
# Store two facts.
age = 18
has_ticket = True

# Both requirements must hold.
can_enter = age >= 18 and has_ticket

# Display the combined result.
print(can_enter)

# Reverse a Boolean.
print(not has_ticket)
```

Output:

```
True
False
```

With non-Boolean operands, Python’s and and or can return an operand rather than True or False. We will use Boolean conditions here so their purpose stays clear.

### Short-circuit evaluation

Short-circuit evaluation means Python can skip the second part of a Boolean expression when the first part already determines its outcome.

```python
# A denominator that would make division invalid.
denominator = 0

# The first condition is False.
# Python therefore skips the division on the right.
is_large = denominator != 0 and 10 / denominator > 2

# Display False without dividing by zero.
print(is_large)
```

For and, a false first condition makes the whole condition false.

For or, a true first condition makes the whole condition true.

This behavior will later help us avoid accessing nonexistent list positions.

### Practice

1. Guided: You have 23 objects and boxes that hold 4 objects. Calculate the number of full boxes and leftover objects.
2. Prediction: Evaluate 3 + 2 * 5, (3 + 2) * 5, and 7 != 7.
3. Independent: Store a number in number. Produce a Boolean that is true exactly when the number is at least 10 and at most 20.

#### Answers and explanations

1.

```python
# Store the amount and box capacity.
objects = 23
capacity = 4

# Count full boxes and remaining objects.
full_boxes = objects // capacity
leftover = objects % capacity

# Display both results.
print(full_boxes, leftover)
```

Output:

```
5 3
```

2.

- 3 + 2 * 5 gives 13.
- (3 + 2) * 5 gives 25.
- 7 != 7 gives False.

3.

```python
# Choose a value to test.
number = 15

# Require both boundaries.
in_range = number >= 10 and number <= 20

# Display the result.
print(in_range)
```

Output: True.

Python also allows 10 <= number <= 20. The longer form makes the two requirements explicit.

## Chapter 1.5: Conditionals and indentation

A conditional chooses what code to execute based on a condition.

Think of a conditional as a fork in a set of instructions:

- If a requirement holds, perform one action.
- Otherwise, perform another.

### An if statement

```python
# Store a score.
score = 75

# Execute the indented instruction only if the comparison is True.
if score >= 60:
    print("Pass")

# This instruction is outside the conditional.
print("Finished")
```

Output:

```
Pass
Finished
```

The condition is score >= 60.

The colon : ends the line introducing the controlled instructions.

Indentation means spaces at the beginning of a line.

A block is a group of statements controlled together. Python uses indentation to identify blocks.

Use four spaces per indentation level.

### Adding else

```python
# Store a score.
score = 45

# Choose exactly one of these two branches.
if score >= 60:
    print("Pass")
else:
    print("Try again")
```

Output:

```
Try again
```

A branch is one possible path through a conditional.

### More than two choices

elif means “else if.”

```python
# Store a score.
score = 82

# Test conditions in order.
if score >= 90:
    print("A")
elif score >= 80:
    print("B")
elif score >= 70:
    print("C")
else:
    print("Below C")
```

Output:

```
B
```

Python enters the first matching branch, then skips the remaining branches in that chain.

| Condition checked | Result | Action |
| --- | --- | --- |
| 82 >= 90 | False | Continue checking |
| 82 >= 80 | True | Print B |
| Remaining branches | Not checked | Skip |

### A beginner mistake: testing broad conditions first

This code runs, but its order is wrong for the intended grading rule:

```python
# Intentionally flawed ordering.
score = 95

# A score of 95 already satisfies this broad condition.
if score >= 60:
    print("Pass")
elif score >= 90:
    print("A")
```

It prints Pass. The A branch is never reached for any score of at least 90.

The fix is to test the more restrictive high-score condition first.

### Separate if statements behave differently

```python
# Store a value.
number = 12

# This condition is evaluated independently.
if number > 0:
    print("Positive")

# This condition is also evaluated independently.
if number % 2 == 0:
    print("Even")
```

Output:

```
Positive
Even
```

Use independent if statements when multiple actions may apply.

Use an if/elif/else chain when choosing one branch from a sequence.

### Nested conditionals

Nested means placed inside another structure.

```python
# Store two facts.
has_account = True
password_correct = False

# Check the outer condition.
if has_account:
    # This test happens only when has_account is True.
    if password_correct:
        print("Welcome")
    else:
        print("Incorrect password")
else:
    print("Create an account")
```

Output:

```
Incorrect password
```

Nested code needs an additional indentation level.

### Truthiness

Truthiness is how Python treats a value when a Boolean decision is required.

Common false values include:

- False
- None
- Numeric zero, such as 0
- Empty strings
- Empty collections, which we will learn shortly

A nonempty string is true in this sense.

```python
# Store an empty string.
name = ""

# An empty string is false in a conditional.
if name:
    print("A name was provided")
else:
    print("No name was provided")
```

Output:

```
No name was provided
```

Initially, explicit comparisons can be easier to read. Learn truthiness so you can understand code that uses it.

### What beginners often get wrong

Indentation is part of Python’s meaning. Moving a line out of a block changes when it executes.

Also, an else belongs to a matching if at the same indentation level.

### Practice

1. Guided: Print "Even" if number is even, otherwise print "Odd".
2. Independent: Print "Negative", "Zero", or "Positive" for a stored number.
3. Prediction: What does this program print?

```python
# Independent conditions can both succeed.
value = 10

if value >= 5:
    print("A")

if value >= 10:
    print("B")
else:
    print("C")
```

#### Answers and explanations

1.

```python
# Choose a number.
number = 7

# Check its remainder after division by two.
if number % 2 == 0:
    print("Even")
else:
    print("Odd")
```

Output: Odd.

2.

```python
# Choose a value.
number = -3

# Select one category.
if number < 0:
    print("Negative")
elif number == 0:
    print("Zero")
else:
    print("Positive")
```

Output: Negative.

3.

```
A
B
```

The first if prints A. The second if prints B. Its associated else is skipped.

## Chapter 1.6: Loops

A loop repeats a block of code.

One execution of a loop’s body is an iteration.

The body is the block of instructions controlled by the loop.

We will learn two forms:

- for: process values supplied by something you can iterate over.
- while: repeat while a condition remains true.

### A for loop

```python
# Visit the integers 0, 1, and 2.
for number in range(3):
    # Execute this line once for each visited integer.
    print(number)
```

Output:

```
0
1
2
```

range(3) represents the integer sequence starting at 0 and stopping before 3.

An iterable is something Python can obtain items from one at a time. A range is iterable. Lists and strings will also be iterable.

The name number receives the next value before the body runs.

### Understanding range

| Expression | Values visited |
| --- | --- |
| range(4) | 0, 1, 2, 3 |
| range(2, 5) | 2, 3, 4 |
| range(1, 8, 2) | 1, 3, 5, 7 |
| range(5, 0, -1) | 5, 4, 3, 2, 1 |

The general form is:

```python
range(start, stop, step)
```

The stop value is excluded.

The step is the amount added to get the next value. It cannot be zero.

A range represents the progression without constructing a full list of all its integers.

### Worked example: a running total

An accumulator is a variable that stores a result built up over repeated steps.

We want to calculate:

```
1 + 2 + 3 + 4
```

```python
# Before processing any numbers, the total is zero.
total = 0

# Visit 1, 2, 3, and 4.
for number in range(1, 5):
    # Add the current number to the accumulated total.
    total = total + number

# Display the total after the loop finishes.
print(total)
```

Output:

```
10
```

| Iteration | number | total before | Calculation | total after |
| --- | --- | --- | --- | --- |
| 1 | 1 | 0 | 0 + 1 | 1 |
| 2 | 2 | 1 | 1 + 2 | 3 |
| 3 | 3 | 3 | 3 + 3 | 6 |
| 4 | 4 | 6 | 6 + 4 | 10 |

### Why start at zero?

Because before seeing any numbers, we have added nothing. Zero represents that situation.

### A common incorrect attempt

```python
# Intentionally incorrect placement of initialization.
for number in range(1, 5):
    # This resets the previous work on every iteration.
    total = 0

    # Only the current number is retained.
    total = total + number

print(total)
```

This prints 4.

The mistake is not addition. The mistake is resetting the accumulated result inside the loop.

### A while loop

```python
# Start a countdown.
remaining = 3

# Repeat while there is time remaining.
while remaining > 0:
    # Display the current value.
    print(remaining)

    # Change the value so the loop can eventually stop.
    remaining = remaining - 1

# This executes after the loop ends.
print("Go")
```

Output:

```
3
2
1
Go
```

| Condition check | Result | Action |
| --- | --- | --- |
| 3 > 0 | True | Print 3, reduce to 2 |
| 2 > 0 | True | Print 2, reduce to 1 |
| 1 > 0 | True | Print 1, reduce to 0 |
| 0 > 0 | False | Leave the loop |

The condition is tested before each iteration. A while loop can run zero times.

### Infinite loops

An infinite loop continues without reaching a stopping condition.

If the countdown never updates remaining, its condition stays true.

When writing a while loop, identify:

1. What starts the loop?
2. What changes during an iteration?
3. Why will the condition eventually become false?

If you accidentally create an infinite loop, use Thonny’s stop control.

### break and continue

break immediately leaves the nearest enclosing loop.

```python
# Search a small range.
for number in range(1, 6):
    # Stop when the target is reached.
    if number == 3:
        break

    # This is not reached for number 3.
    print(number)
```

Output:

```
1
2
```

continue skips the remaining instructions in the current iteration and moves to the next iteration.

```python
# Visit integers from 1 through 5.
for number in range(1, 6):
    # Skip even values.
    if number % 2 == 0:
        continue

    # Display only odd values.
    print(number)
```

Output:

```
1
3
5
```

Be careful with continue in a while loop. If it skips the update needed to reach the stopping condition, the loop may never finish.

### Nested loops

```python
# Choose an outer value.
for row in range(2):
    # For each outer value, visit all three inner values.
    for column in range(3):
        # Display the current pair.
        print(row, column)
```

Output:

```
0 0
0 1
0 2
1 0
1 1
1 2
```

The inner loop completes once for every iteration of the outer loop.

Here, the print statement executes 2 × 3 = 6 times.

That counting habit will become essential in complexity analysis.

### Practice

1. Guided: Print integers 1 through 5, including 5.
2. Independent: Calculate the sum of the even integers from 1 through 10.
3. Independent: Use a while loop to print 4, 3, 2, 1.
4. Prediction: How many times does print("X") execute below?

```python
# Repeat a group of three prints twice.
for outer in range(2):
    for inner in range(3):
        print("X")
```

#### Answers and explanations

1.

```python
# Stop before 6 so that 5 is included.
for number in range(1, 6):
    print(number)
```

2.

```python
# Start before any numbers have been included.
total = 0

# Examine 1 through 10.
for number in range(1, 11):
    # Include only even values.
    if number % 2 == 0:
        total = total + number

# Display 2 + 4 + 6 + 8 + 10.
print(total)
```

Output: 30.

3.

```python
# Start at four.
number = 4

# Continue while the value remains positive.
while number > 0:
    print(number)

    # Move toward the stopping condition.
    number = number - 1
```

4. Six times. There are two outer iterations, each containing three inner iterations.
