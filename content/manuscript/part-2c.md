# Part 2 continued: Chapters 2.6–2.8, glossary, and readiness

## Chapter 2.6: Debugging as an investigation

Debugging works best when you replace random changes with testable explanations.

A hypothesis is a proposed explanation you can investigate.

For example:

The function skips the last element because its loop stops too early.

That is useful because it tells you what evidence to inspect.

“Python is acting weird” does not identify an observable cause.

### A debugging procedure

1. State the intended behavior.
2. Find an input that produces the wrong behavior.
3. Write the expected result independently.
4. Record the actual result.
5. Reduce the input while preserving the failure.
6. Form a specific hypothesis.
7. Trace or inspect the relevant state.
8. Change the cause.
9. Run the failing example again.
10. Keep that example as a future check.

A reproducible failure is a failure you can trigger again with known conditions.

A minimal failing example is a small example that still exposes the bug. It does not have to be the mathematically smallest possible example to be useful.

### Worked investigation: a broken maximum function

```python
# Intentionally incorrect for some inputs.
def largest_value(numbers):
    largest = 0

    for number in numbers:
        if number > largest:
            largest = number

    return largest
```

Suppose the intended input is a nonempty list of integers.

Test:

- Input: [-8, -3, -10]
- Expected: -3
- Actual: 0

Reduce it:

- Input: [-1]
- Expected: -1
- Actual: 0

Hypothesis:

The starting value assumes zero is a valid candidate, even though it might not appear in the input.

Trace:

| Step | number | largest | Condition |
| --- | --- | --- | --- |
| Initialization | — | 0 | — |
| First iteration | -1 | 0 | -1 > 0 is false |
| Return | — | 0 | Wrong result |

Correction:

```python
# Input requirement: numbers must be nonempty.
def largest_value(numbers):
    # Begin with an actual input value.
    largest = numbers[0]

    for number in numbers:
        if number > largest:
            largest = number

    return largest
```

Checks:

```python
assert largest_value([-1]) == -1
assert largest_value([-8, -3, -10]) == -3
assert largest_value([2, 9, 4]) == 9
assert largest_value([5, 5]) == 5
```

The correction follows from the failed assumption.

### Worked investigation: returning too early

```python
# Intentionally incorrect.
def contains_value(numbers, target):
    for number in numbers:
        if number == target:
            return True
        else:
            return False
```

Test:

- Input: [4, 7], target 7
- Expected: True
- Actual: False

Trace:

1. Read 4.
2. Compare 4 == 7: false.
3. Execute return False.
4. End the entire function.
5. Never examine 7.

The mistake is treating “this value does not match” as evidence that “no value matches.”

Correct version:

```python
# Return whether any value matches the target.
def contains_value(numbers, target):
    for number in numbers:
        if number == target:
            return True

    # Only conclude absence after checking every value.
    return False
```

This also gives the correct result for an empty list.

### Inspecting values with useful labels

```python
# Temporary diagnostic version.
def contains_value(numbers, target):
    for index in range(len(numbers)):
        number = numbers[index]

        # Label the values so the output is interpretable.
        print("index:", index, "number:", number, "target:", target)

        if number == target:
            return True

    return False
```

This is more informative than:

```python
print(number)
```

The label and position explain what the value represents.

### Inspecting unexpected types

```python
# A value that looks numeric may still be text.
value = "12"

print("Value:", value)
print("Type:", type(value))
```

Output:

```
Value: 12
Type: <class 'str'>
```

The printed appearance of 12 alone does not establish its type.

### A debugger

A debugger is a tool that lets you pause execution and inspect program state.

A breakpoint is a chosen location where a debugger pauses.

Common debugger actions include:

- Step over: execute the next statement without entering its function calls one line at a time.
- Step into: enter a called function so you can inspect its execution.
- Step out: finish the current function and return to its caller.
- Continue: run until another breakpoint or stopping event.

Exact controls vary by editor. The underlying task is the same: inspect the state at a relevant point.

A debugger does not decide whether your algorithm is correct. You still need an expected behavior to compare against.

### Keep the failed case

A regression is a bug introduced or reintroduced after a change.

A regression test preserves a case that previously failed so you can check that the failure stays fixed.

After correcting contains_value, keep:

```python
# The target appears after a nonmatching first element.
assert contains_value([4, 7], 7) == True
```

Also test other meaningful cases:

```python
assert contains_value([7, 4], 7) == True
assert contains_value([4, 5], 7) == False
assert contains_value([], 7) == False
```

