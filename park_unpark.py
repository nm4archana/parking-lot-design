# Lastline parking challenge. Please see task description in accompanying PDF for details.

import threading
from datetime import datetime
import math
# define the 15 minute minimum parking interval
MINIMUM_PARKING_INTERVAL_SECONDS = 15*60
# define the minimum number of spaces for each row
MAXIMUM_NO_OF_SPACES_PER_ROW = 10

GOT_SPACE   = True
LOST_SPACE  = False
NO_SPACE    = None

CHARGE_HANDICAPPED = 5
CHARGE_COMPACT     = 5
CHARGE_LARGE       = 7.50


class InvalidInputError(Exception):
    """
    Raised if the provided API input is invalid.
    """


def park(size, has_handicapped_placard):
    """
    Return the most appropriate available parking space for this vehicle. Refer to
    challenge description for explanation of how to determine the most appropriate space

    :param size: vehicle size. For now this is 'compact_car' or 'large_car'
    :type size: `str`
    :param has_handicapped_placard: if True, provide handicapped space (if available)
    :type has_handicapped_placard: `bool`
    :returns: parking location. tuple of (level, row, space), or None if no spaces available.
       Level, row and space numbers start at 1.
    :rtype: tuple(`int`,`int`,`int`)
    :raises InvalidInputError: if size invalid
    """
    if size not in ['compact_car','large_car']:
        raise InvalidInputError('Wrong input!!')

    # Flag set to True if allocated a space in row corresponding to 'large_car'
    charge_high = False

    if has_handicapped_placard is True:
        # t_space is a tuple - (space,boolean) returned from findspace method
        t_space = findspace(code['handicapped'])

        # Restart search if space lost to different thread
        space = t_space[0] if t_space[1] is GOT_SPACE else park(size, has_handicapped_placard)

        # If no 'handicapped' space available, continue search in 'compact_car' & 'large_car'
        if space is NO_SPACE:
            if size is 'compact_car':
                t_space = findspace(code['compact_car'])
                space = t_space[0] if t_space[1] is GOT_SPACE else park(size, has_handicapped_placard)
            if space is NO_SPACE or size in 'large_car':
                t_space = findspace(code['large_car'])
                space = t_space[0] if t_space[1] is GOT_SPACE else park(size, has_handicapped_placard)
    else:
        if size is "compact_car":
            t_space = findspace(code['compact_car'])

            space = t_space[0] if t_space[1] is GOT_SPACE else park(size, has_handicapped_placard)

            if space is NO_SPACE:
                charge_high = True
                t_space = findspace(code['large_car'])
                space = t_space[0] if t_space[1] is GOT_SPACE else park(size, has_handicapped_placard)
        else: # size is "large_car"
            t_space = findspace(code['large_car'])
            space = t_space[0] if t_space[1] is GOT_SPACE else park(size, has_handicapped_placard)

    if space is NO_SPACE:
        print "The parking is full!!"
        return -1, -1, -1

    # update the park_details dictionary which is used for calculating the time and cost
    if has_handicapped_placard is True:
        park_details[space] = (CHARGE_HANDICAPPED, datetime.now())
    elif size is "compact_car" and charge_high is False:
        park_details[space] = (CHARGE_COMPACT, datetime.now())
    else:
        park_details[space] = (CHARGE_LARGE, datetime.now())

    return space


def findspace(code_v):

    """
    Return the space (if available) for parking
    :param code_v: code for 'compact_car' or 'large_car' or 'handicapped'
    :type code_v: int
    :returns: Space allocated
    :rtype: tuple
    """
    # Iterate through every level
    for i in range(len(parking_structure)):
        size_space_tuples = parking_structure[i]

        # Iterate through every row
        for j in range(len(size_space_tuples)):
            # Check if the row belongs to the code (compact_car or large_car or hadicapped) and if space is available
            if parking_structure[i][j][0] is code_v and parking_structure[i][j][1] < MAXIMUM_NO_OF_SPACES_PER_ROW:
                spot = getspot(i, j, parking_structure[i][j][1])
                space = ()

                # If the thread gets the space , then space is allocated and returned
                if spot[0] is GOT_SPACE:
                    space = (i + 1, j + 1, spot[1])
                    return space, GOT_SPACE
                else:
                    # Returned if the thread dis not acquire the lock i.e No space is allocated yet
                    return space, LOST_SPACE

    # Returned if parking is full
    return NO_SPACE, True


