import heapq
from src.Node import Node

class SearchSolution:
    def __init__(self, start, conRow, conColumn, conDiagonal, domains =None):
        self.solution = None
        if domains is None:
            domains = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        self.start = start
        self.domains = domains
        self.conRow = conRow
        self.conColumn = conColumn
        self.conDiagonal = conDiagonal
        self.assigned = []
        self.curr = []

    def isValid(self, node):
        #Evaluate if established values are able to reach each constraint.
        if node.sumMin() > self.conDiagonal[0] or node.sumMax() > self.conDiagonal[1]:
            return False
        if node.sumMin(True) < self.conDiagonal[0] or node.sumMax(True) < self.conDiagonal[1]:
            return False
        for i in range(len(node.value)):
            if node.sumRow(i) > self.conRow[i] or node.sumColumn(i) > self.conColumn[i]:
                return False
            if node.sumRow(i, True) < self.conRow[i] or node.sumColumn(i, True)< self.conColumn[i]:
                return False
        return True

#Simple backtrace method.

#Unassigned Variables function
#Considers rows as variables with unitialized values. Finds the most constrained variable and returns the list.
    def getUnassginedVar(self, node):
        unassigned = [var for var in node.value if var not in self.assigned]
        return min(unassigned, key = lambda var: node.totalVar(var))

    def search(self, node):
        self.solution = self. backtrace(node)
        return self.solution
    #Main backtrack algorithm as a helper.
    def backtrace(self, node):
        #Base case
        if len(self.assigned) == len(self.start.value):
            return self.curr
        #Recursive case
        #May need to run smaller constraint problem for each list.
        var = self.getUnassginedVar(node)
        self.curr.append(self.setList(node, var))
        self.assigned.append(var)
        result = self.backtrace(node)
        if result is not None:
            return result
        self.assigned.pop()
        return None

    def setList(self, node, var):
        currlst = list(tuple(var))
        for i in range(len(var)):
            for value in self.domains:
                if currlst[i] == -1:
                    if self.isConsistent(node, var, i, value):
                        var[i] = value


        return currlst

    #accept the state as a node, the row, and position being worked on, as well as the potential value.
    #Check if consistency is broken after assignment.
    def isConsistent(self, node, row, i, candidate):
        row[i] = candidate
        if node.sumMin() > self.conDiagonal[0] or node.sumMax() > self.conDiagonal[1]:
            return False
        #This doesn't actually check if value is consistent.
        for j in range(len(node.value)):
            if node.sumRow(j) > self.conRow[j] or node.sumColumn(j) > self.conColumn[j]:
                return False
        return True

    def isGoal(self, node):
        if node.sumMin() != self.conDiagonal[0] or node.sumMax() != self.conDiagonal[1]:
            return False
        for i in range(len(node.value)):
            if node.sumRow(i) != self.conRow[i] or node.sumColumn(i) != self.conColumn[i]:
                return False
        return True


