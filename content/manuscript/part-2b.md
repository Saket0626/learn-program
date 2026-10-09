# Part 2 continued

## Chapter 2.3: Mutation, reassignment, and copying

This chapter explains why changing one variable sometimes appears to change another.

The key question is:

Are there two separate objects, or two names referring to one object?

### Reassignment

Reassignment makes a name refer to a different object or result.

```python
# Both names initially refer to the integer value 10.
a = 10
b = a

# Change what a refers to.
a = 20

print(a)  # 20
print(b)  # 10
```

Reassigning a does not reassign b.

### Mutation

Mutation changes an existing mutable object.

```python
# Create one list.
a = [10, 20]

# Make another name refer to the same list.
b = a

# Change the existing shared list.
a.append(30)

print(a)  # [10, 20, 30]
print(b)  # [10, 20, 30]
```

Before the append, both names refer to one list. After the append, both names still refer to that same list. Its contents have changed.

### A trace that tracks object identity

We can assign imaginary labels to objects while tracing.

These labels are for our notebook. They are not actual memory addresses.

```python
# Create the first list object.
a = [1, 2]

# Share the first list.
b = a

# Mutate the first list.
a.append(3)

# Create a second list and reassign a.
a = [9]

print(a)
print(b)
```

| Instruction | a refers to | b refers to | List L1 | List L2 |
| --- | --- | --- | --- | --- |
| a = [1, 2] | L1 | Not assigned | [1, 2] | Does not exist |
| b = a | L1 | L1 | [1, 2] | Does not exist |
| a.append(3) | L1 | L1 | [1, 2, 3] | Does not exist |
| a = [9] | L2 | L1 | [1, 2, 3] | [9] |

Output:

```
[9]
[1, 2, 3]
```

The reassignment of a does not destroy L1, because b still refers to it.

### Equality versus identity

`==` asks whether values compare equal.

`is` asks whether two references identify the same object.

```python
# Create two separate lists with equal contents.
a = [1, 2]
b = [1, 2]

# Compare values.
print(a == b)  # True

# Compare identity.
print(a is b)  # False
```

Now add an alias:

```python
# Make c refer to a's existing list.
c = a

print(a == c)  # True
print(a is c)  # True
```

Do not infer identity from equality.

Do not use `is` to compare numeric or string values. Python may reuse some immutable objects internally, and your algorithm should not depend on that behavior.

Use:

```python
# Compare numeric values.
number == 5
```

Use `is` for intended identity checks, especially:

```python
# Test the special absence marker.
result is None
```

### A shallow copy

A shallow copy creates a new outer collection but retains references to the same contained objects.

```python
# Create an original list.
original = [1, 2]

# Create a different outer list.
copied = original.copy()

# Changing the new outer list does not change the original outer list.
copied.append(3)

print(original)  # [1, 2]
print(copied)    # [1, 2, 3]
```

For a flat list of integers, this often gives the behavior beginners expect from a copy.

For nested lists, there is another layer.

### Nested lists and shared inner objects

```python
# Create an outer list containing two inner lists.
original = [[1, 2], [3, 4]]

# Copy only the outer list.
copied = original.copy()

# Change an inner list shared by both outer lists.
copied[0].append(9)

print(original)
print(copied)
```

Output:

```
[[1, 2, 9], [3, 4]]
[[1, 2, 9], [3, 4]]
```

The outer lists differ. The inner lists are shared.

Replacing an element in the copied outer list behaves differently:

```python
# Create a nested list and a shallow copy.
original = [[1, 2], [3, 4]]
copied = original.copy()

# Replace a reference in the copied outer list.
copied[0] = [99]

print(original)  # [[1, 2], [3, 4]]
print(copied)    # [[99], [3, 4]]
```

This changes one slot in copied. It does not mutate the original shared inner list.

### A deep copy

A deep copy recursively copies contained objects as appropriate, instead of copying only the outer collection.

For nested lists of ordinary values:

