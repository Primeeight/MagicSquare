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
        self.confSets = self.initDict(self.varlist)


    #Determines if there is a valid solution.
    def isValid(self, node):
        # Evaluate if variables are larger than constraints.
        if node.sumMin() > self.conDiagonal[0] or node.sumMax() > self.conDiagonal[1]:
            return False
        # Evaluate if variables with max values are able to reach constraints.
        if node.sumMin(True) < self.conDiagonal[0] or node.sumMax(True) < self.conDiagonal[1]:
            return False
        for i in range(len(node.value)):
            if node.sumRow(i) > self.conRow[i] or node.sumColumn(i) > self.conColumn[i]:
                return False
            if node.sumRow(i, True) < self.conRow[i] or node.sumColumn(i, True)< self.conColumn[i]:
                return False
        return True

    #Create an empty dictionary with an entry for all variables.
    def initDict(self, varlist):
        dict = {}
        for var in varlist:
            dict[tuple(var)] = []
        return dict
    #Unassigned Variables function
    #Treat individual elements as variables, return a tuple as the index of the element.
    def getUnassignedVar(self, node):
        #Order is assigned using heuristics at the beginning of program.
        unassigned = [x for x in self.varlist if x not in list(self.assigned.keys())]
        return unassigned[0]
    #Heuristic function, returns a pair of min value, negative degree value
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
        print("Var list is:")
        for i in varlist:
            print(i)
        return varlist

    #Main search function
    def search(self):
        print("checking variables:")
        if self.isValid(self.start):
            solution = self.cdBackjump(self.start)
            return solution

    #Conflict Directed Back jumping
    def cdBackjump(self, node):
        #Base case
        if len(self.assigned) == len(self.varlist) and self.isGoalValue(node.value):
            self.isGoalReached = True
            return self.curr
            # Recursive case
        if len(self.assigned) != len(self.varlist):
            ijvar = self.getUnassignedVar(node)
            i, j = ijvar[0], ijvar[1]
            newnode = copy.deepcopy(self.curr)
            if (i,j) in self.confSets:
                self.confSets[(i, j)] = (self.confSets[(i, j)] + [value for value in newnode.getConflicts([i, j], list(self.assigned.keys())) if
                                                 value not in self.confSets[(i, j)]])
            else:
                self.confSets[(i, j)] = newnode.getConflicts([i, j], list(self.assigned.keys()))
            for value in self.domains:
                newnode.value[i][j] = value
                if self.checkConsistency(newnode):
                    print(tuple(ijvar))
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

                # conflict set generation
            current = self.confSets.get((i, j))
            current = [i for i in self.assigned if i in current]
            #Get the most recent variable
            parentvar = current.pop()
            parent = self.confSets[tuple(parentvar)]
            #join operation
            # self.confSets[tuple(parentvar)] =  [value for value in current if value not in parent] + parent
            newcurrent = list(set.union(set(parent), set(current)))
            self.confSets[tuple(parentvar)] = newcurrent
            self.confSets.pop(tuple(ijvar))
            if ijvar in self.assigned:
                self.assigned.pop(tuple(ijvar))
                self.curr.value[ijvar[0]][ijvar[1]] = -1
            return parentvar

    # Native backtrace method.
    def backtrace(self, node):
        # Base case
        if len(self.assigned) == len(self.varlist) and self.isGoalValue(node.value):
            return self.curr
        # Recursive case
        if len(self.assigned) != len(self.varlist):
            ijvar = self.getUnassignedVar(node)
            i, j = ijvar[0], ijvar[1]
            newnode = copy.deepcopy(self.curr)
            for value in self.domains:
                newnode.value[i][j] = value
                if self.checkConsistency(newnode):
                    self.assigned.append(ijvar)
                    self.curr.value[i][j] = value
                    result = self.backtrace(copy.deepcopy(self.curr))
                    if result is not None:
                        return result
                    self.assigned.pop()
                    self.curr.value[i][j] = -1

    #Checks if a node is consistent.
    def checkConsistency(self, newnode):
        if newnode.sumMin() > self.conDiagonal[0] or newnode.sumMax() > self.conDiagonal[1]:
            return False
        for j in range(len(newnode.value)):
            if newnode.sumRow(j) > self.conRow[j] or newnode.sumColumn(j) > self.conColumn[j]:
                return False
        return True

    #Checks if value is the goal value.
    def isGoalValue(self, value):
        node = Node(value)
        if node.sumMin() != self.conDiagonal[0] or node.sumMax() != self.conDiagonal[1]:
            return False
        for i in range(len(node.value)):
            if node.sumRow(i) != self.conRow[i] or node.sumColumn(i) != self.conColumn[i]:
                return False
        return True

    def mapConnections(self, table):
        for i in range(len(table)):
            newlst = list(map(lambda x: 0 if x!= -1 else x ,table[i]))
            table[i] = newlst
        return table
