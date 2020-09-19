
def CostCalculation(tour,cost_matrix):
    """
    FUNCTION: CostCalculation
     
    DESCRIPTION:  This fuction calculates the total cost of a route and returns its cost
    
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
    
def SwapTwo(tour,i,k):
    """
    FUNCTION: SwapTwo
     
    DESCRIPTION:  This fuction recreates a tour swaping nodes in positions i and k. 
    The functions breaks the tour in the position i-1, reconnects the position i-1 with position k and inverts the central tour to reconnect position i with k+1.  
    
    INPUT: (tour)      - List containing the sequence of nodes visited
           (i)         - Position of the first node in the list
           (k)         - Position of the second node in the list 
               
           
           
    OUTPUT: (new_tour)   - New tour recreated.
    """ 
    
    first_route = tour[0:i]
    second_route = tour[i:k+1][::-1]
    third_route = tour[k+1:] 
    new_tour = list()
    new_tour = first_route + second_route + third_route
            
    return new_tour

def TwoOpt(tour, cost_matrix):
    """
    FUNCTION: TwoOpt
     
    DESCRIPTION:  This function applies the 2-opt algorithm to find a new tour with a lower cost than the input tour. 
    The algorithm scans all nodes i,j and swaps two edges connecting the current tour. If an iprovement is found the tour is swapped 
    and the new tour is returned to be evaluated for further improvements. The algorithms stops when no further improvement can be found by swapping two edges.
    
    INPUT: (tour)      - List containing the sequence of nodes visited
           (cost_matrix) - Cost matrix (full) with the associated cost of moving from node i to node j 
    
    OUTPUT: (tour) - New tour recreated.
    """    
    tour = tour[1:-1]
    size = len(tour) #length of the tour
    best_cost = CostCalculation([0]+tour+[0],cost_matrix)
    improve = 0 #auxiliary variable that stops the algorithm if no improvement is found
    while(improve <= 1):
        
        for i in range(0,size-1): # the depot (0) is not considered for swapping

            for k in range(i+1,size): # the depot (0) is not considered for swapping
                new_tour = SwapTwo(tour,i,k)   
                new_cost = CostCalculation([0]+new_tour+[0],cost_matrix)
                if (new_cost < best_cost):

                    tour = new_tour
                    best_cost = new_cost
                    improve = 0  

            
        improve += 1
    return [0]+ tour +[0]
    
    
def SwapTwoFast(tour,i,k):
    """
    FUNCTION: SwapTwo
     
    DESCRIPTION:  This fuction recreates a tour swaping nodes in positions i and k. 
    The functions breaks the tour in the position i-1, reconnects the position i-1 with position k and inverts the central tour to reconnect position i with k+1.  
    
    INPUT: (tour)      - List containing the sequence of nodes visited
           (i)         - Position of the first node in the list
           (k)         - Position of the second node in the list 
               
           
           
    OUTPUT: (new_tour)   - New tour recreated.
    """ 
    
    first_route = tour[0:i+1]
    second_route = tour[i+1:k+1][::-1]
    third_route = tour[k+1:] 
    new_tour = list()
    new_tour = first_route + second_route + third_route
            
    return new_tour


    
def TwoOptFast(tour,dist):
    size = len(tour) #length of the tour
    while True: 
        minchange = 0
        for i in range(0,size-2):
            for j in range(i+2,size-1):
                 change = dist[tour[i]][tour[j]] + dist[tour[i+1]][tour[j+1]]- dist[tour[i]][tour[i+1]] - dist[tour[j]][tour[j+1]]
                 
                 if minchange > change:
                     
                     
                     minchange = change
                     mini = i
                     minj = j
        if (minchange >= 0): break              
        tour = SwapTwoFast(tour, mini,minj)
                
    return tour,CostCalculation(tour,dist)


def LSFast(tour,tour_cost,cost_matrix):
#    print "LS"
    size = len(tour) #length of the tour
    
    while (True):
        minchange = 0
        for i in range(1,size-1):
            for j in range(i+1,size-1): 
                
                change_M1 = 0
                change_M2 = 0
                change_M3 = 0
                change_M4 = 0
                change_M5 = 0
                change_M6 = 0
                change_M7 = 0
                                
                change_M1 = cost_matrix[tour[i-1]][tour[i+1]] + cost_matrix[tour[j]][tour[i]] + cost_matrix[tour[i]][tour[j+1]] - cost_matrix[tour[j]][tour[j+1]] - cost_matrix[tour[i]][tour[i+1]] - cost_matrix[tour[i-1]][tour[i]]     
        
         
                if j >= i+2:
                   change_M2 = cost_matrix[tour[i-1]][tour[i+2]] + cost_matrix[tour[j]][tour[i]] + cost_matrix[tour[j+1]][tour[i+1]] - cost_matrix[tour[i+1]][tour[i+2]] - cost_matrix[tour[i-1]][tour[i]] - cost_matrix[tour[j]][tour[j+1]]

        
                if j >= i+2:
                    change_M3 = cost_matrix[tour[i-1]][tour[i+2]] + cost_matrix[tour[j]][tour[i+1]] + cost_matrix[tour[j+1]][tour[i]] - cost_matrix[tour[i+1]][tour[i+2]] - cost_matrix[tour[i-1]][tour[i]] - cost_matrix[tour[j]][tour[j+1]]
                
                if i+1 != j:
                   enter_M4 = cost_matrix[tour[i-1]][tour[j]] + cost_matrix[tour[j]][tour[i+1]] + cost_matrix[tour[j-1]][tour[i]]  + cost_matrix[tour[i]][tour[j+1]]           
                   leave_M4 = cost_matrix[tour[i-1]][tour[i]] + cost_matrix[tour[i]][tour[i+1]] +cost_matrix[tour[j]][tour[j+1]]+cost_matrix[tour[j-1]][tour[j]]
                   change_M4 = enter_M4 - leave_M4
                else:
                   enter_M4 = cost_matrix[tour[i-1]][tour[j]]  + cost_matrix[tour[i]][tour[j+1]]
                   leave_M4 = cost_matrix[tour[i-1]][tour[i]] +  cost_matrix[tour[j]][tour[j+1]]
                   change_M4 = enter_M4 - leave_M4
                if  j > i+1:
                   if j == i+2:
                       enter_M5 = cost_matrix[tour[i-1]][tour[j]] + cost_matrix[tour[j]][tour[i]] + cost_matrix[tour[i+1]][tour[j+1]]             
                       leave_M5 = cost_matrix[tour[i-1]][tour[i]] + cost_matrix[tour[i+1]][tour[i+2]] +cost_matrix[tour[j]][tour[j+1]]
                       change_M5 = enter_M5 - leave_M5
                   else:
                       enter_M5 = cost_matrix[tour[i-1]][tour[j]] + cost_matrix[tour[j]][tour[i+2]] + cost_matrix[tour[j-1]][tour[i]]  + cost_matrix[tour[i+1]][tour[j+1]]           
                       leave_M5 = cost_matrix[tour[i-1]][tour[i]] + cost_matrix[tour[i+1]][tour[i+2]] +cost_matrix[tour[j]][tour[j+1]]+cost_matrix[tour[j-1]][tour[j]]
                       change_M5 = enter_M5 - leave_M5
                       
                if j < size-2 and j >= i+2:                   
                   if  j == i+2:
                       enter_M6 = cost_matrix[tour[j+1]][tour[i]] +  cost_matrix[tour[i+1]][tour[j+2]]+ cost_matrix[tour[i-1]][tour[j]]     
                       leave_M6 = cost_matrix[tour[i-1]][tour[i]] + cost_matrix[tour[i+1]][tour[i+2]]+cost_matrix[tour[j+1]][tour[j+2]]
                       change_M6 = enter_M6 - leave_M6
                   else:           
                       enter_M6 = cost_matrix[tour[i-1]][tour[j]] +cost_matrix[tour[j+1]][tour[i+2]] + cost_matrix[tour[j-1]][tour[i]] + cost_matrix[tour[i+1]][tour[j+2]] 
                       leave_M6 = cost_matrix[tour[i-1]][tour[i]] + cost_matrix[tour[i+1]][tour[i+2]] + cost_matrix[tour[j-1]][tour[j]] + cost_matrix[tour[j+1]][tour[j+2]]
                       change_M6 = enter_M6 - leave_M6
                
                change_M7 = cost_matrix[tour[i]][tour[j]] + cost_matrix[tour[i+1]][tour[j+1]]- cost_matrix[tour[i]][tour[i+1]] - cost_matrix[tour[j]][tour[j+1]]
        
                change = min(change_M1,change_M2,change_M3,change_M4,change_M5,change_M6,change_M7)
                
                if change == change_M1:
                    t = 1
                elif change == change_M2:
                    t = 2
                elif change == change_M3:
                    t = 3
                elif change == change_M4:
                    t = 4
                elif change == change_M5:
                    t = 5
                elif change == change_M6:
                    t = 6
                elif change == change_M7:
                    t = 7
         
                if minchange > round(change,2):
#                    print "pure:",change
#                    print "round:",round(change,2)
                    minchange = change
                    mini = i
                    minj = j
                    mint = t
                  
                    
        if (minchange >= 0): break         
        if mint == 1:
            new_tour = tour[:mini] + tour[mini+1:minj+1] +[tour[mini]]+ tour[minj+1:]
            tour = new_tour
        elif mint == 2:
            new_tour = tour[:mini] +tour[mini+2:minj+1]+[tour[mini],tour[mini+1]]+ tour[minj+1:]
            tour = new_tour
        elif mint == 3:
            new_tour = tour[:mini] +tour[mini+2:minj+1]+[tour[mini+1],tour[mini]]+ tour[minj+1:]
            tour = new_tour    
        elif mint == 4:
            new_tour = list(tour)
            aux = new_tour[mini]
            new_tour[mini] = new_tour[minj]
            new_tour[minj] = aux
            
            tour = new_tour
        elif mint == 5:
            new_tour = tour[:mini]+[tour[minj]]+ tour[mini+2:minj]+tour[mini:mini+2]+tour[minj+1:]
            tour = new_tour
        elif mint == 6:
            new_tour = list(tour)
            aux = new_tour[mini]
            new_tour[mini] = new_tour[minj]
            new_tour[minj] = aux
                                    
            aux = new_tour[mini+1]
            new_tour[mini+1] = new_tour[minj+1]
            new_tour[minj+1] = aux
            
            tour = new_tour
                
        elif mint == 7:
            new_tour = SwapTwoFast(tour,mini,minj)
            tour = new_tour
        tour_cost = tour_cost + minchange
#    print "LS Done"        
    return tour,tour_cost   
