# @Oleg Puchkov
import sys 
import os
import Queue as queue
from random import shuffle


class Puzzle: 
    def __init__(self, arr):
        self.goal    = [1,2,3,8,0,4,7,6,5]
        self.state   = State(arr)
        self.initial = State(arr)
    
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

    # calling aux method with priority queue that contains the initial state
    def solve (self):
        q = queue.PriorityQueue()
        q.put(self.state)
        self.solveBFS(q)
    
    # while queue is not empty, get first item from queue, check if it is goal
    # if it is not goal then check if it has been visited, if it has not
    # then add it to visited and create successors of this state, and out them on queue
    def solveBFS (self, queue):
        visited = []
        count = 0
        while queue != None:
            state = queue.get()
            if state.arr == self.goal:
                pathAction = self.buildPathAction(state) 
                path = self.buildPath(state)

                print("The exact path and its move is:")
                for i in range(len(path)): print(str(path[i]) + "   " + str(pathAction[i]))
                print("Depth = " + str(len(path)))
                print ("it took " + str(count) + " states")
                return visited
            if state not in visited: 
                visited.append(state.arr)
                count = count +1
                self.state.arr = state.arr
                queue = state.createSuccessors(queue, visited)
        return visited
   
class State: 
    def __init__(self, arr, parent = None, action = ""):
        self.arr    = arr
        self.parent = parent
        self.goal   = [1,2,3,8,0,4,7,6,5]
        self.weight = 0
        self.action = action
        self.depth  = 0
    
    # creates succcessors for current state, where it first sees if move is possible, 
    # then it puts this possible move on the queue, as long as it has not yet been visited
    def createSuccessors (self, q, visited):
        index_of_0 = self.arr.index(0); 

        if index_of_0 in [0,1,3,4,6,7]:
            new_state = self.arr[:]
            new_state[index_of_0], new_state[index_of_0 + 1] = new_state[index_of_0 + 1], new_state[index_of_0]
            if (new_state not in visited): 
                q.put(State(new_state, self, "L"))

        if index_of_0 in [3,4,5,6,7,8]:
            new_state = self.arr[:]
            new_state[index_of_0], new_state[index_of_0 - 3] = new_state[index_of_0 - 3], new_state[index_of_0]
            if (new_state not in visited): 
                q.put(State(new_state, self, "D"))
        
        if index_of_0 in [0,1,2,3,4,5]:
            new_state = self.arr[:]
            new_state[index_of_0], new_state[index_of_0 + 3] = new_state[index_of_0 + 3], new_state[index_of_0]
            if (new_state not in visited): 
                q.put(State(new_state, self, "U"))

        if index_of_0 in [1,2,4,5,7,8]:
            new_state = self.arr[:]
            new_state[index_of_0], new_state[index_of_0 - 1] = new_state[index_of_0 - 1], new_state[index_of_0]
            if (new_state not in visited): 
                q.put(State(new_state, self, "R")) 

        return q

''' easy Puzzle     - tested and it solves after looking at 6 states        '''
print("BFS Level: Easy")
my_puzzle = Puzzle([1,3,4,8,6,2,7,0,5])
my_puzzle.solve()

''' medium Puzzle   - tested and it solves after looking at 441 states     '''
#print("BFS Level: Medium")
#my_puzzle = Puzzle([2,8,1,0,4,3,7,6,5])
#my_puzzle.solve()

''' hard Puzzle     - tested and it solves after looking at 4104 states     '''
#print("BFS Level: Hard")
#my_puzzle = Puzzle([5,6,7,4,0,8,3,2,1])
#my_puzzle.solve()
