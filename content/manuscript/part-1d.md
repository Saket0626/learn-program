# Part 1 continued: Chapters 1.10–1.13, glossary, and readiness

## Chapter 1.10: Dictionaries

A dictionary associates keys with values.

Think of a contact book:

- A person’s name is the lookup label.
- Their phone number is the associated information.

A key identifies an entry. A dictionary’s value is the information associated with that key.

```python
# Associate names with scores.
scores = {
    "Ava": 90,
    "Ben": 82,
}

# Look up the value associated with a key.
print(scores["Ava"])
```

Output:

```
90
```

Unlike a list, the dictionary does not require you to know the item’s numeric position.

### Adding and updating entries

```python
# Start with an empty dictionary.
scores = {}

# Add two entries.
scores["Ava"] = 90
scores["Ben"] = 82

# Replace the value associated with an existing key.
scores["Ava"] = 95

# Inspect the updated value.
print(scores["Ava"])

# Count the number of keys.
print(len(scores))
```

Output:

```
95
2
```

A dictionary has one current value per key. Assigning to an existing key updates that entry.

### Membership checks keys

```python
# Store one key-value pair.
scores = {"Ava": 90}

# Test keys, not values.
print("Ava" in scores)
print(90 in scores)
```

Output:

```
True
False
```

### Missing keys

scores["Mia"] raises a KeyError if "Mia" is absent.

You can check first:

```python
# Store known scores.
scores = {"Ava": 90}

# Use direct lookup only when the key exists.
if "Mia" in scores:
    print(scores["Mia"])
else:
    print("No score recorded")
```

Or use get:

```python
# Store known scores.
scores = {"Ava": 90}

# Return the default value 0 if the key is absent.
print(scores.get("Mia", 0))
```

Output:

```
0
```

get does not insert the default into the dictionary.

If you omit its default argument, a missing key returns None.

### Which values can be keys?

Dictionary keys must be hashable.

A hashable object supports a stable numeric hash used for lookup and follows the required consistency rules for equality. We will explain hashing in Part 4.

For now:

- Integers and strings are suitable keys.
- Lists, dictionaries, and ordinary sets are not.
- A tuple is usable as a key only when all its elements are hashable.

The dictionary’s associated values do not have to be hashable.

### Worked example: count frequencies

A frequency is the number of times a value occurs.

For:

```python
["red", "blue", "red"]
```

we want:

```python
{"red": 2, "blue": 1}
```

First, the explicit version:

```python
# Count how often each word occurs.
def count_words(words):
    # No words have been recorded yet.
    counts = {}

    # Process each occurrence.
    for word in words:
        # Existing words already have a count.
        if word in counts:
            counts[word] = counts[word] + 1
        else:
            # This is the first occurrence.
            counts[word] = 1

    return counts

print(count_words(["red", "blue", "red"]))
```

Expected output:

```
{'red': 2, 'blue': 1}
```

| Current word | Previous count | New count | Dictionary afterward |
| --- | --- | --- | --- |
| red | Absent | 1 | {"red": 1} |
| blue | Absent | 1 | {"red": 1, "blue": 1} |
| red | 1 | 2 | {"red": 2, "blue": 1} |

Now the shorter update:

```python
# Count occurrences using a default for unseen words.
def count_words(words):
    counts = {}

    for word in words:
        # An unseen word starts from zero before adding this occurrence.
        counts[word] = counts.get(word, 0) + 1

    return counts
```

Do not memorize that line as an unexplained formula. Read it as:

Get the old count, using zero if there is none, then add one.

### Iterating through a dictionary

```python
# Store counts.
counts = {"red": 2, "blue": 1}

# Ordinary iteration provides keys.
for word in counts:
    print(word, counts[word])

# items() provides key-value pairs.
# Unpacking places each pair into two names.
for word, count in counts.items():
    print(word, count)
```

Each loop prints:

```
red 2
blue 1
```

