import unittest
from ..commands import DeadlockDetection
from . import Utils
from ..LockTree import ThreadNode
from ..LockTree import LockNode
import random
import time
from ..Utils import DeadLock

from ..commands import DeadlockDetection as Base
from ..commands import DeadlockDetection2 as PaperImpl
from ..commands import DeadlockDetection4 as Optimized2

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
        res = Optimized2.check(self.trees)


    def test_conformance(self):
        self.pr.disable()
        random.seed(123)
        trees = [ThreadNode(0),ThreadNode(1)]
        (ltree,ltree2,introduced_deadlocks) = createDeadlockedPair(15,3)
        trees[0].addChild(ltree)
        trees[1].addChild(ltree2)

        res2 = PaperImpl.check(self.trees)
        res3 = Optimized2.check(self.trees)
        res = []
        for d in res2:
            if d not in res:
                res.append(d)
        res2_d = res        
        res = []
        for d in res3:
            if d not in res:
                res.append(d)
        res3_d = res
        str_res2 = [str(d) for d in res2]
        str_res3 = [str(d) for d in res3]
        str_res2_d = [str(d) for d in res2_d]
        str_res3_d = [str(d) for d in res3_d]
        with open("paper.txt", "w") as file:
            for r in str_res2:
                file.write(r+"\n")
            file.write("----------------------\n")
            for r in str_res2_d:
                file.write(r+"\n")
            for tree in self.trees:
                file.write(tree.printSubTree())

        with open("mine.txt", "w") as file:
            for r in str_res3:
                file.write(r+"\n")
            file.write("----------------------\n")
            for r in str_res3_d:
                file.write(r+"\n")
            for tree in self.trees:
                file.write(tree.printSubTree())
        print(str_res3)
        self.assertCountEqual(str_res3_d, str_res2_d)


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
 
        
        