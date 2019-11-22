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
        self.current_room_id = None
        self.current_room = None
        self.last_room = None

    def dft(self):
        # print(self.current_room, f"line 58")
        s = Stack()
        s.push(self.current_room["room_id"])
        visited = set()
        
        
        last_direction = None

        while s.size() > 0:
            if self.current_room["room_id"] not in self.vertices:
                  self.vertices[self.current_room["room_id"]] = {}
                  for direction in self.current_room["exits"]:
                        self.vertices[self.current_room["room_id"]][direction] = "?"
            if last_direction:
              self.vertices[self.current_room["room_id"]][direction_reversed[last_direction]] = self.last_room

            # print(self.vertices)
            self.last_room = self.current_room["room_id"]
            v = s.pop()
            if v not in visited:
                visited.add(v)
                exits = self.current_room["exits"]
                
                while True: 
                    direction = exits[random.randint(0, len(exits) - 1)]
                    if self.vertices[self.current_room["room_id"]][direction] == "?":
                            time.sleep(self.current_room["cooldown"])
                            (print("dft"))
                            the_new_room = requests.post('https://lambda-treasure-hunt.herokuapp.com/api/adv/move/', json={'direction':f'{direction}'}, headers={'Authorization': 'Token 511b799007ac9e828b320eaf2c3d6525557e9502'})  
                            new_room = the_new_room.json()
                            # print(new_room, the_new_room, direction)
                            self.vertices[self.last_room][direction] = new_room["room_id"] 
                            last_direction = direction
                            s.push(new_room["room_id"])
                            self.current_room = new_room
                            grid_with_all_info[new_room["room_id"]] = new_room
                            print(self.current_room)
                            break
                    break
        self.current_room_id = self.current_room["room_id"]

    def bfs(self):
        q = Queue()
        q.enqueue([self.current_room_id])
        visited = set()
        while q.size() > 0:
            path = q.dequeue()
            v = path[-1]
            if v not in visited:
                for direction in ["s", "n", "e", "w"]:
                    try: 
                        if self.vertices[v][direction] == "?":
                            return path
                    except KeyError:
                        None
                visited.add(v)
                for key, value in self.vertices[v].items():
                    new_path = list(path)
                    new_path.append(value)
                    q.enqueue(new_path)
      
    def traverse(self):
      response = requests.get(
      ' https://lambda-treasure-hunt.herokuapp.com/api/adv/init/',
      headers={'Authorization': 'Token 511b799007ac9e828b320eaf2c3d6525557e9502'},
      )
        
      json_response = response.json()


      grid_with_all_info[json_response["room_id"]] = json_response

      self.current_room = json_response

      while len(self.vertices) < 500: # maybe 499 => needs to be checked 
          self.dft()
          
          shortest_path_bfs = self.bfs()
          # print(shortest_path_bfs)
      
          try:
              for index in range(len(shortest_path_bfs)):
                  for direction in ["n", "s", "e", "w"]:
                      try:
                          if self.vertices[shortest_path_bfs[index]][direction] == shortest_path_bfs[index + 1]: 
                              time.sleep(self.current_room["cooldown"])
                              print("bfs", shortest_path_bfs)
                              the_new_room = requests.post('https://lambda-treasure-hunt.herokuapp.com/api/adv/move/', json={'direction':f'{direction}', 
                              "next_room_id": f'{shortest_path_bfs[index + 1]}'}, headers={'Authorization': 'Token 511b799007ac9e828b320eaf2c3d6525557e9502'})
                              new_room = the_new_room.json()
                              self.current_room = new_room
                              self.current_room_id = new_room["room_id"]
                              print(self.current_room)
                              
                              break
                      except KeyError:
                          None
                      except IndexError:
                          None
          except TypeError:
            None

graph = Graph()
graph.traverse()
print(grid_with_all_info)

print(graph.vertices)
