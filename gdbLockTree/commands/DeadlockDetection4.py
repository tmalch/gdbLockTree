from ..Node import Node
from ..Utils import Thread
from ..LockTree import LockNode
from ..Utils import DeadLock
from gdbLockTree.LockTree import ThreadNode



def check(trees):
    """ checks for Deadlock between all Locktrees given a list of tree roots
        returns a list of possible deadlocks"""
    deadLocks = list()
    for t1 in trees:
        for t2 in trees:
            if t1 != t2:
                deadLocks.extend(checkTreePair(t1,t2))
    return deadLocks

def __intersect(nodeset1,nodeset2):
    """ intersect two sequences by using the function cmp to compare their elements 
        returns a list with intersecting elements for each of the two sets"""
    intersection1 = list()
    intersection2 = list()
    for node1 in nodeset1:
        for node2 in nodeset2:
            if node1.value == node2.value:
                intersection1.append(node1)
                intersection2.append(node2)
    return (set(intersection1),set(intersection2))


Above = dict()
Below = dict()
def getBelow(node):
    if node in Below:
        return Below[node]
    l = node.getDescendantsList()
    del l[0]
    Below[node] = l
    return l
def getAbove(node):
    if node in Above:
        return Above[node]
    if node.isRoot():
        l=[]
        Above[node] = l
        return l
    else:
        l = [n for n in node.getAllParents() ]
        del l[0]
        del l[-1]
        Above[node] = l
        return l

def checkTreePair(tree1,tree2):
    """ returns list of all nodes that may cause a deadlock between thread t1 and t2"""
    deadlocks = list()
    for node1 in tree1.getDescendantsList():
        if not isinstance(node1, LockNode):
            continue
        t1below_node = getBelow(node1)
        t1above_node = getAbove(node1)
        for node2 in tree2.findAll(node1.value):
            t2above_node = getAbove(node2)
            (t1gatelocks,t2gatelocks) = __intersect(t1above_node, t2above_node)
            if len(t1gatelocks) == 0:
                (t1deadlocks,t2deadlocks) = __intersect(t1below_node,t2above_node)
                if len(t1deadlocks) > 0: #check for gatelock
                    deadlocks.append(DeadLock((tree1.value,tree2.value),(node1,t1deadlocks),(node2,t2deadlocks)))
    return deadlocks

    












