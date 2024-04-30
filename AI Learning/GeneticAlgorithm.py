import random

def problem(x,y,z): # Problem returns a number. This will need to expand for greater use.
    return 6*x**6 + y + z - 100

def fitness(x,y,z): #Determines how close it is to the target.
    ans = problem(x,y,z) #Creates 1 simulation of the problem with given params

    if ans == 0: #If target is dead on, return really high value
        return 99999
    else: # Else return value that grows as target is closer.
        return abs(1/ans)
    
def mutation(ranked_solutions): # Function to add variance to the best solutions currently to try again
    best_solutions = ranked_solutions[:100]

    elements = []

    for s in best_solutions: #Adds all solutions into a pool of elements.
        elements.append(s[1][0])
        elements.append(s[1][1])
        elements.append(s[1][2])

    new_gen = []
    for _ in range(1000):
        ex = random.choice(elements) * random.uniform(0.99, 1.01) #Takes the random elements and adds variance of 2%
        ey = random.choice(elements) * random.uniform(0.99, 1.01)
        ez = random.choice(elements) * random.uniform(0.99, 1.01)

        new_gen.append( (ex, ey, ez) ) #Create new list with new slightly varied params

    return new_gen #Returns to replace current generated solutions to try again in the next gen


generated_solutions = []
solutions_count_to_generate = 5000
lower_bound = 0
upper_bound = 10000
for w in range(solutions_count_to_generate): #Generates the initial sample sets of solutions
    generated_solutions.append( (random.uniform(lower_bound, upper_bound), random.uniform(lower_bound, upper_bound), random.uniform(lower_bound, upper_bound)) )


for i in range(5000): #Runs x amount of generations
    ranked_solutions = []
    for s in generated_solutions: #Simulates fitness for all generated solutions
        ranked_solutions.append( (fitness(s[0], s[1], s[2]), s) )
    
    ranked_solutions.sort(reverse=True) #Sorts them from highest fitness to lowest

    print(f"Gen {i}")
    print(ranked_solutions[0])

    if ranked_solutions[0][0] > 99999: #If close enough, break
        break

    generated_solutions = mutation(ranked_solutions) #Creates variance within the pool of the current best solutions, calculated using fitness