"""Part 5 companion: every algorithm from Chapters 5.1–5.21, plus the example checks."""

from collections import deque
import heapq


def recursive_sum(numbers, index=0):
    # The empty suffix contributes zero.
    if index == len(numbers):
        return 0
    # Add the current value to the sum of the remaining suffix.
    return numbers[index] + recursive_sum(numbers, index + 1)


def insertion_sort(numbers):
    # Preserve the caller's list.
    result = numbers.copy()
    for index in range(1, len(result)):
        # Save the value before shifting over its original position.
        current = result[index]
        position = index - 1
        # Shift larger values one position to the right.
        while position >= 0 and result[position] > current:
            result[position + 1] = result[position]
            position -= 1
        # Insert into the gap.
        result[position + 1] = current
    return result


def merge_sort(numbers):
    # Empty and one-element lists are already sorted.
    if len(numbers) <= 1:
        return numbers.copy()
    middle = len(numbers) // 2
    # Sort the two halves.
    left = merge_sort(numbers[:middle])
    right = merge_sort(numbers[middle:])
    result = []
    i = 0
    j = 0
    # Repeatedly take the smaller unused front value.
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1
    # At most one side still has unused elements.
    result.extend(left[i:])
    result.extend(right[j:])
    return result


def binary_search(numbers, target):
    # Candidate indices form a closed interval [left, right].
    left = 0
    right = len(numbers) - 1
    while left <= right:
        middle = left + (right - left) // 2
        if numbers[middle] == target:
            return middle
        if numbers[middle] < target:
            # The middle and everything before it are too small.
            left = middle + 1
        else:
            # The middle and everything after it are too large.
            right = middle - 1
    return -1


def lower_bound(numbers, target):
    # Search for a boundary in the half-open interval [left, right).
    left = 0
    right = len(numbers)
    while left < right:
        middle = (left + right) // 2
        if numbers[middle] < target:
            left = middle + 1
        else:
            # Middle might be the first qualifying position.
            right = middle
    return left


def sorted_pair_sum(numbers, target):
    left = 0
    right = len(numbers) - 1
    while left < right:
        total = numbers[left] + numbers[right]
        if total == target:
            return left, right
        if total < target:
            left += 1
        else:
            right -= 1
    return None


def move_zeros(numbers):
    write = 0
    for read in range(len(numbers)):
        if numbers[read] != 0:
            # Write the next retained value.
            numbers[write] = numbers[read]
            write += 1
    # Fill the unused suffix with zeros.
    for index in range(write, len(numbers)):
        numbers[index] = 0


def max_fixed_window(numbers, k):
    if k < 1 or k > len(numbers):
        raise ValueError("Require 1 <= k <= input length")
    total = 0
    # Build the first complete window.
    for index in range(k):
        total += numbers[index]
    best = total
    for right in range(k, len(numbers)):
        total += numbers[right]
        total -= numbers[right - k]
        best = max(best, total)
    return best


def min_positive_window(numbers, target):
    # Contract: target and every input value are positive.
    left = 0
    total = 0
    best = len(numbers) + 1
    for right in range(len(numbers)):
        total += numbers[right]
        # Remove left values while the current window still qualifies.
        while total >= target:
            best = min(best, right - left + 1)
            total -= numbers[left]
            left += 1
    if best == len(numbers) + 1:
        return 0
    return best


def build_prefix(numbers):
    prefix = [0]
    for number in numbers:
        prefix.append(prefix[-1] + number)
    return prefix


def count_target_subarrays(numbers, target):
    counts = {0: 1}
    prefix = 0
    answer = 0
    for number in numbers:
        prefix += number
        # Count earlier prefixes before recording the current prefix.
        answer += counts.get(prefix - target, 0)
        counts[prefix] = counts.get(prefix, 0) + 1
    return answer


def merge_intervals(intervals):
    # Contract: each interval has start <= end.
    ordered = sorted(intervals)
    merged = []
    for start, end in ordered:
        if not merged or start > merged[-1][1]:
            # Start a new merged interval.
            merged.append([start, end])
        else:
            # Extend only if this interval reaches farther.
            merged[-1][1] = max(merged[-1][1], end)
    return merged


def bfs_distances(adjacency, start):
    # Vertices are valid integers from 0 through V - 1.
    distance = [-1] * len(adjacency)
    distance[start] = 0
    pending = deque([start])
    while pending:
        vertex = pending.popleft()
        for neighbor in adjacency[vertex]:
            if distance[neighbor] == -1:
                # Mark immediately when the vertex enters the queue.
                distance[neighbor] = distance[vertex] + 1
                pending.append(neighbor)
    return distance


