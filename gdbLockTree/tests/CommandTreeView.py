import unittest
from ..commands import TreeView
from ..LockTree import ThreadNode
from . import Utils


class GraphvizTests(unittest.TestCase):
    
    def test_showGraphwin1(self):
        """ empty tree list """
        trees = []
        TreeView.generateDotCode(trees, 5)
    def test_showGraphwin2(self):
        """ empty graph """
        trees = [ThreadNode(tid) for tid in range(10)]
        TreeView.generateDotCode(trees, 5)
    def test_showGraphwin3(self):
        """ not existing thread """
        trees = [ThreadNode(tid) for tid in range(10)]
        TreeView.generateDotCode(trees, 11)
    def test_showGraphwin4(self):
        """ random tree """
        trees = [ThreadNode(tid) for tid in range(10)]
        (root,_) = Utils.randomTree(15)
        trees[5].addChild(root)
        TreeView.generateDotCode(trees, 5)

