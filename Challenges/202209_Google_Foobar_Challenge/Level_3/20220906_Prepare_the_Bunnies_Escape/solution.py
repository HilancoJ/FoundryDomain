def solution(map):

    # Ensure map height and width are within bounds.
    if (len(map) < 2 or len(map[0]) < 2 or len(map) > 20 or len(map[0]) > 20):
        return "The height and width of the map should be between 2 to 20 (inclusive)."


    # Create a class of the map. 
    class Map:
        # Contains the actual map, height, width and shortest path.
        def __init__(self, m):
            self.m = m
            self.h = len(m)-1
            self.w = len(m[0])-1
            self.p = []

    # Create a class for entities which will navigate/route through the map.
    class Entity:
        # Contains the number of valid "options/moves" and their locations (Up, Down, Left, Right).
        options = 0
        u = None
        d = None
        l = None
        r = None

        # Contains the current entity (x, y) co-ordinates and route length.
        def __init__(self, x, y, length):
            self.x = x
            self.y = y
            self.length = length


    # Create all of the potential maps.
    maps_list = create_maps(class_Map=Map, map=map, class_Bunny=Entity)

    # Determine the shortest path for each map.
    for m in maps_list:

        # Initialise the first entity (bunny) in the top left hand corner.
        bunny_list = [Entity(x=0, y=0, length=1)]

        # Create a flag to continue traversing through the map.
        searching = True

        # Initialise the while loop.
        while (searching == True):

            # Initialise empty list of new possible routes for each iteration.
            bunny_new = []

            # Evaluate each route which could be taken.
            for b in bunny_list:

                # Determine the number of valid "options/moves" and their locations (Up, Down, Left, Right).
                determine_options(map=m, entity=b)

                # Create new entities to explore multiple routes. Store them in the new empty list.
                create_bunny(class_Bunny=Entity, bunny_list=bunny_new, bunny=b)

                # Move the entity along it's current route.
                move_bunny(map=m, bunny=b)

                # If the exit node has been reached, stop traversing the map.
                if (b.x == m.w and b.y == m.h):
                    m.p.append(b.length)
                    searching = False
                    break

            # Add the new entities to the master routes list.
            bunny_list.extend(bunny_new)

            # Remove any duplicate entities.
            merge_bunny(map=m, bunny_list=bunny_list)

            # If there are no more routes to explore, stop searching.
            if (len(bunny_list) == 0):
                searching = False

    # Initialise variable to store each map's shortest path.
    paths_list = []

    # Loop through each map.
    for m in maps_list:

        # If a shortest path was found, add it to the list of paths.
        if (m.p != []):
            paths_list.append(m.p[0])

    return min(paths_list)



# Create all of the potential maps.
def create_maps(class_Map, map, class_Bunny):

    # Initialise the list of maps.
    maps_list = [map]

    # Loop through every node in the base map.
    for i in range(len(map)):
        for j in range(len(map[0])):

            # Only consider creating a new map if the current node is a wall.
            if (map[i][j] == 1):

                # Create a node for the current (x, y) co-ordinates.
                node = class_Bunny(x=j, y=i, length=0)

                # Determine the number of valid "options/moves".
                determine_options(map=class_Map(map), entity=node)

                # Only make the node passable if there is a way through (More than one way in and out).
                if (node.options > 1):

                    # Initialse an empty map.
                    new_map = []

                    # Create a copy of the base map.
                    for row in map:
                        new_map.append(row[:])

                    # Make the current wall passable.
                    new_map[i][j] = 0

                    # Add the new map to the list of maps.
                    maps_list.append(new_map)

    # Convert all current maps to the class of Maps.
    for i in range(len(maps_list)):
        maps_list[i] = class_Map(maps_list[i])

    return maps_list



# Determine the number of valid "options/moves" and their locations (Up, Down, Left, Right).
def determine_options(map, entity):

    # Clear all current values.
    entity.options = 0
    entity.u = None
    entity.d = None
    entity.l = None
    entity.r = None

    # Stop if the exit node has been reached.
    if (entity.x != map.w or entity.y != map.h):

        # Ensure it is possible to move "Up".
        if ((entity.y-1 >= 0 and map.m[entity.y-1][entity.x] == 0)):
            entity.u = entity.y-1
            entity.options += 1

        # Ensure it is possible to move "Down".
        if ((entity.y+1 <= map.h and map.m[entity.y+1][entity.x] == 0)):
            entity.d = entity.y+1
            entity.options += 1

        # Ensure it is possible to move "Left".
        if ((entity.x-1 >= 0 and map.m[entity.y][entity.x-1] == 0)):
            entity.l = entity.x-1
            entity.options += 1

        # Ensure it is possible to move "Right".
        if ((entity.x+1 <= map.w and map.m[entity.y][entity.x+1] == 0)):
            entity.r = entity.x+1
            entity.options += 1