### What beginners often get wrong

Changing the failing test’s expected answer to match the program hides the problem.

Establish the expected answer from the specification and a manual calculation.

### Chapter practice

1. Find a small failing input for a function that initializes the smallest value to 0.
2. Fix the loop boundary in the program below.
3. Explain why the second function fails to add all values.
4. Write a regression test for a search function that used to skip the final item.

```python
# Problem 2: intentionally incorrect.
def print_all(numbers):
    index = 0

    while index <= len(numbers):
        print(numbers[index])
        index = index + 1
```

```python
# Problem 3: intentionally incorrect.
def total(numbers):
    result = 0

    for number in numbers:
        result = result + number
        return result
```

#### Answers and explanations

1. For a nonempty input requirement, [1] is enough. The correct smallest value is 1. A function starting at 0 and replacing only when it sees a smaller value incorrectly returns 0.

2.

```python
# Print only valid positions.
def print_all(numbers):
    index = 0

    while index < len(numbers):
        print(numbers[index])
        index = index + 1
```

index == len(numbers) is outside the valid nonnegative range.

3. return result is inside the loop. The function ends after its first iteration.

Correct version:

```python
# Return only after every input has been processed.
def total(numbers):
    result = 0

    for number in numbers:
        result = result + number

    return result
```

This also returns 0 for an empty input.

4. For a function returning an index:

```python
# The only match is at the final position.
assert find_position([2, 4, 9], 9) == 2
```

The test directly exercises the previously skipped position.

## Chapter 2.7: Testing your own code

A test checks behavior under specified conditions.

A test case usually contains:

- An input.
- An expected result or property.
- A comparison with actual behavior.

A test suite is a collection of tests.

### Begin with a contract

A function’s contract describes what callers must supply and what the function promises.

A precondition is a requirement that must hold before the function runs.

A postcondition is a requirement that must hold after successful execution.

For a maximum function:

Precondition: The input is a nonempty list of integers.

Postcondition: The returned integer appears in the input and is at least as large as every input value.

Mutation rule: The input list remains unchanged.

Without a contract, it is difficult to decide whether an unusual result is a bug.

For example, should an empty maximum input:

- Return None?
- Raise an exception?
- Be prohibited?

Any of these can be part of an appropriate contract. The choice must be stated.

### Test categories

For a function that searches a list for a target:

| Category | Example | Expected result |
| --- | --- | --- |
| Empty input | [], 5 | -1 |
| One item, present | [5], 5 | 0 |
| One item, absent | [4], 5 | -1 |
| First position | [5, 2, 3], 5 | 0 |
| Middle position | [2, 5, 3], 5 | 1 |
| Last position | [2, 3, 5], 5 | 2 |
| Absent target | [2, 3, 4], 5 | -1 |
| Repeated target | [5, 2, 5], 5 | 0 |
| Negative values | [-3, -1], -1 | 1 |

These cases test different possible mistakes.

Writing ten tests that all place the target in the middle does not provide the same coverage.

### Boundary tests

A boundary is a point where behavior changes.

For:

```python
if score >= 60:
```

use values around 60:

| Score | Expected classification |
| --- | --- |
| 59 | Fail |
| 60 | Pass |
| 61 | Pass |

The exact boundary, 60, distinguishes >= from >.

### A test oracle

A test oracle is the source you use to determine the expected answer.

For small exercises, your oracle can be:

- A manual calculation.
- A direct reading of the specification.
- A trusted built-in operation.
- A slower reference implementation that is easier to verify.

Do not use the same potentially incorrect reasoning to produce both the solution and its expected answer.

### Assertions with helpful messages

```python
# Check a result and include context if the check fails.
actual = find_position([2, 3, 5], 5)

assert actual == 2, f"Expected index 2, received {actual}"
```

The expression after the comma provides the assertion’s error message.

A small suite can use a list of tuples:

```python
# Each tuple contains: input list, target, expected index.
test_cases = [
    ([], 5, -1),
    ([5], 5, 0),
    ([4], 5, -1),
    ([2, 3, 5], 5, 2),
    ([5, 2, 5], 5, 0),
]

# Unpack each case into three names.
for numbers, target, expected in test_cases:
    actual = find_position(numbers, target)

    assert actual == expected, (
        f"Input={numbers}, target={target}, "
        f"expected={expected}, actual={actual}"
    )

print("Search checks passed")
```

The parentheses allow the assertion message to span source lines. Adjacent string literals and f-strings inside this expression are combined into one message.

