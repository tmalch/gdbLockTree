import unittest
from ..commands import DeadlockDetection
from . import Utils
from ..LockTree import ThreadNode
from ..LockTree import LockNode
import random
import time
from ..Utils import DeadLock

from ..commands import DeadlockDetection as BaseLine
from ..commands import DeadlockDetection2 as PaperImpl
from ..commands import DeadlockDetection3 as Optimized1
from ..commands import DeadlockDetection4 as Optimized2

import cProfile
import pstats
        
class DeadLockTests(unittest.TestCase):
    def setUp(self):
        random.seed(6789)
        self.trees = [ThreadNode(tid) for tid in range(20) ]
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
        print("*********DeadlockDetection3**************")
        res = Optimized1.check(self.trees)
        res = Optimized1.check(self.trees)

    def test_time2(self):
        """ many large trees """
        print("*********DeadlockDetection4**************")
        res = Optimized2.check(self.trees)
        res = Optimized2.check(self.trees)

    def test_conformance(self):
        #self.pr.disable()
        random.seed(123)
        trees = [ThreadNode(0),ThreadNode(1)]
        (ltree,ltree2,introduced_deadlocks) = createDeadlockedPair(10,2)
        trees[0].addChild(ltree)
        trees[1].addChild(ltree2)

        base = [str(d) for d in BaseLine.check(self.trees)]
        res2 = [str(d) for d in Optimized1.check(self.trees)]
        res3 = [str(d) for d in Optimized2.check(self.trees)]

        self.assertCountEqual(base, res2)
        self.assertCountEqual(base, res3)

def gen_randomIndex(length):
    indexes = [i for i in range(0,length-1)]
    ri = random.randint(0,length-1)
    i = indexes[ri]
    del indexes[ri]
    yield i
    while len(indexes) > 0:
        ri = random.randint(0,len(indexes)-1)
        i = indexes[ri]
        del indexes[ri]
        yield i
        
def createDeadlockedPair(size,numdeadlocks=1):
    
    origtree_lockrange = (1,5*size)
    cpytree_lockrange = (5*size+1,10*size)
    #create tree
    (tree,nodelist) = Utils.randomTree(size, origtree_lockrange)
    #copy tree
    import copy
    nodelist_cpy = copy.deepcopy(nodelist)
    tree_cpy = nodelist_cpy[0]
    #change all locks of copy
    for n in nodelist_cpy:
        n.value = random.randint(cpytree_lockrange[0],cpytree_lockrange[1])
    #insert deadlocks
    index_gen = gen_randomIndex(len(nodelist))
    deadlocklist = list()
    used = list()
    while numdeadlocks > 0:
        try:
            indexP = next(index_gen)
        except StopIteration:
            print("was not able insert all deadlocks; "+str(numdeadlocks)+" Deadlocks missing" )
            break
        nodeP = nodelist[indexP]
        if nodeP.isLeaf():
            continue
        nodeC = random.choice([n for n in nodeP.getDescendants() if n != nodeP])
        indexC = nodelist.index(nodeC)
        if (indexP in used) or (indexC in used):
            continue
        used.extend([indexP,indexC])
        used.extend([nodelist.index(p) for p in nodeP.getAllParents()])
        nodeP_cpy = nodelist_cpy[indexP]
        nodeC_cpy = nodelist_cpy[indexC]
        
        (nodeP_cpy.value,nodeC_cpy.value) = (nodeC.value, nodeP.value)
        deadlocklist.append(DeadLock((None,None),(nodeP,set([nodeC])),(nodeP_cpy,set([nodeC_cpy]))))
        numdeadlocks = numdeadlocks-1
    return (tree,tree_cpy,deadlocklist)
 
        
        