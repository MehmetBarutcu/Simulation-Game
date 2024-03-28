# Distant Planet Exploration

## Introduction

The Distant Planet Exploration Game simulates agents exploring a remote planet, collecting valuable resources, avoiding obstacles, and cooperating with other agents for efficient resource gathering. This report provides an overview of the game mechanics, the architecture of the agents, their action policy, the project directory structure, and instructions for running the code.

The objective is to explore a distant planet, more concretely, to collect samples of a particular type of precious rock. The location of the rock samples is not known in advance, but they are typically clustered in certain spots. A number of autonomous vehicles are available that can drive around the planet collecting samples and later reenter the a depot to go back to earth. There is no detailed map of the planet available, although it is known that the terrain is full of obstacles-hills, 
valleys, etc. -which prevent the vehicles from exchanging any communication. 

Possible actions for robots are move, wait, collect and passing the gold to a nearby robot. Robots can only sense 8 neighbor of cells. Simulation ends when all golds in the map are transferred to the depot.

## Concrete Architecture of Agents

The agents in the game utilize a perception-action cycle, where they perceive the environment through sensors and then decide on actions based on their perception. The architecture includes:

- **Perception**: Agents use sensors to gather information about their surroundings, including nearby obstacles, resources, other agents, and the gradient field emerging from the depot.
- **Action**: Based on their perception, agents decide on actions to take. These actions include moving to nearby locations, collecting resources, depositing resources at the depot, and exchanging resources with other agents.

## Action Policy

The action policy layers of an agent is outlined below:

1. If agent is stuck and there are another agents with no golds nearby, then transfer the golds to the one that is nearest to depot location

2. If agent has gold and at the depot, then drop the gold.

3. If agent has gold and there is another agent with no gold at the location where agent wants to move towards the gradient signal coming from depot, then transfer the golds to that agent, otherwise move to that location and drop 2 radioactive crumbs.

4. If agent has no golds and there are gold units nearby, randomly select one of them, move to that location and collect 1 gold.

5. If agent has no golds and there are radioactive crumbs nearby, then select the location where maximum number of crumbs are located, move to that location and collect 1 crumb.

6. Else, move randomly to a available locations if any, otherwise wait.

## Project Directory Structure

```
project_root/
│
├── game_elements/
│   ├── __init__.py
│   ├── agent.py
│   ├── grid_world.py
│   └── simulation.py
│
├── main.py
├── simulate.py
├── report.md
└── env.inp
```

## Running the Code
```
python simulate.py --input-file env.inp --export-file results.txt
```

## Optional parameters:

- --input-file: Specifies the input file path containing the initial configuration of the game.
- --random-generate-instance: Generates a random map, agents, and units if specified.
- --export-file: Exports the simulation results to a text file.
