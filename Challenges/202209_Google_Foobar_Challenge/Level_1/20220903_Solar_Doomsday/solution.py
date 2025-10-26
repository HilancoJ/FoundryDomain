import math

def solution(area):
    
    # Restrict the scope of the total solar panel area.
    if (area != 0 and (area < 1 or area > 1000000)):
        return "The total area of solar panels must be between 1 and 1000000 (inclusive)."

    # Create an empty list of sqaure solar panels.
    solar_panels = []

    # Return the list of square solar panels when there are no more solar panels to allocate.
    if (area == 0):
        return solar_panels

    # Assign square solare panels to the given area.
    else:
        # Determine the largest square solar panel to allocate to the given area.
        square = int(math.pow(math.floor(math.sqrt(area)),2))

        # Add the current square solar panel to the list of square solar panels.
        solar_panels.append(square)

        # Recursively identify the remaining sqaure solar panels and extend/add them to the list of square solar panels.
        solar_panels.extend(solution(area-square))

    # Return the list of square solar panels once the square size has been determined.
    return solar_panels




print(solution(15324))
print(solution(12))