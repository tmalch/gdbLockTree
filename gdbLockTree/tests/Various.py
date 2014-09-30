import unittest
from ..Utils import DeadLock
from ..Node import Node
import random

class Various(unittest.TestCase):
    def setUp(self):
        unittest.TestCase.setUp(self)
        random.seed()
    def test_deadlockHashEq1(self):
        """ strange values"""
        t1 = None
        t2 = genRandomDeadlockObj();
        self.assertFalse(t1 == t2)
        self.assertFalse(t2 == t1)
        self.assertFalse(hash(t1) == hash(t2))
        t1 = Node("test")
        self.assertFalse(t1 == t2)
        self.assertFalse(t2 == t1)
        self.assertFalse(hash(t1) == hash(t2))
        th = (Node(None),Node(0))
        l = (Node(None),[Node(None)])
        t1 = DeadLock(th,l,l)
        self.assertTrue(hash(t1) == hash(t1))
        self.assertTrue(t1 == t1)
        t2 = DeadLock(th,(Node(None),[Node(None),Node(None)]),l)
        self.assertTrue(hash(t1) == hash(t2))
        self.assertTrue(t1 == t2)
        
    def test_deadlockHashEq2(self):
        """ euals self and copys"""
        t1 = genRandomDeadlockObj();
        self.assertTrue(t1 == t1)
        self.assertTrue(hash(t1) == hash(t1))
        import copy
        t2 = copy.copy(t1)
        self.assertTrue(t1 == t2)
        self.assertTrue(hash(t1) == hash(t2))
        t3 = copy.deepcopy(t1)
        self.assertTrue(t3 == t1)
        self.assertTrue(hash(t3) == hash(t1))
        
    def test_deadlockHashEq3(self):
        """ equals with non-numerical Node values"""
        th = (Node("dfgsdgf"),Node(9))
        l = (Node(345),[Node("ghjkl"),Node(8926)])
        t1 = DeadLock(th,l,l)
        self.assertTrue(t1 == t1)
        self.assertTrue(hash(t1) == hash(t1))
        t2 = DeadLock(th,(Node(345),[Node("ghjkl"),Node(8926),Node(8926)]),l)
        self.assertTrue(t2 == t1)
        self.assertTrue(hash(t2) == hash(t1))
        
    def test_deadlockHashEq4(self):
        for i in range(100):  
            t1 = genRandomDeadlockObj();
            t2 = genRandomDeadlockObj();
            self.assertEqual((t1 == t2) ,(hash(t1) == hash(t2)))
    def test_deadlockHashEq5(self):
        """ test deadlock with set operations"""
        res2 = [genRandomDeadlockObj() for i in range(50)]
        res3 = [genRandomDeadlockObj() for i in range(50)]
        nodup2_own = nodup(res2)
        nodup3_own = nodup(res3)
        diff_own = intersect(res2,res3)
        nodup2 = set(res2)
        nodup3 = set(res3)
        diff = nodup2 ^ nodup3 
        self.assertCountEqual(nodup2, nodup2_own)
        self.assertCountEqual(nodup3_own, nodup3)
        self.assertCountEqual(diff, diff_own)

def genRandomDeadlockObj():
    locknode = Node(random.randint(0,99999))
    lockset = random.sample(range(10000000), random.randint(1,5))
    locknodeset = [Node(l) for l in lockset]
    return DeadLock((random.randint(0,99),random.randint(100,200)), (locknode,locknodeset), (locknode,locknodeset))

def nodup(duplist):
    r = []
    for d in duplist:
        if d not in r:
            r.append(d)
    return r

def intersect(l1,l2):
    l = list()
    for node1 in l1:
        if node1 not in l2:
            l.append(node1)
    for node2 in l2:
        if node2 not in l1:
            l.append(node2)
    return nodup(l) 