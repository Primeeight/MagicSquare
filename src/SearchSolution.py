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
        self.curr = []
        self.isGoalReached = False
        self.assigned = []

    #Determines if there is a valid solution.
    def isValid(self, node):
        # Evaluate if variables are larger than constriants.
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
    def getUnassignedVar(self, node):
        unassigned = [i for i in (range(len(node.value))) if i not in self.assignedIndex]
        #Call heuristic function
        return min(unassigned, key = lambda i: node.totalVar(node.value[i]))

    # Simple backtrace method.
    def search(self):
        if self.isValid(self.start):
            solution = self.sortLists(self.backtrace(self.start))
            self.isGoalReached = self.isGoalValue(solution)
            return solution

    # Backtrace function
    # Helper to main search function
    def backtrace(self, node):
        #Base case
        if len(self.assignedIndex) == len(self.start.value):
            return self.curr
        #Recursive case
        ivar = self.getUnassignedVar(node)
        self.curr.append(self.setList(node, ivar))
        self.assignedIndex.append(ivar)
        result = self.backtrace(node)
        if result is not None:
            return result
        self.assignedIndex.pop()
        return None

    #Sort the lists prior to returning the solution.
    def sortLists(self, value):
        return [x for _, x in sorted(zip(self.assignedIndex, value))]

    def setList(self, node, ivar):
        # Each list is a variable
        # Each list is also treated as a CSP, and its elements as variables.
        var = node.value[ivar]
        for i in range(len(var)):
            if var[i] == -1:
                #test each value in the domain set
                for value in self.domains:
                    newnode = copy.deepcopy(node)
                    if self.isConsistent(newnode, ivar, i, value):
                        var[i] = value
        return var


    #Assigns a value to an element of a list.
    #Check if consistency is broken after assignment.
    def isConsistent(self, newnode, ivar, i, candidate):
        #Add the candidate to the variable.
        row = newnode.value[ivar]
        row[i] = candidate
        # Run tests
        return self.checkConsistency(newnode)

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


