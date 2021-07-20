# https://ieeexplore.ieee.org/document/5578409
# http://www.123seminarsonly.com/Seminar-Reports/038/59360985-Maze-Solving-Algorithms.pdf
# 12 partition
# backstep - check if last_node is not connected
# decrease junction by 1 if encountered again
import mouse
# part
# eg1: 175  175  187
# eg2: 48.8  84.8  54.8
# eg3: 172  180  172
# eg4: 704  390.5  342.5
# eg5: 220  585  226
# tot: 1322.8  1415.3  982.3
# 13:  283.5  311
# 50:  596  168
# 87sin:  299  205
# 87us:  157.5  169.5
# apec1998:  214.5  214.5
# gdfs
# eg4: 148
# eg2:60.8
# eg3:176 backstep, junction added


class Node():

    def __init__(self, location, parent, degree=-1):
        self.location = location           # (x,y)
        # self.orientation = orientation     # (n,s,e,w)
        self.parent = parent
        # self.action = action
        self.heuristic = mouse.mannhattan_distance(self.location)
        self.junction_deg = degree
        self.last_node = None
        self.mode = 0


class Frontier():

    def __init__(self):
        self.frontier = []
        self.first = True

    def add(self, node):
        self.frontier.append(node)

    def contains(self, location):
        return any(node.location == location for node in self.frontier)

    def is_empty(self):
        return len(self.frontier) == 0

    def get_list(self):
        return self.frontier

    def _is_connected(self, node, location, orientation):
        xo, yo = location
        loc = node.location
        if location == (0, 0):
            return True
        wall = {
            0: {
                'n': 'Front',
                'e': 'Right',
                'w': 'Left'
            },
            2: {
                's': 'Front',
                'w': 'Right',
                'e': 'Left'
            },
            1: {
                'e': 'Front',
                's': 'Right',
                'n': 'Left'
            },
            3: {
                'w': 'Front',
                'n': 'Right',
                's': 'Left'
            }
        }
        right = loc == (
            xo + 1, yo) and not mouse.sense_wall(wall[orientation]['e'])
        left = loc == (
            xo - 1, yo) and not mouse.sense_wall(wall[orientation]['w'])
        top = loc == (
            xo, yo + 1) and not mouse.sense_wall(wall[orientation]['n'])
        bottom = loc == (
            xo, yo - 1) and not mouse.sense_wall(wall[orientation]['s'])
        return top or bottom or left or right

    def _is_restricted(self, location, r_mode):
        if r_mode:
            x, y = location
            if x >= 6 and x <= 9 and y >= 6 and y <= 9:
                return False
            else:
                return True
        return False

    def __partitioned(self, location, orientation, r_mode):
        FRL = ['Front', 'Right', 'Left']
        FLR = ['Front', 'Left', 'Right']
        LFR = ['Left', 'Front', 'Right']
        RFL = ['Right', 'Front', 'Left']
        partition = {
            'P1': {
                0: FRL,
                1: LFR,
                2: LFR,
                3: RFL
            },
            'P2': {
                0: FLR,
                1: LFR,
                2: RFL,
                3: RFL
            },
            'P3': {
                0: LFR,
                1: RFL,
                2: FRL,
                3: LFR
            },
            'P4': {
                0: RFL,
                1: RFL,
                2: FLR,
                3: LFR
            },
            'P9': {
                0: LFR,
                1: LFR,
                2: RFL,
                3: FRL
            },
            'P10': {
                0: LFR,
                1: RFL,
                2: RFL,
                3: FLR
            },
            'P11': {
                0: RFL,
                1: FLR,
                2: LFR,
                3: RFL
            },
            'P12': {
                0: RFL,
                1: FRL,
                2: LFR,
                3: LFR
            },
        }

        x, y = location
        if x <= 6 and y <= 6:
            P = 'P1'
        elif x >= 9 and y <= 6:
            P = 'P2'
        elif x >= 9 and y >= 9:
            P = 'P3'
        elif x <= 6 and y >= 9:
            P = 'P4'
        elif y == 7:
            if x <= 6:
                P = 'P4'
            elif x >= 9:
                P = 'P3'
        elif y == 8:
            if x <= 6:
                P = 'P1'
            elif x >= 9:
                P = 'P2'
        elif x == 7:
            if y <= 6:
                P = 'P9'
            elif y >= 9:
                P = 'P10'
        elif x == 8:
            if y <= 6:
                P = 'P11'
            elif y >= 9:
                P = 'P12'

        dir = {0: (1, 0, 0, 0), 1: (0, 0, 1, 0),
               2: (0, 1, 0, 0), 3: (0, 0, 0, 1)}
        n, s, e, w = dir[orientation]
        choices = {
            'Front': (x+e-w, y+n-s),
            'Right': (x+n-s, y+w-e),
            'Left': (x+s-n, y+e-w)
        }
        for direction in partition[P][orientation]:
            for i, node in enumerate(self.frontier):
                if node.location == choices[direction] and self._is_connected(node, location, orientation) and not self._is_restricted(node.location, r_mode):
                    return i
        raise Exception("Deadend")

    def remove(self, location, orientation, r_mode):
        '''Finds and removes node with minimum heuristic to goal\n
        if connected to current location.'''
        if not self.is_empty():
            # Pick the first connected node you find as the initial guess.
            # for i, node in enumerate(self.frontier):
            #     if self._is_connected(node, location, orientation):
            #         best_choice = i
            #         break
            # # Find min
            # for i, node in enumerate(self.frontier):
            #     h_best = self.frontier[best_choice].heuristic
            #     if node.heuristic <= h_best and self._is_connected(node, location, orientation):
            #         best_choice = i

            for i, node in enumerate(self.frontier):
                mouse.log(f'\t{i}::{node.location}::{node.heuristic}')

            # Corner case of start node
            if self.first:
                self.first = False
                return self.frontier.pop()
            best_choice = self.__partitioned(location, orientation, r_mode)

            return self.frontier.pop(best_choice)
        else:
            raise Exception("Empty Frontier")


