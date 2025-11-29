def solution(l):

    # Initialise list to store all lucky triples.
    lucky_triples = []

    # Loop through all i, j, k list indices.
    for i in range(len(l)-2):
        for j in range(i+1, len(l)-1):
            for k in range(j+1, len(l)):

                # If z is divisible by y and y is divisible by x.
                if (l[k]%l[j] == 0 and l[j]%l[i] == 0):

                    # Add lucky triple to list of triples.
                    lucky_triples.append((l[i], l[j], l[k]))

    # Print all lucky triples.
    print '\n', l
    for i in lucky_triples:
        print i

    return len(lucky_triples)




print(solution([1, 2, 3, 4, 5, 6])) # 3
print(solution([1, 1, 1])) # 1