def unpark(location):

    """
    Return the charge for parking at this location based on location type and time spent.
    Refer to challenge description for details on how to calculate parking rates.

    :param location: parking space the vecicle was parked at as tuple (level, row, space)
    :type location: tuple(`int`,`int`,`int`)
    :returns: The total amount that the parker should be charged (eg: 7.5)
    :rtype: float
    :raises InvalidInputError: if location invalid or empty
    """
    if location not in park_details:
        raise InvalidInputError('Wrong input!!')

    # Calculate the time difference in seconds
    time_diff = (datetime.now() - park_details[location][1]).total_seconds()

    # Calculate the total amount
    if time_diff <= MINIMUM_PARKING_INTERVAL_SECONDS:
        total_amount = park_details[location][0]
    else:
        total_amount = park_details[location][0] * math.ceil(time_diff/MINIMUM_PARKING_INTERVAL_SECONDS)

    i = location[0]-1
    j = location[1]-1

    #Call function to release spot after unpark
    releasespot(i, j, location[2]-1)

    park_details.pop(location, None)

    # Return the total amount
    return total_amount


def getspot(level, row, space_count):
    """
    Allocates a space for parking
    :param level: Level in which the space has to be allocated
    :param row: Row in which the space has to be allocated
    :param space_count: Space allocated
    :return: Returns tuple of flag(space allocated or not allocated) and the space
    """
    # Acquire the lock before making changes to level
    lock.acquire()

    set_flag = False
    k = -1
    if space_count is parking_structure[level][row][1]:
        spot = parking_structure[level][row][2]
        for k in range(len(spot)):
            if spot[k] is 0:
                # Allocating a space
                spot[k] = spot[k] + 1
                break
        parking_structure[level][row][2] = spot
        # Incrementing the count in the level
        parking_structure[level][row][1] = parking_structure[level][row][1] + 1
        set_flag = True

    # Release the lock
    lock.release()

    return set_flag, k+1


def releasespot(level,row,s):
    """
     Releases the spot allocated.
    :param level:  Level in which the space is allocated
    :param row:  Row in which the space is allocated
    :param s:  Space allocated
    """
    # Acquire the lock before making changes to level
    lock.acquire()

    # Decrementing the count in the level
    parking_structure[level][row][1] = parking_structure[level][row][1] - 1
    spot = parking_structure[level][row][2]
    for k in range(len(spot)):
        if k is s:
            # De-allocating a space
            spot[k] = spot[k]-1
            parking_structure[level][row][2] = spot
            break

    # Release the lock
    lock.release()

def printlevel():
    """
    Prints the parking levels
    """
    print "\n************PARKING STRUCTURE********************"
    for i in range(len(parking_structure)):
        list_a = []
        for j in range(len(parking_structure[i])):
            list_a.append(parking_structure[i][j][1])
        print "Level:",i+1,list_a
    print "**************************************************\n"


def init():
    """
    Called on system initialization before any park/unpark function is called.
    """
    global code, parking_structure, lock, park_details
    # Dictionary to store the codes for type of car and 'handicapped'
    code = {'compact_car': 1, 'large_car': 2, 'handicapped': 3}

    """
    List to store the rows in each level, type of row(compact_car or handicapped or large_car),space count & spaces.
    parking_structure[l][r] = {[type-code, count, space]..}, where space = [0]*10
    """
    parking_structure = [[[3, 0, [0] * 10], [3, 0, [0] * 10], [1, 0, [0] * 10], [1, 0, [0] * 10], [1, 0, [0] * 10], [1, 0, [0] * 10]],
             [[1, 0, [0] * 10], [1, 0, [0] * 10], [1, 0, [0] * 10], [1, 0, [0] * 10], [2, 0, [0] * 10], [2, 0, [0] * 10], [2, 0, [0] * 10], [2, 0, [0] * 10]],
             [[1, 0, [0] * 10], [1, 0, [0] * 10], [1, 0, [0] * 10], [1, 0,[0] * 10], [2, 0, [0] * 10], [2, 0, [0] * 10], [2, 0, [0] * 10], [2, 0, [0] * 10]]]

    # Dictionary to store the allocated space , time and cost
    park_details = dict()
    # Thread object
    lock = threading.Lock()
