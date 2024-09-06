import sys
from Node import Node
from SearchSolution import SearchSolution as Search

def main():
    fname = sys.argv[1]
    dimension, square = None, []
    with open(fname, "r") as file:
        dimension = int(file.readline())
        for i in range(dimension):
            square.append(list(map(int, file.readline().split())))
        conRows = list(map(int, file.readline().split()))
        conColumns = list(map(int, file.readline().split()))
        conDiagonals = tuple(map(int, file.readline().split()))
        ss = Search(Node(square), conRows, conColumns, conDiagonals)
        result = ss.search()
        if result:
            print("True")
            for i in result.value:
                print(i)
        else:
            print("False")

if __name__ == '__main__':
    main()