import itertools

def convert_to_path(perm):
    perm = list(perm)
    perm = [0] + perm + [-1]
    path = list()
    for i in range(1, len(perm)):
        path.append((perm[i - 1], perm[i]))
    return path

def solution(times, times_limit):
    rows = len(times)
    bunnies = rows - 2

    for i in times:
        print i 
    print

    for k in range(rows):
        for i in range(rows):
            for j in range(rows):
                if times[i][j] > times[i][k] + times[k][j]:
                    times[i][j] = times[i][k] + times[k][j]

    for r in range(rows):
        if times[r][r] < 0:
            return [i for i in range(bunnies)]

    for i in reversed(range(bunnies + 1)):
        print i

        for perm in itertools.permutations(range(1, bunnies + 1), i):
            total_times = 0
            path = convert_to_path(perm)
            for start, end in path:
                total_times += times[start][end]
            if total_times <= times_limit:
                return sorted(list(i - 1 for i in perm))
    return None




print(solution([[0, 2, 2, 2, -1], [9, 0, 2, 2, -1], [9, 3, 0, 2, -1], [9, 3, 2, 0, -1], [9, 3, 2, 2, 0]], 1)) # [1, 2]

# print(solution([[0, 1, 1, 1, 1], [1, 0, 1, 1, 1], [1, 1, 0, 1, 1], [1, 1, 1, 0, 1], [1, 1, 1, 1, 0]], 3)) # [0, 1]