Modern Python dictionaries preserve insertion order. That does not mean their keys are automatically sorted.

Do not add or remove dictionary entries while iterating over that dictionary. We will study safe alternatives when needed.

### Common misconception

counts[word] = 1 on every iteration does not count occurrences. It repeatedly resets the count to one.

### Practice

1. Guided: Create a dictionary associating "apple" with 3 and "banana" with 2. Update the apple count to 4.
2. Independent: Write character_counts(text) to return a dictionary of character frequencies.
3. Prediction: What does {"a": 1, "a": 7} contain?
4. Independent: Given {"a": 3, "b": 2}, use a loop to calculate the sum of its values.

#### Answers and explanations

1.

```python
# Create the initial associations.
counts = {"apple": 3, "banana": 2}

# Update one existing key.
counts["apple"] = 4

print(counts)  # {'apple': 4, 'banana': 2}
```

2.

```python
# Count every character, including spaces and punctuation.
def character_counts(text):
    counts = {}

    for character in text:
        counts[character] = counts.get(character, 0) + 1

    return counts

print(character_counts("aba"))  # {'a': 2, 'b': 1}
```

3.

```
{'a': 7}
```

The later value for the repeated key replaces the earlier one.

4.

```python
# Store the input dictionary.
counts = {"a": 3, "b": 2}

# Accumulate its values.
total = 0

for key in counts:
    total = total + counts[key]

print(total)  # 5
```

## Chapter 1.11: Sets

A set is a collection of distinct, hashable elements.

Distinct means no duplicate values are retained.

A set is useful when you care whether something is present, rather than where it occurs or how many times it occurs.

```python
# Repeated values are retained only once.
numbers = {2, 5, 2, 7}

# Count distinct values.
print(len(numbers))

# Check membership.
print(5 in numbers)
print(9 in numbers)
```

Output:

```
3
True
False
```

A set does not provide positional indexing or a guaranteed iteration order. Do not depend on the order in which its elements print.

### Creating an empty set

```python
# Create an empty set.
seen = set()

# Add values.
seen.add("red")
seen.add("blue")
seen.add("red")

# The repeated value does not increase the size.
print(len(seen))
```

Output:

```
2
```

{} creates an empty dictionary, not an empty set.

### Removing elements

```python
# Create a set.
colors = {"red", "blue"}

# Remove a present element.
colors.remove("red")

# Discard does not fail when the element is absent.
colors.discard("green")

# Inspect membership.
print("red" in colors)
```

Output:

```
False
```

remove raises a KeyError when the value is absent. discard does not.

### Set operations

```python
# Define overlapping groups.
a = {1, 2, 3}
b = {3, 4}

# Union: values in either set.
union = a | b

# Intersection: values in both sets.
intersection = a & b

# Difference: values in a that are not in b.
difference = a - b

# Check the mathematical contents without depending on print order.
print(union == {1, 2, 3, 4})
print(intersection == {3})
print(difference == {1, 2})
```

Output:

```
True
True
True
```

### Worked example: detect a duplicate

A duplicate is a repeated value.

Our question is:

Does any value appear at least twice?

We do not need every count. We only need to remember what has already appeared.

```python
# Assume the list contains hashable values, such as integers.
def has_duplicate(numbers):
    # Initially, no values have been encountered.
    seen = set()

    # Process the input in order.
    for number in numbers:
        # A prior occurrence means a duplicate has been found.
        if number in seen:
            return True

        # Record the current value for future membership checks.
        seen.add(number)

    # No repeated value was found.
    return False

print(has_duplicate([4, 1, 4]))  # True
print(has_duplicate([4, 1, 7]))  # False
print(has_duplicate([]))        # False
```

| Current number | Already in seen? | Action | seen afterward |
| --- | --- | --- | --- |
| 4 | No | Add it | {4} |
| 1 | No | Add it | {1, 4} |
| 4 | Yes | Return True | No further update |

