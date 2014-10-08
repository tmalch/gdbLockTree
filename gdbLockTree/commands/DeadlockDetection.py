
from ..Utils import DeadLock
from .AcquireRelease import LockNode


def check(trees_list):
    d = DeadlockDetection(trees_list)
    return d.detect()

class DeadlockDetection():
    def __init__(self,trees):
        self.trees = trees
        self.Above = dict()
        self.Below = dict()
        self.Lockmaps = DeadlockDetection.generateLockMaps(self.trees)

    def detect(self):
        """ checks for Deadlock between all Locktrees given a list of tree roots
            returns a list of possible deadlocks"""
        deadlocks = list()
        zipped = list(zip(self.trees,self.Lockmaps))
        for t1 in self.trees:
            for t2,lockmap2 in zipped:
                if t1 != t2:
                    deadlocks.extend(self.checkTreePair(t1,t2,lockmap2))
        return deadlocks

    def checkTreePair(self,tree1,tree2,lockmap2):
        """ returns list of all nodes that may cause a deadlock between thread t1 and t2"""
        deadlocks = list()
        for node1 in tree1.getDescendantsList():
            if not isinstance(node1, LockNode):
                continue
            t1below_node = self.getBelow(node1)
            t1above_node = self.getAbove(node1)
            if node1.value not in lockmap2:
                continue
            for node2 in lockmap2[node1.value]:
                t2above_node = self.getAbove(node2)
                (t1gatelocks,t2gatelocks) = self.intersect(t1above_node, t2above_node)
                if len(t1gatelocks) == 0:
                    (t1deadlocks,t2deadlocks) = self.intersect(t1below_node,t2above_node)
                    if len(t1deadlocks) > 0: #check for gatelock
                        deadlocks.append(DeadLock((tree1.value,tree2.value),(node1,t1deadlocks),(node2,t2deadlocks)))
        return deadlocks
    
    def generateLockMaps(trees):
        res = list()
        for tree in trees:
            res.append(DeadlockDetection.generateLockMap(tree))
        return res
    def generateLockMap(tree):
        d = dict()
        for node in tree.getDescendantsList():
            if not isinstance(node, LockNode):
                continue
            if node.value in d:
                d[node.value].append(node)
            else:
                d[node.value] = [node,]
        return d

    def getBelow(self,node):
        if node in self.Below:
            return self.Below[node]
        l = node.getDescendantsList()
        del l[0]
        self.Below[node] = l
        return l
    def getAbove(self,node):
        if node in self.Above:
            return self.Above[node]
        if node.isRoot():
            l=[]
            self.Above[node] = l
            return l
        else:
            l = [n for n in node.getAllParents() ]
            del l[0]
            del l[-1]
            self.Above[node] = l
            return l

    def intersect(self,nodeset1,nodeset2):
        """ intersect two sequences of nodes by their values 
            returns a list with intersecting nodes for each of the two sets"""
        intersection1 = list()
        intersection2 = list()
        for node1 in nodeset1:
            for node2 in nodeset2:
                if node1.value == node2.value:
                    intersection1.append(node1)
                    intersection2.append(node2)
        return (set(intersection1),set(intersection2))










