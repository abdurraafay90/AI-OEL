import random


distance_matrix = [
    [0, 15, 20, 25],
    [20, 10, 45, 35],
    [5, 25, 10, 40],
    [30, 35, 40, 10],
]


num_cities = len(distance_matrix)


def fitness_function(route):
    total_distance = sum(
        distance_matrix[route[i]][route[i + 1]] for i in range(len(route) - 1)
    )
    total_distance += distance_matrix[route[-1]][route[0]]
    return 1 / total_distance


def generate_population(pop_size, num_cities):
    return [random.sample(range(num_cities), num_cities) for _ in range(pop_size)]


def select_parents(population, fitnesses):
    total_fitness = sum(fitnesses)
    probabilities = [f / total_fitness for f in fitnesses]
    return random.choices(population, weights=probabilities, k=2)


def crossover(parent1, parent2):
    start, end = sorted(random.sample(range(num_cities), 2))
    child = [-1] * num_cities
    child[start:end + 1] = parent1[start:end + 1]

    pointer = 0
    for gene in parent2:
        if gene not in child:
            while child[pointer] != -1:
                pointer += 1
            child[pointer] = gene

    return child


def mutate(route, mutation_rate):
    if random.random() < mutation_rate:
        i, j = random.sample(range(num_cities), 2)
        route[i], route[j] = route[j], route[i]
    return route


def genetic_algorithm(
    distance_matrix,
    pop_size,
    generations,
    crossover_probability,
    mutation_probability,
):

    population = generate_population(pop_size, num_cities)

    for generation in range(generations):

        fitnesses = [fitness_function(route) for route in population]
        new_population = []
        while len(new_population) < pop_size:
            parent1, parent2 = select_parents(population, fitnesses)

            if random.random() < crossover_probability:
                child = crossover(parent1, parent2)
            else:
                child = parent1[:]

            child = mutate(child, mutation_probability)

            new_population.append(child)
        population = new_population

        best_route = max(population, key=fitness_function)
        best_distance = 1 / fitness_function(best_route)
        print(
            f"Generation {generation + 1}: Best Route = {best_route}, Distance = {best_distance}"
        )

    best_route = max(population, key=fitness_function)
    best_distance = 1 / fitness_function(best_route)
    return best_route, best_distance



POP_SIZE = 10
GENERATIONS = 50
CROSSOVER_PROBABILITY = 0.8
MUTATION_PROBABILITY = 0.2


best_route, best_distance = genetic_algorithm(
    distance_matrix,
    POP_SIZE,
    GENERATIONS,
    CROSSOVER_PROBABILITY,
    MUTATION_PROBABILITY,
)
print(f"\nBest Route: {best_route}, Distance: {best_distance}")
