# Command to run the code file
# python <filename> <maze file> <population size> <mutation rate> <generation size>
# Eg: python task3.py maze.txt 100 0.1 100

import sys
import random

class Maze:
    def __init__(self, filename, population_size, mutation_rate, generation_size):
        self.filename = filename
        self.population_size = population_size
        self.mutation_rate = mutation_rate
        self.generation_size = generation_size

        with open(filename) as f:
            contents = f.read()

        # Validate start and goal
        if contents.count("A") != 1:
            raise Exception("maze must have exactly one start point")
        if contents.count("B") != 1:
            raise Exception("maze must have exactly one goal")

        # calculating the dimensions of the maze
        contents = contents.splitlines()
        self.height = len(contents)
        self.width = max(len(line) for line in contents)

        # reading the walls in the maze
        self.walls = []
        for i in range(self.height):
            row = []
            for j in range(self.width):
                try:
                    if contents[i][j] == "A":
                        self.start = (i, j)
                        row.append(False)
                    elif contents[i][j] == "B":
                        self.goal = (i, j)
                        row.append(False)
                    elif contents[i][j] == " ":
                        row.append(False)
                    else:
                        row.append(True)
                except IndexError:
                    row.append(False)
            self.walls.append(row)

        self.solution = None

    def print_maze(self):
        solution = self.solution if self.solution is not None else None
        for i in range(self.height):
            for j in range(self.width):
                if self.walls[i][j]:
                    print("█", end="")
                elif (i, j) == self.start:
                    print("A", end="")
                elif (i, j) == self.goal:
                    print("B", end="")
                elif solution is not None and (i, j) in solution:
                    print("*", end="")
                else:
                    print(" ", end="")
            print()
        print()

    def neighbors(self, state):
        row, col = state
        candidates = [
            ("up", (row - 1, col)),
            ("down", (row + 1, col)),
            ("left", (row, col - 1)),
            ("right", (row, col + 1))
        ]

        result = []
        for action, (r, c) in candidates:
            if 0 <= r < self.height and 0 <= c < self.width and not self.walls[r][c]:
                result.append((action, (r, c)))
        return result
    
    # Generates random traversable paths
    def path(self):
        start = self.start
        # initialising to start position
        path = [start]
        # randomly explores the maze
        while path[-1] != self.goal:
            direction = random.choice(self.neighbors(path[-1]))
            new_state = direction[1]
            path.append(new_state)
        return path
    
    # calculates the fitness of the paths
    def fitness(self, path):
        x, y = path[-1]
        target = self.goal
        # calculates the manhattan distance
        return 1 / (abs(x - target[0]) + abs(y - target[1]) + 1)

    def mutation_path(self, path):
        for i in range(1, len(path) - 1):
            if random.random() < self.mutation_rate:
                # reads the maze neighbours and walls
                directions = self.neighbors(path[i]) 
                #checks the validation of the directions
                if directions:
                    new_direction = random.choice(directions)
                    new_state = new_direction[1]
                    path[i] = new_state
        return path

    def maze(self):
        
        # calls the path function to generate random paths  
        population = [self.path() for _ in range(self.population_size)]

        for _ in range(self.generation_size):
            # calls the fitness function to to calculate fitness score
            fitness_scores = [self.fitness(path) for path in population]
            
            # storing the top fitness scores
            top_paths = []
            for _ in range(self.population_size):
                top_paths.append(population[fitness_scores.index(max(fitness_scores))])

            # Generating new population using crossover and mutation
            new_population = []
            while len(new_population) < self.population_size:
                parent1 = random.choice(top_paths)
                parent2 = random.choice(top_paths)
                batchs = random.randint(1, min(len(parent1), len(parent2)) - 1)
                child = parent1[:batchs] + parent2[batchs:]
                
                # Generating random mutations
                child = self.mutation_path(child)
                new_population.append(child)
            population = new_population
        
        # final population based on fitness score
        self.solution = max(population, key=self.fitness)
        return self.solution


# reading input from the user
maze_file = sys.argv[1]
population_size = int(sys.argv[2])
mutation_rate = float(sys.argv[3])
generation_size = int(sys.argv[4])

# passing the arguments to the maze
maze = Maze(maze_file, population_size, mutation_rate, generation_size)
print('Solving the maze problem')

#Solving the maze
result = maze.maze()

# printing the maze
maze.print_maze()