def dfs_order(adjacency, start):
    seen = [False] * len(adjacency)
    order = []

    def visit(vertex):
        # Mark before following edges to prevent cycles from repeating work.
        seen[vertex] = True
        order.append(vertex)
        for neighbor in adjacency[vertex]:
            if not seen[neighbor]:
                visit(neighbor)

    visit(start)
    return order


def all_subsets(numbers):
    # Contract: input values are distinct.
    result = []
    path = []

    def choose(index):
        if index == len(numbers):
            # Save a snapshot of the current selection.
            result.append(path.copy())
            return
        # Choice 1: exclude this element.
        choose(index + 1)
        # Choice 2: include this element.
        path.append(numbers[index])
        choose(index + 1)
        # Restore the state before returning to the caller.
        path.pop()

    choose(0)
    return result


def finish_time(interval):
    return interval[1]


def select_meetings(intervals):
    ordered = sorted(intervals, key=finish_time)
    chosen = []
    last_end = None
    for start, end in ordered:
        if last_end is None or start >= last_end:
            chosen.append((start, end))
            last_end = end
    return chosen


def topological_order(adjacency):
    indegree = [0] * len(adjacency)
    for neighbors in adjacency:
        for neighbor in neighbors:
            indegree[neighbor] += 1
    ready = deque()
    for vertex in range(len(adjacency)):
        if indegree[vertex] == 0:
            ready.append(vertex)
    order = []
    while ready:
        vertex = ready.popleft()
        order.append(vertex)
        for neighbor in adjacency[vertex]:
            indegree[neighbor] -= 1
            if indegree[neighbor] == 0:
                ready.append(neighbor)
    if len(order) != len(adjacency):
        return None
    return order


def dijkstra(adjacency, start):
    # Each adjacency entry contains (neighbor, weight) pairs.
    for neighbors in adjacency:
        for neighbor, weight in neighbors:
            if weight < 0:
                raise ValueError("Dijkstra requires nonnegative weights")
    distance = [float("inf")] * len(adjacency)
    distance[start] = 0
    pending = [(0, start)]
    while pending:
        current_distance, vertex = heapq.heappop(pending)
        if current_distance != distance[vertex]:
            # A later discovery improved this vertex.
            continue
        for neighbor, weight in adjacency[vertex]:
            candidate = current_distance + weight
            if candidate < distance[neighbor]:
                distance[neighbor] = candidate
                heapq.heappush(pending, (candidate, neighbor))
    return distance


def days_needed(weights, capacity):
    # Contract: capacity is at least the largest weight.
    days = 1
    load = 0
    for weight in weights:
        if load + weight > capacity:
            days += 1
            load = 0
        load += weight
    return days


def minimum_capacity(weights, days):
    # Contract: nonempty positive weights and days >= 1.
    left = max(weights)
    right = sum(weights)
    while left < right:
        middle = (left + right) // 2
        if days_needed(weights, middle) <= days:
            # This capacity works. Search for a smaller working value.
            right = middle
        else:
            # This capacity is too small.
            left = middle + 1
    return left


def count_set_bits(number):
    if number < 0:
        raise ValueError("Require a nonnegative integer")
    count = 0
    while number:
        number = number & (number - 1)
        count += 1
    return count


def single_unpaired(numbers):
    answer = 0
    for number in numbers:
        answer ^= number
    return answer


def next_greater_values(numbers):
    answer = [None] * len(numbers)
    pending = []
    for index in range(len(numbers)):
        while pending and numbers[index] > numbers[pending[-1]]:
            previous = pending.pop()
            answer[previous] = numbers[index]
        pending.append(index)
    return answer


def stairs_recursive(n):
    # Contract: n is a nonnegative integer.
    if n <= 1:
        return 1
    return stairs_recursive(n - 1) + stairs_recursive(n - 2)


def stairs_memo(n):
    # Store the known base answers.
    memo = {0: 1, 1: 1}

    def solve(remaining):
        if remaining not in memo:
            memo[remaining] = solve(remaining - 1) + solve(remaining - 2)
        return memo[remaining]

    return solve(n)


def stairs_table(n):
    dp = [0] * (n + 1)
    # One empty sequence reaches zero steps.
    dp[0] = 1
    for step in range(1, n + 1):
        # Sequences whose final move is one step.
        dp[step] = dp[step - 1]
        if step >= 2:
            # Sequences whose final move is two steps.
            dp[step] += dp[step - 2]
    return dp[n]


def minimum_coins(coins, amount):
    impossible = amount + 1
    dp = [impossible] * (amount + 1)
    dp[0] = 0
    for total in range(1, amount + 1):
        for coin in coins:
            if coin <= total:
                dp[total] = min(dp[total], dp[total - coin] + 1)
    if dp[amount] == impossible:
        return -1
    return dp[amount]