The displayed set contents in the table describe membership, not a stored positional order.

### A mistake caused by changing the order of operations

If you add the current number before testing whether it is present, the membership test will always succeed.

The required sequence is:

1. Ask whether an earlier occurrence exists.
2. Then record the current occurrence.

This is your first example of a general algorithmic idea: the meaning of stored information depends on exactly when you update it.

### Choosing between collections

| Need | Starting choice |
| --- | --- |
| Keep items in a sequence, including repeats | List |
| Map a label to associated information | Dictionary |
| Track distinct values or previous presence | Set |
| Work with text | String |
| Store a fixed ordered grouping | Tuple |

This is a starting guide, not a complete performance comparison. Part 4 will explain implementation and costs.

### Practice

1. Guided: Count the distinct values in [3, 3, 1, 2, 1] using a set.
2. Independent: Write all_unique(numbers) to return True when no value repeats. Assume integer inputs.
3. Independent: Write unique_in_order(numbers) to remove duplicates while preserving the order of first appearance.
4. Prediction: What is the difference between {} and set()?

#### Answers and explanations

1.

```python
# Store repeated values.
numbers = [3, 3, 1, 2, 1]

# Construct a set from the list.
distinct = set(numbers)

print(len(distinct))  # 3
```

2.

```python
# Determine whether every value appears at most once.
def all_unique(numbers):
    seen = set()

    for number in numbers:
        if number in seen:
            return False

        seen.add(number)

    return True

print(all_unique([1, 2, 3]))  # True
print(all_unique([1, 2, 1]))  # False
print(all_unique([]))        # True
```

An empty list has no repeated values.

3.

```python
# Preserve the first occurrence of each integer.
def unique_in_order(numbers):
    # Track membership with a set.
    seen = set()

    # Track output order with a list.
    result = []

    for number in numbers:
        if number not in seen:
            seen.add(number)
            result.append(number)

    return result

print(unique_in_order([3, 1, 3, 2, 1]))  # [3, 1, 2]
```

not in tests absence.

The list and set have different jobs. The list records order. The set records whether a value has appeared.

4.

- {} creates an empty dictionary.
- set() creates an empty set.

## Chapter 1.12: Reading error messages

A bug is a flaw in a program.

Debugging is finding and correcting bugs.

Not every bug produces an error message. A program can run successfully and compute the wrong answer.

We will distinguish three broad cases.

| Kind | Meaning | Example |
| --- | --- | --- |
| Syntax error | The code violates the language’s grammatical rules | Missing a required colon |
| Runtime error | An operation fails while the program executes | Dividing by zero |
| Logic error | The program runs but does the wrong thing | Counting all values instead of only positive ones |

Syntax means the language’s rules for arranging symbols and words.

### Case 1: syntax error

Intentionally incorrect code:

```python
# Intentionally incorrect: the if line needs a colon.
score = 70
if score >= 60
    print("Pass")
```

Python reports a SyntaxError.

The correction is:

```python
# Correct syntax.
score = 70
if score >= 60:
    print("Pass")
```

An error marker identifies where Python detected a problem. The underlying mistake can occur earlier, such as an unclosed quotation mark or parenthesis on the preceding line.

### Case 2: runtime error

Intentionally incorrect code:

```python
# Store text.
age_text = "18"

# Intentionally incorrect: add an integer to a string.
next_age = age_text + 1
print(next_age)
```

A representative error report ends with:

```
TypeError: can only concatenate str (not "int") to str
```

Exact wording can vary by Python version.

A traceback reports the chain of execution leading to an error.

Read an unfamiliar traceback in this order:

1. Read the last line for the error category and message.
2. Find the relevant filename and line number.
3. Examine the expression on that line.
4. Identify the actual values and types involved.
5. Compare them with what the operation requires.

For this example:

- Actual left operand: string "18".
- Actual right operand: integer 1.
- Intended action: arithmetic.
- Needed correction: convert the input to an integer before adding.