```python
# Import Python's copying module.
import copy

# Create nested mutable data.
original = [[1, 2], [3, 4]]

# Copy the nested list structure.
copied = copy.deepcopy(original)

# Change an inner list in the copy.
copied[0].append(9)

print(original)  # [[1, 2], [3, 4]]
print(copied)    # [[1, 2, 9], [3, 4]]
```

A module is a reusable unit of Python code that provides related functionality.

An import makes a module or selected functionality available to your program.

Deep copying is not automatically the best choice. It performs additional work and may be unnecessary. First determine which objects you need to change independently.

### A classic trap: repeated rows

Suppose you want a grid with three rows and two columns.

A grid is a collection arranged in rows and columns.

This looks reasonable but shares one inner list:

```python
# Intentionally creates three references to one row.
grid = [[0, 0]] * 3

# Change the first entry of the first row.
grid[0][0] = 7

print(grid)
```

Output:

```
[[7, 0], [7, 0], [7, 0]]
```

Why?

`[0, 0]` creates one row. Repeating the outer list repeats references to that row.

To create separate rows:

```python
# Begin with an empty outer list.
grid = []

# Create a new row during each iteration.
for row_number in range(3):
    grid.append([0, 0])

# Change only the first row.
grid[0][0] = 7

print(grid)
```

Output:

```
[[7, 0], [0, 0], [0, 0]]
```

### An update operator can mutate

In Part 1, numeric `+=` acted like an arithmetic reassignment.

For a list, `+=` extends the existing list:

```python
# Share one list.
a = [1, 2]
b = a

# Extend the existing list.
a += [3]

print(b)  # [1, 2, 3]
```

Compare ordinary list addition:

```python
# Share one list.
a = [1, 2]
b = a

# Build a new list and reassign a.
a = a + [3]

print(a)  # [1, 2, 3]
print(b)  # [1, 2]
```

This is why “+= always means exactly the same thing as assigning with +” is too broad.

### Common misconception

“If two variables have different names, they must hold separate data.”

Different names can refer to one mutable object. Track objects as well as names.

### Chapter practice

1. Predict both printed lists in the first program.
2. Explain why the nested-list copy in the second program affects a.
3. Construct a two-row, three-column zero grid with independent rows.
4. Predict the equality and identity results in the third program.

```python
# Problem 1.
a = [1]
b = a

b.append(2)
b = [8]

print(a)
print(b)
```

```python
# Problem 2.
a = [[1], [2]]
b = a.copy()

b[1].append(3)

print(a)
```

```python
# Problem 4.
a = [5]
b = a.copy()
c = a

print(a == b)
print(a is b)
print(a is c)
```

#### Answers and explanations

1.

```
[1, 2]
[8]
```

`b.append(2)` mutates the shared list. `b = [8]` then makes b refer to a different list.

2. Output:

```
[[1], [2, 3]]
```

The shallow copy creates a new outer list but shares the inner lists. `b[1].append(3)` changes one of those shared inner lists.

3.

```python
# Construct a fresh row on every iteration.
grid = []

for row_number in range(2):
    grid.append([0, 0, 0])

# Verify that the rows are independent.
grid[0][0] = 9

assert grid == [[9, 0, 0], [0, 0, 0]]
```

4.

```
True
False
True
```

a and b have equal contents but are different lists. a and c refer to the same list.

## Chapter 2.4: Function calls, local names, and the call stack

When a function runs, Python must remember:

- Its arguments.
- Its local variables.
- Where execution currently is inside that function.
- Where to continue after the function returns.

That information belongs to the current function call.

### Call frames

A call frame is the execution context for one function call, including its local names and execution position.

Consider:

```python
# Double one number.
def double(number):
    result = number * 2
    return result


# Make two separate calls.
first = double(3)
second = double(7)

print(first, second)
```

Output:

```
6 14
```

The first call has its own local number and result.

The second call has another call frame with its own local names.

