import unittest
import random
from gdbLockTree.tests import Utils
from gdbLockTree.Utils import DeadLock
from gdbLockTree.commands import DeadlockDetectionBase as Base
from gdbLockTree.commands import DeadlockDetectionPaper as PaperImpl
from gdbLockTree.commands import DeadlockDetection as Optimized
from gdbLockTree.commands.AcquireRelease import ThreadNode
import cProfile
import pstats
        
class DeadLockTests(unittest.TestCase):
    def setUp(self):
        random.seed()
        self.trees = [ThreadNode(tid) for tid in range(10) ]
        for tree in self.trees:
            (root,_) = Utils.randomTree(100)
            for n in root.children:
                tree.addChild(n)
        self.pr = cProfile.Profile()
        self.pr.enable()
    def tearDown(self):
        p = pstats.Stats(self.pr)
        p.strip_dirs()
        p.sort_stats ('cumtime')
        p.print_stats ()

    def test_time1(self):
        """ many large trees """
        print("*********DeadlockDetection2**************")
        res = PaperImpl.check(self.trees)


    def test_time2(self):
        """ many large trees """
        print("*********DeadlockDetection4**************")
        res = Optimized.check(self.trees)

    def test_lockDictGen(self):
        """ many large trees """
        print("*********DeadlockDetection4**************")
        res = Optimized.DeadlockDetection.generateLockMaps(self.trees)





        
        