### Test mutation promises

A returned value can be correct while the function still violates its contract.

For example, a function might return a sorted result but unexpectedly alter its input.

```python
# Return a sorted copy.
def sorted_copy(numbers):
    return sorted(numbers)

# Preserve the original input for comparison.
numbers = [3, 1, 2]
before = numbers.copy()

result = sorted_copy(numbers)

# Check the result.
assert result == [1, 2, 3]

# Check the no-mutation promise.
assert numbers == before

# Check that the output is a separate list.
assert result is not numbers
```

Each assertion verifies a different requirement.

For nested data, remember that a shallow snapshot can share inner objects. Choose a suitable copy for the mutation behavior being tested.

### Test repeated calls

A function should not accidentally carry information from one call into another unless that behavior is intentional.

This is one reason to avoid mutable default arguments.

A default argument value is a value used when the caller omits an argument.

Safe basic example:

```python
# Use 1 when amount is omitted.
def increase(number, amount=1):
    return number + amount

assert increase(5) == 6
assert increase(5, 3) == 8
```

But this is dangerous:

```python
# Intentionally problematic default.
def record(value, items=[]):
    items.append(value)
    return items
```

The default list is created when the function definition executes. It is then reused by calls that omit items.

If run in a fresh session:

```python
print(record(1))  # [1]
print(record(2))  # [1, 2]
```

Use None when you want a fresh list for each omitted argument:

```python
# Create a new list for each call that omits items.
def record(value, items=None):
    if items is None:
        items = []

    items.append(value)
    return items

assert record(1) == [1]
assert record(2) == [2]
```

This function still intentionally mutates a list explicitly supplied by the caller.

### Testing properties

Sometimes you can check a property even when you have not manually written the complete expected output.

A property is a requirement that should hold across a class of inputs.

For a string-reversal function:

Reversing a string twice should recover the original string.

```python
# Use the reverse_text function from Part 1.
text = "abcd"

assert reverse_text(reverse_text(text)) == text
```

Another property:

```python
# Reversal should preserve length.
assert len(reverse_text(text)) == len(text)
```

These are useful, but neither property alone proves that reversal is correct.

A function that returns its input unchanged passes both checks.

Therefore, also check a concrete example:

```python
assert reverse_text("abcd") == "dcba"
```

### Testing relationships between inputs

A metamorphic test checks a known relationship between related inputs and outputs.

For a total function:

Appending zero should not change the total.

```python
numbers = [2, -3, 5]

assert total(numbers + [0]) == total(numbers)
```

For a duplicate detector:

Appending another copy of an existing value must create a duplicate.

```python
numbers = [2, 4, 7]

assert has_duplicate(numbers + [4]) == True
```

Such tests supplement concrete expected-answer tests.

### Passing tests does not prove correctness

Suppose a function is:

```python
# Intentionally incorrect general solution.
def largest_value(numbers):
    return numbers[-1]
```

It passes:

```python
assert largest_value([1, 2, 3]) == 3
assert largest_value([4, 5, 6]) == 6
```

Both tests happen to place the largest value last.

The function fails:

```python
assert largest_value([9, 1, 2]) == 9
```

Tests provide evidence for the cases and properties they check.

A correctness argument explains why the algorithm satisfies its contract for every allowed input.

We will develop those arguments more formally later.

### Common misconception

“It passed the examples, so it is correct.”

Examples can miss an entire category of failures. Ask what assumption each example actually checks.

### Chapter practice

1. Design three tests that distinguish score > 60 from score >= 60.
2. Write four meaningful cases for a duplicate detector.
3. State a precondition and postcondition for first_repeat.
4. Give a concrete test that catches a fake reversal function which returns its input unchanged.
5. Explain why testing only positive values would miss a maximum function initialized to zero.

#### Answers and explanations

1. For the intended rule “60 or higher passes”:

```python
assert passes(59) == False
assert passes(60) == True
assert passes(61) == True
```

The 60 case directly catches the wrong comparison operator.

2.

```python
# Empty input.
assert has_duplicate([]) == False

# One value cannot duplicate itself without another occurrence.
assert has_duplicate([5]) == False

# Distinct values.
assert has_duplicate([1, 2, 3]) == False

# A repeat separated from its earlier occurrence.
assert has_duplicate([1, 2, 1]) == True
```

An adjacent repeat such as [5, 5] is another useful case.

3. Precondition: The input is a list of integers.

