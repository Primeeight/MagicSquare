import unittest
from src.Node import Node
from src.SearchSolution import SearchSolution as Search

class MyTestCase(unittest.TestCase):
    def testadd(self):
        node = Node([[1, -1, 3], [4, 5, 6]])
        result = node.sumRow(0, False)
        result2 = node.sumRow(0, True)
        self.assertEqual(result, 4)
        self.assertEqual(result2, 13)
    def testaddDiag(self):
        node = Node([[1, 2, 3], [4, -1, 6], [7, 8, 9]])
        result = node.sumMax()
        result2 = node.sumMax(True)
        self.assertEqual(result, 10)
        self.assertEqual(result2, 19)
    def testIsValid(self):
        node = Node([[1, -1, 3], [4, 5, 6], [7, 8, 9]])
        ss = Search(node, [13,15, 24],[12,22, 18], [15, 15])
        self.assertTrue(ss.isValid(node))
    def testGetUnassigned(self):
        node = Node([[1, -1, -1], [-1, -1, 6], [7, -1, 9]])
        ss = Search(node, [13,15, 24],[12,22, 18], [15, 15])
        self.assertEqual(node.value[ss.getUnassignedVar(node)], [-1, -1, 6])
    def testIsConsistent(self):
        node = Node([[1, -1, -1], [-1, -1, 6], [7, -1, 9]])
        ss = Search(node, [13, 15, 24], [12, 22, 18], [15, 15])
        self.assertTrue(ss.isConsistent(node, 0, 2, 1))
    def testBacktrace(self):
        node = Node([[1, -1, -1], [-1, -1, 6], [7, -1, 9]])
        ss = Search(node, [13, 15, 24], [12, 22, 18], [15, 15])
        result = ss.search()
        if result:
            print(True)
        else:
            print(False)
        for i in range(len(result)):
            print(result[i])
            print(ss.conRow[i])
    def testGoal(self) :
        node = Node([[1, -1, -1], [-1, -1, 6], [7, -1, 9]])
        ss = Search(node, [13, 15, 24], [12, 22, 18], [15, 15])
        result = ss.search()
        goal = ss.isGoalValue(result)
        self.assertTrue(goal)

    def testFile(self):
        fname = ["src/sample1.txt", "src/sample2.txt", "src/sample3.txt", "src/sample2_fail.txt", "src/sample3_fail.txt"]
        dimension, square = None, []
        for i in range(len(fname)):
            with open(fname[i], "r") as file:
                dimension = int(file.readline())
                for j in range(dimension):
                    square.append(list(map(int, file.readline().split())))
                conRows = list(map(int, file.readline().split()))
                conColumns = list(map(int, file.readline().split()))
                conDiagonals = tuple(map(int, file.readline().split()))
                ss = Search(Node(square), conRows, conColumns, conDiagonals)
                result = ss.search()
                dimension, square = None, []
                if fname[i].__contains__("fail"):
                    self.assertFalse(ss.isGoalReached)
                else:
                    self.assertTrue(ss.isGoalReached)

    def testFileLarge(self):
        fname = "src/sample3.txt"
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
            for i in result:
                print (i)
            self.assertTrue(ss.isGoalReached)

if __name__ == '__main__':
    unittest.main()
