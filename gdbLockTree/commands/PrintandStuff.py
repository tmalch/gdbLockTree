
from .AcquireRelease import LockNode
from ..Utils import Thread

def printThreads(trees):
    """returns list of string representations of all threads that have a lockTree"""
    ids = []
    infos = []
    for n in trees:
        if isinstance(n.value, Thread):
            ids.append(str(n.value.ID))
            infos.append(str(n.value.info))
    return (ids,infos)


def uselessLocks(trees):
    """ reports all Locks that are only acquired in a single thread as a list of Lock obj"""
    counted_locks = dict()
    for tree in trees:
        lockset = set([n.value for n in tree.getDescendants() if isinstance(n, LockNode)]) #so that a lock is counted only once if it occurs multiple times in a Locktree
        for lid in lockset:
                counted_locks[lid] = counted_locks.get(lid,0) + 1
    
    useless_locks = []
    for lock,count in counted_locks.items():
        if count == 1:
            useless_locks.append(lock)#lock is useless
    return useless_locks


def printTree(tree):
    return printSubTree(tree)

def printSubTree(node,prefix=""):
    """ returns string representation of the subTree starting in node"""
    if node is None:
        return ""
    res = prefix+"|--"+str(node.value)+"\n"
    for n in node.children:
        res += printSubTree(n,prefix=prefix+"|  ")
    return res