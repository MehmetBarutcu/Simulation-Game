from .agent import Agent
from .grid_world import GridWorld

class Simulation:
    def __init__(self, world, agents, total_golds):
        self.world = world
        self.agents = agents
        self.is_over = False
        self.total_golds = total_golds
    
    def print_grid(self,return_grid=False):
        grid = [['__' for _ in range(self.world.n)] for _ in range(self.world.n)]

        for crumb,value in self.world.radioactive_crumbs.items():
            if value > 0:
                grid[crumb[0]][crumb[1]] = '*{}'.format(value)
        
        grid[list(self.world.depot.keys())[0][0]][list(self.world.depot.keys())[0][1]] = 'D{}'.format(list(self.world.depot.values())[0])
        for agent in self.agents:
            if agent.samples == 0:
                grid[agent.x][agent.y] = 'r{}'.format(agent.id)
            else:
                grid[agent.x][agent.y] = 'R{}'.format(agent.id)
        for obstacle in self.world.obstacles:
            grid[obstacle[0]][obstacle[1]] = 'O'
        for coord, gold in self.world.gold_units.items():
            grid[coord[0]][coord[1]] = 'G{}'.format(gold)
        
        for row in grid:
            print(' '.join(row))
            
        if return_grid:
            return grid
    
    def simulate(self):
        step = 0
        print("Initial scene:")
        self.print_grid()
        while not self.is_over:
            step += 1
            print("\nScene after step {}:".format(step))
            for agent in self.agents:
                percept = agent.see(self.world)
                agent.act(self.world, percept)
            # print(f'Before reset:{self.world.gold_exchange}')
            self.world.reset_gold_exchange()
            # print(f'After reset:{self.world.gold_exchange}')
            if sum(list(self.world.depot.values())) == self.total_golds:
                self.is_over = True
            self.print_grid()
        
        print("\nGoal achieved in {} steps. Final scene:".format(step))
        self.print_grid()

# def main():
#     n, obstacles, gold_clusters, depot, num_agents, agents, total_golds = read_input("env.inp")
#     world = GridWorld(n, agents, obstacles, gold_clusters, depot)
#     simulation = Simulation(world, agents, total_golds)
#     simulation.simulate()

# if __name__ == "__main__":
#     main()