def coin_combinations(coins, amount):
    dp = [0] * (amount + 1)
    # One empty combination makes zero.
    dp[0] = 1
    for coin in coins:
        for total in range(coin, amount + 1):
            dp[total] += dp[total - coin]
    return dp[amount]


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


def lcs_table(first, second):
    dp = []
    for i in range(len(first) + 1):
        dp.append([0] * (len(second) + 1))
    for i in range(1, len(first) + 1):
        for j in range(1, len(second) + 1):
            if first[i - 1] == second[j - 1]:
                dp[i][j] = dp[i - 1][j - 1] + 1
            else:
                dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])
    return dp


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


def lcs_small_space(first, second):
    # Keep the shorter string on the table's column dimension.
    if len(second) > len(first):
        first, second = second, first
    previous = [0] * (len(second) + 1)
    for character in first:
        current = [0] * (len(second) + 1)
        for j in range(1, len(second) + 1):
            if character == second[j - 1]:
                current[j] = previous[j - 1] + 1
            else:
                current[j] = max(previous[j], current[j - 1])
        previous = current
    return previous[-1]


def knapsack_small_space(weights, values, capacity):
    dp = [0] * (capacity + 1)
    for i in range(len(weights)):
        # Descending order prevents reusing the current item.
        for space in range(capacity, weights[i] - 1, -1):
            dp[space] = max(dp[space], values[i] + dp[space - weights[i]])
    return dp[capacity]


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
    result.reverse()
    return "".join(result)


def run_examples():
    assert recursive_sum([3, 1, 4]) == 8
    assert insertion_sort([4, 1, 3, 2]) == [1, 2, 3, 4]
    assert merge_sort([4, 1, 3, 2]) == [1, 2, 3, 4]
    assert binary_search([2, 4, 7, 9, 12], 9) == 3
    assert lower_bound([1, 2, 2, 5], 2) == 1
    assert sorted_pair_sum([1, 2, 4, 7, 11], 9) == (1, 3)
    values = [0, 1, 0, 3, 12]
    move_zeros(values)
    assert values == [1, 3, 12, 0, 0]
    assert max_fixed_window([2, 1, 5, 1, 3], 3) == 9
    assert min_positive_window([2, 3, 1, 2, 4, 3], 7) == 2
    assert build_prefix([3, -1, 4, 2]) == [0, 3, 2, 6, 8]
    assert count_target_subarrays([1, -1, 1], 1) == 3
    assert merge_intervals([[1, 3], [2, 6], [8, 10], [10, 12]]) == [[1, 6], [8, 12]]
    graph = [[1, 2], [0, 3], [0, 3], [1, 2], []]
    assert bfs_distances(graph, 0) == [0, 1, 1, 2, -1]
    assert dfs_order(graph, 0) == [0, 1, 3, 2]
    assert all_subsets([1, 2]) == [[], [2], [1], [1, 2]]
    assert select_meetings([(0, 6), (1, 2), (2, 4), (4, 6)]) == [(1, 2), (2, 4), (4, 6)]
    assert topological_order([[2], [2], [3], []]) == [0, 1, 2, 3]
    assert topological_order([[1], [0]]) is None
    weighted = [[(1, 4), (2, 1)], [(3, 1)], [(1, 2), (3, 5)], []]
    assert dijkstra(weighted, 0) == [0, 3, 1, 4]
    assert minimum_capacity([3, 2, 2, 4, 1, 4], 3) == 6
    assert count_set_bits(13) == 3
    assert single_unpaired([4, 1, 2, 1, 2]) == 4
    assert next_greater_values([2, 1, 2, 4, 3]) == [4, 2, 4, None, None]
    assert stairs_recursive(5) == stairs_memo(5) == stairs_table(5) == stairs_small_space(5) == 8
    assert minimum_coins([1, 3, 4], 6) == 2
    assert minimum_coins([2], 3) == -1
    assert coin_combinations([1, 2], 3) == 2
    assert grid_paths([[0, 0, 0], [0, 1, 0], [0, 0, 0]]) == 2
    assert lcs_table("abcde", "ace")[-1][-1] == 3
    assert lcs_small_space("abcde", "ace") == 3
    assert lcs_sequence("abcde", "ace") == "ace"
    assert knapsack_table([2, 3, 4], [4, 5, 7], 5) == 9
    assert knapsack_small_space([2, 3, 4], [4, 5, 7], 5) == 9
    assert lis_length([3, 1, 2, 5, 4]) == 3
    print("All Part 5 example checks passed.")


if __name__ == "__main__":
    run_examples()
