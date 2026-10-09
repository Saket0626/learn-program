"""From Zero to LeetCode Hard, Part 7.

Each named class corresponds to one LeetCode problem. Rename that class to
Solution when submitting its method. LeetCode supplies ListNode for linked
list problems. Run this file to execute example and differential checks.
"""

from collections import deque
import heapq
from itertools import count, product
from string import ascii_lowercase


class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next


class TwoSum:
    def twoSum(self, nums, target):
        seen = {}  # Earlier value -> its index.
        for index, value in enumerate(nums):
            needed = target - value  # Solve value + needed = target.
            if needed in seen:  # Check before insertion to avoid self-use.
                return [seen[needed], index]
            seen[value] = index
        return []  # Outside the official guarantee of one solution.


class ValidParentheses:
    def isValid(self, s):
        opening_for = {')': '(', ']': '[', '}': '{'}
        stack = []  # Openers still waiting to be closed.
        for char in s:
            if char in opening_for:  # This is a closing bracket.
                if not stack or stack[-1] != opening_for[char]:
                    return False
                stack.pop()  # Resolve the most recent opener.
            else:
                stack.append(char)
        return not stack  # Every opener must have been resolved.


class Stock:
    def maxProfit(self, prices):
        cheapest = prices[0]  # Cheapest price on an earlier day.
        best = 0
        for day in range(1, len(prices)):
            price = prices[day]
            best = max(best, price - cheapest)  # Sell today.
            cheapest = min(cheapest, price)  # Candidate for future days.
        return best


class MergeTwo:
    def mergeTwoLists(self, list1, list2):
        dummy = ListNode()  # Temporary anchor, not part of the answer.
        tail = dummy
        while list1 is not None and list2 is not None:
            if list1.val <= list2.val:
                tail.next = list1
                list1 = list1.next
            else:
                tail.next = list2
                list2 = list2.next
            tail = tail.next
        tail.next = list1 if list1 is not None else list2
        return dummy.next


class LongestSubstring:
    def lengthOfLongestSubstring(self, s):
        last_seen = {}  # Character -> latest processed index.
        left = 0
        best = 0
        for right, char in enumerate(s):
            if char in last_seen:
                left = max(left, last_seen[char] + 1)  # Never move backward.
            last_seen[char] = right
            best = max(best, right - left + 1)
        return best


class Islands:
    def numIslands(self, grid):
        rows, cols = len(grid), len(grid[0])
        seen = set()  # Preserves the caller's grid.
        islands = 0
        directions = ((1, 0), (-1, 0), (0, 1), (0, -1))
        for row in range(rows):
            for col in range(cols):
                if grid[row][col] != '1' or (row, col) in seen:
                    continue
                islands += 1  # A previously unvisited component.
                stack = [(row, col)]
                seen.add((row, col))  # Mark when scheduled.
                while stack:
                    current_row, current_col = stack.pop()
                    for dr, dc in directions:
                        nr, nc = current_row + dr, current_col + dc
                        if (0 <= nr < rows and 0 <= nc < cols
                                and grid[nr][nc] == '1'
                                and (nr, nc) not in seen):
                            seen.add((nr, nc))
                            stack.append((nr, nc))
        return islands


class CoinChange:
    def coinChange(self, coins, amount):
        impossible = amount + 1  # More coins than any valid answer needs.
        dp = [impossible] * (amount + 1)
        dp[0] = 0
        for total in range(1, amount + 1):
            for coin in coins:
                if coin <= total:
                    dp[total] = min(dp[total], dp[total - coin] + 1)
        return -1 if dp[amount] == impossible else dp[amount]


class CourseSchedule:
    def canFinish(self, numCourses, prerequisites):
        following = [[] for _ in range(numCourses)]
        indegree = [0] * numCourses
        for course, prerequisite in prerequisites:
            following[prerequisite].append(course)
            indegree[course] += 1
        ready = deque(i for i in range(numCourses) if indegree[i] == 0)
        completed = 0
        while ready:
            course = ready.popleft()
            completed += 1
            for next_course in following[course]:
                indegree[next_course] -= 1
                if indegree[next_course] == 0:
                    ready.append(next_course)
        return completed == numCourses


