def solution(l):

    # If the list is already sorted, it doesn't need to loop through the entire list multiple times.
    already_sorted = True

    # Initialise Bubble Sort. Loop through all array elements.
    for i in range(len(l)-1):

        # Loop the element from the current position until the end of the list.
        for j in range(0, len(l)-i-1):

            # Determine the current element's major, minor and revision version numbers.
            c = get_version(l[j])

            # Exit loop if invalid elevator version is found.
            if (c.error):
                return c.error

            # Determine the next element's major, minor and revision version numbers.
            n = get_version(l[j+1])

            # Exit loop if invalid elevator version is found.
            if (n.error):
                return n.error

            # Determine if the current element is larger than the next element.
            if ((c.major > n.major) or 
                (c.major == n.major and c.minor > n.minor) or 
                (c.major == n.major and c.minor == n.minor and c.revision > n.revision) or 
                (c.major == n.major and c.minor == n.minor and c.revision == n.revision and c.string > n.string)):

                # The list is not sorted, turn off the flag.
                already_sorted = False

                # Switch the current and next element.
                l[j], l[j+1] = l[j+1], l[j]
        
        # If no elements were swithced, exit the for loops.
        if (already_sorted):
            break

    return l



def get_version(e):

    # Create a class representing the elevator version numbers.
    class Version:
        string = e
        major = None
        minor = None
        revision = None
        error = None
    
    # Create an instance of the v.
    v = Version()        

    # Assign the major, minor and revision numbers.
    if (e.count(".") == 0 and len(e) >= 1):
        v.major = int(e)
        v.minor = 0
        v.revision = 0
    elif (e.count(".") == 1 and len(e) >= 3):
        v.major = int(e[0:e.find(".")])
        v.minor = int(e[len(str(v.major))+1:])
        v.revision = 0
    elif (e.count(".") == 2 and len(e) >= 5):
        v.major = int(e[0:e.find(".")])
        v.minor = int(e[(len(str(v.major))+1):e.find(".",len(str(v.major))+1)])
        v.revision = int(e[(len(str(v.major))+len(str(v.minor))+2):])
    else:
        v.error = "\""+v.string+"\" is not a valid elevator version."

    return v




print(solution(["1.11", "2.0.0", "1.2", "2", "0.1", "1.2.1", "1.1.1", "2.0"]))
print(solution(["1.1.2", "1.0", "1.3.3", "1.0.12", "1.0.2"]))