import sys


class MouseCrashedError(Exception):
    pass


def command(args, return_type=None):
    line = " ".join([str(x) for x in args]) + "\n"
    sys.stdout.write(line)
    sys.stdout.flush()
    if return_type:
        response = sys.stdin.readline().strip()
        if return_type == bool:
            return response == "true"
        return return_type(response)


def log(string):
    sys.stderr.write("{}\n".format(string))
    sys.stderr.flush()


def sense_wall(direction):
    return command(args=[f"wall{direction}"], return_type=bool)


def move(orientation, from_loc, to_loc):
    if from_loc == to_loc:
        return to_loc, orientation

    x1, y1 = from_loc
    x2, y2 = to_loc
    if x1 == x2:
        dist = y2 - y1
        if dist > 0:
            if orientation == 1:
                turn('Left')
                orientation = 0
            else:
                while orientation != 0:
                    turn('Right')
                    orientation = (orientation + 1) % 4
        else:
            dist = -dist
            if orientation == 3:
                turn('Left')
                orientation = 2
            else:
                while orientation != 2:
                    turn('Right')
                    orientation = (orientation + 1) % 4
    elif y1 == y2:
        dist = x2 - x1
        if dist > 0:
            if orientation == 0:
                turn('Right')
                orientation = 1
            else:
                while orientation != 1:
                    turn('Left')
                    orientation = (orientation - 1) % 4
        else:
            dist = -dist
            if orientation == 0:
                turn('Left')
                orientation = 3
            else:
                while orientation != 3:
                    turn('Right')
                    orientation = (orientation + 1) % 4

    log(f'moving to...{to_loc}')
    _move_forward(dist)
    return to_loc, orientation


def rotate(current_rot, new_rot):
    new = {
        0: {
            0: False,
            1: 'R',
            2: 'T',
            3: 'L'
        },
        1: {
            0: 'L',
            1: False,
            2: 'R',
            3: 'T'
        },
        2: {
            0: 'T',
            1: 'L',
            2: False,
            3: 'R'
        },
        3: {
            0: 'R',
            1: 'T',
            2: 'L',
            3: False
        }
    }
    o = new[current_rot][new_rot]
    log(o)
    if o == 'R':
        turn('Right')
    elif o == 'L':
        turn('Left')
    elif o == 'T':
        turn('Right')
        turn('Right')
    return new_rot


def turn(direction):
    command(args=["turn"+direction], return_type=str)


def _move_forward(distance):
    args = ["moveForward"]
    if distance is not None:
        args.append(distance)
    response = command(args=args, return_type=str)
    if response == "crash":
        raise MouseCrashedError()


def setWall(x, y, direction):
    command(args=["setWall", x, y, direction])


# Not used
def clearWall(x, y, direction):
    command(args=["clearWall", x, y, direction])


def mannhattan_distance(location):
    x, y = location

    if x < 8 and y < 8:
        return 7 - x + 7 - y
    elif x < 8 and y >= 8:
        return 7 - x + y - 8
    elif x >= 8 and y < 8:
        return x - 8 + 7 - y
    elif x >= 8 and y >= 8:
        return x - 8 + y - 8


# Below not used
def setText(x, y, text):
    command(args=["setText", x, y, text])


def clearText(x, y):
    command(args=["clearText", x, y])


def clearAllText():
    command(args=["clearAllText"])


def wasReset():
    return command(args=["wasReset"], return_type=bool)


def ackReset():
    command(args=["ackReset"], return_type=str)
