# Part 1 continued: Chapters 1.7–1.9

## Chapter 1.7: Functions

A function packages a task under a name.

Think of a small machine:

- You supply inputs.
- It performs a defined task.
- It may return an output.

Unlike a physical machine, a function can also perform actions such as printing. We need to distinguish those actions from returning a value.

### Defining a function

A function definition specifies the function’s name, its input names, and its body.

```python
# Define a reusable calculation.
def add_one(number):
    # Produce the result for the caller.
    return number + 1

# Call the function with the argument 4.
answer = add_one(4)

# Display the returned result.
print(answer)
```

Output:

```
5
```

New pieces:

- def introduces a function definition.
- add_one is the function name.
- number is a parameter, a name that receives an input when the function is called.
- 4 is the argument, the actual value supplied in this call.
- return ends the function call and gives a value back to the code that called it.
- The caller is the code making the function call.

Defining the function does not execute its body.

### Execution order

| Step | What happens |
| --- | --- |
| 1 | Python executes the definition, making add_one available. |
| 2 | Python reaches add_one(4). |
| 3 | The parameter number receives 4. |
| 4 | The function calculates number + 1, producing 5. |
| 5 | return gives 5 to the caller. |
| 6 | answer receives 5. |
| 7 | print(answer) displays 5. |

### More than one parameter

```python
# Define a calculation with two inputs.
def rectangle_area(width, height):
    # Multiply the dimensions and return the result.
    return width * height

# Supply arguments in the same order as the parameters.
area = rectangle_area(6, 4)

# Display the returned value.
print(area)
```

Output:

```
24
```

The first argument goes to the first parameter. The second goes to the second.

### print and return are different

```python
# This function displays a value but does not explicitly return one.
def show_double(number):
    print(number * 2)

# Call the function and store its return value.
result = show_double(5)

# Inspect what was returned.
print(result)
```

Output:

```
10
None
```

The function prints 10.

Then it reaches the end without an explicit return, so its return value is None.

Compare:

```python
# This function supplies a result to its caller.
def double(number):
    return number * 2

# Store and reuse the result.
result = double(5)

# Further calculations are possible because result is an integer.
print(result + 3)
```

Output:

```
13
```

For algorithm problems, you will usually need to return the required answer. Printing it is not a substitute.

### Early return

A function can return before reaching its final line.

```python
# Return the nonnegative magnitude of an integer.
def absolute_value(number):
    # A negative input needs its sign reversed.
    if number < 0:
        return -number

    # This line is reached only for nonnegative inputs.
    return number

# Exercise both paths.
print(absolute_value(-7))
print(absolute_value(4))
```

Output:

```
7
4
```

Once return executes, the current function call ends.

### Local variables and scope

A local variable belongs to a particular function call.

Scope describes where a name can be accessed.

```python
# Define a function with a local variable.
def calculate_total(price, quantity):
    total = price * quantity
    return total

# Store the function's result in a different name.
answer = calculate_total(3, 4)

# This name exists outside the function.
print(answer)
```

Output:

```
12
```

The local name total does not automatically become available outside the function.

For now:

- Give functions the information they need through parameters.
- Return the information they produce.
- Avoid making functions depend on unrelated changing variables elsewhere.

### Worked example: count even integers from 1 through a limit

Assume limit is a nonnegative integer.

```python
# Count even integers from 1 through limit, inclusive.
def count_evens(limit):
    # No qualifying values have been seen yet.
    count = 0

    # Visit every integer in the requested range.
    for number in range(1, limit + 1):
        # Increase the count only for even values.
        if number % 2 == 0:
            count = count + 1

    # Return after all numbers have been examined.
    return count

# The qualifying integers are 2, 4, and 6.
print(count_evens(6))
```

Output:

```
3
```

Notice where return count appears. It is outside the loop.

If placed inside the loop, it would end the function after the first iteration.

### Common misconception

A function does not “remember to finish the loop later” after return. That call ends immediately.

### Practice

1. Guided: Define square(number) to return the number multiplied by itself.
2. Independent: Define larger(a, b) to return the larger value. Either value is acceptable when they are equal.
3. Independent: Define sum_up_to(limit) to return 1 + 2 + ... + limit. Assume limit is a nonnegative integer.
4. Prediction: What does this function return for example(5)?

```python
# There can be instructions that a particular call never reaches.
def example(number):
    if number > 0:
        return 10

    return 20
```

#### Answers and explanations

1.

```python
# Return the product of a number with itself.
def square(number):
    return number * number

print(square(5))  # 25
```

2.

