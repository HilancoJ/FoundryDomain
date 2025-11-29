def solution(n):

    # Ensure total number of bricks are valid.
    if (n < 3 or n > 200):
        return "Please enter valid number of bricks"

    # Initialise counter.
    i = 0

    # Loop through all generators.
    for staircase in find_all_stairways_to_heaven(total_bricks=n):
        i += 1
        print sum(staircase), '\t\t', staircase

    return n, i



def find_all_stairways_to_heaven(total_bricks, step_max_height=None, extend_staircase=[]):

    # If no maximum step height has been supplied, use the total number of bricks.
    if (step_max_height == None):
        
        # Build a staircase.
        staircase = build_staircase_brick_by_brick(total_bricks=total_bricks, step_max_height=total_bricks-1)

    # Use the maximum step height if it has been supplied.
    else:

        # Build a staircase.
        staircase = build_staircase_brick_by_brick(total_bricks=total_bricks, step_max_height=step_max_height)


    # If the total number of supplied bricks is equal to the total bricks in the current staircase.
    if (total_bricks == sum(staircase)):

        # If the current staircase is a main staircase.
        if (extend_staircase == []):

            # Yield the main staircase.
            yield staircase

        # If the current staircase is a sub-staircase.
        else:

            # Extend the main staircase with the sub-staircase.
            extend_staircase.extend(staircase)

            # Yield the main staircase.
            yield extend_staircase

        # Determine the maximum number bricks a specific height could fill. Tn = 0.5(n^2 - n)
        bricks_max = int((0.5)*(staircase[0]*staircase[0] - staircase[0]))

        # Can the current staircase configuration create more staircases.
        if (bricks_max > sum(staircase[1:])):

            # Determine all sub-staircases.
            sub_staircases = determine_sub_staircases(staircase=staircase)

            # Loop through all sub-staircases.
            for s in sub_staircases:

                # If the current sub-staircase has more than three bricks.
                if (sum(s) >= 3):

                    # If the current sub-staircase is derived from a main staircase.
                    if (extend_staircase == []):

                        # Evaluate the current sub-staircase.
                        for i in find_all_stairways_to_heaven(total_bricks=sum(s), step_max_height=s[0]-1, extend_staircase=staircase[0:int(len(staircase)-len(s))]):            
                            yield i

                    # If the current sub-staircase is derived from a sub-staircase.
                    else:

                        # Evaluate the current sub-staircase.
                        for i in find_all_stairways_to_heaven(total_bricks=sum(s), step_max_height=s[0]-1, extend_staircase=extend_staircase[0:int(len(extend_staircase)-len(s))]):            
                            yield i


            # If the current staircase is a main staircase.
            if (extend_staircase == []):

                # Evaluate the current staircase.
                for i in find_all_stairways_to_heaven(total_bricks=sum(staircase), step_max_height=staircase[0]-1):    
                    yield i

            # If the current staircase is a sub-staircase.
            else:

                # Evaluate the current staircase.
                for i in find_all_stairways_to_heaven(total_bricks=sum(staircase), step_max_height=staircase[0]-1, extend_staircase=extend_staircase[0:int(len(extend_staircase)-len(staircase))]):    
                    yield i



# Build a staircase.
def build_staircase_brick_by_brick(total_bricks, step_max_height):

    # Initialise the list to store each step's height.
    staircase = []

    # Populate the current step's maximum height.
    staircase.append(step_max_height)

    # Determine the next step's maximum height. It is the minimum amount of bricks between the current step height (lesub_staircases one) or the remaining number of bricks.
    next_step_max_height = min((step_max_height-1), (total_bricks-step_max_height))

    if (next_step_max_height > 0):
        staircase.extend(build_staircase_brick_by_brick(total_bricks=total_bricks-step_max_height, step_max_height=next_step_max_height))

    return staircase



# Determine sub-staircases.
def determine_sub_staircases(staircase):

    # Initialise empty list of sub-staircases.
    sub_staircases = []

    # Loop through all steps in the staircase.
    for i in range(1, len(staircase)):

        # Add current sub-staircase to list of sub-staircases.
        sub_staircases.append(staircase[i:])

    return sub_staircases




print(solution(9))
# print(solution(30))