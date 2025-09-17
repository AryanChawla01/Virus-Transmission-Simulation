# Base for simple simulation of virus transmission between pedestrians on a sidewalk.
# Written by Aryan Chawla

import random
import math
from matplotlib import pyplot as plt, colors
from matplotlib.animation import FuncAnimation

rand = random.Random()
SIDEWALK_WIDTH = 25  # This is the y-dimension of the sidewalk
SIDEWALK_LENGTH = 200  # This is the x-dimension of the sidewalk
INTERARRIVAL = 3 # Average number of time steps between arrivals (each side handled separately)
CONCERN_DISTANCE = 4
SAFE_THRESHOLD = 5


# Setup for graphical display
colourmap = colors.ListedColormap(["lightgrey", "green", "red", "yellow", "blue"])
normalizer = colors.Normalize(vmin=0.0, vmax=4.0)

class Person:
    def __init__(self, id, sidewalk):
        self.id = id
        self.active = False
        self.sidewalk = sidewalk
        self.x = self.startx = rand.choice([0, SIDEWALK_LENGTH - 1])
        self.direction = 1 if self.startx == 0 else -1
        self.team = 'eastward' if self.startx == 0 else 'westward'
        self.starty = self.y = rand.randint(0, SIDEWALK_WIDTH - 1)
    def enter_sidewalk(self, x, y):
        if self.sidewalk.enter_sidewalk(self, x, y):
            self.active = True
    def step(self):
        nearby_agents = self.sidewalk.get_nearest_list(self.x, self.y, CONCERN_DISTANCE)
        opposing_agents = [agent for agent in nearby_agents if agent.team != self.team]
        teammates = [agent for agent in nearby_agents if agent.team == self.team]
        if len(opposing_agents) >= 1 and len(teammates) < SAFE_THRESHOLD:
            self.move_away_from_opposition(opposing_agents)
        else:
            self.move_towards_target()
    def move_away_from_opposition(self, opposition_agents):
        for agent in opposition_agents:
            dx = agent.x - self.x
            dy = agent.y - self.y
            if dx > 0: #left
                self.move(-1, 0)
            elif dx < 0: #right
                self.move(1, 0)
            elif dy > 0: #down
                self.move(0, -1)
            elif dy < 0: #up
                self.move(0, 1)
    def move_towards_target(self):
        if self.team == 'eastward':
            if self.x < SIDEWALK_LENGTH - 1:
                self.move(1, 0)  
        else:
            if self.x > 0:
                self.move(-1, 0) 
    def move(self, dx, dy):
        desiredx = self.x + dx
        desiredy = self.y + dy
        desiredx = max(min(desiredx, SIDEWALK_LENGTH - 1), 0)
        desiredy = max(min(desiredy, SIDEWALK_WIDTH - 1), 0)
        self.sidewalk.attemptmove(self, desiredx, desiredy)
    def __str__(self):
        return f"id: {self.id}  x: {self.x}  y: {self.y}"
class Sidewalk:
    def __init__(self):
        self.storage = SWGrid()
        self.bitmap = [[0.0 for _ in range(SIDEWALK_LENGTH)] for _ in range(SIDEWALK_WIDTH)]
        self.agent_id_counter = 0
    def add_random_agent(self):
        team = 'eastward' if rand.choice([True, False]) else 'westward' 
        new_person = Person(self.agent_id_counter, self)
        self.agent_id_counter += 1
        start_x = 0 if team == 'eastward' else SIDEWALK_LENGTH - 1  
        new_person.enter_sidewalk(start_x, rand.randint(0, SIDEWALK_WIDTH - 1))  
    def enter_sidewalk(self, person, x, y):
        if self.storage.isoccupied(x, y):
            return False
        self.storage.add_item(x, y, person)
        person.x = x
        person.y = y
        return True
    def attemptmove(self, person, x, y):
        if abs(person.x - x) + abs(person.y - y) > 1:
            return False
        if self.storage.isoccupied(x, y):
            return False
        person.x = x
        person.y = y
        self.storage.move_item(x, y, person)
        return True
    def get_nearest_list(self, x, y, max_distance=None):
        sort_list = []
        for agent in self.storage.get_list():
            distance = abs(agent.x - x) + abs(agent.y - y)
            if max_distance and distance <= max_distance:
                sort_list.append((distance, agent))
        sort_list.sort(key=lambda i: i[0])
        return [i[1] for i in sort_list]
    def refresh_image(self):
        self.bitmap = [[0.0 for _ in range(SIDEWALK_LENGTH)] for _ in range(SIDEWALK_WIDTH)]
        for person in self.storage.get_list():
            x = person.x
            y = person.y
            colour = 1 if person.team == 'eastward' else 2
            self.bitmap[y][x] = colour
    def run_step(self, time_step):
        if time_step % INTERARRIVAL == 0:
            self.add_random_agent()
        for person in self.storage.get_list():
            if person.active:
                person.step()
        
        self.refresh_image()
    def isoccupied(self, x, y):
        return self.storage.isoccupied(x, y)
class SWGrid:
    def __init__(self):
        self.dic = dict()
    def isoccupied(self, x, y):
        return (x, y) in self.dic
    def add_item(self, x, y, item):
        if (x, y) in self.dic:
            return False
        self.dic[(x, y)] = item
        return True
    def move_item(self, x, y, item):
        if self.isoccupied(x, y):
            raise Exception("Move to occupied square!")
        oldloc = next(key for key, value in self.dic.items() if value == item)
        del self.dic[oldloc]
        self.add_item(x, y, item)
    def remove_item(self, item):
        oldloc = next(key for key, value in self.dic.items() if value == item)
        del self.dic[oldloc]
    def get_item(self, x, y):
        return self.dic.get((x, y), None)
    def get_list(self):
        return list(self.dic.values())
#Run
sw = Sidewalk()
personlist = [Person(i, sw) for i in range(40)]
for person in personlist:
    person.enter_sidewalk(person.startx, person.starty)

display = plt.figure(figsize=(15, 5))
image = plt.imshow(sw.bitmap, cmap=colourmap, norm=normalizer, animated=True)
t = 0
def updatefigure(*args):
    global t
    t += 1
    if t % 100 == 0:
        print(f"Time: {t}")
    sw.run_step(t)
    sw.refresh_image()
    image.set_array(sw.bitmap)
    return image,
#It looks better and more fun when it is a little fast : )
anim = FuncAnimation(display, updatefigure, frames=2000, interval=50, blit=True, repeat=False)
plt.show()
print("Done!")