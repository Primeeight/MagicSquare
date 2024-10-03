import copy
import unittest
import random
import timeit
from Node import Node
from SearchSolution import SearchSolution as Search

class MyTestCase(unittest.TestCase):
    # def testadd(self):
    #     node = Node([[1, -1, 3], [4, 5, 6]])
    #     result = node.sumRow(0, False)
    #     result2 = node.sumRow(0, True)
    #     self.assertEqual(result, 4)
    #     self.assertEqual(result2, 13)
    #
    # def testaddDiag(self):
    #     node = Node([[1, 2, 3], [4, -1, 6], [7, 8, 9]])
    #     result = node.sumMax()
    #     result2 = node.sumMax(True)
    #     self.assertEqual(result, 10)
    #     self.assertEqual(result2, 19)
    #
    # def testIsValid(self):
    #     node = Node([[1, -1, 3], [4, 5, 6], [7, 8, 9]])
    #     ss = Search(node, [13,15, 24],[12,22, 18], [15, 15])
    #     self.assertTrue(ss.isValid(node))
    # #
    # def testGetUnassignedValue(self):
    #     node = Node([[1, -1, -1], [-1, -1, 6], [7, -1, 9]])
    #     ss = Search(node, [13,15, 24],[12,22, 18], [15, 15])
    #     self.assertEqual(ss.getUnassignedVar(node), [0, 2])
    #
    # def testHeuristic(self):
    #     result, result2, lst = [], [], []
    #     node = Node([[-1, -1, 0], [5, -1, 2], [-1, -1, -1]])
    #     ss = Search(node, [10, 8, 9], [12, 10, 5], [9, 3])
    #     result = ss.getVarList(node)
    #     result.sort(key = lambda x: ss.heuristic(x, node))
    #     lst = ss.getVarList(node)
    #     for i in lst:
    #         result2.append(ss.heuristic(i, node))
    #     result2.sort()
    #     self.assertEqual(result, [[1,1], [2,0],[2,2],[0,0],[2,1],[0,1]])
    #     self.assertEqual(result2, [(1, -5), (3,-4),(3,-4),(7,-4),(9,-4),(10,-3)])

    # def testGetUnassignedVar(self):
    #     node = Node([[-1, -1, 0], [5, -1, 2], [-1, -1, -1]])
    #     ss = Search(node, [10,8, 9],[12,10, 5], [9, 3])
    #     self.assertEqual(ss.getUnassignedVar(node), [1, 1])
    #     node = Node([[-1, -1, 0], [5, 1, 2], [-1, -1, -1]])
    #     ss = Search(node, [10, 8, 9], [12, 10, 5], [9, 3])
    #     self.assertEqual(ss.getUnassignedVar(node), [2, 0])
    #     node = Node([[-1, -1, 0], [5, 1, 2], [2, -1, -1]])
    #     ss = Search(node, [10, 8, 9], [12, 10, 5], [9, 3])
    #     self.assertEqual(ss.getUnassignedVar(node), [2, 2])
    #     node = Node([[-1, -1, 0], [5, 1, 2], [2, -1, 3]])
    #     ss = Search(node, [10, 8, 9], [12, 10, 5], [9, 3])
    #     self.assertEqual(ss.getUnassignedVar(node), [2, 1])
    #     result = ss.search()
    #     if result:
    #         print("able to get an unassigned var, result:")
    #         print(result.value)
    #     self.assertTrue(ss.isGoalValue(result.value))

    # def testGetConflicts(self):
    #     node = Node([[5, 5, 0], [5, 1, 2], [-1, 5, 2]])
    #     ss = Search(node, [10, 8, 9], [12, 10, 5], [9, 3])
    #     result = node.getConflicts([2,1], [[0,0], [0,1], [1,1], [2,1], [2,2]])
    #     self.assertEqual(result, [[0,1], [1,1], [2,2]])
    # #
    # def testCheckConsistency(self):
    #     node = Node([[1, -1, -1], [-1, -1, 6], [7, -1, 9]])
    #     ss = Search(node, [13, 15, 24], [12, 22, 18], [15, 15])
    #     self.assertTrue(ss.checkConsistency(node))
    #
    # def testMinRemain(self):
    #     node = Node([[1, -1, -1], [-1, -1, 6], [7, -1, 9]])
    #     ss = Search(node, [13, 15, 24], [12, 22, 18], [15, 15])
    #     result = node.minRemaining(2, 1, ss.conDiagonal, ss.conRow, ss.conColumn)
    #     self.assertEqual(result, 8)

    # def testInitDict(self):
    #     node = Node([[-1, -1, 0], [5, -1, 2], [-1, -1, -1]])
    #     ss = Search(node, [10, 8, 9], [12, 10, 5], [9, 3])
    #     result = ss.confSets
    #     if result:
    #         print(result.keys())
    #         print(result.values())
    #     self.assertFalse(result[list(result.keys())[0]])

    # def testSearchSampleNative(self):
    #     node = Node([[-1, -1, 0], [5, -1, 2], [-1, -1, -1]])
    #     ss = Search(node, [10, 8, 9], [12, 10, 5], [9, 3])
    #     result = ss.backtrace(node)
    #     reached = ss.isGoalValue(result.value)
    #     if result:
    #         print("testing sample with native backtrace")
    #         print(result.value)
    #     self.assertTrue(reached)

    # def testSearchSampleBackJump(self):
    #     node = Node([[-1, -1, 0], [5, -1, 2], [-1, -1, -1]])
    #     ss = Search(node, [10, 8, 9], [12, 10, 5], [9, 3])
    #     result = ss.search()
    #     if result:
    #         print("testing sample with back jumping")
    #     self.assertTrue(ss.isGoalReached)
    #
    #
    # def testSearchBackjumpLarger(self):
    #     node = Node([[8,7,3,1], [2, 4, -1, 8], [-1, -1, 9, 0], [0, 2, -1, -1]])
    #     ss = Search(node, [19, 20, 12, 12], [11, 15, 22, 15], [27, 9])
    #     result = ss.search()
    #     if result:
    #         print(result.value)
    #     self.assertTrue(ss.isGoalReached)

    # def testSearchBackjump5(self):
    #     node = Node([[4, -1, -1, 4, 4],
    #                  [8, -1, -1, -1, 8],
    #                  [4, 4, -1, -1, 4],
    #                  [1, -1, -1, 1, 1],
    #                  [2, 2, 2, -1, 2]])
    #     ss = Search(node, [18, 25, 18, 9, 11], [19, 15, 14, 14, 19], [13, 15])
    #     result = ss.search()
    #     self.assertTrue(ss.isGoalReached)

    # def testSearchBackjump5(self):
    #     node = Node([[4, 2, 3, 7, 8, 7, 3, 7],
    #                  [2, 8, -1, 8, 4, -1, 2, 5],
    #                  [3, 5, 8, -1, -1, 1, 5, 0],
    #                  [1, 0, 1, -1, 8, 0, 8, 4],
    #                  [5, 0, 7, 0, 6, 0, 6, 7],
    #                  [0, 2, -1, 0, 0, 8, -1, 0],
    #                  [6, 7, 4, -1, 6, 4, -1, 3],
    #                  [3, 4, 4, 6, 4, 0, 7, 3]])
    #     ss = Search(node, [41, 35, 28, 25, 31, 16, 36, 31, 43],
    #                 [24, 28, 33, 30, 39, 23, 37, 29],
    #                 [43, 31])
    #     result = ss.search()
    #     self.assertTrue(ss.isGoalReached)

    # def testSearchBackjump8extra(self):
    #     node = Node([[4, 2, 3, 7, 8, 7, 3, 7],
    #                  [2, 8, 3, 8, 4, 3, 2, 5],
    #                  [-1, 5, 8, -1, -1, 1, 5, 0],
    #                  [1, 0, 1, -1, 8, 0, 8, 4],
    #                  [5, 0, 7, 0, 6, 0, 6, 7],
    #                  [-1, 2, -1, 0, 0, 8, -1, 0],
    #                  [6, 7, 4, -1, 6, 4, -1, 3],
    #                  [3, 4, 4, 6, 4, 0, 7, 3]])
    #     ss = Search(node, [41, 35, 28, 25, 31, 16, 36, 31, 43],
    #                 [24, 28, 33, 30, 39, 23, 37, 29],
    #                 [43, 31])
    #     result = ss.search()
    #     self.assertTrue(ss.isGoalReached)

    # def testSearchSampleBackjumpVar(self):
    #     n = 8
    #     conRow, conCol, conDiag = [], [], []
    #     lst = [-1] * n
    #     for i in range(len(lst)):
    #         lst[i] = random.choices(list(range(0,9)), k=n)
    #     node = Node(copy.deepcopy(lst))
    #     for i in range(len(lst)):
    #         conRow.append(node.sumRow(i, True))
    #         conCol.append(node.sumColumn(i, True))
    #     conDiag = [node.sumMin(True), node.sumMax(True)]
    #
    #     for i in range(len(node.value)):
    #         for j in range(len(node.value)):
    #             value = node.value[i][j]
    #             node.value[i][j] = random.choice([value, value, -1])
    #     lst = []
    #     ss = Search(node, conRow, conCol, conDiag)
    #     result = ss.search()
    #     if result:
    #         print ("original")
    #         print(lst)
    #         print("testing sample with back jumping")
    #         print(result.value)
    #     self.assertTrue(ss.isGoalReached)

    # def testSearchSampleBackTraceVar(self):
    #     n = 3
    #     conRow, conCol, conDiag = [], [], []
    #     lst = [-1] * n
    #     for i in range(len(lst)):
    #         lst[i] = random.choices([random.randint(0, 9), -1], [.667, .333], k=n)
    #     node = Node(copy.deepcopy(lst))
    #     for i in range(len(lst)):
    #         conRow.append(node.sumRow(i, True))
    #         conCol.append(node.sumColumn(i, True))
    #     conDiag = [node.sumMin(True), node.sumMax(True)]
    #     ss = Search(node, conRow, conCol, conDiag)
    #     result = ss.backtrace(node)
    #     if result:
    #         print ("original")
    #         print(lst)
    #         print("testing sample with backtracing")
    #         print(result.value)

    # def testBacktraceAndBackJump(self):
    #     n = 5
    #     conRow, conCol, conDiag = [], [], []
    #     lst = [-1]*n
    #     for i in range(len(lst)):
    #         lst[i] = random.choices([random.randint(0,9), -1],[.667, .333], k=n)
    #     node = Node(copy.deepcopy(lst))
    #     for i in range(len(lst)):
    #         conRow.append(node.sumRow(i, True))
    #         conCol.append(node.sumColumn(i, True))
    #     conDiag = [node.sumMin(True), node.sumMax(True)]
    #     ss = Search(node, conRow, conCol, conDiag)
    #     bjtime = timeit.default_timer()
    #     result = ss.search()
    #     bjtime = round((timeit.default_timer() - bjtime)/1000000000, 3)
    #     if result:
    #         print ("original:")
    #         print(lst)
    #         print("testing sample with back jumping")
    #         print(result.value)
    #         print(bjtime)
    #     self.assertTrue(ss.isGoalReached)
    #     ss = Search(node, conRow, conCol, conDiag)
    #     bttime = timeit.default_timer()
    #     result = ss.backtrace(node)
    #     bttime = round((timeit.default_timer() - bttime) / 1000000000, 3)
    #     if result:
    #         print ("original:")
    #         print(lst)
    #         print(result.value)
    #         print(bttime)

    # def testIsGoalValue(self) :
    #     node = Node([[1, -1, -1], [-1, -1, 6], [7, -1, 9]])
    #     ss = Search(node, [13, 15, 24], [12, 22, 18], [15, 15])
    #     result = ss.search()
    #     goal = ss.isGoalValue(result.value)
    #     self.assertTrue(goal)

    # def testFile(self):
    #     fname = ["src/sample1.txt", "src/sample2.txt", "src/sample2_fail.txt", "src/sample3_fail.txt"]
    #     dimension, square = None, []
    #     for i in range(len(fname)):
    #         with open(fname[i], "r") as file:
    #             dimension = int(file.readline())
    #             for j in range(dimension):
    #                 square.append(list(map(int, file.readline().split())))
    #             conRows = list(map(int, file.readline().split()))
    #             conColumns = list(map(int, file.readline().split()))
    #             conDiagonals = tuple(map(int, file.readline().split()))
    #             ss = Search(Node(square), conRows, conColumns, conDiagonals)
    #             ss.search()
    #             dimension, square = None, []
    #             if fname[i].__contains__("fail"):
    #                 self.assertFalse(ss.isGoalReached)
    #             else:
    #                 self.assertTrue(ss.isGoalReached)

    # def testSample2(self):
    #     fname = "src/sample2.txt"
    #     dimension, square = None, []
    #     with open(fname, "r") as file:
    #         dimension = int(file.readline())
    #         for i in range(dimension):
    #             square.append(list(map(int, file.readline().split())))
    #         conRows = list(map(int, file.readline().split()))
    #         conColumns = list(map(int, file.readline().split()))
    #         conDiagonals = tuple(map(int, file.readline().split()))
    #         ss = Search(Node(square), conRows, conColumns, conDiagonals)
    #         result = ss.search()
    #         print(result.value)
    #         self.assertTrue(ss.isGoalReached)

    # Currently this test does not get a solution due to the problem size, will lead to hanging.
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
            # mapping = ss.mapConnections(square)
            # for i in mapping:
            #     print(i)
            result = ss.search()
            for i in result:
                print (i)
            self.assertTrue(ss.isGoalReached)



if __name__ == '__main__':
    unittest.main()
