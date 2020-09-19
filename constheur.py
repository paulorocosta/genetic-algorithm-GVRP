import random
import numpy as np
import networkx as nx

def NN(A):
    """Nearest neighbor algorithm.
    A is an NxN array indicating distance between N locations
    start is the index of the starting location
    Returns the path and cost of the found solution
    """
    A = np.array(A)
    path = [0]
    cost = 0
    N = A.shape[0]
    mask = np.ones(N, dtype=bool)  # boolean values indicating which 
                                   # locations have not been visited
    mask[0] = False

    for i in range(N-1):
        last = path[-1]
        next_ind = np.argmin(A[last][mask]) # find minimum of remaining locations
        next_loc = np.arange(N)[mask][next_ind] # convert to original location
        path.append(next_loc)
        mask[next_loc] = False
        cost += A[last, next_loc]
        

    return path+[0]

def InsertionCost(matrix,i,k,j):
    return matrix[i][k] + matrix[k][j] - matrix[i][j]
    
def RandomInsertion(matrix):
    n = len(matrix)
    nodes = set(range(0,n))
    
    start_node = random.randint(1,n-1)
    tour =[0,start_node,0]
    
    while (len(tour) < n+1):
        best_cost = np.Inf
        tour_set  = set(tour)
        remaining_nodes = nodes - tour_set
        k = random.choice(list(remaining_nodes))

        for i in range(0,len(tour)-1):
                j=i+1
                
                cost = InsertionCost(matrix,tour[i],k,tour[j])
                if cost < best_cost:
                    best_cost = cost
                    start = i
                    end = j
        tour = tour[:start+1]+[k]+tour[end:]        
    return tour       
    
def ClarkeWright(matrix):
    n = len(matrix)
#    print "size", n
    depot = 0
    
    tours = [] 
    for node in range(1,n):
        tours.append([node,depot,node])
#    print "tours", tours  
    savings=[]
    
    for i in range(0,n-1):
        for j in range(i+1,n):
                saving = matrix[0][i] + matrix[0][j] - matrix[i][j]
                savings.append((saving,i,j))
                     
    savings = sorted(savings,reverse=True)           
#    print savings           
    new_tour =[]
    while True:
        for save,i,j in savings:
            if new_tour == []:
                tour_1 = tours[i-1]
                tour_2 = tours[j-1]
                new_tour = tour_1[1:]+tour_2[:-1]
                
#                print new_tour
            elif new_tour[-2] == j and i not in new_tour:
                 new_tour = new_tour[:-1]+tours[i-1][:-1]
#                 print new_tour
            elif new_tour[1] == j and i not in new_tour:
                 new_tour = tours[i-1][1:]+new_tour[1:]         
#                 print new_tour
            elif new_tour[-2] == i and j not in new_tour:
                 new_tour = new_tour[:-1]+tours[j-1][:-1]
#                 print new_tour
            elif new_tour[1] == i and j not in new_tour:
                 new_tour = tours[j-1][1:]+new_tour[1:]
#                 print new_tour
        if len(new_tour) >= n+1:break        
#    print len(new_tour) 
#    print len(set(new_tour))            
    return new_tour
    
def MSTPreOrder(matrix):    
    numpy_matrix = np.array(matrix)
    G = nx.from_numpy_matrix(numpy_matrix)
    T = nx.minimum_spanning_tree(G) 
    return list(nx.dfs_preorder_nodes(T,0))+[0]     