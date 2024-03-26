import random

class GridWorld:
    def __init__(self, n, agents, obstacles, gold_clusters, depot):
        self.n = n
        self.obstacles = obstacles
        self.gold_units = gold_clusters
        self.depot = depot
        self.agents = agents
        self.radioactive_crumbs = {}

        self.gold_exchange = []
    
    def get_available_agents_to_exchange(self, neighbor_agents):
        agent_ids = []
        for neigbor in neighbor_agents:
            for ag in self.agents:
                if (neigbor[0],neigbor[1]) == (ag.x,ag.y):
                    if ag.samples == 0:
                        agent_ids.append(ag.id)
        return agent_ids
    
    def exchange(self,agent_id1,agent_id2):
        self.agents[agent_id1].samples -=1
        self.agents[agent_id2].samples +=1

    def sense_neighbors(self, agent):
        neighbors = []
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                if (dx != 0 and dy != 0) and (0 <= agent.x + dx < self.n) and (0 <= agent.y + dy < self.n):
                    neighbors.append((agent.x + dx, agent.y + dy))
        return neighbors
    
    def reset_gold_exchange(self):
        self.gold_exhange = []