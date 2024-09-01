import sys
from src.SearchSolution import SearchSolution as Search

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
        ss = Search(square, conRows, conColumns, conDiagonals)
        result = ss.search()
        for i in result:
            print(i)

if __name__ == '__main__':
    main()