```python
# Compare the inputs directly.
def larger(a, b):
    if a >= b:
        return a

    return b

print(larger(3, 8))  # 8
print(larger(4, 4))  # 4
```

3.

```python
# Add all integers from 1 through limit.
def sum_up_to(limit):
    # Zero is also the correct result when limit is zero.
    total = 0

    for number in range(1, limit + 1):
        total = total + number

    return total

print(sum_up_to(4))  # 10
print(sum_up_to(0))  # 0
```

4. It returns 10. The first return ends the call, so the second return is not reached.

## Chapter 1.8: Lists

A collection stores multiple values together.

A list is an ordered, changeable collection of items.

Ordered means items have positions. It does not mean the values are sorted.

A sequence is a collection organized by position. Lists and strings are sequences.

### Creating and accessing a list

```python
# Store three scores in order.
scores = [72, 85, 91]

# Display the first score.
print(scores[0])

# Display the third score.
print(scores[2])

# Display how many items the list contains.
print(len(scores))
```

Output:

```
72
91
3
```

An element is an item in a collection.

An index is a position used to access an element.

Python list indices begin at zero.

| Index | Element |
| --- | --- |
| 0 | 72 |
| 1 | 85 |
| 2 | 91 |

If a list contains n elements, its nonnegative valid indices run from 0 through n - 1.

len returns the number of elements.

### Negative indices

```python
# Store three values.
scores = [72, 85, 91]

# Access from the end.
print(scores[-1])
print(scores[-2])
```

Output:

```
91
85
```

-1 means the last item. -2 means the second-to-last item.

### Changing a list

A mutable object can be changed after creation. Lists are mutable.

An object is a Python value stored during program execution, together with its type and associated behavior.

```python
# Create a list.
scores = [72, 85, 91]

# Replace the item at index 1.
scores[1] = 88

# Add an item at the end.
scores.append(95)

# Display the updated list.
print(scores)
```

Output:

```
[72, 88, 91, 95]
```

A method is an operation accessed through an object, usually with a dot.

scores.append(95) calls the list’s append method.

### Common list operations

| Operation | Meaning |
| --- | --- |
| items.append(value) | Add one item at the end |
| items.pop() | Remove and return the last item |
| items.pop(index) | Remove and return the item at that position |
| items.remove(value) | Remove the first matching value |
| len(items) | Obtain the item count |
| value in items | Check whether an equal value appears |
| items[index] | Access one item |
| items[index] = value | Replace one item |

pop fails when its requested position does not exist. remove fails when the requested value does not appear.

```python
# Start with three items.
numbers = [10, 20, 30]

# Remove the last item and retain it.
last = numbers.pop()

# Display the remaining list and the removed value.
print(numbers)
print(last)
```

Output:

```
[10, 20]
30
```

### Iterating over values

```python
# Store values to add.
numbers = [4, 7, 2]

# Initialize a running total.
total = 0

# Read each value directly.
for number in numbers:
    total = total + number

# Display the result.
print(total)
```

Output:

```
13
```

You do not need indices if you only need values.

### Iterating over indices

Use positions when you need to replace elements:

```python
# Create a list to modify.
numbers = [4, 7, 2]

# Visit all valid nonnegative indices.
for index in range(len(numbers)):
    # Replace the item at the current position.
    numbers[index] = numbers[index] * 2

# Display the changed list.
print(numbers)
```

Output:

```
[8, 14, 4]
```

### Slicing

A slice selects a portion of a sequence.

```python
# Store an ordered sequence.
numbers = [10, 20, 30, 40, 50]

# Include index 1, stop before index 4.
print(numbers[1:4])

# Select from the beginning, stopping before index 2.
print(numbers[:2])

# Select from index 3 through the end.
print(numbers[3:])
```

Output:

```
[20, 30, 40]
[10, 20]
[40, 50]
```

The stop position is excluded, as with range.

A list slice creates a new list containing references to the selected elements. The distinction between that and a deep copy will matter for nested collections in Part 2.

### Assignment is not copying

```python
# Create one list.
original = [1, 2]

# Give the same list another name.
alias = original

# Modify that shared list.
alias.append(3)

# Both names refer to the changed list.
print(original)
print(alias)
```

Output:

```
[1, 2, 3]
[1, 2, 3]
```

An alias is another name referring to the same object.

To copy a flat list of integers:

```python
# Create an original list.
original = [1, 2]

# Create a separate outer list.
copied = original.copy()

# Modify only the copied list.
copied.append(3)

# Inspect both lists.
print(original)
print(copied)
```

Output:

```
[1, 2]
[1, 2, 3]
```

