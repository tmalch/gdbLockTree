from ..Utils import DeadLock
from gdbLockTree.LockTree import LockNode


Above = dict()
Below = dict()
def check(trees):
    """ checks for Deadlock between all Locktrees given a list of tree roots
        returns a list of possible deadlocks"""
    global Above,Below
    Above = dict()
    Below = dict()
    deadLocks = list()
    generateLockMaps(trees)
    for t1 in trees:
        for t2 in trees:
            if t1 != t2:
                deadLocks.extend(checkTreePair(t1,t2))
    return deadLocks

def checkTreePair(tree1,tree2): # http://ti.arc.nasa.gov/m/pub-archive/archive/0177.pdf
    deadlist = list()
    for child in tree1.children:
        deadlist.extend(analyzeThis(tree1,child,tree2))
    return deadlist
def notBelowMark(node):
    for n in node.getAncestorList():
        if "mark" in n.attributes and n.attributes["mark"] == True:
            return False
    return True
def checkO(node1,below_node1,node2,tree1,tree2):
    above_node2 = getAbove(node2)
    (node1_,node2_) = __intersect(below_node1 ,above_node2)
    if len(node1_) > 0:
        return DeadLock((tree1.value,tree2.value),(node1,node1_),(node2,node2_))
def analyzeThis(tree1,node1,tree2):
    deadlist = list()
    if node1.value not in tree2.attributes["map"]:
        return []
    found = tree2.attributes["map"][node1.value]
    N = [n for n in found if notBelowMark(n)]
    below_node1 = getBelow(node1)
    for node2 in N:
        deadlock = checkO(node1,below_node1,node2,tree1,tree2)
        if deadlock != None:
            deadlist.append(deadlock)
    for n in N:
        n.attributes["mark"] = True
    for child in node1.children:
        deadlist.extend(analyzeThis(tree1,child,tree2))
    for n in N:
        n.attributes["mark"] = False
    return deadlist
        
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

def generateLockMaps(trees):
    for tree in trees:
        d = dict()
        for node in tree.getDescendantsList():
            if not isinstance(node, LockNode):
                continue
            if node.value in d:
                d[node.value].append(node)
            else:
                d[node.value] = [node,]
        tree.attributes["map"] = d










