import argparse
import random
from game_elements import Simulation, GridWorld, Agent

def read_input(file_name):
    with open(file_name, 'r') as file:
        lines = file.readlines()
        n = int(lines[0])
        num_agents = int(lines[1])
        num_gold_clusters = int(lines[2])
        num_obstacles = int(lines[3])
        obstacles = []
        gold_clusters = {}
        depot = {}
        agents = []
        for line in lines[4:]:
            parts = line.split()
            obj_type = parts[0]
            x, y = int(parts[1])-1, int(parts[2])-1
            if obj_type == 'r':
                agents.append(Agent(x, y, len(agents)+1))  # Assigning IDs sequentially
            elif obj_type == 'g':
                gold_clusters[(x, y)] = int(parts[3])
            elif obj_type == 'o':
                obstacles.append((x, y))
            elif obj_type == 'd':
                depot[(x, y)] = 0
        return n, obstacles, gold_clusters, depot, num_agents, agents

def find_remaining_locations(l1,l2):
    return list(set(l1)-set(l2))

def generate_random_instance(n, num_agents, num_gold_clusters, num_obstacles):
    map = [(x,y) for x in range(n) for y in range(n)]
    obstacles = random.choices(map,k=num_obstacles)
    map = find_remaining_locations(map,obstacles)
    gold_cluster_locations = random.choices(map,k=num_gold_clusters)
    gold_clusters = {loc:random.randint(1, 5) for loc in gold_cluster_locations}
    map = find_remaining_locations(map,gold_cluster_locations)
    depot = {random.choice(map): 0}
    map = find_remaining_locations(map,list(depot.keys()))
    agent_locations = random.choices(map,k=num_agents)
    agents = [Agent(loc[0], loc[1], id+1) for id, loc in enumerate(agent_locations)]
    return obstacles, gold_clusters, depot, agents

def export_results(filename, iteration, grid):
    with open(filename, 'a') as file:
        file.write("Scene after step {}:\n".format(iteration))
        for row in grid:
            file.write(' '.join(row) + '\n')
        file.write('\n')

def main():
    parser = argparse.ArgumentParser(description='Distant Planet Exploration Simulation')
    parser.add_argument('--input-file', type=str, help='Input file path')
    parser.add_argument('--random-generate-instance', action='store_true', help='Generate random map, agents, and units')
    parser.add_argument('--export-file', type=str, help='Export results to a txt file')

    args = parser.parse_args()

    if args.random_generate_instance:
        # Generate random map, agents, and units
        n = random.randint(5, 15)
        num_agents = random.randint(1, 5)
        num_gold_clusters = random.randint(1, 5)
        num_obstacles = random.randint(1, 10)
        obstacles, gold_clusters, depot, agents = generate_random_instance(n, num_agents, num_gold_clusters, num_obstacles)
        world = GridWorld(n, agents, obstacles, gold_clusters, depot)
    elif args.input_file:
        # Read input from file
        n, obstacles, gold_clusters, depot, num_agents, agents = read_input(args.input_file)
        world = GridWorld(n, agents, obstacles, gold_clusters, depot)
    else:
        print("Please provide input file or specify --random-generate-instance option.")
        return

    total_golds = sum(gold_clusters.values()) if gold_clusters else 0

    simulation = Simulation(world, agents, total_golds)
    if args.export_file:
        with open(args.export_file, 'w') as file:
            file.write("Initial scene:\n")
        iteration = 0
        print("Initial scene:")
        simulation.print_grid()
        while not simulation.is_over:
            iteration += 1
            print("\nScene after step {}:".format(iteration))
            for agent in agents:
                percept = agent.see(world)
                agent.act(world, percept)
            world.reset_gold_exchange()
            if sum(list(world.depot.values())) == total_golds:
                simulation.is_over = True  
            export_results(args.export_file, iteration, simulation.print_grid(return_grid=True))
        print("\nGoal achieved in {} steps. Final scene:".format(iteration))
        simulation.print_grid()
    else:
        simulation.simulate()

if __name__ == "__main__":
    main()
