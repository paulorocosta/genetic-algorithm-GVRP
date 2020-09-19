import random
import numpy as np
import time as tm
import matplotlib.pyplot as plt
import constheur as const
import math
import bisect
opt2 = __import__('2opt')
opt3 = __import__('3opt')



def FirstTourCreation(cost_matrix):
    """
    FUNCTION: FirstTourCreation
     
    DESCRIPTION:  This function creates initial solutions for the TSP. Random solutions are created.
    
    Random Solutions: Solutions selected randomly are formed by a permutation of the client's nodes appending the depot (0) at first and last positions.
   
    INPUT: (cost_matrix) - Cost matrix (full) with the associated cost of moving from node i to node j. 
  
    OUTPUT: (tour)       - List containing the TSP tour.
    """     
        
    random_walk = list()
    random_walk = range(1,len(cost_matrix))
    random.shuffle(random_walk)
    

    tour = [0]+random_walk+[0]    
    
    
    return tour

def CostCalculation(tour,cost_matrix):
    """
    FUNCTION: CostCalculation
     
    DESCRIPTION:  This function calculates the total cost of a route and returns its cost
    
    INPUT: (tour)    - List containing the sequence of nodes visited
           (cost_matrix) - Cost matrix (full) with the associated cost of moving from node i to node j 
    
    OUTPUT: (tour_cost)      - Total cost of the input tour.
    """    
    tour_cost = 0
    for i in range(len(tour)-1):
        node_i = tour[i]
        node_j = tour[i+1]          
        tour_cost = tour_cost + cost_matrix[node_i][node_j]  
    return round(tour_cost,2)


def Fitness(cost,scale = 1.0e4):
    """
    FUNCTION: Fitness
     
    DESCRIPTION:  This function calculates the tour fitness. In this case the tour fitness is defined as the tour cost
    
    INPUT: (cost)  - Cost of the tour
           (scale) - Scale factor
    
    OUTPUT: (fitness) - Total fitness of the input tour.
    """      

    return round(cost,2)

def GetFittest(population):
    """
    FUNCTION: GetFittest     
    
    DESCRIPTION:  This function returns the fittest given a population 
    
    INPUT: (population)  - Current population
           
    OUTPUT: First postion in the population
    """   
    return population[0]


    
def GetPopulationSize(population):
    """
    FUNCTION: GetPopulationSize     
    
    DESCRIPTION:  This function returns the size given a population 
    
    INPUT: (population)  - Current population
           
    OUTPUT: Size of the population
    """ 
    return len(population)


    

def BiContains(pop, item):
    """
    FUNCTION: BiContains     
    
    DESCRIPTION:  Bisection to find an item in  a list. 
    
    INPUT: (pop)  - Current population
           (item) - Lookup item
           
    OUTPUT: True - If item in pop. False - Otherwise
    """
    fit, tour,cost = zip(*pop)
    index = bisect.bisect_left(cost, item)
    return (item <= cost[-1]) and (cost[index] == item)
 
 
 
def InitialPopulation(n,cost_matrix):
    """
    FUNCTION: InitialPopulation    
    
    DESCRIPTION:  This function creates a list of N members to form a population 
    
    INPUT: (n)           - Number of individuals required in the initial population
           (cost_matrix) - Cost matrix (full) with the associated cost of moving from node i to node j.
        
           
    OUTPUT: (sorted(pop)) - Sorted population by Fitness value
    """ 
    pop = list()
    #Clarke and Wright 
    tour_cw = const.ClarkeWright(cost_matrix)
#    print len(tour_cw)
    cost_cw = CostCalculation(tour_cw,cost_matrix)
    fitness_cw = Fitness(cost_cw)
    pop.append((fitness_cw,tour_cw,cost_cw))
    
    #Nearest Neighbour
    tour_nn = const.NN(cost_matrix)
#    print len(tour_nn)
    cost_nn = CostCalculation(tour_nn,cost_matrix)
    fitness_nn = Fitness(cost_nn)
    if fitness_nn != fitness_cw:      
        pop.append((fitness_nn,tour_nn,cost_nn))
    
    #Random Insertion
    tour_ri = const.RandomInsertion(cost_matrix)