# Create new entities to explore multiple routes.
def create_bunny(class_Bunny, bunny_list, bunny):

    # Only create new entities if there is more than one direction.
    for j in range(bunny.options-1):

        # Create a new entity "Up" and remove this direction from the current entity.
        if (bunny.u != None):
            bunny_list.append(class_Bunny(x=bunny.x, y=bunny.u, length=bunny.length+1))
            bunny.u = None
            bunny.options -= 1
            continue

        # Create a new entity "Down" and remove this direction from the current entity.
        if (bunny.d != None):
            bunny_list.append(class_Bunny(x=bunny.x, y=bunny.d, length=bunny.length+1))
            bunny.d = None
            bunny.options -= 1
            continue

        # Create a new entity "Left" and remove this direction from the current entity.
        if (bunny.l != None):
            bunny_list.append(class_Bunny(x=bunny.l, y=bunny.y, length=bunny.length+1))
            bunny.l = None
            bunny.options -= 1
            continue

        # Create a new entity "Right" and remove this direction from the current entity.
        if (bunny.r != None):
            bunny_list.append(class_Bunny(x=bunny.r, y=bunny.y, length=bunny.length+1))
            bunny.r = None
            bunny.options -= 1
            continue



# Move the entity along it's current route.
def move_bunny(map, bunny):

    # Ensure there is only one route to take. All other routes should be explored by new entites.
    if (bunny.options == 1):

        # Update the terrain as "explored" with value 2. Move the entity "Up" and increase route length. Finally, remove this direction from the current entity.
        if (bunny.u != None):
            map.m[bunny.y][bunny.x] = 2
            bunny.y = bunny.u
            bunny.length += 1
            bunny.u = None
            bunny.options -= 1

        # Update the terrain as "explored" with value 2. Move the entity "Down" and increase route length. Finally, remove this direction from the current entity.
        if (bunny.d != None):
            map.m[bunny.y][bunny.x] = 2
            bunny.y = bunny.d
            bunny.length += 1
            bunny.d = None
            bunny.options -= 1

        # Update the terrain as "explored" with value 2. Move the entity "Left" and increase route length. Finally, remove this direction from the current entity.
        if (bunny.l != None):
            map.m[bunny.y][bunny.x] = 2
            bunny.x = bunny.l
            bunny.length += 1
            bunny.l = None
            bunny.options -= 1

        # Update the terrain as "explored" with value 2. Move the entity "Right" and increase route length. Finally, remove this direction from the current entity.
        if (bunny.r != None):
            map.m[bunny.y][bunny.x] = 2
            bunny.x = bunny.r
            bunny.length += 1
            bunny.r = None
            bunny.options -= 1



# Remove any duplicate entities.
def merge_bunny(map, bunny_list):

    # Initialise empty list of entities to remove.
    rem_list = []

    # Compare each entity to the next entity in the list.
    for i in range(len(bunny_list)):
        for j in range(i+1, len(bunny_list)):

            # If the entities share the same (x, y) co-ordinates and have the same length, add them to the remove list.
            if (bunny_list[i].x == bunny_list[j].x and bunny_list[i].y == bunny_list[j].y):# and bunny_list[i].length == bunny_list[j].length):
                rem_list.append(bunny_list[i])
                break        

    # Remove all duplicate entities.
    for r in rem_list:
        bunny_list.remove(r)

    # Initialise empty list of entities to remove.
    rem_list = []

    # Find all entities which cannot move in any direction.
    for b in bunny_list:

        # Determine the number of valid "options/moves" and their locations (Up, Down, Left, Right).
        determine_options(map=map, entity=b)

        # Add them to the remove list and update the terrain as "explored" with value 2.
        if (b.options == 0 and (b.x != map.w or b.y != map.h)):
            rem_list.append(b)
            map.m[b.y][b.x] = 2

    # Remove all stuck entities.
    for r in rem_list:
        bunny_list.remove(r)




print(solution([[0, 1, 1, 0], [0, 0, 0, 1], [1, 1, 0, 0], [1, 1, 1, 0]]))
print(solution([[0, 0, 0, 0, 0, 0], [1, 1, 1, 1, 1, 0], [0, 0, 0, 0, 0, 0], [0, 1, 1, 1, 1, 1], [0, 1, 1, 1, 1, 1], [0, 0, 0, 0, 0, 0]]))