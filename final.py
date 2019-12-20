# @Oleg Puchkov
import sys 
import os
import Queue as queue
import heapq as heap
import math 

from random import shuffle

class Puzzle: 
    def __init__(self, arr, algorithm):
        self.goal    = [1,2,3,8,0,4,7,6,5]
        self.state   = State(arr)
        self.initial = State(arr)
        self.isDone  = False
        self.algorithm = algorithm # UC - Uniform Cost, BFS - Best-First Search, A1, A2.
    
    def printBoard (self, arr):
        # output = [[0]* 3]*3
        # x = 0
        temp = []
        for i in range(0,10):
            if i % 3 == 0 and i != 0: 
                print(temp)
                temp = []
            if i < 9:     
                temp.append(arr[i])

    # builds path of moves back to the root once the element has been found
    def buildPathAction (self, end):
        path = []
        state = end
        while state.parent:
            path.append(state.action)
            state = state.parent
        path = path[::-1]
        path.append("")
        return path 

    # builds path of states back to the root once the element has been found
    def buildPath (self, end):
        path = []
        state = end
        while state.parent:
            path.append(state.arr)
            state = state.parent
        path.append(self.initial.arr)
        return path[::-1]
    ''' --------------------------------------------------------------------------------------------------
     solve() just creates minHeap and calls solveAUX on intial state where heap contains it.
     solveAUX() keeps track of visited and basically it just loops through while heap is not empty and 
     checks if the poped element of the heap is a goal and if not then it creates successors for it 
     --------------------------------------------------------------------------------------------------'''
    def solve (self):
        h = []
        heap.heappush(h, (0, self.state))  # adding initial state on the heap
        heap.heapify(h)                    # creating the heap 
        self.solveAUX(h)                   # calling helper function where heap contains inital state

    def solveAUX (self, h):
        visited = []                       # declaring visited arr and count 
        count = 0
        cost = 0
        while h != None:                   # we will pop everything from the heap until it is empty or until we find goal 
            state = heap.heappop(h)        # poping off a state that has min comparison. Comparison changes depending on heuristic 
            cost = cost + state [0]
            state = state[1] 
            if (state.arr == self.goal):   # goal check
                pathAction = self.buildPathAction(state) #building paths in order to show the output 
                path = self.buildPath(state)
                
                print("The exact path and its move is:")
                for i in range(len(path)): print(str(path[i]) + '   ' + str(pathAction[i]))
                print("Depth = " + str(len(path)))
                print("Cost = " + str(cost))
                print ("it took " + str(count) + " states")
                return visited
            if state not in visited:       # as long as state is not repeated
                visited.append(state.arr)  # put current state's array in visited
                count = count +1           # increment count to see how many states have been visited
                self.state.arr = state.arr # assignment of current state to state because it then creates its successors
                h = state.createSuccessors(h, visited, self.algorithm) 
        return visited
              
