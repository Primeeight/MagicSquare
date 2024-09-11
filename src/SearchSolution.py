import copy
from Node import Node


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
        self.currconf = []
        self.conf = []

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

    #Unassigned Variables function
    #Treat individual elements as variables, return a tuple as the index of the element.
    def getUnassignedVar(self, node):
        unassigned = [[i, j]
                      for i in (range(len(node.value)))
                      for j in range(len(node.value))
                      if [i, j] not in self.assignedIndex and [i, j] in self.varlist]
        #Call heuristic function
        return min(unassigned, key= lambda index: self.heuristic(index, node))

    def heuristic(self, index, node):
        result =(node.minRemaining(index[0], index[1],self.conDiagonal,self.conRow,self.conColumn),
                  -node.totalVar(index[0], index[1]))
        return result
    #Get the non-variables and add them to assigned.
    def getVarList(self, node):
        varlist = [[i, j]
                    for i in (range(len(node.value)))
                    for j in range(len(node.value))
                    if node.value[i][j] == -1]
        return varlist

    def search(self):
        if self.isValid(self.start):
            solution = self.cdBackjump(self.start)
            if solution is not None:
                self.isGoalReached = True
            return solution

    def cdBackjump(self, node):
        #Base case
        if len(self.assignedIndex) == len(self.varlist) and self.isGoalValue(node.value):
            return self.curr
            # Recursive case
        if len(self.assignedIndex) != len(self.varlist):
            # Will likely need to clear the conflict set after a variable is chosen.
            ijvar = self.getUnassignedVar(node)
            i, j = ijvar[0], ijvar[1]
            newnode = copy.deepcopy(self.curr)
            for value in self.domains:
                newnode.value[i][j] = value
                if self.checkConsistency(newnode):
                    self.assignedIndex.append(ijvar)
                    self.curr.value[i][j] = value
                    result = self.cdBackjump(copy.deepcopy(self.curr))
                    if result is not None:
                        return result
                    self.currconf = newnode.getConflicts([i, j], self.assignedIndex)
                    if ijvar in self.assignedIndex:
                        self.assignedIndex.pop()
                        self.curr.value[i][j] = -1
                        # Back jumping code here causes issues with the chronological version.
            if self.currconf:
                self.conf = self.conf + [value for value in self.currconf if value not in self.conf]
                var = self.conf.pop()
                if var in self.assignedIndex:
                    self.assignedIndex.remove(var)
                    self.curr.value[var[0]][var[1]] = -1
                self.currconf.clear()

    # Native backtrace method.
    def backtrace(self, node):
        # Base case
        if len(self.assignedIndex) == len(self.varlist) and self.isGoalValue(node.value):
            return self.curr
        # Recursive case
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


