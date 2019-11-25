import json
import random
import requests
import time

class Queue():
    def __init__(self):
        self.queue = []

    def enqueue(self, value):
        self.queue.append(value)

    def dequeue(self):
        if self.size() > 0:
            return self.queue.pop(0)
        else:
            return None

    def size(self):
        return len(self.queue)


class Stack():
    def __init__(self):
        self.stack = []

    def push(self, value):
        self.stack.append(value)

    def pop(self):
        if self.size() > 0:
            return self.stack.pop()
        else:
            return None

    def size(self):
        return len(self.stack)

# grid_with_all_info = {}

# direction_reversed = {'n': 's', 's': 'n', 'e': 'w', 'w': 'e'}

# class Graph:

#     def __init__(self):
#         self.vertices = {}
#         self.current_room_id = None
#         self.current_room = None
#         self.last_room = None

#     def dft(self):
#         s = Stack()
#         s.push(self.current_room["room_id"])
#         visited = set()

#         last_direction = None

#         while s.size() > 0:
#             if self.current_room["room_id"] not in self.vertices:
#                 self.vertices[self.current_room["room_id"]] = {}
#                 for direction in self.current_room["exits"]:
#                     self.vertices[self.current_room["room_id"]
#                                   ][direction] = "?"
#             if last_direction:
#                 self.vertices[self.current_room["room_id"]
#                               ][direction_reversed[last_direction]] = self.last_room

#             self.last_room = self.current_room["room_id"]
#             v = s.pop()
#             if v not in visited:
#                 visited.add(v)
#                 exits = self.current_room["exits"]

#                 while True:
#                     direction = exits[random.randint(0, len(exits) - 1)]
#                     if self.vertices[self.current_room["room_id"]][direction] == "?":
#                         time.sleep(self.current_room["cooldown"])
#                         the_new_room = requests.post('https://lambda-treasure-hunt.herokuapp.com/api/adv/move/', json={
#                         'direction': f'{direction}'}, headers={'Authorization': 'Token b998850f7eea4d86b11aa5894d59ecc8cafa888c'})
#                         new_room = the_new_room.json()
#                         self.vertices[self.last_room][direction] = new_room["room_id"]
#                         last_direction = direction
#                         s.push(new_room["room_id"])
#                         self.current_room = new_room
#                         grid_with_all_info[new_room["room_id"]] = new_room
#                         break
#                     break
#         self.current_room_id = self.current_room["room_id"]

#     def bfs(self):
#         q = Queue()
#         q.enqueue([self.current_room_id])
#         visited = set()
#         while q.size() > 0:
#             path = q.dequeue()
#             v = path[-1]
#             if v not in visited:
#                 for direction in grid_with_all_info[v]["exits"]:
#                     if self.vertices[v][direction] == "?":
#                         return path

#                 visited.add(v)
#                 for key, value in self.vertices[v].items():
#                     new_path = list(path)
#                     new_path.append(value)
#                     q.enqueue(new_path)

#     def traverse(self):
#         response = requests.get(
#             ' https://lambda-treasure-hunt.herokuapp.com/api/adv/init/',
#             headers={
#                 'Authorization': 'Token b998850f7eea4d86b11aa5894d59ecc8cafa888c'},
#         )

#         json_response = response.json()

#         grid_with_all_info[json_response["room_id"]] = json_response

#         self.current_room = json_response

#         while len(self.vertices) < 499:
#             self.dft()
#             shortest_path_bfs = self.bfs()

#             for room in shortest_path_bfs[1:]:
#                 for direction in grid_with_all_info[self.current_room["room_id"]]["exits"]:
#                     if self.vertices[self.current_room["room_id"]][direction] == room:
#                         time.sleep(self.current_room["cooldown"])
#                         the_new_room = requests.post('https://lambda-treasure-hunt.herokuapp.com/api/adv/move/', json={'direction': f'{direction}',
#                         "next_room_id": f'{room}'}, headers={'Authorization': 'Token b998850f7eea4d86b11aa5894d59ecc8cafa888c'})
#                         new_room = the_new_room.json()
#                         self.current_room = new_room
#                         self.current_room_id = new_room["room_id"]
#                         break

# graph = Graph()
# graph.traverse()

# with open('grid_with_all_infos.txt', 'w') as outfile:
#     json.dump(grid_with_all_info, outfile)

# with open('grid_with_all_directionss.txt', 'w') as outfile:
#     json.dump(graph.vertices, outfile)





#     # if "small treasure" in self.current_room["items"] or :
#     # updated_room = requests.post('https://lambda-treasure-hunt.herokuapp.com/api/adv/take/', json={"name":"treasure"}, headers={'Authorization': 'Token b998850f7eea4d86b11aa5894d59ecc8cafa888c'})
#     # time.sleep(20)