class State: 
    def __init__(self, arr, parent=None, direction="", depth = 0):
        self.arr    = arr
        self.parent = parent
        self.goal   = [1,2,3,8,0,4,7,6,5]
        self.weight = 0
        self.action = direction
        self.depth  = depth

    # def buildPath(self, arr):
    #     if self.parent is None: return arr
    #     else: 
    #         arr.append(self.parent.action)
    #         return self.parent.buildPath(arr)
        
    ''' --------------------------------------------------------------------------------------------------
     creates successors where if move is possible the newly created state will be stored on the heap.
     Note that successors are created the same way, but stored differently depending on the comparison
     which depends on the heuristic. Thus you can uncomment the lines and test each algorithm indivisually
     --------------------------------------------------------------------------------------------------'''
    def createSuccessors (self, h, visited, algorithm):
        index_of_0 = self.arr.index(0)
        
        moveUp = self.swap(index_of_0, [3,4,5,6,7,8], -3, visited, "U", algorithm)
        moveDown = self.swap(index_of_0, [0,1,2,3,4,5], 3, visited, "D", algorithm)
        moveRight = self.swap(index_of_0, [0,1,3,4,6,7], 1, visited, "R", algorithm)
        moveLeft = self.swap(index_of_0, [1,2,4,5,7,8], -1, visited, "L", algorithm)
        
        if moveUp is not None: 
            heap.heappush(h, moveUp)

        if moveDown is not None: 
            heap.heappush(h, moveDown)
        
        if moveRight is not None: 
            heap.heappush(h, moveRight)
        
        if moveLeft is not None: 
            heap.heappush(h, moveLeft)

        return h
    
    def swap (self, index_of_0, arr, i, visited, direction, algorithm):
        # Uniform-Cost - not optimal as it will keep swapping 1,2,3,4,5,6,7,8 with 0 in that order
        if algorithm == "UC" and index_of_0 in arr:
            new_state = self.arr[:]
            new_state[index_of_0], new_state[index_of_0 + i] = new_state[index_of_0 + i], new_state[index_of_0]
            if (new_state not in visited): # Comparison = cost of move
                return new_state[index_of_0], State(new_state, self, direction, self.depth + 1)

        # Best-Fisrt - one of the best algorithms with my data!
        elif algorithm == "BFS" and index_of_0 in arr:
            new_state = self.arr[:]
            new_state[index_of_0], new_state[index_of_0 + i] = new_state[index_of_0 + i], new_state[index_of_0]
            values_out_of_position = 0
            for i in range(len(new_state)):
                if self.goal[i] != new_state[i]:
                    values_out_of_position += 1
            if (new_state not in visited): # Comparison = values out of position
                return values_out_of_position, State(new_state, self, direction)

        # A*1
        elif algorithm == "A1" and index_of_0 in arr:
            new_state = self.arr[:]
            new_state[index_of_0], new_state[index_of_0 + i] = new_state[index_of_0 + i], new_state[index_of_0]
            values_out_of_position = 0
            for i in range(len(new_state)):
                if self.goal[i] != new_state[i]:
                    values_out_of_position += 1
            if (new_state not in visited):  # Comparison = values out of position + cost of move
                return values_out_of_position + new_state[index_of_0], State(new_state, self, direction) 
        
        # A*2
        elif algorithm == "A2" and index_of_0 in arr:
            new_state = self.arr[:]
            new_state[index_of_0], new_state[index_of_0 + i] = new_state[index_of_0 + i], new_state[index_of_0]
            manhattan_d = self.ManDistance(new_state)  # Manhattan Distance 
            if (new_state not in visited): # Comparison = manhattan distance + cost of move
                return manhattan_d + new_state[index_of_0], State(new_state, self, direction)  

    # creating 2D array out of 1D arr
    def create2DArray(self, arr):
        output = [[0]*3]*3
        output[0] = arr[0:3] 
        output[1] = arr[3:6] 
        output[2] = arr[6:9]
        return output

    # counting manhattan distance from each cell of current state until the goal state
    def ManDistance(self, state):
        state_2D = self.create2DArray(state)
        goal_2D  = self.create2DArray(self.goal)
        manDist = 0
        for i in range(3):
            for j in range(3): 
                if (state_2D[i][j] != goal_2D[i][j] and state_2D[i][j] != 0):
                    index_of_val = self.goal.index(state_2D[i][j])
                    index_of_val1= state.index(state_2D[i][j])

                    m = (index_of_val - 1) // 3
                    n = (index_of_val  - 1) % 3 
                    l = (index_of_val1 - 1) // 3
                    k = (index_of_val1  - 1) % 3 
                    
                    row_state = (l - 1) / 3 
                    row_goal  = (m - 1) / 3 
                    col_state = (k - 1) % 3 
                    col_goal  = (n - 1) % 3 
                    
                    manDist += math.fabs(row_state - row_goal) + math.fabs(col_state - col_goal)
                    pass
        return int (manDist)

''' Easy Puzzle - Uniform Cost'''
my_puzzle = Puzzle([1,3,4,8,6,2,7,0,5], "UC")
my_puzzle.solve()

''' Medium Puzzle - Unifrom Cost'''
#my_puzzle = Puzzle([2,8,1,0,4,3,7,6,5], "UC")
#my_puzzle.solve()

''' Hard Puzzle - Uniform Cost'''
#my_puzzle = Puzzle([5,6,7,4,0,8,3,2,1], "UC")
#my_puzzle.solve()


''' Easy Puzzle - Best First Search'''
#my_puzzle = Puzzle([1,3,4,8,6,2,7,0,5], "BFS")
#my_puzzle.solve()

''' Medium Puzzle - Best First Search'''
#my_puzzle = Puzzle([2,8,1,0,4,3,7,6,5], "BFS")
#my_puzzle.solve()

''' Hard Puzzle - Best First Search'''
#my_puzzle = Puzzle([5,6,7,4,0,8,3,2,1], "BFS")
#my_puzzle.solve()

''' Easy Puzzle - A Star One'''
#my_puzzle = Puzzle([1,3,4,8,6,2,7,0,5], "A1")
#my_puzzle.solve()

''' Medium Puzzle - A Star One'''
#my_puzzle = Puzzle([2,8,1,0,4,3,7,6,5], "A1")
#my_puzzle.solve()

''' Hard Puzzle - A Star One'''
#my_puzzle = Puzzle([5,6,7,4,0,8,3,2,1], "A1")
#my_puzzle.solve()

''' Easy Puzzle - A Star Two (Manhattan Distance) '''
#my_puzzle = Puzzle([1,3,4,8,6,2,7,0,5], "A2")
#my_puzzle.solve()

''' Medium Puzzle - A Star Two (Manhattan Distance)'''
#my_puzzle = Puzzle([2,8,1,0,4,3,7,6,5], "A2")
#my_puzzle.solve()

''' Hard Puzzle - A Star Two (Manhattan Distance)'''
#my_puzzle = Puzzle([5,6,7,4,0,8,3,2,1], "A2")
#my_puzzle.solve()
