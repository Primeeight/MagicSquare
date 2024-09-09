class Node:
    def __init__(self, value = None):
        self.value = value
    #Adds all the elements of a list together, can treat variables as max value for determining a solution.
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
    def getConflicts(self, value, assigned):
        i, j, conflicts = value[0], value[1], []
        #get major and minor axis
        #get columns and rows
        for k in range(len(self.value)):
            if i == len(self.value) - j - 1 and [k, len(self.value) - k - 1] not in conflicts:
                conflicts.append([k, len(self.value) - k - 1])
            if i == j and [k, k] not in conflicts:
                conflicts.append([k, k])
            #check columns
            if [k, j] not in conflicts:
                conflicts.append([k, j])
            #check rows
            if [i, k] not in conflicts:
                conflicts.append([i, k])
        conflicts = [i for i in assigned if i in conflicts]
        return conflicts





