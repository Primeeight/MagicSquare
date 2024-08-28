
def main():
    dimension, Square, sumRows, sumColumns, sumDiagonals = None, [], None, None, None
    with open("sample1.txt", "r") as file:
        dimension = int(file.readline())
        for i in range(dimension):
            Square.append(list(map(int, file.readline().split())))
        sumRows = list(map(int, file.readline().split()))
        sumColumns = list(map(int, file.readline().split()))
        sumDiagonals = tuple(map(int, file.readline().split()))
if __name__ == '__main__':
    main()