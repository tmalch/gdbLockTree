import unittest
from gdbLockTree.commands import DeadlockDetectionBase as Base
from gdbLockTree.commands import DeadlockDetectionPaper as PaperImpl
from gdbLockTree.commands import DeadlockDetection
from gdbLockTree.commands.AcquireRelease import ThreadNode 

from . import Utils
from ..Utils import DeadLock
import random
import time

class DeadLockTests(unittest.TestCase):
    def test_empty1(self):
        """ no trees """
        res = DeadlockDetection.check([])
        self.assertListEqual(res, [])
    def test_empty2(self):
        """ only empty trees"""
        trees = [ThreadNode(tid) for tid in range(10) ]
        res = DeadlockDetection.check(trees)
        self.assertListEqual(res, [])
    def test_single1(self):
        """ one empty tree"""
        trees = [ThreadNode(0)]
        res = DeadlockDetection.check(trees)
        self.assertListEqual(res, [])
    def test_single2(self):
        """ one tree """
        trees = [ThreadNode(0)]
        (root,_) = Utils.randomTree(10)
        trees[0].addChild(root)
        res = DeadlockDetection.check(trees)
        self.assertListEqual(res, [])
    def test_single3(self):
        """ one tree + empty trees"""
        trees = [ThreadNode(tid) for tid in range(10) ]
        (root,_) = Utils.randomTree(10)
        trees[0].addChild(root)
        res = DeadlockDetection.check(trees)
        self.assertListEqual(res, [])
    def test_trees1(self):
        """ two trees without intersecting locks """
        trees = [ThreadNode(tid) for tid in range(10) ]
        (root1,_) = Utils.randomTree(20,(1,50))
        (root2,_) = Utils.randomTree(20,(55,100))
        trees[3].addChild(root1)
        trees[6].addChild(root2)
        res = DeadlockDetection.check(trees)
        self.assertListEqual(res, [])
    def test_trees2(self):
        """ two trees without intersecting locks double entrys """
        trees = [ThreadNode(tid) for tid in range(10) ]
        (root1,_) = Utils.randomTree(50,(1,20))
        (root2,_) = Utils.randomTree(50,(30,50))
        trees[3].addChild(root1)
        trees[6].addChild(root2)
        start = time.process_time()
        res = DeadlockDetection.check(trees)
        end = time.process_time()
        print("test_trees2 duration: "+str(end-start))
        self.assertListEqual(res, [])
    def test_trees3(self):
        """ two trees without intersecting locks double entrys """
        trees = [ThreadNode(tid) for tid in range(10) ]
        Utils.randomTree(50,(1,20),trees[3])
        Utils.randomTree(50,(30,50),trees[6])
        start = time.process_time()
        res = DeadlockDetection.check(trees)
        end = time.process_time()
        print("test_trees3 duration: "+str(end-start))
        self.assertListEqual(res, [])
    def test_trees4(self):
        """ 10 trees with intersecting locks and double entries """
        trees = [ThreadNode(tid) for tid in range(10) ]
        for tree in trees:
            Utils.randomTree(50,(1,20),tree)

        start = time.process_time()
        res = DeadlockDetection.check(trees)
        end = time.process_time()
        print("test_trees4 duration: "+str(end-start))


    def test_deadlock(self):
        random.seed(123)
        trees = [ThreadNode(0),ThreadNode(1)]
        (ltree,ltree2,introduced_deadlocks) = createDeadlockedPair(10,3)
        trees[0].addChild(ltree)
        trees[1].addChild(ltree2)
        
        print(trees[0].printSubTree())
        print(trees[1].printSubTree())
        start = time.process_time()
        res = DeadlockDetection.check(trees)
        end = time.process_time()
        print("test_trees4 duration: "+str(end-start))
        for d in introduced_deadlocks:
            print(d)
        for d in res:
            print(d)

    def test_conformance(self):
        random.seed(123)
        trees = [ThreadNode(0),ThreadNode(1)]
        (ltree,ltree2,introduced_deadlocks) = createDeadlockedPair(15,3)
        trees[0].addChild(ltree)
        trees[1].addChild(ltree2)

        res2 = PaperImpl.check(trees)
        res3 = DeadlockDetection.check(trees)

        nodup2 = set(res2)
        nodup3 = set(res3)
        diff = nodup2 ^ nodup3 
        print(str(sorted([str(i) for i in diff])))
        self.assertCountEqual(nodup2, nodup3)

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
        deadlocklist.append(DeadLock((0,1),(nodeP,set([nodeC])),(nodeC_cpy,set([nodeP_cpy]))))
        numdeadlocks = numdeadlocks-1
    return (tree,tree_cpy,deadlocklist)
 
        
        