| Call | Local number | Local result | Returned value |
| --- | --- | --- | --- |
| double(3) | 3 | 6 | 6 |
| double(7) | 7 | 14 | 14 |

The second call does not resume the first call’s local state.

### The call stack

A stack is a structure where the most recently added item is the first one removed.

The call stack tracks active function calls. When one function calls another, the caller waits while the newer call runs.

We will implement general stacks in Part 4. Here, we only need their role in function execution.

### Worked example: one function calls another

```python
# Add one to an input.
def add_one(number):
    result = number + 1
    return result


# Call add_one, then double its returned result.
def calculate(number):
    increased = add_one(number)
    doubled = increased * 2
    return doubled


# Begin the calculation.
answer = calculate(4)

print(answer)
```

Output:

```
10
```

Execution order:

1. The outer program calls calculate(4).
2. calculate receives number = 4.
3. calculate calls add_one(4).
4. add_one receives its own number = 4.
5. add_one calculates and returns 5.
6. calculate resumes, assigning 5 to increased.
7. calculate calculates 10.
8. calculate returns 10.
9. The outer program assigns 10 to answer.
10. The outer program prints 10.

At the deepest point, the active calls are:

| Position | Execution context | Status |
| --- | --- | --- |
| Most recent | add_one(4) | Running |
| Below it | calculate(4) | Waiting for add_one |
| Oldest | Outer program | Waiting for calculate |

After add_one returns:

| Position | Execution context | Status |
| --- | --- | --- |
| Most recent | calculate(4) | Running again |
| Oldest | Outer program | Waiting |

The two parameters named number are separate local names in separate call frames.

### Return resumes the caller

```python
# Return a computed value.
def triple(number):
    return number * 3


# Evaluate the call before finishing the addition.
answer = triple(4) + 2

print(answer)  # 14
```

The caller behaves as though the function-call expression has been replaced with its returned value:

```python
answer = 12 + 2
```

That is a mental tracing technique, not a literal rewrite of your source file.

### Local reassignment does not reassign the caller’s variable

```python
# Reassign a local parameter.
def change_number(number):
    number = 99
    return number


# Store the caller's value.
original = 5

# Retain the returned result separately.
changed = change_number(original)

print(original)  # 5
print(changed)   # 99
```

Initially, original and the parameter number refer to the same integer value.

Then `number = 99` changes only the local name.

### Mutation through a parameter can affect the caller

```python
# Change the list supplied by the caller.
def add_marker(items):
    items.append("done")


# Create a list.
tasks = ["read"]

# The parameter refers to this same list.
add_marker(tasks)

print(tasks)  # ['read', 'done']
```

The function did not reassign tasks.

It changed the object that tasks refers to.

A side effect is an observable action beyond returning a value, such as changing a supplied list or printing output.

### Rebinding the parameter behaves differently

Binding means associating a name with an object. Rebinding means changing that association.

```python
# Replace only the local parameter's binding.
def replace_list(items):
    items = ["new"]


# Create the caller's list.
tasks = ["read"]

replace_list(tasks)

print(tasks)  # ['read']
```

The function creates another list and makes its local parameter refer to it.

The caller’s name still refers to the original list.

### A useful rule for arguments

When a Python function is called, its parameter names are bound to the supplied argument objects.

Consequences:

- Reassigning a parameter does not reassign the caller’s name.
- Mutating a supplied mutable object can affect what the caller sees.

This rule is more useful than memorizing ambiguous phrases such as “Python passes everything by reference.”

### State your mutation behavior

These two functions have different promises:

```python
# Return a new list without modifying the input.
def doubled_copy(numbers):
    result = []

    for number in numbers:
        result.append(number * 2)

    return result
```

```python
# Modify the supplied list directly.
def double_in_place(numbers):
    for index in range(len(numbers)):
        numbers[index] = numbers[index] * 2
```

In place means modifying the existing data structure rather than returning a separate replacement structure.