class TopK:
    def topKFrequent(self, nums, k):
        frequency = {}
        for value in nums:
            frequency[value] = frequency.get(value, 0) + 1
        buckets = [[] for _ in range(len(nums) + 1)]
        for value, occurrences in frequency.items():
            buckets[occurrences].append(value)
        answer = []
        for occurrences in range(len(nums), 0, -1):
            for value in buckets[occurrences]:
                answer.append(value)
                if len(answer) == k:
                    return answer
        return answer


class WordSearch:
    def exist(self, board, word):
        rows, cols = len(board), len(board[0])
        if len(word) > rows * cols:
            return False
        path = set()  # Cells in this candidate path, not global visitation.

        def search(row, col, index):
            if not (0 <= row < rows and 0 <= col < cols):
                return False
            if (row, col) in path or board[row][col] != word[index]:
                return False
            if index == len(word) - 1:
                return True
            path.add((row, col))
            found = (search(row, col + 1, index + 1)
                     or search(row + 1, col, index + 1)
                     or search(row, col - 1, index + 1)
                     or search(row - 1, col, index + 1))
            path.remove((row, col))  # Undo even when a child succeeds.
            return found

        for row in range(rows):
            for col in range(cols):
                if search(row, col, 0):
                    return True
        return False


def trap_brute(height):
    water = 0
    for i in range(len(height)):
        left_max = max(height[:i + 1])
        right_max = max(height[i:])
        water += min(left_max, right_max) - height[i]
    return water


def trap_arrays(height):
    if not height:
        return 0
    n = len(height)
    left_max = [0] * n
    right_max = [0] * n
    left_max[0], right_max[-1] = height[0], height[-1]
    for i in range(1, n):
        left_max[i] = max(left_max[i - 1], height[i])
    for i in range(n - 2, -1, -1):
        right_max[i] = max(right_max[i + 1], height[i])
    return sum(min(left_max[i], right_max[i]) - height[i]
               for i in range(n))


class RainWater:
    def trap(self, height):
        left, right = 0, len(height) - 1
        left_max = right_max = water = 0
        while left <= right:
            left_max = max(left_max, height[left])
            right_max = max(right_max, height[right])
            if left_max <= right_max:
                water += left_max - height[left]
                left += 1
            else:
                water += right_max - height[right]
                right -= 1
        return water


def merge_k_scan(lists):
    heads = list(lists)  # Copies references, not linked nodes.
    dummy = ListNode()
    tail = dummy
    while True:
        chosen = -1
        for i, node in enumerate(heads):
            if node is not None and (chosen == -1 or node.val < heads[chosen].val):
                chosen = i
        if chosen == -1:
            break
        node = heads[chosen]
        heads[chosen] = node.next
        tail.next = node
        tail = node
    tail.next = None
    return dummy.next


def merge_k_sort(lists):
    nodes = []
    for head in lists:
        while head is not None:
            nodes.append(head)
            head = head.next
    nodes.sort(key=lambda node: node.val)
    dummy = ListNode()
    tail = dummy
    for node in nodes:
        tail.next = node
        tail = node
    tail.next = None
    return dummy.next


class MergeK:
    def mergeKLists(self, lists):
        heap = []
        serial = count()  # Unique integer to break equal-value ties.
        for node in lists:
            if node is not None:
                heap.append((node.val, next(serial), node))
        heapq.heapify(heap)
        dummy = ListNode()
        tail = dummy
        while heap:
            _, _, node = heapq.heappop(heap)
            following = node.next  # Save successor before changing links.
            tail.next = node
            tail = node
            if following is not None:
                heapq.heappush(heap, (following.val, next(serial), following))
        tail.next = None
        return dummy.next


def ladder_scan(begin, end, words):
    remaining = set(words)
    if end not in remaining:
        return 0
    remaining.discard(begin)
    queue = deque([(begin, 1)])
    while queue:
        word, length = queue.popleft()
        if word == end:
            return length
        for candidate in list(remaining):
            if sum(a != b for a, b in zip(word, candidate)) == 1:
                remaining.remove(candidate)
                queue.append((candidate, length + 1))
    return 0


