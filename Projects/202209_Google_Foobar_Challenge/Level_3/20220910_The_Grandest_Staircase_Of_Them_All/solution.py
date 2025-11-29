def solution(n):

    # Ensure the total number of bricks are valid.
    if (n < 3 or n > 200):
        return "Please enter valid number of bricks"

    # Initialise the list to store the number of combinations. The rows indicate the maximum step height. The columns indicate the given number of bricks.
    staircase_combinations = []

    # Populate an empty list of staircase combinations.
    for i in range(n+1):
        temp = []
        for j in range(n+1):
            temp.append(0)

        staircase_combinations.append(temp)

    # Initialise the base case. With a maximum step height of 0 with 0 bricks, there is only 1 combination. This is an invalid configuration, but required to seed the recursion.
    staircase_combinations[0][0] = 1

    # Loop through all step heights.
    for max_step_height in range(1, n+1):

        # Loop through all bricks.
        for total_bricks in range(0, n+1):

            # As each step height increases, the number of combinations is at least the previous step height for the same number of bricks. Each step height is a superset of the previous step height.
            staircase_combinations[max_step_height][total_bricks] = staircase_combinations[max_step_height - 1][total_bricks]

            # Determine the number of remaining bricks.
            remaining_bricks = total_bricks - max_step_height

            # If the number of remaining bricks are greater than or equal to zero. 
            if (remaining_bricks >= 0):

                # Fetch the number of combinations from the previous step height for the remaining bricks and add it to the current number of combinations.
                staircase_combinations[max_step_height][total_bricks] += staircase_combinations[max_step_height - 1][remaining_bricks]
                
    # Remove one combination from the result since the base case is an invalid combination which has been transferred to all other step heights.
    return staircase_combinations[n][n]-1




print(solution(200)) # 487067745
print(solution(3)) # 1