import unittest
from gdbLockTree.commands import PrintandStuff
from gdbLockTree.commands.AcquireRelease import ThreadNode
import random
from . import Utils

class PrintTests(unittest.TestCase):
    def setUp(self):
        pass
    def test_printThreads1(self):
        trees = []
        exp_res = [] 
        res = PrintandStuff.printThreads(trees)
        self.assertListEqual(res, exp_res)
    def test_printThreads2(self):
        trees = [ThreadNode(tid) for tid in range(10) ]
        exp_res = [str(tid) for tid in range(10)] 
        res = PrintandStuff.printThreads(trees)
        self.assertListEqual(res, exp_res)

    def test_uselessLocks1(self):
        trees = []
        exp_res = []
        res = PrintandStuff.uselessLocks(trees)
        self.assertCountEqual(res, exp_res)
    def test_uselessLocks2(self):
        trees = [ThreadNode(0)]
        exp_res = []
        res = PrintandStuff.uselessLocks(trees)
        self.assertCountEqual(res, exp_res)
    def test_uselessLocks3(self):
        trees = [ThreadNode(tid) for tid in range(10)]
        exp_res = []
        res = PrintandStuff.uselessLocks(trees)
        self.assertCountEqual(res, exp_res)
    def test_uselessLocks4(self):
        trees = [ThreadNode(tid) for tid in range(10)]
        (root,nodelist) = Utils.randomTree(20)
        random.choice(trees).addChild(root)
        exp_res = set([n.value for n in nodelist])
        res = PrintandStuff.uselessLocks(trees)
        self.assertCountEqual(res, exp_res)
    def test_uselessLocks5(self):
        trees = [ThreadNode(tid) for tid in range(10)]
        (root,nodelist) = Utils.randomTree(20)
        root_cpy = Utils.cloneTree(root)
        threadnode = trees[0]
        threadnode.addChild(root)
        threadnode_cpy = trees[9]
        threadnode_cpy.addChild(root_cpy)
        
        exp_res = []
        res = PrintandStuff.uselessLocks(trees)
        self.assertCountEqual(res, exp_res)
    def test_uselessLocks6(self):
        """ 2 Trees mit mehrfach vorhandenen locks aber keine überscheidung zw den locks"""
        trees = [ThreadNode(tid) for tid in range(10)]
        (locktree,nodelist1) = Utils.randomTree(20,(1,15))
        trees[2].addChild(locktree)
        (locktree,nodelist2) = Utils.randomTree(20,(20,35))
        trees[6].addChild(locktree)
        exp_res  = set([n.value for n in nodelist1]) ^ set([n.value for n in nodelist2])
        res = PrintandStuff.uselessLocks(trees)
        self.assertCountEqual(res, exp_res)
    def test_uselessLocks7(self):
        trees = [ThreadNode(tid) for tid in range(10)]
        for root in trees:
            (locktree,nodelist) = Utils.randomTree(20,(1,15))
            root.addChild(locktree)
        res = PrintandStuff.uselessLocks(trees)
        self.assertTrue(len(res) == 0)
        
    def test_printTree1(self):
        """ no LockNodes"""
        res = PrintandStuff.printTree(ThreadNode(random.randint(0,9)))
        print(res)
    def test_printTree2(self):
        """ only one LockNode """
        tree = ThreadNode(6)
        (root,_) = Utils.randomTree(1)
        tree.addChild(root)
        res = PrintandStuff.printTree(tree)
        print(res)
    def test_printTree3(self):
        """ large random tree """
        tree = ThreadNode(6)
        (root,_) = Utils.randomTree(50,(1,25))
        tree.addChild(root)
        res = PrintandStuff.printTree(tree) 
        print(res)
    def test_printTree5(self):
        """ empty tree list """
        res = PrintandStuff.printTree(None)
        print(res)
        















    
    
    