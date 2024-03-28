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
    
    def sense_available_locations(self, world, neighbors):
        agent_locations = [(a.x, a.y) for a in world.agents]
        obstacle_locations = set(world.obstacles)
        return [(neighbor_x, neighbor_y) for neighbor_x, neighbor_y in neighbors
                if (neighbor_x, neighbor_y) not in agent_locations and (neighbor_x, neighbor_y) not in obstacle_locations]


    def sense_nearby_agents(self,world,neighbors):
        return [(neighbor_x, neighbor_y) for neighbor_x, neighbor_y in neighbors if (neighbor_x, neighbor_y) in [(a.x, a.y) for a in world.agents]]
    
    def sense_nearby_crumbs(self,world,neighbors):
        crumbs = {}
        for neighbor in neighbors:
            if world.radioactive_crumbs.get(neighbor) and world.radioactive_crumbs[neighbor] >0:
                crumbs[neighbor] =  world.radioactive_crumbs.get(neighbor)
        return crumbs
    
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
        percept['nearby_crumbs'] = self.sense_nearby_crumbs(world,percept['available_locations'])
        percept['nearby_gold_units'] = self.sense_nearby_gold_units(world,percept['available_locations'])
        percept['depot_location'] = list(world.depot.keys())[0]
        # print(f'Agent id: {self.id}')
        # print(f'Agent location: {(self.x,self.y)}')
        # print(f'Neighbors:{neighbors}')
        # print(f'Perception: {percept}')
        # print(f'Gold Exchange List: {world.gold_exchange}')
        # print(f'Crumbs in map: {world.radioactive_crumbs}')
        # # print(f'Crumb Collected: {self.crumb_collected}')
        # print('*'*10)
        
        return percept
    
    def act(self,world,percept):
        if not percept['available_locations'] and (self.x,self.y) not in world.depot and self.samples > 0:
            if self.id not in world.gold_exchange and percept['nearby_agents'] :
                agent_ids, agent_locations = world.get_available_agents_to_exchange(percept['nearby_agents'])
                if agent_locations:
                    selected_agent_location = self.calculate_distance_to_depot(agent_locations,percept['depot_location'],sense='min')
                    agent_id = agent_ids[agent_locations.index(selected_agent_location)]
                    world.exchange(self.id,agent_id)
                    world.gold_exchange.append(self.id)
                    world.gold_exchange.append(agent_id)

        else:
            if self.samples:
                if (self.x,self.y) in world.depot:
                    # Drop the samples
                    world.depot[(self.x,self.y)] += self.samples
                    self.samples = 0
                else:
                    if self.id not in world.gold_exchange:
                        agent_ids, agent_locations = world.get_available_agents_to_exchange(percept['nearby_agents'])
                    else:
                        agent_ids, agent_locations =[], []

                    if not percept['available_locations']+agent_locations:
                        chosen_direction = (self.x,self.y)
                    else:
                        chosen_direction = self.calculate_distance_to_depot(percept['available_locations']+agent_locations,percept['depot_location'],sense='min')
                    
                    if chosen_direction in percept['nearby_agents']:
                        # print(self.id)
                        # print(self.x)
                        # print(self.y)
                        # print(chosen_direction)
                        # print(percept['nearby_agents'])
                        # print(agent_locations)
                        # print(agent_ids)
                        # print('*'*10)
                        agent_id = agent_ids[agent_locations.index(chosen_direction)]
                        world.exchange(self.id,agent_id)
                        world.gold_exchange.append(self.id)
                        world.gold_exchange.append(agent_id)
                    else:
                        self.move(chosen_direction)
                        world.radioactive_crumbs[(self.x,self.y)] = world.radioactive_crumbs.get((self.x,self.y),0) + 2
            else: 
                if percept['nearby_gold_units']:
                    chosen_direction = random.choice(percept['nearby_gold_units'])
                    self.move(chosen_direction)
                    self.samples +=1
                    world.gold_units[chosen_direction] -=1

                elif percept['nearby_crumbs']:
                    max_crumbs_nearby =  max(percept['nearby_crumbs'].values())
                    max_crumb_locations = [k for k,v in percept['nearby_crumbs'].items() if v == max_crumbs_nearby]
                    if len(max_crumb_locations) > 1:
                        # print('Go to away from depot')
                        chosen_direction = self.calculate_distance_to_depot(max_crumb_locations,percept['depot_location'],sense='max')
                    else: 
                        chosen_direction = max_crumb_locations[0]
                    self.move(chosen_direction)
                    world.radioactive_crumbs[(self.x,self.y)] -= 1
                
                else:
                    if percept['available_locations']:
                        chosen_direction = random.choice(percept['available_locations'])
                        self.move(chosen_direction)