#    print len(tour_ri)
    cost_ri = CostCalculation(tour_ri,cost_matrix)
    fitness_ri =  Fitness(cost_ri)
    if fitness_ri != fitness_cw and fitness_ri != fitness_nn: 
        pop.append((fitness_ri,tour_ri,cost_ri))
    
    pop = sorted(pop)
    
    i = 3
    count = 0
  
    while (i < n):
        tour = FirstTourCreation(cost_matrix)
        cost = CostCalculation(tour,cost_matrix)
        fitness = Fitness(cost)
        
        insert = 1
        if len(pop) != 0:
            if (BiContains(pop,cost)):
                insert = 0
                
        if insert == 1:
            pop.append((fitness,tour,cost))
            i = i+1
        
        count = count + 1
        if count >= 4*n:
            raise ValueError("Could not form the entire population!")
    
    pop = sorted(pop)      
    return pop 


def Rotate(l,n):
    """
    FUNCTION: Rotate   
    
    DESCRIPTION:  This function rotates a list given a new start position.
    
    INPUT: (l)  - List containing a TSP tour
           (n)  - New position of the first element 
        
           
    OUTPUT: Rotated list
    """ 
    return l[-n:] + l[:-n]

def OXCrossover(parent_1,parent_2):
    """
    FUNCTION: OXCrossover   
    
    DESCRIPTION:  This function performs an ordered crossover between two tours.
    First, a random slice is swapped between the two tours, as in a two-point crossover. Second, repeated cities
    not in the swapped area are removed, and the remaining integers are added
    from the other tour, in the order that they appear starting from the end
    index of the swapped section.
    
    INPUT: (parent_1)  - List containing a TSP tour
           (parent_2)  - List containing a TSP tour 
        
           
    OUTPUT: (child_1,child_2) - Two offsprings generated by the input parents
    """ 
     
    parent_1 = list(parent_1[1:-1])
    parent_2 = list(parent_2[1:-1])
       
    n =  len(parent_1)
 

    start = random.randint(0,n-1)
    end   = random.randint(start+1,n)
    
    child_1 = list()
    child_2 = list()
    
    
    child_1[start:end] =  parent_1[start:end]
    child_2[start:end] =  parent_2[start:end]
    
     
     
    for i in range(0,n):
        current_index = (end + i) % n

        current_node_parent_1 = parent_1[current_index]
        current_node_parent_2 = parent_2[current_index]
      
        if current_node_parent_2 not in child_1:
            child_1.append(current_node_parent_2)
      
        if current_node_parent_1 not in child_2:
            child_2.append(current_node_parent_1)
            
    child_1 = Rotate(child_1,start)
    child_2 = Rotate(child_2,start)
    
    child_1 = [0]+child_1+[0]
    child_2 = [0]+child_2+[0]
    return child_1,child_2        
    
def SelectParent(pop):
    """
    FUNCTION: SelectParent   
    
    DESCRIPTION:  This function performs the parent selection, given a population.
    Parents are selected randomly.
    
    INPUT: (pop)  - Population of the Genetic Algortihm
           
    OUTPUT: ([fit,tour,cost]) - An entry o the GA population containing the fitness, tour and cost
    """ 
    index = random.choice(range(0,len(pop)))       
    return pop[index]
    

            
 
def Mutation(child,child_cost,cost_matrix):
    """
    FUNCTION: Mutation   
    
    DESCRIPTION:  This function performs the mutation in the GA. Mutation is performed by firt attempting a LS move. 
    a 3-opt move is attempted with probability (p).
    
    INPUT: (child)  - TSP tour
           (child_cost) - cost of the TSP tour
           (cost_matrix)  - Cost matrix (full) with the associated cost of moving from node i to node j.
           
    OUTPUT: (mutation) - An entry o the GA population containing the  tour
            (mutation_cost) - An entry o the GA population containing the cost
    """ 

        
    mutation,mutation_cost = opt2.LSFast(child,child_cost,cost_matrix)   

    r = random.uniform(0,1)
    if r < 0.5:
        mutation,mutation_cost = opt3.ThreeOptFast(mutation,cost_matrix)
        
    return mutation,mutation_cost 

