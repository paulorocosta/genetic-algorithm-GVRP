import random

def CostCalculation(tour,cost_matrix):
    """
    FUNCTION: CostCalculation
     
    DESCRIPTION:  This fuction calculates the total cost of a route and returns its cost
    
    INPUT: (tour)        - List containing the sequence of nodes visited
           (cost_matrix) - Cost matrix (full) with the associated cost of moving from node i to node j 
    
    OUTPUT: (tour_cost)  - Total cost of the input tour.
    """    
    tour_cost = 0
    for i in range(len(tour)-1):
        node_i = tour[i]
        node_j = tour[i+1]          
        tour_cost = tour_cost + cost_matrix[node_i][node_j]  
    return tour_cost


def SwapThree(tour,a,c,e,choose):
    """
    FUNCTION: SwapThree
     
    DESCRIPTION:  This fuction recreates a route by disconnecting and reconnecting 3 edges ab, cd
    and ef (such that the result is still a complete and feasible tour).
    This function only takes into account pure 3-opt moves. No 2-opt moves are allowed. 
    
    INPUT: (tour)        - List containing the sequence of nodes visited
           (a)           - Position of the first node in the list
           (c)           - Position of the second node in the list
           (e)           - Position of the third node in the list     
    
    OUTPUT: (tour_cost)  - Total cost of the input tour.
    """    
    # nodes are sorted to allow a simpler implementation
    a, c, e = sorted([a, c, e])
    b, d, f = a+1, c+1, e+1
    
    new_tour = list()
    # four different reconnections of tours are considered
    if choose == 1:
        new_tour = tour[:a+1] + tour[c:b-1:-1] + tour[e:d-1:-1] + tour[f:] # 3-opt
    elif choose == 2:
        new_tour = tour[:a+1] + tour[d:e+1]    + tour[b:c+1]    + tour[f:] # 3-opt
    elif choose == 3:
        new_tour = tour[:a+1] + tour[d:e+1]    + tour[c:b-1:-1] + tour[f:] # 3-opt
    elif choose == 4:
        new_tour = tour[:a+1] + tour[e:d-1:-1] + tour[b:c+1]    + tour[f:] # 3-opt

    return new_tour


def ThreeOpt(tour, cost_matrix):
    """
    FUNCTION: ThreeOpt
     
    DESCRIPTION:  This function applies the 3-opt algorithm to find a new tour with a lower cost than the input tour. 
    The algorithm scans all nodes a,c,e and swaps three edges connecting the current tour. All four different reconnections of the three edges are attempted and the algorithm is stopped at the first improvement. 
    If an iprovement is found the tour is swapped and the new tour is used in the evaluation of further improvements. 
    The algorithm stops when no further improvement can be found by swapping three edges considering one of the 4 possibilities.
    
    INPUT: (tour)      - List containing the sequence of nodes visited
           (cost_matrix) - Cost matrix (full) with the associated cost of moving from node i to node j 
    
    OUTPUT: (tour) - New tour recreated.
    """ 
    
    size = len(tour) #length of the tour
    which  = random.choice([1,2,3,4]) #One of all four possibilities of reconnecting the tour are tested

    best_cost = CostCalculation(tour,cost_matrix)

    improve = 0
    while(improve <= 0):        
        for a in range(1,size-2):
            for c in range(a+1,size-1):
                for e in range(c+1,size):
                        new_tour = SwapThree(tour,a,c,e,which) 
                        new_cost = CostCalculation(new_tour,cost_matrix)
                        if (new_cost < best_cost):
                            tour = new_tour
                            best_cost = new_cost
                            improve = 0
            
        improve += 1
    return tour
    

def ThreeOptFast(tour,dist):
    """
    FUNCTION: ThreeOpt
     
    DESCRIPTION:  This function applies the 3-opt algorithm to find a new tour with a lower cost than the input tour. 
    The algorithm scans all nodes a,c,e and swaps three edges connecting the current tour. All four different reconnections of the three edges are attempted and the algorithm is stopped at the first improvement. 
    If an iprovement is found the tour is swapped and the new tour is used in the evaluation of further improvements. 
    The algorithm stops when no further improvement can be found by swapping three edges considering one of the 4 possibilities.
    
    INPUT: (tour)      - List containing the sequence of nodes visited
           (dist) - Cost matrix (full) with the associated cost of moving from node i to node j 
    
    OUTPUT: (tour) - New tour recreated.
    """
    size = len(tour) #length of the tour
    tour_cost = CostCalculation(tour,dist)
    a = random.randint(0,size-4)
    print "3 opt starting at", a
    while True: 
        minchange = 0
        for i in range(a,size-3):
            for j in range(i+2,size-2):
                for k in range(j+2,size-1):

                     change_1 = dist[tour[i]][tour[j]] + dist[tour[i+1]][tour[k]] + dist[tour[j+1]][tour[k+1]] - dist[tour[i]][tour[i+1]] - dist[tour[j]][tour[j+1]] - dist[tour[k]][tour[k+1]]
                     change_2 = dist[tour[i]][tour[j+1]] + dist[tour[k]][tour[i+1]] + dist[tour[j]][tour[k+1]] - dist[tour[i]][tour[i+1]] - dist[tour[j]][tour[j+1]] -  dist[tour[k]][tour[k+1]]
                     change_3 = dist[tour[i]][tour[j+1]] + dist[tour[j]][tour[k]] + dist[tour[i+1]][tour[k+1]] - dist[tour[i]][tour[i+1]] - dist[tour[j]][tour[j+1]] -  dist[tour[k]][tour[k+1]] 
                     change_4 = dist[tour[i]][tour[k]] + dist[tour[j+1]][tour[i+1]] + dist[tour[j]][tour[k+1]] - dist[tour[i]][tour[i+1]] - dist[tour[j]][tour[j+1]] -  dist[tour[k]][tour[k+1]]
                     best_move = min(change_1,change_2,change_3,change_4)
                     change = best_move
                     if best_move == change_1:
                         which = 1
                     elif best_move == change_2:
                         which = 2
                     elif best_move == change_3:
                         which = 3
                     else:
                         which = 4                         
                     if minchange > round(change,2):

                         minchange = change
                         
                         mini = i
                         minj = j
                         mink = k
                         move = which
        if (minchange >= 0): break              
        tour = SwapThree(tour, mini,minj,mink,move)
        tour_cost = tour_cost + minchange
    return tour,tour_cost
    