Postcondition: Return the value whose second occurrence appears earliest when scanning left to right. Return None if no value repeats.

Mutation rule: Do not change the input list.

4.

```python
assert reverse_text("ab") == "ba"
```

A one-character string or palindrome would not expose the fake implementation.

A palindrome is a sequence that reads the same forward and backward.

5. Any positive value is greater than the incorrect initial zero, so positive-only tests may replace zero and appear to work.

An all-negative input exposes the invalid starting candidate:

```python
assert largest_value([-3, -8]) == -3
```

## Chapter 2.8: Complete investigation and test design

We will combine tracing, debugging, contracts, and testing in one problem.

This is an introductory sequence problem. It uses only ideas already introduced.

### Problem: longest strictly increasing consecutive run

Given a list of integers, return the length of its longest strictly increasing consecutive run.

A consecutive run uses neighboring positions without skipping any.

Strictly increasing means each next value is greater than the immediately preceding value. Equal values break the run.

| Input | Longest qualifying run | Answer |
| --- | --- | --- |
| [1, 2, 3] | [1, 2, 3] | 3 |
| [3, 2, 1] | Any one item | 1 |
| [1, 2, 2, 3, 4] | Final [2, 3, 4] | 3 |
| [1, 3, 2, 4, 5] | [2, 4, 5] | 3 |
| [] | None | 0 |

A run is not allowed to skip positions.

For [1, 3, 2, 4, 5], choosing [1, 2, 4, 5] skips the 3. That is a different problem.

### State the contract

Precondition: numbers is a list of integers.

Postcondition: Return the maximum length of a consecutive strictly increasing run. Return 0 for an empty list.

Mutation rule: Leave the input unchanged.

### Work through an example by hand

Input:

```
[1, 2, 2, 3, 4, 1]
```

Read left to right:

1. Start with [1], length 1.
2. 2 > 1, so extend to [1, 2], length 2.
3. The next 2 is not greater than 2, so start a new run [2].
4. 3 > 2, giving [2, 3], length 2.
5. 4 > 3, giving [2, 3, 4], length 3.
6. 1 is not greater than 4, so start [1].

The longest length encountered is 3.

### Identify what must be remembered

We need two quantities:

- current_length: length of the increasing run ending at the current position.
- best_length: longest run encountered anywhere so far.

These meanings are different.

If we store only the current run length, we lose an earlier best when a later run breaks.

### A plausible incorrect attempt

```python
# Intentionally incorrect: counts increases without resetting.
def longest_run_wrong(numbers):
    if len(numbers) == 0:
        return 0

    count = 1

    for index in range(1, len(numbers)):
        if numbers[index] > numbers[index - 1]:
            count = count + 1

    return count
```

Test:

- Input: [1, 2, 0, 1]
- Expected: 2
- Actual: 3

Why?

It counts two successful increases occurring in different runs and combines them.

Trace:

| Pair examined | Increasing? | count afterward |
| --- | --- | --- |
| 1, 2 | Yes | 2 |
| 2, 0 | No | 2 |
| 0, 1 | Yes | 3 |

The code does not represent consecutive-run length.

### A second incomplete correction

Suppose we reset on a break but return only the final run length.

That fails for:

```
[1, 2, 3, 0]
```

The final run has length 1, but the best earlier run has length 3.

This establishes why we need two separate variables.

### Correct algorithm in plain English

1. If there are no values, return zero.
2. Start the current run length at one.
3. Start the best run length at one.
4. For each position after the first:
   - If the value exceeds the previous value, extend the current run.
   - Otherwise, start a new run of length one.
5. Update the best length if the current run is longer.
6. Return the best length.

### Implementation

```python
# Return the longest consecutive strictly increasing run length.
def longest_increasing_run(numbers):
    # Define the answer for an empty input.
    if len(numbers) == 0:
        return 0

    # A nonempty list begins with a one-element run.
    current_length = 1

    # That first run is initially the best known run.
    best_length = 1

    # Compare each later element with its immediate predecessor.
    for index in range(1, len(numbers)):
        if numbers[index] > numbers[index - 1]:
            # Extend the run ending at the previous position.
            current_length = current_length + 1
        else:
            # The current element starts a new run.
            current_length = 1

        # Preserve the best result even if later runs become shorter.
        if current_length > best_length:
            best_length = current_length

    return best_length
```

### Full trace

Input:

```
[1, 2, 2, 3, 4, 1]
```