def GA(cost_matrix,population_size, population, mutation_rate, number_success, number_unsuccess ):
    """
    FUNCTION: GA   
    
    DESCRIPTION:  This function performs the Genetic Algorithm. 
    The algorithm selects two parents and generates two offsprings (children) using the OX crossover procedure. 
    The child is selected and mutation can happen with probability = mutation rate. 
    The new child is added to the new population if there is no copies present in the population (to maintain variability).
    Thealgorithm stops when the entire population success or no_improve their max.
    
    INPUT: (cost_matrix)  - Cost matrix (full) with the associated cost of moving from node i to node j.
           (population_size)  - Size of the desired population
           (population) - current population
           (mutation_rate) - Probability of having a mutation in the best offspring
           (number_success)  - max number of sucessful offspring
           (number_unsuccess)  - max number of unsucessful offspring
           
           
    OUTPUT: (population) - A GA population containing fitness, tour and cost for al ts members.
    """   
    
    success = 0
    no_improve = 0
    while (success < number_success and no_improve < number_unsuccess):
        current_best = population[0]
        parent_1_candidate_1 = SelectParent(population)
        parent_1_candidate_2 = SelectParent(population)
        
        
        if parent_1_candidate_1[2] < parent_1_candidate_2[2]:
            parent_1 = parent_1_candidate_1[1]
            
        else:    
            parent_1 = parent_1_candidate_2[1]
            
        parent_2_candidate_1 = SelectParent(population)
        parent_2_candidate_2 = SelectParent(population)
        
        
        if parent_2_candidate_1[2] < parent_2_candidate_2[2]:
            parent_2 = parent_2_candidate_1[1]
        else:    
            parent_2 = parent_2_candidate_2[1]

        
    
        child_1,child_2 = OXCrossover(parent_1,parent_2)
        
        which_child = random.choice([1,2])
        
        if which_child == 1 :
            child = list(child_1)
        else:
            child = list(child_2)

        rand = random.uniform(0, 1) 
        
        child_cost = CostCalculation(child,cost_matrix)
        if  rand < mutation_rate:
            child,child_cost = Mutation(child,child_cost,cost_matrix)
        
        child_fitness = Fitness(child_cost)            

        k = random.randint(math.floor(population_size/2.0),population_size-1)

        add = 1
        if BiContains(population,child_cost):
            add = 0

        if add == 1 and child_cost < population[k][2] :
            population[k] =  (child_fitness,child,child_cost)
            success = success + 1

        population = sorted(population)
        if population[0] == current_best:
            no_improve += 1
#            print no_improve

    print "number of success....", success
    print "no improvement....", no_improve

    return population    


def PrintResults(matrix,fittest,solutions,time,plot = True):
    """
    FUNCTION: PrintResults   
    
    DESCRIPTION:  This function prints the results of the GA.
    
    INPUT: (matrix)  - Cost matrix (full) with the associated cost of moving from node i to node j.
           (fittest)  - [fit,tour,cost] of the best solution found
           (solutions) - list with solutionf at each generation
           (time)  - Running time of the algorithm
           (plot) - Boolean to define show a graph of the solution's evolution
           
    OUTPUT: None.
    """  
    print "The TSP has",len(matrix), "nodes, including the depot (0) and", len(matrix)-1,"clients." 
    print "The first population's best solution was:",solutions[0]
    print "The algorithm took ",round(time,2),"(s) to run." 
    print "It has generated", len(solutions), "restarts."
    print "The best tour found is", fittest[1]
    print "The best cost found is", fittest[2]
    
    if plot:
        print "\n"        
        print "Solution Value x Restart"
        plt.plot(solutions)
        plt.show()
        plt.close()




