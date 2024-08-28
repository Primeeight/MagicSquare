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
        ss = Search(node, [13,15, 24],[12,21, 18], [15, 15])
        self.assertTrue(ss.isValid(node))
    def testGetUnassigned(self):
        node = Node([[1, -1, -1], [-1, -1, 6], [7, -1, 9]])
        ss = Search(node, [13,15, 24],[12,21, 18], [15, 15])
        self.assertEqual(ss.getUnassginedVar(node), [7, -1, 9])
    def testIsConsistent(self):
        node = Node([[1, -1, -1], [-1, -1, 6], [7, -1, 9]])
        ss = Search(node, [13, 15, 24], [12, 21, 18], [15, 15])
        self.assertTrue(ss.isConsistent(node, node.value[0], 2, 1))
    # def testIsConsistentList(self):
    #     node = Node([[1, -1, -1], [-1, -1, 6], [7, -1, 9]])
    #     ss = Search(node, [13, 15, 24], [12, 21, 18], [15, 15])
    #     self.assertTrue(ss.setList(node, node.value[0], 1))
    def testBacktrace(self):
        node = Node([[1, -1, -1], [-1, -1, 6], [7, -1, 9]])
        ss = Search(node, [13, 15, 24], [12, 21, 18], [15, 15])
        result = ss.search(node)
        for i in result:
            print(i)
if __name__ == '__main__':
    unittest.main()