| Index | Previous value | Current value | Strict increase? | current_length afterward | best_length afterward |
| --- | --- | --- | --- | --- | --- |
| 0 | — | 1 | Initialization | 1 | 1 |
| 1 | 1 | 2 | Yes | 2 | 2 |
| 2 | 2 | 2 | No | 1 | 2 |
| 3 | 2 | 3 | Yes | 2 | 2 |
| 4 | 3 | 4 | Yes | 3 | 3 |
| 5 | 4 | 1 | No | 1 | 3 |

Returned value: 3.

### Why the algorithm works

We can explain each variable’s meaning.

After processing position index:

- current_length is the length of the longest strictly increasing consecutive run ending exactly at index.
- best_length is the longest such run found through index.

There are only two possibilities for extending a run:

Case 1: the current value is greater than the previous value.

The current run can extend the run ending at the previous position.

Therefore: new current length = previous current length + 1

Case 2: the current value is not greater than the previous value.

No strictly increasing consecutive run can cross that pair.

The current value must start a new run of length one.

After either case, comparing current_length against best_length preserves the best result seen.

This reasoning applies to every position, including repeated and negative values.

### Choose tests by failure mode

| Test | Expected | Mistake it can expose |
| --- | --- | --- |
| [] | 0 | Accessing the first element without checking emptiness |
| [7] | 1 | Incorrect initialization |
| [1, 2, 3] | 3 | Failing to extend a run |
| [3, 2, 1] | 1 | Failing to reset |
| [2, 2, 2] | 1 | Using >= instead of > |
| [1, 2, 0, 1] | 2 | Combining separate runs |
| [1, 2, 3, 0] | 3 | Returning only the final run |
| [5, 1, 2, 3] | 3 | Missing a best run at the end |
| [-3, -2, -1] | 3 | Assuming values must be positive |

### Runnable test suite

```python
# Each case contains an input list and expected answer.
test_cases = [
    ([], 0),
    ([7], 1),
    ([1, 2, 3], 3),
    ([3, 2, 1], 1),
    ([2, 2, 2], 1),
    ([1, 2, 0, 1], 2),
    ([1, 2, 3, 0], 3),
    ([5, 1, 2, 3], 3),
    ([-3, -2, -1], 3),
    ([1, 2, 2, 3, 4, 1], 3),
]

for numbers, expected in test_cases:
    # Retain a snapshot to check the no-mutation promise.
    before = numbers.copy()

    # Call the function.
    actual = longest_increasing_run(numbers)

    # Check the returned answer.
    assert actual == expected, (
        f"Input={numbers}, expected={expected}, actual={actual}"
    )

    # Check that the input was preserved.
    assert numbers == before

print("Longest-run checks passed")
```

### Useful properties

For a nonempty input:

1 ≤ answer ≤ number of elements

Appending one element cannot reduce the best run already present.

```python
# The old input remains a prefix of the extended input.
numbers = [1, 2, 0, 1]

old_answer = longest_increasing_run(numbers)
new_answer = longest_increasing_run(numbers + [5])

assert new_answer >= old_answer
```

Adding the same integer to every value preserves all greater-than relationships:

```python
# Construct an input with every value shifted by ten.
numbers = [1, 2, 0, 1]
shifted = []

for number in numbers:
    shifted.append(number + 10)

assert longest_increasing_run(shifted) == longest_increasing_run(numbers)
```

These property checks supplement the concrete test cases.

### Chapter practice

1. Trace the algorithm for [4, 1, 2, 3, 0, 5].
2. Change the rule from strictly increasing to nondecreasing. Which comparison changes?
3. Write a function returning the longest consecutive run of equal values.
4. Give an input that catches a version which resets current_length to zero instead of one.
5. Explain why current_length and best_length cannot be replaced by one variable in this approach.

#### Answers and explanations

1.

| Value processed | current_length | best_length |
| --- | --- | --- |
| 4 | 1 | 1 |
| 1 | 1 | 1 |
| 2 | 2 | 2 |
| 3 | 3 | 3 |
| 0 | 1 | 3 |
| 5 | 2 | 3 |

Answer: 3, from [1, 2, 3].

2. Nondecreasing means each next value is greater than or equal to the previous value.

Change:

```python
numbers[index] > numbers[index - 1]
```

to:

```python
numbers[index] >= numbers[index - 1]
```

Under this revised rule, [2, 2, 2] has a qualifying run of length 3.

3.