```python
# Store the original text.
age_text = "18"

# Convert before performing arithmetic.
next_age = int(age_text) + 1
print(next_age)  # 19
```

### Common errors

| Error | What to inspect |
| --- | --- |
| SyntaxError | Colons, parentheses, quotes, and the previous line |
| IndentationError | Which lines belong inside a block |
| NameError | Spelling, capitalization, and whether a name was assigned |
| TypeError | Whether an operation supports the actual operand types |
| ValueError | Whether a value is acceptable for the requested operation |
| IndexError | Whether the list or string position exists |
| KeyError | Whether the requested dictionary key or set element exists |
| ZeroDivisionError | Whether a divisor is zero |

For example:

- int("hello") raises ValueError.
- [10, 20][2] raises IndexError.
- {"a": 1}["b"] raises KeyError.

An exception is Python’s mechanism for reporting and potentially handling many errors encountered during execution.

### Case 3: logic error

This program intends to total all values:

```python
# Intentionally incorrect algorithm.
def incorrect_total(numbers):
    total = 0

    for number in numbers:
        # This replaces the accumulated result.
        total = number

    return total

print(incorrect_total([2, 3, 4]))
```

It prints 4, but the intended answer is 9.

No exception appears because every operation is valid.

The correction is:

```python
# Accumulate instead of replacing.
def calculate_total(numbers):
    total = 0

    for number in numbers:
        total = total + number

    return total
```

### Inspecting values while debugging

```python
# Display intermediate states to investigate behavior.
numbers = [2, 3, 4]
total = 0

for number in numbers:
    print("Before:", total, "Current:", number)
    total = total + number
    print("After:", total)

print("Final:", total)
```

This is diagnostic output: temporary output used to inspect behavior.

Predicted output:

```
Before: 0 Current: 2
After: 2
Before: 2 Current: 3
After: 5
Before: 5 Current: 4
After: 9
Final: 9
```

Useful diagnostic output answers a specific question. Printing every value everywhere can make the relevant information harder to find.

### Handling an expected error

Sometimes invalid input is an anticipated situation.

try identifies code whose exception you want to handle. except identifies a matching response.

```python
# Ask for an integer.
text = input("Enter a whole number: ")

try:
    # This may raise ValueError for input such as "hello".
    number = int(text)

    # This runs only if conversion succeeds.
    print("Twice your number:", number * 2)
except ValueError:
    # Respond to the specific expected conversion problem.
    print("That was not a valid whole number.")
```

Do not use a broad exception handler to hide unexplained bugs. First understand the operation that failed.

### Checking results with assert

An assertion states a condition that should be true at a particular point.

```python
# Define a small function.
def square(number):
    return number * number

# Each assertion checks one expected result.
assert square(3) == 9
assert square(0) == 0
assert square(-2) == 4

# Reaching this line means all preceding checks passed.
print("Checks passed")
```

If an assertion’s condition is false, Python raises AssertionError.

Assertions are useful for learning and development checks. They are not a substitute for ordinary input validation, and Python can disable them in optimized execution.

### Edge cases

An edge case is an input near a boundary or outside the ordinary-looking examples.

For list-processing functions, useful cases include:

- An empty list.
- A one-element list.
- All equal values.
- All negative values.
- A desired value at the first or last position.
- No matching values.

Always respect the problem’s stated input rules. If empty input is prohibited, you do not need to invent an answer for it, though understanding what would fail can still be informative.

### What beginners often get wrong

Changing several lines at once makes it difficult to know which change mattered.

Use a repeatable input, identify one hypothesis, make one relevant change, and check again.

### Practice

1. Guided: Explain and fix print("Total: " + 5).
2. Independent: Explain why numbers = [10, 20] followed by print(numbers[2]) fails. Print the last element correctly.
3. Independent: Fix this function and test it on positive, negative, zero, and empty inputs.
4. Independent: Write three assertions for count_character from Chapter 1.9.

