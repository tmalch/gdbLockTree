from ..Utils import Thread
from .AcquireRelease import LockNode
from ..Utils import DeadLock



def newNode(trees, newnode):
    """ callback if new node is added"""
    root = [n for n in newnode.getAllParents_G if n.isRoot ][0]
    if not isinstance(root.value, Thread):
        return
    continousCheck(trees, root,newnode)

def continousCheck(trees, changedTree, addedNode):
    node1 = addedNode
    above_node1 = [n for n in node1.getAllParents() if ((n is not node1) and (n is not changedTree))] 
    for tree in trees:
        if tree is changedTree:
            continue
        for node2 in tree.findAll(node1.value):
            above_node2 = [n for n in node2.getAllParents_G() if ((n is not node2) and (n is not tree))  ] 
            (gates1,gates2) = __intersect(above_node1, above_node2)

            below_node2 = [n for n in node2.getDescendants() if n is not node2]
            (d1,d2) = __intersect(above_node1, below_node2)
            #in changedTree deadlock between node1 and dC
            #in tree deadlock between node2 and d2

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



def checkTreePair(tree1,tree2):
    """ returns list of all nodes that may cause a deadlock between thread t1 and t2"""
    deadlocks = list()
    for node1 in tree1.getDescendants():
        if not isinstance(node1, LockNode):
            continue
        t1below_node = [ n for n in node1.getDescendants() if n is not node1 ]
        t1above_node = [n for n in node1.getAllParents_G() if ((n is not node1) and (n is not tree1)) ]
        for node2 in tree2.findAll(node1.value):
            t2above_node = [ n for n in node2.getAllParents_G() if ((n is not node2) and (n is not tree2))]
            (t1gatelocks,t2gatelocks) = __intersect(t1above_node, t2above_node)
            if len(t1gatelocks) == 0:
                (t1deadlocks,t2deadlocks) = __intersect(t1below_node,t2above_node)
                if len(t1deadlocks) > 0: #check for gatelock
                    deadlocks.append(DeadLock((tree1.value,tree2.value),(node1,t1deadlocks),(node2,t2deadlocks)))
    return deadlocks
