import copy
from src.Node import Node


class SearchSolution:
    def __init__(self, startNode, conRow, conColumn, conDiagonal, domains =None):
        self.start = startNode
        self.conRow = conRow
        self.conColumn = conColumn
        self.conDiagonal = conDiagonal
        if domains is None:
            domains = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
        self.domains = domains
        self.assignedIndex = []
        self.curr = self.start
        self.isGoalReached = False
        self.varlist = self.getVarList(self.start)

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

    # Unassigned Variables function
    # Considers rows as variables with uninitialized values. Finds the most constrained variable
    # returns the index of the list.

    #Treat individual elements as variables, return a tuple as the index of the element.
    def getUnassignedVar(self, node):
        unassigned = [[i, j]
                      for i in (range(len(node.value)))
                      for j in range(len(node.value))
                      if [i, j] not in self.assignedIndex and [i, j] in self.varlist]
        #Call heuristic function
        return min(unassigned, key = lambda index: node.totalVar(index[0], index[1]))

    #Get the non-variables and add them to assigned.
    def getVarList(self, node):
        varlist = [[i, j]
                    for i in (range(len(node.value)))
                    for j in range(len(node.value))
                    if node.value[i][j] == -1]
        return varlist

    # Simple backtrace method.
    def search(self):
        if self.isValid(self.start):
            solution = self.backtrace(self.start)
            if solution is not None:
                self.isGoalReached = True
            return solution
    #constantly retries values of 2,1 before erroring out, cannot find new value.
    #Torwards the end, values in the last variable are left while the variable is not in assigned, causing consistency to be broken.
    #If last variable does not retain value, able to find solution.
    def backtrace(self, node):
        #Base case
        if len(self.assignedIndex) == len(self.varlist) and self.isGoalValue(node.value):
            return self.curr
        #Recursive case
        if len(self.assignedIndex) != len(self.varlist):
            ijvar = self.getUnassignedVar(node)
            i, j = ijvar[0], ijvar[1]
            newnode = copy.deepcopy(self.curr)
            for value in self.domains:
                newnode.value[i][j] = value
                if self.checkConsistency(newnode):
                    self.assignedIndex.append(ijvar)
                    self.curr.value[i][j] = value
                    result = self.backtrace(copy.deepcopy(self.curr))
                    if result is not None:
                        return result
                    self.assignedIndex.pop()
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