### Worked example: find the largest number

A tempting initial idea is:

Start largest at zero. Replace it whenever a larger number appears.

That fails for [-8, -3, -10], because zero does not appear in the list and is larger than every input.

A better starting point is an actual input value.

```python
# Return the largest number, or None for an empty list.
def find_largest(numbers):
    # Define the behavior for an input with no elements.
    if len(numbers) == 0:
        return None

    # Start with a value that really appears in the input.
    largest = numbers[0]

    # Examine every input value.
    for number in numbers:
        # Replace the best value only when an improvement appears.
        if number > largest:
            largest = number

    # Return the best value after the full scan.
    return largest

print(find_largest([-8, -3, -10]))  # -3
print(find_largest([]))            # None
```

A scan means examining the items of a sequence in turn.

| Current number | largest before | Replace it? | largest after |
| --- | --- | --- | --- |
| -8 | -8 | No | -8 |
| -3 | -8 | Yes | -3 |
| -10 | -3 | No | -3 |

The empty-list behavior is a design choice. We state it explicitly instead of allowing an accidental failure at numbers[0].

### Useful built-ins, after understanding the process

Python supplies operations such as:

```python
# Store a nonempty list of numbers.
numbers = [4, 7, 2]

# Compute familiar results.
print(sum(numbers))  # 13
print(min(numbers))  # 2
print(max(numbers))  # 7
```

Learning the manual versions teaches how to maintain information during a scan. Using built-ins later can improve clarity.

### Sorting and return values

To sort means to arrange values into an order, such as smallest to largest.

```python
# Create an unsorted list.
numbers = [3, 1, 2]

# Create a separate sorted list.
ordered = sorted(numbers)

# Compare the two lists.
print(numbers)
print(ordered)
```

Output:

```
[3, 1, 2]
[1, 2, 3]
```

In contrast, numbers.sort() changes the existing list and returns None.

### What beginners often get wrong

Do not write numbers = numbers.sort() when you want to keep the list. That assigns the returned value, None, to numbers.

Likewise, append changes a list and returns None.

### A brief companion type: tuples

A tuple is an ordered collection whose stored positions cannot be reassigned after creation.

```python
# Store a fixed pair of values.
point = (3, 5)

# Access values by position.
print(point[0])
print(point[1])
```

A tuple is immutable, meaning the tuple itself cannot be changed after creation. If it contains a mutable object, that contained object can still change.

We introduce tuples now because some operations return pairs.

Unpacking assigns the items of a collection to separate names:

```python
# Unpack a two-item tuple into two names.
x, y = (3, 5)

# Display the separate values.
print(x, y)
```

Output:

```
3 5
```

### Practice

1. Guided: For [6, 2, 9], print the first item, last item, and length.
2. Independent: Write count_positive(numbers) to count values greater than zero.
3. Independent: Write doubled(numbers) to return a new list containing each input multiplied by two. Leave the original list unchanged.
4. Prediction: What does [10, 20, 30, 40][1:3] produce?

#### Answers and explanations

1.

```python
# Store the input.
numbers = [6, 2, 9]

# Read the requested information.
print(numbers[0])   # 6
print(numbers[-1])  # 9
print(len(numbers)) # 3
```

2.

```python
# Count values strictly greater than zero.
def count_positive(numbers):
    count = 0

    for number in numbers:
        if number > 0:
            count = count + 1

    return count

print(count_positive([-2, 0, 4, 7]))  # 2
print(count_positive([]))            # 0
```

3.

```python
# Construct a separate output list.
def doubled(numbers):
    result = []

    for number in numbers:
        result.append(number * 2)

    return result

original = [2, 5]
print(doubled(original))  # [4, 10]
print(original)          # [2, 5]
```

4.

```
[20, 30]
```

Index 1 is included. Index 3 is excluded.

## Chapter 1.9: Strings

A string is an immutable sequence of text.

For our early examples, think of it as a row of characters.

```python
# Store a word.
word = "code"

# Access characters and inspect the length.
print(word[0])
print(word[-1])
print(len(word))
```

Output:

```
c
e
4
```

More precisely, Python strings store Unicode code points, numbered units used to represent text from many writing systems. A visible symbol can sometimes consist of more than one code point. Our early examples use ordinary English letters, where that distinction does not complicate indexing.

### Strings use familiar sequence operations

```python
# Store a word.
word = "python"

# Extract part of the string.
print(word[1:4])

# Check for a consecutive piece of text.
print("th" in word)

# Visit one character at a time.
for character in word:
    print(character)
```

The first two results are:

```
yth
True
```

The loop then prints p, y, t, h, o, n on separate lines.

A substring is a consecutive portion of a string.

Membership in a string checks for a substring. It is not limited to one character.

### Immutability

This is intentionally incorrect:

```python
# Intentionally incorrect: strings do not support item replacement.
word = "cat"
word[0] = "b"
```

Instead, create a new string:

```python
# Store the original word.
word = "cat"

# Construct a different string and reassign the name.
word = "b" + word[1:]

# Display the new value.
print(word)
```

Output:

```
bat
```

Immutability does not prevent reassigning the variable. It prevents changing the existing string object itself.

Python’s documentation distinguishes between indexing, slicing, and immutable strings, and confirms that string-building operations produce new values. Python 3.14.7 documentation.

### Useful string methods

```python
# Store text with surrounding whitespace.
text = "  Hello World  "

# Produce a string without surrounding whitespace.
cleaned = text.strip()

# Produce lowercase text.
lowercase = cleaned.lower()

# Display both results.
print(cleaned)
print(lowercase)
```

Output:

```
Hello World
hello world
```

Whitespace includes spaces, tabs, and line breaks.

These methods do not modify text.

| Expression | Meaning |
| --- | --- |
| text.lower() | Return lowercase text |
| text.upper() | Return uppercase text |
| text.strip() | Remove surrounding whitespace |
| text.split() | Split at whitespace into a list of words |
| separator.join(parts) | Join strings with the chosen separator |
| text.replace(old, new) | Return text with matching occurrences replaced |

### Splitting and joining

```python
# Split whitespace-separated words into a list.
words = "red blue red".split()

# Display the list.
print(words)

# Join the strings with a hyphen between them.
combined = "-".join(words)

# Display the new string.
print(combined)
```

Output:

```
['red', 'blue', 'red']
red-blue-red
```

join requires strings. A list of integers must be converted or otherwise handled before joining as text.

### Formatted strings

An f-string inserts expression results into text.

```python
# Store values to display.
name = "Saket"
score = 90

# The leading f enables expression substitution inside braces.
message = f"{name} scored {score}"

# Display the constructed string.
print(message)
```

Output:

```
Saket scored 90
```

The braces identify expressions to evaluate and include.

### Worked example: count vowels

We will count the English vowels a, e, i, o, and u, treating uppercase and lowercase as equivalent.

```python
# Count English vowel letters.
def count_vowels(text):
    # Start before any characters have been counted.
    count = 0

    # Make comparisons use one consistent letter case.
    lowered = text.lower()

    # Examine every character.
    for character in lowered:
        # Check whether it is one of the chosen vowels.
        if character in "aeiou":
            count = count + 1

    # Return after examining the complete string.
    return count

print(count_vowels("Apple"))  # 2
print(count_vowels(""))       # 0
```

| Character | In "aeiou"? | Count afterward |
| --- | --- | --- |
| a | Yes | 1 |
| p | No | 1 |
| p | No | 1 |
| l | No | 1 |
| e | Yes | 2 |

A tempting mistake is to compare an entire word with "aeiou". We need to examine each character because the requested answer is a count of vowel occurrences.

### Practice

1. Guided: Remove surrounding whitespace from "  Python  " and convert the result to lowercase.
2. Independent: Write count_character(text, target) to count a one-character target. Treat uppercase and lowercase as different.
3. Independent: Write reverse_text(text) using a loop. For this exercise, do not use slicing.
4. Prediction: What does "a  b   c".split() produce?

#### Answers and explanations

1.

```python
# Store the original text.
text = "  Python  "

# Apply the transformations in two visible steps.
cleaned = text.strip()
lowered = cleaned.lower()

print(lowered)  # python
```

2.

```python
# Count exact matches for a one-character target.
def count_character(text, target):
    count = 0

    for character in text:
        if character == target:
            count = count + 1

    return count

print(count_character("banana", "a"))  # 3
print(count_character("Banana", "b"))  # 0
```

3.

```python
# Build a reversed string for this beginner exercise.
def reverse_text(text):
    result = ""

    for character in text:
        # Put each new character before the previous result.
        result = character + result

    return result

print(reverse_text("cat"))  # tac
print(reverse_text(""))     # Empty output line
```

For "cat", the intermediate strings are "c", "ac", and "tac".

This version is useful for learning. Repeated string construction can be costly for long inputs. Part 3 will explain why a short-looking statement can perform substantial work.

4.

```
['a', 'b', 'c']
```

With no separator argument, split() groups consecutive whitespace and does not produce empty entries for those gaps.
