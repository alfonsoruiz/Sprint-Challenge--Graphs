from room import Room
from player import Player
from world import World

import random
from ast import literal_eval

from util import Stack


class Graph():
    def __init__(self):
        self.visited = {}
        self.rev_path = Stack()
        self.rev_directions = {
            'n': 's',
            'w': 'e',
            'e': 'w',
            's': 'n'
        }

    def not_visited_exits(self, id):
        not_visited = []
        exits = self.visited[id]

        for direction, exit in exits.items():
            if exit == '?':
                not_visited.append(direction)

        return not_visited

    def add_direction(self, id, direct, dest=None):
        if dest is None:
            dest = '?'

        self.visited[id][direct] = dest

    def add_room(self, id):
        self.visited[id] = {}

    def dft(self, direct=None, prev=None):
        if len(self.visited) == len(room_graph):
            return

        if direct is not None:
            player.travel(direct)
            traversal_path.append(direct)
            self.rev_path.push(self.rev_directions[direct])

        curr_room = player.current_room

        if curr_room.id not in self.visited:
            self.add_room(curr_room.id)
            exits = curr_room.get_exits()

            for exit in exits:
                self.add_direction(curr_room.id, exit)

        if prev is not None:
            self.add_direction(prev.id, direct, curr_room.id)
            self.add_direction(
                curr_room.id, self.rev_directions[direct], prev.id)

        non_visited_exits = self.not_visited_exits(curr_room.id)

        if len(non_visited_exits) > 0:
            for exit in non_visited_exits:
                self.dft(exit, curr_room)

        rev_step = self.rev_path.pop()
        player.travel(rev_step)
        traversal_path.append(rev_step)


# Load world
world = World()


# You may uncomment the smaller graphs for development and testing purposes.
# map_file = "maps/test_line.txt"
# map_file = "maps/test_cross.txt"
# map_file = "maps/test_loop.txt"
# map_file = "maps/test_loop_fork.txt"
map_file = "maps/main_maze.txt"

# Loads the map into a dictionary
room_graph = literal_eval(open(map_file, "r").read())
world.load_graph(room_graph)

# Print an ASCII map
world.print_rooms()

player = Player(world.starting_room)

# Fill this out with directions to walk
# traversal_path = ['n', 'n']
traversal_path = []
world_graph = Graph()
world_graph.dft()


# TRAVERSAL TEST - DO NOT MODIFY
visited_rooms = set()
player.current_room = world.starting_room
visited_rooms.add(player.current_room)

for move in traversal_path:
    player.travel(move)
    visited_rooms.add(player.current_room)

if len(visited_rooms) == len(room_graph):
    print(
        f"TESTS PASSED: {len(traversal_path)} moves, {len(visited_rooms)} rooms visited")
else:
    print("TESTS FAILED: INCOMPLETE TRAVERSAL")
    print(f"{len(room_graph) - len(visited_rooms)} unvisited rooms")


#######
# UNCOMMENT TO WALK AROUND
#######
player.current_room.print_room_description(player)
while True:
    cmds = input("-> ").lower().split(" ")
    if cmds[0] in ["n", "s", "e", "w"]:
        player.travel(cmds[0], True)
    elif cmds[0] == "q":
        break
    else:
        print("I did not understand that command.")