def ImproveGA(pop,cost_matrix):
    """
    FUNCTION: ImproveGA   
    Every time the GA is restarted this function is called to improve some of its solutions. 
    The function attempts to create 8 new solutions  and checks for each one of them if they are better then the worst solution.
    If so, include the solution. If not, we crossover with the entire population until we find a solution to substitue.
    
    DESCRIPTION:     
    INPUT: (cost_matrix)  - Cost matrix (full) with the associated cost of moving from node i to node j.
           
           (pop) - current population

           
           
    OUTPUT: (new_pop) - A GA population containing fitness, tour and cost for al ts members.
    """   

    new_tours = [] 
    for i in range(0,8):
        tour = FirstTourCreation(cost_matrix)
        cost = CostCalculation(tour,cost_matrix)
        fitness = Fitness(cost)
        new_tours.append((fitness,tour,cost))
    new_tours = sorted(new_tours)

    new_pop = list(pop)
    
    for fit,tour,cost in new_tours:
        worst = new_pop[-1]
        if cost <  worst[2] and BiContains(new_pop,cost) == False:
            new_pop[-1] = (fit,tour,cost)
            
            new_pop = sorted(new_pop)
            
        else:
            for pop_fit,pop_tour,pop_cost in new_pop:
                
                child_1,child_2 = OXCrossover(tour,pop_tour)
                child_1_cost = CostCalculation(child_1,cost_matrix)
                child_2_cost = CostCalculation(child_2,cost_matrix)
                if  child_1_cost < child_2_cost:
                    
                    child = child_1
                    child_cost = child_1_cost
                else:
                    child = child_2
                    child_cost = child_2_cost
                if (child_cost < worst[2] and BiContains(new_pop,child_cost) == False):
                    new_pop[-1] = (Fitness(child_cost),child,child_cost)
                    new_pop = sorted(new_pop)
                    break
                    
    return new_pop        
                
                
    
        
    
        
def main(matrix,pop_size,num_of_restarts = 5, max_restart_no_improvement = 5,mutation_rate = 0.005, num_of_success = 500,number_of_unsuccess = 250,show= True ):
    """
    FUNCTION: main   
    
    DESCRIPTION:  This function runs the Genetic Algorithm. The GA needs a set o parameters to be initiated.
    The cost_matrix, the population size, the number of generations, the maximum number of generations where no improvement is seen, 
    mutation rate, elitism and printing the solution. The algorithm first generates an initail population. Sobsequeten populations are generated 
    until the maximum number of generations or the maximum number of generations with no improvements is reached. The best solutions of each generations are saved. 
    
    INPUT: (matrix)  - Cost matrix (full) with the associated cost of moving from node i to node j.
           (pop_size)  - Number of distinct individual in each population
           (num_of_restarts) - Max. number of restarts (default = 5)
           (max_restart_no_improvement)  - Max. number of restarts with no improvemnt (default = 5). 
           (mutation_rate) - Probability of having a mutation in the best offspring
           (number_success)  - max number of sucessful offspring
           (number_unsuccess)  - max number of unsucessful offspring
          

           (show)  - Boolean that prints the results on the screen
    OUTPUT: None.
    """  
    time_start = tm.time()
    

            
    best_solution = []
    
    pop = InitialPopulation(pop_size,matrix)
    best_solution.append(GetFittest(pop)[2])
    print "Population: 0 created" 

    
    count_no_improve = 0
    for i in range(1,num_of_restarts+1):
        print "GA run: ",i, "created"
        if i > 1:
            pop = ImproveGA(pop,matrix)
        pop = GA(matrix,pop_size,pop,mutation_rate,num_of_success,number_of_unsuccess)

        best_solution.append(GetFittest(pop)[2])
        
        if best_solution[i] == best_solution[i-1]:
            count_no_improve += 1
        else:
            count_no_improve = 0
            
        if  count_no_improve == max_restart_no_improvement:
            break   
        
    time_finish = tm.time()
    total_time  =  time_finish - time_start
    if show:
        PrintResults(matrix,GetFittest(pop),best_solution,total_time)
        
    return GetFittest(pop),total_time


        
def GenerateMatrix(a_text_file = False, a_matrix = False):
    """
    FUNCTION: GenerateMatrix   
    
    DESCRIPTION:  This function transforms a np.array matrix in a list. 
    
    INPUT: (a_text_file)  - Text file cost matrix (full) with the associated cost of moving from node i to node j.
           (a_matrix)     - Python cost matrix (full) with the associated cost of moving from node i to node j.
    OUTPUT: None.
    """  
    
    if a_text_file:
        matrix  = np.genfromtxt(a_text_file, dtype='float64')
        mean = np.nanmean(matrix)
        matrix[np.isnan(matrix)] = mean
        matrix = matrix.tolist()
        for i in range(0,len(matrix)):
            for j in range(0,len(matrix)):
                matrix[i][j] = round(matrix[i][j],2) 
        return matrix
    
    else:
        matrix  = a_matrix
        mean = np.nanmean(matrix)
        matrix[np.isnan(matrix)] = mean
        matrix = matrix.tolist()
        for i in range(0,len(matrix)):
            for j in range(0,len(matrix)):
                matrix[i][j] = round(matrix[i][j],2) 

    
        return matrix

    