from util import Stack, Queue
import random
import requests
import time

#Content-Type application/json

# init => GET https://lambda-treasure-hunt.herokuapp.com/api/adv/init/

# movement => POST '{"direction":"n"}' https://lambda-treasure-hunt.herokuapp.com/api/adv/move/

# header Authorization Token 511b799007ac9e828b320eaf2c3d6525557e9502 

# example data {
#     "room_id": 329,
#     "title": "A misty room",
#     "description": "You are standing on grass and surrounded by a dense mist. You can barely make out the exits in any direction.",
#     "coordinates": "(65,69)",
#     "elevation": 0,
#     "terrain": "NORMAL",
#     "players": [],
#     "items": [],
#     "exits": [
#         "w"
#     ],
#     "cooldown": 1.0,
#     "errors": [],
#     "messages": []
# }

# requests.post('https://httpbin.org/post', data={'key':'value'}, headers={'Authorization': 'Token 511b799007ac9e828b320eaf2c3d6525557e9502'}) 

# response = requests.get(
#     ' https://lambda-treasure-hunt.herokuapp.com/api/adv/init/',
#     headers={'Authorization': 'Token 511b799007ac9e828b320eaf2c3d6525557e9502'},
# )
# json_response = response.json()

grid_with_all_info = {}

# grid_with_all_info[json_response["room_id"]] = json_response

# current_room = json_response

# print(grid_with_all_info)

direction_reversed = {'n':'s', 's':'n', 'e':'w', 'w':'e'}


class Graph:

    def __init__(self):
        self.vertices = {}

    def dft(self):
        response = requests.get(
        ' https://lambda-treasure-hunt.herokuapp.com/api/adv/init/',
        headers={'Authorization': 'Token 511b799007ac9e828b320eaf2c3d6525557e9502'},
        )
        json_response = response.json()


        grid_with_all_info[json_response["room_id"]] = json_response

        current_room = json_response
      
        s = Stack()
        s.push(current_room["room_id"])
        visited = set()
        last_room = None
        last_direction = None

        while s.size() > 0:
            if current_room["room_id"] not in self.vertices:
                  self.vertices[current_room["room_id"]] = {}
                  for direction in current_room["exits"]:
                        self.vertices[current_room["room_id"]][direction] = "?"
            if last_direction:
              self.vertices[current_room["room_id"]][direction_reversed[last_direction]] = last_room

            print(self.vertices)
            last_room = current_room["room_id"]
            v = s.pop()
            if v not in visited:
                visited.add(v)
                exits = current_room["exits"]
                
                while True: 
                    direction = exits[random.randint(0, len(exits) - 1)]
                    if self.vertices[current_room["room_id"]][direction] == "?":
                            time.sleep(3)
                            the_new_room = requests.post('https://lambda-treasure-hunt.herokuapp.com/api/adv/move/', json={'direction':f'{direction}'}, headers={'Authorization': 'Token 511b799007ac9e828b320eaf2c3d6525557e9502'})  
                            new_room = the_new_room.json()
                            print(new_room, the_new_room, direction)
                            self.vertices[last_room][direction] = new_room["room_id"] 
                            last_direction = direction
                            s.push(new_room["room_id"])
                            current_room = new_room
                            grid_with_all_info[new_room["room_id"]] = new_room
                            break
                    break
                    

    # def bfs(self):
    #     q = Queue()
    #     q.enqueue([player.currentRoom.id])
    #     visited = set()
    #     while q.size() > 0:
    #         path = q.dequeue()
    #         v = path[-1]
    #         if v not in visited:
    #             for direction in ["s", "n", "e", "w"]:
    #                 try: 
    #                     if self.vertices[v][direction] == "?":
    #                         return path
    #                 except KeyError:
    #                     None
    #             visited.add(v)
    #             for key, value in self.vertices[v].items():
    #                 new_path = list(path)
    #                 new_path.append(value)
    #                 q.enqueue(new_path)
      
    def traverse(self):
      # while len(self.vertices) < 500: # maybe 499 => needs to be checked 
        self.dft()
          
          # shortest_path_bfs = self.bfs()
      
          # try:
          #     for index in range(len(shortest_path_bfs)):
          #         for direction in ["n", "s", "e", "w"]:
          #             try:
          #                 if self.vertices[shortest_path_bfs[index]][direction] == shortest_path_bfs[index + 1]: 
          #                     player.travel(direction) # CALL MOVEMENT ONLY EVERY SECOND
          #                     break
          #             except KeyError:
          #                 None
          #             except IndexError:
          #                 None
          # except TypeError:
          #   return

graph = Graph()
graph.traverse()
print(grid_with_all_info)
