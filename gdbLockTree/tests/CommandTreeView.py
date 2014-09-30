import unittest
from gdbLockTree.commands import TreeView
from gdbLockTree.commands.AcquireRelease import ThreadNode
from gdbLockTree.commands.AcquireRelease import LockNode
from . import Utils


class GraphvizTests(unittest.TestCase):
    
    def test_showGraphwin1(self):
        """ empty tree list """
        TreeView.generateDotCode(None)
    def test_showGraphwin2(self):
        """ empty graph """
        TreeView.generateDotCode(ThreadNode(5))
        TreeView.generateDotCode(LockNode(5))
    def test_showGraphwin3(self):
        """ random tree """
        tree = ThreadNode(0)
        (root,_) = Utils.randomTree(15)
        tree.addChild(root)
        TreeView.generateDotCode(tree)

