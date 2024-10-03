import copy
from Node import Node


class SearchSolution:
    def __init__(self, startNode, conRow, conColumn, conDiagonal, domains =None):
        #Initial node provided
        self.start = startNode
        #Constraints
        self.conRow = conRow
        self.conColumn = conColumn
        self.conDiagonal = conDiagonal
        if domains is None:
            domains = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
        self.domains = domains
        #Assigned values
        self.assigned = {}
        self.curr = self.start
        self.isGoalReached = False
        #The variables to be assigned
        self.varlist = self.getVarList(self.start)
        #The dictionary of conflict sets.
        #Revise to have empty dictionary.
        self.confSets = {}
        # self.confSets = self.initDict(self.varlist)
        self.visited = []
        self.completed = []
        self.domains = self.initDomains({})


    #Determines if there is a valid solution.
    def isValid(self, node):
        # Evaluate if variables are larger than constraints.
        if node.sumMin() > self.conDiagonal[0] or node.sumMax() > self.conDiagonal[1]:
            return False
        # Evaluate if variables with max values are able to reach constraints.
        newnode = copy.deepcopy(node)
        for i in range(len(newnode.value)):
            for j in range(len(newnode.value)):
                if newnode.value[i][j] == -1:
                    newnode.value[i][j] = max(self.domains[(i,j)])
        i, j = 0,0
        if newnode.sumMin(True) < self.conDiagonal[0] or newnode.sumMax(True) < self.conDiagonal[1]:
            return False
        for i in range(len(newnode.value)):
            if node.sumRow(i) > self.conRow[i] or node.sumColumn(i) > self.conColumn[i]:
                return False
            if newnode.sumRow(i, True) < self.conRow[i] or newnode.sumColumn(i, True)< self.conColumn[i]:
                return False
        return True

    #Initialize the set of domains for each variable, used to determine if there's a valid solution only.
    def initDomains(self, dictionary):
        if len(dictionary.keys()) == len(self.varlist):
            return dictionary
        unassigned = [x for x in self.varlist if x not in list(dictionary.keys())]
        var = unassigned[0]
        lst = [9]*4
        if var[1] == var[0]:
            lst[0] = self.conDiagonal[0] - self.start.sumMin()
        if var[1] == len(self.start.value) -var[0] -1:
            lst[1] = self.conDiagonal[1] - self.start.sumMax()
        lst[2] = self.conRow[var[0]] - self.start.sumRow(var[0])
        lst[3] = self.conColumn[var[1]] - self.start.sumColumn(var[1])
        lst.append(9)
        dictionary[var] = list(range(min(lst)+1))
        return self.initDomains(dictionary)

    #Unassigned Variables function
    #Treat individual elements as variables, return a tuple as the index of the element.
    #The order of variables are static, defined by the heuristic at initialization.
    def getUnassignedVar(self):
        #Order is assigned using heuristics at the beginning of program.
        unassigned = [x for x in self.varlist if x not in list(self.assigned.keys())]
        return unassigned[0]


    #Heuristic function, returns a pair of min value heuristic, negative degree value heuristic
    def heuristic(self, index, node):
        result =(node.minRemaining(index[0], index[1],self.conDiagonal,self.conRow,self.conColumn),
                  -node.totalVar(index[0], index[1]))
        return result

    def getVarList(self, node):
        varlist = [(i, j)
                    for i in (range(len(node.value)))
                    for j in range(len(node.value))
                    if node.value[i][j] == -1]
        #Sort the list of variables by the heuristic.
        varlist.sort(key = lambda index: self.heuristic(index, node))

        return varlist

    #Main search function
    def search(self):
        if self.isValid(self.start):
            print("Back jumping to variables:")
            self.domains = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
            solution = self.cdBackjump(self.start)
            return solution
        return False

    #Conflict Directed Back jumping
    def cdBackjump(self, node):
        #Base case
        if len(self.assigned) == len(self.varlist) and self.isGoalValue(node.value):
            self.isGoalReached = True
            return self.curr
            # Recursive case
        if len(self.assigned) != len(self.varlist):
            ijvar = self.getUnassignedVar()
            i, j = ijvar[0], ijvar[1]
            newnode = copy.deepcopy(self.curr)
            if (i,j) in self.confSets:
                self.confSets[(i, j)] = (self.confSets[(i, j)] + [value for value in newnode.getConflicts([i, j], list(self.assigned.keys())) if
                                                 value not in self.confSets[(i, j)]])
                self.confSets[(i, j)] = [k for k in self.assigned if k in self.confSets.get((i, j))]
            else:
                self.confSets[(i, j)] = newnode.getConflicts([i, j], list(self.assigned.keys()))

            for value in self.domains:
                newnode.value[i][j] = value
                if self.checkConsistency(newnode):
                    self.assigned[tuple(ijvar)] = value
                    self.curr.value[i][j] = value
                    result = self.cdBackjump(copy.deepcopy(self.curr))
                    if result is not None:
                        if self.isGoalReached:
                            return result
                        if result is not ijvar:
                            self.assigned.pop(ijvar)
                            self.curr.value[i][j] = -1
                            return result
                if self.checkCompleteness(ijvar):
                    self.completed.append(ijvar)

                # conflict set generation
            #If a variable does not have a complete assignment, it is in conflict.
            notcompleted = [i for i in self.assigned if i not in self.completed]
            if ijvar in notcompleted:
                notcompleted.remove(ijvar)
            current = self.confSets.get((i, j)) + notcompleted
            current = [i for i in self.assigned if i in current]
            #Get the most recent variable
            parentvar = current.pop()
            parent = self.confSets[tuple(parentvar)]
            #join operation
            newcurrent = list(set.union(set(parent), set(current)))
            self.confSets[tuple(parentvar)] = newcurrent
            self.confSets.pop(tuple(ijvar))
            self.completed.clear()
            if ijvar in self.assigned:
                self.assigned.pop(tuple(ijvar))
                self.curr.value[ijvar[0]][ijvar[1]] = -1
            print (parentvar) if parentvar not in self.visited else ""
            self.visited.append(parentvar) if parentvar not in self.visited else ""
            return parentvar

    #Checks if a node is consistent.
    def checkConsistency(self, newnode):
        if newnode.sumMin() > self.conDiagonal[0] or newnode.sumMax() > self.conDiagonal[1]:
            return False
        for j in range(len(newnode.value)):
            if newnode.sumRow(j) > self.conRow[j] or newnode.sumColumn(j) > self.conColumn[j]:
                return False
        return True
    #Checks if a node is in a complete assignment, the node is in a complete row, column, or diagonal if applicable.
    def checkCompleteness(self, var):
        i, j = var[0], var[1]
        if self.curr.sumRow(i) == self.conRow[i] or self.curr.sumColumn(j) == self.conColumn[j]:
            return True
        if j == i:
            if self.curr.sumMin() == self.conDiagonal[0]:
                return True
        if j == len(self.curr.value) - i -1:
            if self.curr.sumMax() == self.conDiagonal[1]:
                return True
        return False

    #Checks if value is the goal value.
    def isGoalValue(self, value):
        node = Node(value)
        if node.sumMin() != self.conDiagonal[0] or node.sumMax() != self.conDiagonal[1]:
            return False
        for i in range(len(node.value)):
            if node.sumRow(i) != self.conRow[i] or node.sumColumn(i) != self.conColumn[i]:
                return False
        return True