```python
# Return the longest consecutive block of equal values.
def longest_equal_run(numbers):
    if len(numbers) == 0:
        return 0

    current_length = 1
    best_length = 1

    for index in range(1, len(numbers)):
        if numbers[index] == numbers[index - 1]:
            # Equal neighbors extend the current block.
            current_length = current_length + 1
        else:
            # A different value begins a new block.
            current_length = 1

        if current_length > best_length:
            best_length = current_length

    return best_length

assert longest_equal_run([]) == 0
assert longest_equal_run([5]) == 1
assert longest_equal_run([2, 2, 1, 1, 1, 3]) == 3
assert longest_equal_run([1, 2, 3]) == 1
```

4. Use:

```
[3, 1, 2]
```

The correct answer is 2, from [1, 2].

If the break at 1 resets the current length to zero, the increase to 2 brings it only to one. The function can incorrectly return 1.

The current item already forms a one-element run, so reset to one.

5. The current run can become shorter when a break occurs. The best run must retain information about earlier runs.

For [1, 2, 3, 0]:

- Final current length: 1.
- Best length: 3.

One variable cannot hold both of those meanings at that moment.

## Running glossary: additions from Part 2

Retain the Part 1 glossary. These entries extend it.

| Term | Meaning |
| --- | --- |
| Binary | A number system based on powers of two. |
| Binding | An association between a name and an object. |
| Bit | A unit with two possible states, represented as 0 or 1. |
| Boundary | A point where an algorithm’s behavior changes. |
| Breakpoint | A selected location where a debugger pauses execution. |
| Byte | A group of eight bits. |
| Call frame | The execution context for one function call. |
| Call stack | The active function calls organized by their calling relationships. |
| Consecutive run | A sequence using neighboring positions without skipping. |
| Contract | The requirements a function assumes and the behavior it promises. |
| Correctness argument | An explanation of why an algorithm satisfies its contract for every allowed input. |
| Debugger | A tool for pausing and inspecting execution. |
| Deep copy | A copy that recursively copies contained objects as appropriate. |
| Default argument value | A value used when a caller omits an argument. |
| Evaluation order | The sequence in which parts of an expression are evaluated. |
| Hypothesis | A proposed explanation that can be investigated. |
| Import | An instruction making a module or selected functionality available. |
| In place | Modifying an existing data structure directly. |
| Invariant | A statement that remains true at specified points in an algorithm. |
| Loop invariant | A statement maintained before or after each iteration. |
| Memory | Storage used to represent working information. |
| Metamorphic test | A test of a known relationship between related inputs and outputs. |
| Minimal failing example | A small input that still exposes a bug. |
| Module | A reusable unit of Python code. |
| Mutation | A change to an existing mutable object. |
| Nondecreasing | Each next value is greater than or equal to the previous value. |
| Off-by-one error | A boundary mistake that is one position too early or too late. |
| Palindrome | A sequence that reads the same forward and backward. |
| Persistent storage | Storage that retains saved information after execution ends. |
| Postcondition | A promised property after successful execution. |
| Precondition | A requirement that must hold before execution. |
| Property | A requirement expected to hold across a class of inputs. |
| RAM | A computer’s working memory for active programs. |
| Reassignment | Changing which object or result a name refers to. |
| Rebinding | Changing a name’s association with an object. |
| Reference | A connection through which an object can be accessed. |
| Regression | A bug introduced or reintroduced after a change. |
| Regression test | A retained test for behavior that previously failed. |
| Reproducible failure | A failure that can be triggered again under known conditions. |
| Shallow copy | A new outer collection containing references to the original contained objects. |
| Side effect | An observable action beyond returning a result. |
| SSD | A common device providing persistent storage. |
| State | The information describing a program’s current situation. |
| Strictly increasing | Each next value is greater than the previous value. |
| Test case | Specified conditions and a check of expected behavior. |
| Test oracle | The source used to determine an expected answer. |
| Test suite | A collection of tests. |

## Part 2 readiness check

Before Part 3, you should be able to do the following without running the code first:

- Predict the difference between b = a and b = a.copy().
- Explain why a shallow copy can still share inner lists.
- Predict whether a function mutates its caller’s data.
- Trace a function calling another function and returning a value.
- Record a loop’s final failed condition.
- Identify an off-by-one error from a table of valid positions.
- Reduce a failing example and state a specific debugging hypothesis.
- Design tests around empty inputs, boundaries, duplicates, and unusual value ranges.
- Explain the difference between passing tests and justifying correctness.
- Describe the meaning of each important variable throughout a loop.

End of Part 2. Next: Part 3, Big-O and Complexity Analysis.