def ladder_bfs(begin, end, words):
    remaining = set(words)
    if end not in remaining:
        return 0
    remaining.discard(begin)
    queue = deque([(begin, 1)])
    while queue:
        word, length = queue.popleft()
        if word == end:
            return length
        for i in range(len(word)):
            for letter in ascii_lowercase:
                if letter == word[i]:
                    continue
                candidate = word[:i] + letter + word[i + 1:]
                if candidate in remaining:
                    remaining.remove(candidate)
                    queue.append((candidate, length + 1))
    return 0


class WordLadder:
    def ladderLength(self, beginWord, endWord, wordList):
        remaining = set(wordList)
        if endWord not in remaining:
            return 0
        front, back = {beginWord}, {endWord}
        remaining.discard(beginWord)
        remaining.discard(endWord)
        length = 1
        while front and back:
            if len(front) > len(back):
                front, back = back, front
            next_front = set()
            for word in front:
                for i in range(len(word)):
                    for letter in ascii_lowercase:
                        if letter == word[i]:
                            continue
                        candidate = word[:i] + letter + word[i + 1:]
                        if candidate in back:
                            return length + 1
                        if candidate in remaining:
                            remaining.remove(candidate)
                            next_front.add(candidate)
            front = next_front
            length += 1
        return 0


def median_sort(a, b):
    values = sorted(a + b)
    middle = len(values) // 2
    if len(values) % 2:
        return float(values[middle])
    return (values[middle - 1] + values[middle]) / 2


