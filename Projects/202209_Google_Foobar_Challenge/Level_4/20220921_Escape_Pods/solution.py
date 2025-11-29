def solution(entrances, exits, path):
    
    # The path supplied is the adjacency matrix. It has to be a square matrix.
    class ResidualGraph:

        # Store the residual graph and it's length.
        def __init__(self, graph):
            self.graph = graph
            self.len = len(graph)


    # Intialise the residual graph.
    residual_graph = ResidualGraph(path)

    # The initial flow is zero.
    total_max_flow = 0

    # Loop through all entrances and exits.
    for entrance in entrances:
        for exit in exits:

            # The total maximum flow is the sum of all entrance to exit bottlenecks.
            total_max_flow += Ford_Fulkerson(residual_graph, entrance, exit)

    return total_max_flow



# The Ford Fulkerson Algorithm returns the maximum flow from the source to the sink for a given graph.
def Ford_Fulkerson(residual_graph, source, sink):

    # Intialise the array to store the paths from source to sink. Only the indices are stored. 
    parent_tracker = []

    # There is no initial path, thus all values are -1.
    for i in range(residual_graph.len):
        parent_tracker.append(-1)

    # The initial flow for the current source to sink is zero.
    max_flow = 0


    # While there is a path from source to sink, augment/increase the flow and decrease the capacity on the residual graph.
    while (Breadth_First_Search(residual_graph, source, sink, parent_tracker) == True):

        # The initial path flow is set to an infinitely large number.
        path_flow = float("Inf")


        # Begin at the sink.
        v = sink

        # While the path has not reached the source.
        while v != source:

            # Find the parent edge.
            u = parent_tracker[v]

            # Determine the minimum flow between the current edge and it's parent.
            path_flow = min(path_flow, residual_graph.graph[u][v])

            # Set the current edge to it's parent edge. (Moving up the path)
            v = parent_tracker[v]


        # Begin at the sink.
        v = sink

        # While the path has not reached the source.
        while v != source:

            # Find the parent edge.
            u = parent_tracker[v]

            # Reduce the capacity from the current edge to it's parent.
            residual_graph.graph[u][v] -= path_flow

            # Increase the capacity of the parent edge to the current edge. (Reverse edge)
            residual_graph.graph[v][u] += path_flow

            # Set the current edge to it's parent edge. (Moving up the path)
            v = parent_tracker[v]


        # The maximum flow is equal to the bottleneck values of all valid paths from the source to sink.
        max_flow += path_flow

    return max_flow



# The Breadth First Search Algorithm attempts to return a valid path from source to sink using the residual graph.
def Breadth_First_Search(residual_graph, source, sink, parent_tracker):

    # Initialise array to indicate if an edge has been visited.
    visited = []

    # Initially, no edges have been visited.
    for i in range(residual_graph.len):
        visited.append(False)

    # Initialise array to store the queue.
    queue = []

    # Begin at the source node and indicate that it has been visited.
    queue.append(source)
    visited[source] = True

    # While the queue is not empty, keep searching for the next edge.
    while queue != []:

        # Store the current edge in the variable and remove it from the queue.
        current_edge = queue.pop(0)

        # Loop through all edges.
        for i in range(residual_graph.len):

            # If the edge has not been visited and has capacity.
            if (visited[i] == False and residual_graph.graph[current_edge][i] > 0):

                # Add the edge to the queue.
                queue.append(i)

                # Indicate that this edge has been visited.
                visited[i] = True

                # Add the edge as a valid step for the potential path.
                parent_tracker[i] = current_edge

    # If the sink has been reached, return true indicating a valid path has been found and is accessible in the parent_tracker. Otherwise return false.
    if visited[sink] == True:
        return True
    else:
        return False




print(solution([0], [3], [[0, 7, 0, 0], [0, 0, 6, 0], [0, 0, 0, 8], [9, 0, 0, 0]])) # 6
print(solution([0, 1], [4, 5], [[0, 0, 4, 6, 0, 0], [0, 0, 5, 2, 0, 0], [0, 0, 0, 0, 4, 4], [0, 0, 0, 0, 6, 6], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0]])) # 16
print(solution([0, 1], [4, 5], [[0, 0, 4, 6, 0, 0], [0, 0, 5, 2, 0, 0], [0, 0, 0, 0, 4, 4], [0, 2, 0, 0, 6, 6], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0]])) # 16