```python
# Intentionally incorrect: the count is reset during iteration.
def count_positive(numbers):
    count = 0

    for number in numbers:
        count = 0

        if number > 0:
            count = count + 1

    return count
```

#### Answers and explanations

1. The code tries to concatenate a string and an integer.

```python
# Convert the number to text.
print("Total: " + str(5))

# Or let print display separate arguments.
print("Total:", 5)
```

Both display:

```
Total: 5
```

2. A two-element list has nonnegative indices 0 and 1.

```python
# Store two elements.
numbers = [10, 20]

# Use the final valid nonnegative index.
print(numbers[1])

# Or access from the end.
print(numbers[-1])
```

Both display 20.

3.

```python
# Count positive values without resetting the accumulated count.
def count_positive(numbers):
    count = 0

    for number in numbers:
        if number > 0:
            count = count + 1

    return count

# Check several distinct situations.
assert count_positive([1, 2]) == 2
assert count_positive([-1, -2]) == 0
assert count_positive([0]) == 0
assert count_positive([]) == 0
assert count_positive([-1, 0, 5]) == 1
```

4. After defining count_character:

```python
# A repeated target.
assert count_character("banana", "a") == 3

# An absent target.
assert count_character("banana", "z") == 0

# An empty input string.
assert count_character("", "a") == 0
```

## Chapter 1.13: Combining the foundations

We will now build a small program from a written requirement.

This is the first complete application of:

1. Understand.
2. Plan.
3. Implement.
4. Check.

### The problem

Write a function named analyze_words(text).

Its input is a string.

It must return a dictionary containing:

- word_count: total number of words.
- unique_count: number of distinct words.
- frequencies: a dictionary mapping each word to its count.
- most_common: the most frequent word, or None if there are no words.

We need precise rules:

- Uppercase and lowercase count as the same.
- Words are separated using whitespace.
- Punctuation stays attached to words.
- If several words tie for the highest frequency, return the one whose first appearance came earliest.

Those rules matter.

For this program, "hello" and "hello!" are different words. We are not silently assuming punctuation removal.

### Work through an example by hand

Input:

```
Red blue red GREEN blue red
```

After converting to lowercase and splitting:

```python
["red", "blue", "red", "green", "blue", "red"]
```

Expected answer:

```python
{
    "word_count": 6,
    "unique_count": 3,
    "frequencies": {"red": 3, "blue": 2, "green": 1},
    "most_common": "red"
}
```

Before writing code, we know what a correct result looks like.

### Choose the stored information

| Information needed | Representation |
| --- | --- |
| Words in their original order | List |
| Count for each distinct word | Dictionary |
| Current best word | String or None |
| Current highest frequency | Integer |
| Final named results | Dictionary |

We do not need a separate set for the distinct count. The frequency dictionary already has one key per distinct word.

### Plan in plain English

1. Convert the text to lowercase.
2. Split it into words.
3. Count each word using a dictionary.
4. Examine the words in original order using their completed counts.
5. Replace the best word only when a strictly larger frequency appears.
6. Return all requested information.

### Why use completed counts before selecting the winner?

A tempting one-pass approach updates the winner whenever a word’s running count becomes greater than the current best running count.

That can violate our tie rule.

Consider:

```
a b b a
```

Both words finish with frequency 2. The required answer is "a" because it appeared first.

With the tempting approach:

- "a" first leads with 1.
- "b" later reaches 2 and becomes the leader.
- The final "a" reaches 2, but does not exceed 2.
- The answer incorrectly remains "b".

The issue is that temporary counts do not necessarily establish the required ordering among final ties.

Our two-stage approach first learns the final frequencies. Then it examines first appearances in their original order.

This is an example of finding a counterexample: an input showing that a proposed approach is incorrect.

### The complete program

