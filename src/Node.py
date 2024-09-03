class Node:
    def __init__(self, value = None):
        self.value = value
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

    def totalVar(self, i, j):
        count, value = 1, self.value[i][j]
        if value == -1:
            if j == i:
                count -= 1
            if j == len(self.value) - i - 1:
                count -= 1
            for k in range (len(self.value[i])):
                if k == -1:
                    count += 1
            count -= 1
            for k in range(len(self.value)):
                if self.value[k][j] == -1:
                    count += 1
            count -= 1
        return count