The second function returns None implicitly.

Neither style is always better. The problem’s requirements determine which is appropriate.

### What beginners often get wrong

A function can change the caller’s data even when it returns None.

Return values and side effects are separate ways a function can influence the rest of the program.

### Chapter practice

1. Trace outer(3) in the first program.
2. Predict the list printed by the second program.
3. Explain why the third program does not change items.
4. Write a function that returns a new list with 0 appended, without modifying its input.

```python
# Problem 1.
def inner(x):
    return x + 2


def outer(x):
    y = inner(x)
    return y * 3


print(outer(3))
```

```python
# Problem 2.
def change(values):
    values[0] = 99


items = [1, 2]
change(items)

print(items)
```

```python
# Problem 3.
def change(values):
    values = [99, 2]


items = [1, 2]
change(items)

print(items)
```

#### Answers and explanations

1. outer receives x = 3. It calls inner(3). inner returns 5. outer assigns y = 5. outer returns 5 * 3, which is 15. Output: 15.

2.

```
[99, 2]
```

The function mutates the supplied list.

3. It prints:

```
[1, 2]
```

The function reassigns only its local parameter.

4.

```python
# Return an extended copy.
def with_zero(numbers):
    copied = numbers.copy()
    copied.append(0)
    return copied


original = [4, 5]
result = with_zero(original)

assert original == [4, 5]
assert result == [4, 5, 0]
assert result is not original
```

`is not` checks that two references do not identify the same object.

## Chapter 2.5: Tracing code by hand

Tracing is not guessing the final answer.

It is carrying out the program’s rules while recording the changing state.

This distinction matters because a correct guess can hide an incorrect understanding.

### A repeatable tracing procedure

For a small program:

1. Write down the input.
2. List the variables you need to track.
3. Record their starting values.
4. Evaluate the next condition or expression.
5. Update only the values changed by that instruction.
6. Record output when it occurs.
7. Follow jumps caused by calls, returns, branches, or loops.
8. Stop only when execution actually ends.

Do not update a variable before the program does.

### Worked example: count record-breaking values

A value is record-breaking here if it is greater than every earlier value in the list.

For [3, 1, 5, 5, 7]:

- 3 establishes the first record.
- 1 does not exceed 3.
- The first 5 exceeds 3.
- The second 5 does not exceed 5.
- 7 exceeds 5.

The answer is 3.

```python
# Count values that establish a new strict maximum.
def count_records(numbers):
    # An empty list has no record-breaking values.
    if len(numbers) == 0:
        return 0

    # The first element establishes the initial record.
    largest = numbers[0]
    records = 1

    # Process the remaining elements.
    for index in range(1, len(numbers)):
        current = numbers[index]

        # Equality does not establish a new record.
        if current > largest:
            largest = current
            records = records + 1

    return records
```

For [3, 1, 5, 5, 7]:

| Event | index | current | largest before | Condition | largest after | records after |
| --- | --- | --- | --- | --- | --- | --- |
| Initialization | — | — | — | — | 3 | 1 |
| Iteration 1 | 1 | 1 | 3 | 1 > 3: false | 3 | 1 |
| Iteration 2 | 2 | 5 | 3 | 5 > 3: true | 5 | 2 |
| Iteration 3 | 3 | 5 | 5 | 5 > 5: false | 5 | 2 |
| Iteration 4 | 4 | 7 | 5 | 7 > 5: true | 7 | 3 |

Return value: 3.

### Trace conditions explicitly

A common mistake is to write only the variable values after successful branches.

That hides failed conditions, even though failed conditions explain why values did not change.

Recording `5 > 5: false` makes the strict comparison visible.

### Worked example: a while loop

```python
# Find the first position containing target.
# Return -1 when the target is absent.
def find_position(numbers, target):
    index = 0

    while index < len(numbers):
        if numbers[index] == target:
            return index

        index = index + 1

    return -1
```