```python
# Analyze whitespace-separated words under the stated rules.
def analyze_words(text):
    # Treat uppercase and lowercase forms as equivalent.
    normalized = text.lower()

    # Preserve the original word order in a list.
    words = normalized.split()

    # Map each distinct word to its final frequency.
    frequencies = {}

    # First stage: count every occurrence.
    for word in words:
        # Unseen words have a previous count of zero.
        previous_count = frequencies.get(word, 0)

        # Include the current occurrence.
        frequencies[word] = previous_count + 1

    # Empty input should produce no winning word.
    most_common = None

    # Every actual word frequency will be greater than zero.
    highest_count = 0

    # Second stage: examine words in original order.
    for word in words:
        # Read the completed frequency, not a partial count.
        count = frequencies[word]

        # Replace the winner only for a strictly larger frequency.
        # Equal counts keep the earlier winner.
        if count > highest_count:
            highest_count = count
            most_common = word

    # Return every requested field.
    return {
        "word_count": len(words),
        "unique_count": len(frequencies),
        "frequencies": frequencies,
        "most_common": most_common,
    }
```

The source manuscript’s code block ended before the return. The return above is the behavior required by the contract, the traces, and the checks that follow. Do not omit those checks.

Expected output for the worked example, printed field by field:

```
6
3
{'red': 3, 'blue': 2, 'green': 1}
red
```

### First-stage trace

| Word processed | Previous count | Updated frequency dictionary |
| --- | --- | --- |
| red | 0 | {"red": 1} |
| blue | 0 | {"red": 1, "blue": 1} |
| red | 1 | {"red": 2, "blue": 1} |
| green | 0 | {"red": 2, "blue": 1, "green": 1} |
| blue | 1 | {"red": 2, "blue": 2, "green": 1} |
| red | 2 | {"red": 3, "blue": 2, "green": 1} |

### Second-stage trace

| Word examined | Final frequency | highest_count before | Replace? | most_common after |
| --- | --- | --- | --- | --- |
| red | 3 | 0 | Yes | red |
| blue | 2 | 3 | No | red |
| red | 3 | 3 | No | red |
| green | 1 | 3 | No | red |
| blue | 2 | 3 | No | red |
| red | 3 | 3 | No | red |

### Checks to run

Place these after the function definition:

```python
# Repeated words and case normalization.
report = analyze_words("Red blue RED")
assert report["word_count"] == 3
assert report["unique_count"] == 2
assert report["frequencies"] == {"red": 2, "blue": 1}
assert report["most_common"] == "red"

# Empty input.
report = analyze_words("")
assert report["word_count"] == 0
assert report["unique_count"] == 0
assert report["frequencies"] == {}
assert report["most_common"] is None

# Whitespace without words.
report = analyze_words("   ")
assert report["word_count"] == 0
assert report["most_common"] is None

# Tie: the earliest first appearance must win.
report = analyze_words("a b b a")
assert report["most_common"] == "a"

# Punctuation remains part of a word.
report = analyze_words("hello hello!")
assert report["unique_count"] == 2

# This line is reached if all assertions pass.
print("All checks passed")
```

is None checks whether the value is the special None object.

The is operator checks identity, meaning whether two references identify the same object. == checks equality of values. Use is None for this special absence marker. Do not use is as a substitute for numeric or string equality.

### Guided modification

Suppose the user also wants the longest word, with ties going to the earliest occurrence.

What information must you maintain?

- The best word so far.
- A way to compare lengths.

What should the starting value be?

An empty string works under this specification because its length is zero and we can define the empty-input result as "".

```python
# Return the longest whitespace-separated word.
# Preserve its original spelling and punctuation.
def longest_word(text):
    words = text.split()

    # Define the empty-input result.
    longest = ""

    for word in words:
        # Strict comparison preserves the earliest tied word.
        if len(word) > len(longest):
            longest = word

    return longest
```

The important skill is identifying what must be remembered from earlier iterations.