def median_walk(a, b):
    i = j = 0
    previous = current = 0
    total = len(a) + len(b)
    for _ in range(total // 2 + 1):
        previous = current
        if i < len(a) and (j == len(b) or a[i] <= b[j]):
            current = a[i]
            i += 1
        else:
            current = b[j]
            j += 1
    return float(current) if total % 2 else (previous + current) / 2


class Median:
    def findMedianSortedArrays(self, nums1, nums2):
        a, b = nums1, nums2
        if len(a) > len(b):
            a, b = b, a  # Search the shorter array.
        m, n = len(a), len(b)
        half = (m + n + 1) // 2
        low, high = 0, m
        while low <= high:
            i = (low + high) // 2
            j = half - i
            a_left = a[i - 1] if i > 0 else float('-inf')
            a_right = a[i] if i < m else float('inf')
            b_left = b[j - 1] if j > 0 else float('-inf')
            b_right = b[j] if j < n else float('inf')
            if a_left <= b_right and b_left <= a_right:
                if (m + n) % 2:
                    return float(max(a_left, b_left))
                return (max(a_left, b_left) + min(a_right, b_right)) / 2
            if a_left > b_right:
                high = i - 1
            else:
                low = i + 1
        raise ValueError('Inputs must be sorted and not both empty.')


def make_list(values):
    head = None
    for value in reversed(values):
        head = ListNode(value, head)
    return head


def read_list(head):
    values, identities = [], set()
    while head is not None:
        assert id(head) not in identities, 'Linked-list cycle detected'
        identities.add(id(head))
        values.append(head.val)
        head = head.next
    return values


def run_checks():
    """Independent small-input oracles and important edge examples."""
    import random
    rng = random.Random(7)
    checks = 0
    assert TwoSum().twoSum([4, 1, 6, 9], 7) == [1, 2]
    assert TwoSum().twoSum([3, 3], 6) == [0, 1]
    for length in range(7):
        for chars in product('()[]', repeat=length):
            s = ''.join(chars)
            reduced = s
            while '()' in reduced or '[]' in reduced:
                reduced = reduced.replace('()', '').replace('[]', '')
            assert ValidParentheses().isValid(s) == (reduced == '')
            checks += 1
        for chars in product('abc', repeat=length):
            s = ''.join(chars)
            expected = max((j-i for i in range(length+1)
                            for j in range(i, length+1)
                            if len(set(s[i:j])) == j-i), default=0)
            assert LongestSubstring().lengthOfLongestSubstring(s) == expected
            checks += 1
        for heights in product(range(3), repeat=length):
            values = list(heights)
            expected = trap_brute(values)
            assert trap_arrays(values) == expected
            assert RainWater().trap(values) == expected
            checks += 2
    for _ in range(300):
        prices = [rng.randrange(10) for _ in range(rng.randrange(1, 9))]
        expected = max([0] + [prices[j]-prices[i] for i in range(len(prices))
                            for j in range(i+1, len(prices))])
        assert Stock().maxProfit(prices) == expected
        arrays = [sorted(rng.randrange(-4, 5) for _ in range(rng.randrange(6)))
                  for _ in range(rng.randrange(6))]
        expected = sorted(x for array in arrays for x in array)
        for merger in (merge_k_scan, merge_k_sort, MergeK().mergeKLists):
            assert read_list(merger([make_list(a) for a in arrays])) == expected
            checks += 1
        a, b = sorted(prices[:len(prices)//2]), sorted(prices[len(prices)//2:])
        assert read_list(MergeTwo().mergeTwoLists(make_list(a), make_list(b))) == sorted(prices)
        assert median_walk(a, b) == median_sort(a, b)
        assert Median().findMedianSortedArrays(a, b) == median_sort(a, b)
        nums = [rng.randrange(6) for _ in range(rng.randrange(1, 15))]
        k = rng.randrange(1, len(set(nums))+1)
        answer = TopK().topKFrequent(nums, k)
        assert len(answer) == k and len(set(answer)) == k
        assert min(nums.count(x) for x in answer) >= max(
            (nums.count(x) for x in set(nums)-set(answer)), default=0)
        checks += 5
    for coins_tuple in product(range(1, 5), repeat=3):
        coins = list(coins_tuple)
        for amount in range(15):
            queue = deque([(0, 0)])
            seen = {0}
            expected = -1
            while queue:
                total, steps = queue.popleft()
                if total == amount:
                    expected = steps
                    break
                for coin in coins:
                    if total + coin <= amount and total + coin not in seen:
                        seen.add(total + coin)
                        queue.append((total + coin, steps + 1))
            assert CoinChange().coinChange(coins, amount) == expected
            checks += 1
    for cells in product('01', repeat=6):
        grid = [list(cells[:3]), list(cells[3:])]
        unvisited = {(r, c) for r in range(2) for c in range(3) if grid[r][c] == '1'}
        expected = 0
        while unvisited:
            component = {unvisited.pop()}
            expected += 1
            while True:
                additions = {p for p in unvisited if any(
                    abs(p[0]-q[0])+abs(p[1]-q[1]) == 1 for q in component)}
                if not additions:
                    break
                unvisited -= additions
                component |= additions
        snapshot = [row[:] for row in grid]
        assert Islands().numIslands(grid) == expected
        assert grid == snapshot
        checks += 1
    from itertools import permutations
    for mask in range(1 << 9):
        edges = [(i, j) for i in range(3) for j in range(3) if mask & (1 << (3*i+j))]
        expected = any(all(order.index(b) < order.index(a) for a, b in edges)
                       for order in permutations(range(3)))
        assert CourseSchedule().canFinish(3, edges) == expected
        checks += 1
    board = [list('ABCE'), list('SFCS'), list('ADEE')]
    for word, expected in [('ABCCED', True), ('SEE', True), ('ABCB', False)]:
        assert WordSearch().exist(board, word) == expected
        assert board == [list('ABCE'), list('SFCS'), list('ADEE')]
        checks += 1
    assert not WordSearch().exist([list('AB')], 'ABA')
    assert WordSearch().exist([list('A')], 'A')
    universe = [''.join(x) for x in product('ab', repeat=3)]
    for mask in range(1 << len(universe)):
        words = [word for i, word in enumerate(universe) if mask & (1 << i)]
        for begin, end in [('aaa', 'bbb'), ('aab', 'aba')]:
            expected = ladder_scan(begin, end, words)
            assert ladder_bfs(begin, end, words) == expected
            assert WordLadder().ladderLength(begin, end, words) == expected
            checks += 2
    # Exhaustive sorted-array median checks, including an empty input array.
    from itertools import combinations_with_replacement
    arrays = [list(x) for n in range(5) for x in combinations_with_replacement(range(-2, 3), n)]
    for a in arrays:
        for b in arrays:
            if not a and not b:
                continue
            expected = median_sort(a, b)
            assert median_walk(a, b) == expected
            assert Median().findMedianSortedArrays(a, b) == expected
            checks += 2
    print(f'Passed {checks:,} differential and property checks, plus edge examples.')


if __name__ == '__main__':
    run_checks()