For `find_position([8, 3, 6], 6)`:

| index before condition | index < 3 | Value examined | Equals target? | Next action |
| --- | --- | --- | --- | --- |
| 0 | True | 8 | No | Increase index to 1 |
| 1 | True | 3 | No | Increase index to 2 |
| 2 | True | 6 | Yes | Return 2 |

For an absent target, such as 9:

| index before condition | index < 3 | Value examined | Equals target? | Next action |
| --- | --- | --- | --- | --- |
| 0 | True | 8 | No | Increase to 1 |
| 1 | True | 3 | No | Increase to 2 |
| 2 | True | 6 | No | Increase to 3 |
| 3 | False | Not accessed | Not checked | Return -1 |

The final failed loop condition is part of the trace.

### Off-by-one errors

An off-by-one error occurs when a boundary is one position too early or too late.

Examples:

- Using `<= len(numbers)` where `< len(numbers)` is needed.
- Stopping before the final valid item.
- Using `range(1, limit)` when the problem includes limit.

For a list of length 3:

| Index | Valid? |
| --- | --- |
| 0 | Yes |
| 1 | Yes |
| 2 | Yes |
| 3 | No |

The length is not a valid nonnegative index.

### Worked example: nested loops

```python
# Print pairs of positions where the second comes after the first.
numbers = [10, 20, 30]

for first in range(len(numbers)):
    for second in range(first + 1, len(numbers)):
        print(first, second)
```

Trace:

| first | Values available to second | Pairs printed |
| --- | --- | --- |
| 0 | 1, 2 | (0, 1), (0, 2) |
| 1 | 2 | (1, 2) |
| 2 | None | None |

Output:

```
0 1
0 2
1 2
```

The inner loop does not always execute the same number of times.

When first is 2, the inner loop uses `range(3, 3)`, which contains no values.

### Loop invariants

An invariant is a statement that remains true at specified points in an algorithm.

A loop invariant describes something that remains true before or after each iteration.

For a running sum:

```python
total = 0

for number in numbers:
    total = total + number
```

A useful invariant is:

After each iteration, total equals the sum of the values processed so far.

This gives each variable a precise meaning.

If you reset total inside the loop, that meaning stops being true.

You do not need formal proof notation yet. Begin by writing one sentence describing what each important variable represents.

### Common misconception

Knowing what a variable contains on one example is not the same as knowing what it means throughout the algorithm.

“largest is currently 7” describes one state.

“largest is the greatest value processed so far” describes its role.

### Guided example

Trace:

```python
# Count values at least as large as the threshold.
numbers = [2, 5, 5, 1]
threshold = 5
count = 0

for number in numbers:
    if number >= threshold:
        count = count + 1
```

Expected count changes:

0, 1, 2, 2

The comparison uses `>=`, so both occurrences of 5 qualify.

### Chapter practice

1. Trace a running product for [2, 3, 4], starting from product = 1.
2. Trace find_position([4, 9, 4], 4). Which position is returned?
3. Write a sentence describing the meaning of seen immediately before each membership test in has_duplicate.
4. Predict the output of the nested loops below.

```python
# Problem 4.
for row in range(3):
    for column in range(row):
        print(row, column)
```

#### Answers and explanations

1.

```python
# Start with the multiplicative identity.
product = 1

for number in [2, 3, 4]:
    product = product * number
```

| Number | Product before | Product after |
| --- | --- | --- |
| 2 | 1 | 2 |
| 3 | 2 | 6 |
| 4 | 6 | 24 |

Starting at zero would make every later product zero.

2. It returns 0. The function returns immediately when it encounters the first matching value. It never reaches the second occurrence at index 2.

3. Immediately before testing the current value, seen contains the distinct values from all earlier positions. It must not already contain the current occurrence merely because we added it too early.

4.

```
1 0
2 0
2 1
```

For row = 0, range(0) is empty. For row = 1, column takes only 0. For row = 2, column takes 0 and 1.