### Chapter practice

1. Guided: Write count_long_words(text, minimum_length) to count words whose length is at least the given minimum. Split on whitespace.
2. Independent: Write first_repeat(numbers) to return the first integer encountered for a second time. Return None if none repeats.
3. Independent: Write positive_summary(numbers) to return a dictionary with the count and sum of positive values.
4. Independent: Write same_frequencies(text_a, text_b) to check whether two strings contain the same characters with the same frequencies. Treat case and spaces as significant.

#### Answers and explanations

1. Count long words

```python
# Count words satisfying the length requirement.
def count_long_words(text, minimum_length):
    words = text.split()
    count = 0

    for word in words:
        # Include the boundary value.
        if len(word) >= minimum_length:
            count = count + 1

    return count

assert count_long_words("a small red apple", 5) == 2
assert count_long_words("", 5) == 0
assert count_long_words("one two", 3) == 2
```

"small" and "apple" each have five characters.

2. First repeated integer

```python
# Return the value whose second occurrence is encountered first.
def first_repeat(numbers):
    seen = set()

    for number in numbers:
        # Check earlier appearances before recording this one.
        if number in seen:
            return number

        seen.add(number)

    return None

assert first_repeat([2, 1, 3, 1, 2]) == 1
assert first_repeat([5, 5]) == 5
assert first_repeat([1, 2, 3]) is None
assert first_repeat([]) is None
```

For [2, 1, 3, 1, 2], the answer is 1, because its second occurrence comes before the second occurrence of 2.

That differs from “the earliest original value that repeats eventually.”

3. Positive summary

```python
# Describe only values strictly greater than zero.
def positive_summary(numbers):
    count = 0
    total = 0

    for number in numbers:
        if number > 0:
            count = count + 1
            total = total + number

    return {
        "count": count,
        "sum": total,
    }

assert positive_summary([-2, 0, 3, 5]) == {"count": 2, "sum": 8}
assert positive_summary([]) == {"count": 0, "sum": 0}
assert positive_summary([-3, -1]) == {"count": 0, "sum": 0}
```

4. Equal character frequencies

```python
# Build a frequency dictionary for one string.
def character_counts(text):
    counts = {}

    for character in text:
        counts[character] = counts.get(character, 0) + 1

    return counts

# Compare the complete character-frequency information.
def same_frequencies(text_a, text_b):
    counts_a = character_counts(text_a)
    counts_b = character_counts(text_b)

    # Dictionary equality compares key-value associations.
    return counts_a == counts_b

assert same_frequencies("listen", "silent") == True
assert same_frequencies("aab", "abb") == False
assert same_frequencies("", "") == True
assert same_frequencies("A", "a") == False
assert same_frequencies("ab", "a b") == False
```

Merely converting the strings to sets would lose counts.

For example, "aab" and "abb" contain the same distinct characters, but their frequencies differ.

## Running glossary: Part 1