class Maze():

    def __init__(self):
        self.start_location = (0, 0)
        self.start_orientation = 0  # (1, 0, 0, 0)

    def __junction_degree(self, candidates):
        ''' Returns degree of junction, if it is a junction\n
            Any location other than the one from which
            you can move only front is a Junction.\n
            \tJunction with degree 2 or 3 is a decision point.
            \tJunction with 1 degree is a corner.
            \tJunction with 0 degree is a deadend.
            Here 'degree' is 1 less than a typical graph degree'''
        if len(candidates) == 1 and 'Front' in candidates[0]:
            if (0, 1) in candidates[0]:
                return 10   # start state unique degree
            return -1
        else:
            return len(candidates)

    def __neighbours(self, node, orientation, return_type=None):
        x, y = node.location
        dir = {0: (1, 0, 0, 0), 1: (0, 0, 1, 0),
               2: (0, 1, 0, 0), 3: (0, 0, 0, 1)}
        n, s, e, w = dir[orientation]
        choices = {
            'Front': (x+e-w, y+n-s),
            'Right': (x+n-s, y+w-e),
            'Left': (x+s-n, y+e-w)
        }

        candidates = []
        for direction in choices:
            if mouse.sense_wall(direction):
                wall = {
                    0: {
                        'Front': 'n',
                        'Right': 'e',
                        'Left': 'w'
                    },
                    2: {
                        'Front': 's',
                        'Right': 'w',
                        'Left': 'e'
                    },
                    1: {
                        'Front': 'e',
                        'Right': 's',
                        'Left': 'n'
                    },
                    3: {
                        'Front': 'w',
                        'Right': 'n',
                        'Left': 's'
                    }
                }
                _dir = wall[orientation][direction]
                mouse.log(_dir)
                mouse.setWall(x, y, _dir)
            else:
                candidates.append((direction, choices[direction]))

        return candidates, self.__junction_degree(candidates)

    def __backtrack(self, location, orientation, node):
        current_location = location
        current_orientation = orientation
        mouse.log(f'Backtracking...')
        if node.mode == 1:
            node.junction_deg = 0
            return node, current_location, current_orientation
        # Move to the previous decision point.
        while node.junction_deg < 2 and not node.mode == 1:
            node = node.last_node
            while node.junction_deg < 0 and not node.mode == 1:
                node = node.last_node
            current_location, current_orientation = \
                mouse.move(current_orientation,
                           current_location, node.location)
        node.junction_deg -= 1
        mouse.log(node.junction_deg)
        return node, current_location, current_orientation

    def explore(self):
        self.num_explored = 0
        self.explored = set()
        current_pos = self.start_location
        current_rot = self.start_orientation
        r_mode = False
        first = True

        frontier = Frontier()
        all_nodes = Frontier()
        start = Node(location=self.start_location, parent=None, degree=10)
        frontier.add(start)
        all_nodes.add(start)
        node = None

        while True:
            if frontier.is_empty():
                raise Exception("No Solution")

            # Remove node from frontier
            try:
                last_node = node
                node = frontier.remove(current_pos, current_rot, r_mode)
                node.last_node = last_node
                if last_node != None:
                    mouse.log(f'L:{last_node.location}')
            except:
                # Backtrack to last decision point
                decision_point, current_pos, current_rot = self.__backtrack(
                    current_pos, current_rot, node)
                node = decision_point
            current_pos, current_rot = \
                mouse.move(current_rot, current_pos, node.location)

            # Explore Node
            # Start State
            if node.junction_deg == 10:
                if first:
                    first = False
                else:
                    mouse.turn('Right')
                    mouse.turn('Right')
            # Goal Zone
            ''' switch on restricted mode
                if goal, good
                if both dead ends, backtrack, junc becomes 0
                erase everything in zone
                remove restriction '''
            x, y = node.location
            if x >= 6 and x <= 9 and y >= 6 and y <= 9 and node.location not in self.explored:
                x1, y1 = node.last_node.location
                if not (x1 >= 6 and x1 <= 9 and y1 >= 6 and y1 <= 9):
                    node.mode = 1
                    r_mode = True
                    rot = current_rot
            if node.junction_deg == 0:
                mouse.log('erase')
                node.mode = 0
                r_mode = False
                current_rot = mouse.rotate(current_rot, rot)
                # erase explored in goal zone
                for x in range(6, 10):
                    for y in range(6, 10):
                        self.explored.discard((x, y))

            if node.heuristic == 0:
                break

            # add possible nodes to frontier
            neighbours, deg = self.__neighbours(node, current_rot)
            # deadend = True
            mouse.log(neighbours)
            for action, location in neighbours:
                # decrease junc deg if encountered again but is already in explored
                # only if current location is non explored
                if not r_mode and node.location not in self.explored and location in self.explored:
                    for _node in all_nodes.get_list():
                        if _node.location == location and _node.junction_deg > 1:
                            _node.junction_deg -= 1
                if not frontier.contains(location) and location not in self.explored:
                    # FIXME
                    # o = mouse.new_orientation(action, node.orientation)
                    child = Node(location=location, parent=node)
                    frontier.add(child)
                    all_nodes.add(child)

            # Mark node as explored
            if node.location not in self.explored:
                node.junction_deg = deg
                # if node.junction_deg < 2:
                self.num_explored += 1
                self.explored.add(node.location)


m = Maze()
m.explore()
