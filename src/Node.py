class Node:
    def __init__(self, value = None, parent = None, f = 0, g = 0, h = 0):
        self.value = value
        self.parent = parent
        self.f = f
        self.g = g
        self.h = h
        self.children = []
    #May define function to find sum rows, columns, diagonals.
    def sumList(self, row, countVar):
        if countVar:
            row = list (map(lambda x: x + 10 if(x == -1) else x, row))
            return sum(row)
        row = list(map(lambda x: x + 1 if (x == -1) else x, row))
        return sum(row)

    def sumColumn(self, j, countVar = False):
        row = []
        for i in range(len(self.value)):
            row.append(self.value[i][j])
        return self.sumList(row, countVar)

    def sumMin(self, countVar = False):
        row = []
        for i in range(len(self.value)):
            row.append(self.value[i][i])
        return self.sumList(row, countVar)

    def sumMax(self, countVar = False):
        row = []
        for i in range(len(self.value)):
            row.append(self.value[i][len(self.value) -i-1])
        return self.sumList(row, countVar)

    def sumRow(self, i, countVar = False):
        row = list(tuple(self.value[i]))
        return self.sumList(row, countVar)
    #Most constrained value heuristic.
    #Gives the total number of variables in a list, prioritizes variables in the max diagonal, as well as the min diagonal.
    def totalVar(self, list):
        count, i = 0, self.getIndex(list)
        for j in range(len(list)):
            if list[j] == -1:
                if j == i:
                    count -= 1
                if j == len(list) - i -1:
                    count -= 1
                count += 1
        return count

    def getIndex(self, row):
        for i in range(len(self.value)):
            if row == self.value[i]:
                return i


