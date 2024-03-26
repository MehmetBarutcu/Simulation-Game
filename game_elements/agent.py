import random

class Agent:
    def __init__(self, x, y, id):
        self.x = x
        self.y = y
        self.id = id
        self.samples = 0
    
    def move(self, direction):
        self.x = direction[0]
        self.y = direction[1]
    
    def sense_neighbors(self,world):
        neighbors = []
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                if (0 <= self.x + dx < world.n) and (0 <= self.y + dy < world.n) and (self.x +dx, self.y +dy) != (self.x,self.y):
                    neighbors.append((self.x + dx, self.y + dy))
        return neighbors
    
    def sense_available_locations(self,world, neighbors):
        return [(neighbor_x, neighbor_y) for neighbor_x, neighbor_y in neighbors if (neighbor_x, neighbor_y) not in ([(a.x, a.y) for a in world.agents] and world.obstacles)] # check

    def sense_nearby_agents(self,world,neighbors):
        return [(neighbor_x, neighbor_y) for neighbor_x, neighbor_y in neighbors if (neighbor_x, neighbor_y) in [(a.x, a.y) for a in world.agents]]
    
    # def sense_nearby_crumbs(self,world,neighbors):
    #     crumbs = {}
    #     for neighbor in neighbors:
    #         if world.radioactive_crumbs.get(neighbor) and world.radioactive_crumbs[neighbor] >0:
    #             crumbs[neighbor] =  world.radioactive_crumbs.get(neighbor)
    #     return crumbs
    
    def sense_nearby_crumbs(self,world):
        if (self.x,self.y) in world.radioactive_crumbs and world.radioactive_crumbs[(self.x,self.y)]>0:
            return True
        return False
    
    def calculate_distance_to_depot(self,available_locations,depot_location, sense='min'):
        method = {'min':min,'max':max}
        distances = {}
        for loc in available_locations:
            dist = ((loc[0] - depot_location[0]) ** 2 + (loc[1] - depot_location[1]) ** 2)**0.5
            distances[loc] = round(dist,2)
        return method[sense](distances, key=distances.get)

    def sense_nearby_gold_units(self,world, neighbors):
        gold_units = []
        for neighbor in neighbors:
            for coord,value in world.gold_units.items():
                if neighbor == coord and value >0:
                    gold_units.append(coord)
        return gold_units

    def see(self,world):
        percept = {}
        neighbors = self.sense_neighbors(world)
        percept['gold_exchange'] = world.gold_exchange
        percept['available_locations'] = self.sense_available_locations(world,neighbors)
        percept['nearby_agents'] = self.sense_nearby_agents(world,neighbors)
        percept['nearby_crumbs'] = self.sense_nearby_crumbs(world)
        percept['nearby_gold_units'] = self.sense_nearby_gold_units(world,neighbors)
        percept['depot_location'] = list(world.depot.keys())[0]
        # print(f'Agent id: {self.id}')
        # print(f'Agent location: {(self.x,self.y)}')
        # print(f'Neighbors:{neighbors}')
        # print(f'Perception: {percept}')
        # print(f'Crumbs in map: {world.radioactive_crumbs}')
        # print('*'*10)
        
        return percept
    
    def act(self,world,percept):
        if not percept['available_locations']:
            if self.id not in world.gold_exchange and percept['nearby_agents'] and self.samples > 0:
                available_agents = world.get_available_agents_to_exchange(percept['nearby_agents'])
                if available_agents:
                    selected_agent = random.choice(available_agents)
                    world.exhange(self.id,selected_agent)
                    world.gold_exchange.append(self.id)
                    world.gold_exchange.append(selected_agent)
        else:
            if self.samples:
                if (self.x,self.y) in world.depot:
                    # Drop the samples
                    world.depot[(self.x,self.y)] += self.samples
                    self.samples = 0
                else:
                    chosen_direction = self.calculate_distance_to_depot(percept['available_locations'],percept['depot_location'],sense='min')
                    self.move(chosen_direction)
                    world.radioactive_crumbs[(self.x,self.y)] = world.radioactive_crumbs.get((self.x,self.y),0) + 2
            else: 
                if percept['nearby_gold_units']:
                    chosen_direction = random.choice(percept['nearby_gold_units'])
                    self.move(chosen_direction)
                    self.samples +=1
                    world.gold_units[chosen_direction] -=1

                elif percept['nearby_crumbs']:
                    world.radioactive_crumbs[(self.x,self.y)] -= 1
                    chosen_direction = self.calculate_distance_to_depot(percept['available_locations'],percept['depot_location'],sense='max')
                    self.move(chosen_direction)
                
                else:
                    chosen_direction = random.choice(percept['available_locations'])
                    self.move(chosen_direction)