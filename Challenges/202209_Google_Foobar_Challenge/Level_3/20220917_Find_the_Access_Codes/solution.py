def solution(l):

    # If list is empty return 0.
    if (len(l) == 0):
        return 0

    # Ensure list length is between specified values.
    elif (len(l) < 2 or len(l) > 2000):
        return "Please enter valid list length."

    # Ensure list integers are between specified values.
    for i in l:
        if (i < 1 or i > 999999):
            return "Please ensure list integers are between 1 and 999 999."


    # Initialise list to store the number of divisible entries for each integer/index.
    divisible_count = []

    # All indices have an initial count of 0.
    for i in range(len(l)):
        divisible_count.append(0)

    # Loop each integer through the list of remaining integers.
    for i in range(len(l)):

        # Indices need to conform to k > j > i constraint.
        for j in range(i+1, len(l)):

            # If the next index is divisible by the current index.
            if (l[i] > 0 and l[j]%l[i] == 0):

                # Increment the number of divisible integers by 1.
                divisible_count[i] += 1


    # Initialise variable to store the number of lucky triples.
    lucky_triple_count = 0

    # Loop each integer through the list of remaining integers
    for i in range(len(l)):

        # Indices need to conform to k > j > i constraint.
        for j in range(i+1, len(l)):

            # If the next index is divisible by the current index.
            if (l[i] > 0 and l[j]%l[i] == 0):

                # Increase the number of lucky triples by the number of divisible integers for index j. 
                lucky_triple_count += divisible_count[j]
    
    return lucky_triple_count




print(solution([1, 2, 3, 4, 5, 6])) # 3
print(solution([1, 1, 1])) # 1