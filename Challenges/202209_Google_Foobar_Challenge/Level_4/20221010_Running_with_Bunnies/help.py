def solution(times, times_limit):

    shortest_path_graph = [[float('inf') for j in range(len(times))] for i in range(len(times))]

    for source in range(len(times)):

        shortest_path_graph[source][source] = 0

        for relax in range(len(times)):
            for i in range(len(times)):
                for j in range(len(times)):

                    if (shortest_path_graph[source][i] + times[i][j] < shortest_path_graph[source][j]):

                        if (relax == len(times) - 1):
                            return list(range(0, len(times) - 2))

                        shortest_path_graph[source][j] = shortest_path_graph[source][i] + times[i][j]
                        
    path_to_walk = [[0, times_limit, [], [0]]]

    max_bunnies = []

    while len(path_to_walk) > 0:

        current = path_to_walk.pop()
        source = current[0]
        remainingTime = current[1]
        bunnies = current[2]
        path = current[3]

        if (source > 0 and (source < len(times) - 1) and (source not in bunnies)):
            bunnies.append(source)
            bunnies.sort()

        if ((source == len(times) - 1) and (len(bunnies) > len(max_bunnies))):
            max_bunnies = bunnies

            if (len(max_bunnies) == len(times) - 2):
                return list(range(0, len(times) - 2))

        if (len(bunnies) == len(max_bunnies) and sum(bunnies) < sum(max_bunnies)):
            max_bunnies = bunnies

        for i in range(0, len(times)):

            if (i == source):
                continue

            if (remainingTime - shortest_path_graph[source][i] - shortest_path_graph[i][len(times) - 1] < 0):
                continue

            if (shortest_path_graph[i][source] + shortest_path_graph[source][i] == 0 and (i in path)):
                continue

            new_path = path[:]
            new_path.append(i)
            path_to_walk.append([i, remainingTime - shortest_path_graph[source][i], bunnies[:], new_path])

    return  [b - 1 for b in max_bunnies]




print(solution([[0, 2, 2, 2, -1], [9, 0, 2, 2, -1], [9, 3, 0, 2, -1], [9, 3, 2, 0, -1], [9, 3, 2, 2, 0]], 1)) # [1, 2]

print(solution([[0, 1, 1, 1, 1], [1, 0, 1, 1, 1], [1, 1, 0, 1, 1], [1, 1, 1, 0, 1], [1, 1, 1, 1, 0]], 3)) # [0, 1]