| Term | Meaning |
| --- | --- |
| Accumulator | A variable that builds a result across repeated steps. |
| Algorithm | A precise method for solving a problem. |
| Alias | Another name referring to the same object. |
| Argument | An actual value supplied to a function call. |
| Assertion | A check that a condition is true. |
| Assignment | Making a name refer to a value. |
| Block | A group of statements controlled together. |
| Boolean | A logical value, True or False. |
| Branch | One possible path through a conditional. |
| Bug | A flaw in a program. |
| Built-in | Functionality supplied by Python without your defining it. |
| Caller | Code that invokes a function. |
| Character | A unit of text; Python string indexing operates on Unicode code points. |
| Code | Instructions written in a programming language. |
| Collection | A structure holding multiple values. |
| Comment | Text explaining code that Python does not execute. |
| Comparison | A test of a relationship between values. |
| Concatenation | Joining strings. |
| Conditional | Code that selects behavior based on a condition. |
| Conversion | Producing a value of one type from another value. |
| Counterexample | An input or case that disproves a proposed claim or approach. |
| Data type | The kind of a value and its associated behavior. |
| Debugging | Finding and correcting bugs. |
| Dictionary | A collection associating unique keys with values. |
| Distinct | Without duplicate values. |
| Edge case | An input near a boundary or special situation. |
| Editor | Software used to write and change text files. |
| Element | An item in a collection. |
| Evaluate | Determine the value of an expression. |
| Exception | Python’s mechanism for reporting and potentially handling many execution errors. |
| Expression | Code that produces a value. |
| Faded practice | Practice that progressively removes support. |
| Float | A floating-point numeric value, often an approximation of a decimal quantity. |
| Frequency | Number of occurrences of a value. |
| Function | A named operation that can receive inputs and return a result. |
| Function call | A request to execute a function. |
| Hashable | Suitable for hash-based lookup under Python’s stability and equality rules. |
| IDE | An environment combining code editing, execution, and development tools. |
| Identity | Whether references identify the same object. |
| Immutable | Not changeable after creation. |
| Index | A position used to access a sequence element. |
| Indentation | Leading spaces that identify Python blocks. |
| Infinite loop | A loop that does not reach a stopping condition. |
| Input | Information supplied to a program or function. |
| Integer | A whole number. |
| Interpreter | Software that executes Python programs. |
| Iterable | Something that can provide items one at a time. |
| Iteration | One execution of a loop body. |
| Key | A value identifying a dictionary entry. |
| Keyword | A word reserved by the programming language. |
| List | An ordered, mutable collection. |
| Local variable | A variable belonging to a function call. |
| Loop | A structure that repeats code. |
| Method | An operation accessed through an object. |
| Mutable | Changeable after creation. |
| Nested | Located inside another structure. |
| Object | A stored Python value with a type and associated behavior. |
| Operand | A value acted on by an operator. |
| Operator | A symbol or word performing an operation. |
| Output | Information produced by a program. |
| Parameter | A name that receives an argument inside a function. |
| Precedence | Rules determining how operations group together. |
| Program | Instructions a computer can execute. |
| Retrieval practice | Attempting to recall or produce an answer before looking it up. |
| Return | End a function call and provide a result to its caller. |
| Scan | Examine sequence elements in turn. |
| Scope | Where a name is accessible. |
| Script | A file containing code that can be run. |
| Sequence | A collection organized by position. |
| Set | A collection of distinct, hashable elements without positional indexing. |
| Short-circuit evaluation | Skipping an expression part when the result is already determined. |
| Slice | A selected portion of a sequence. |
| Spaced practice | Returning to learning across separate sessions. |
| Statement | An instruction executed by Python. |
| String | An immutable sequence of text code points. |
| Substring | A consecutive portion of a string. |
| Syntax | The grammatical rules of a programming language. |
| Trace | A step-by-step record of program execution. |
| Traceback | A report showing the execution path leading to an error. |
| Truthiness | How a value behaves when used as a Boolean condition. |
| Tuple | An immutable ordered collection. |
| Unpacking | Assigning collection elements to separate names. |
| Value | A piece of information represented in a program. |
| Variable | A name referring to a value. |
| Whitespace | Spaces, tabs, line breaks, and related spacing characters. |

## Part 1 readiness check

Before moving on, try these without copying an earlier solution:

- Explain = versus ==, and print versus return.
- Trace a loop using a table of changing variable values.
- Write a function that counts values meeting a condition.
- Build a frequency dictionary.
- Detect a repeated integer using a set.
- Explain why b = a does not copy a list.
- Read an error message and identify the operation that failed.
- State the expected result for an empty input before writing code.

If one item is difficult, revisit its chapter and solve a slightly changed exercise. For example, after counting positive values, count values divisible by three. The goal is to reconstruct the idea under a changed requirement.

End of Part 1. Next: Part 2, How a Computer Actually Thinks.
