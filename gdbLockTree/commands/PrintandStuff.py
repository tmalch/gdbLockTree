
from .AcquireRelease import LockNode
from .AcquireRelease import ThreadNode
from ..Utils import Thread
from ..Utils import nicestr

def printThreads(trees):
    """returns 2 list of strings; fist one contains the unique id, second one the human readable infos of all threads as string"""
    ids = []
    infos = []
    for n in trees:
        if isinstance(n.value, Thread):
            ids.append(str(n.value))
            infos.append(str(n.value.info))
    return (ids,infos)


def uselessLocks(trees):
    """ reports all Locks that are only used in a single thread as a list of Lock obj"""
    counted_locks = dict()
    for tree in trees:
        lockset = set([n.value for n in tree.getDescendants() if isinstance(n, LockNode)]) #using a set so that a lock is counted only once if it occurs multiple times in a Locktree
        for lid in lockset:
            if lid in counted_locks:
                (count,_) = counted_locks[lid]
                counted_locks[lid] = (count + 1,tree.value)
            else:
                counted_locks[lid] = (1,tree.value)
    
    useless_locks = []
    for lock,(count,thread) in counted_locks.items():
        if count == 1:
            useless_locks.append((lock,thread))#lock is useless
    return useless_locks

def printHoldLocks(tree):
    """ returns list with all locks hold at the moment by the given thread """
    if tree is None:
        return
    if type(tree) is not ThreadNode:
        print("not a locktree root")
        return
    hold_lock_nodes = tree.currentNode.getAncestorList()
    hold_lock_nodes = hold_lock_nodes[:-1]
    if not hold_lock_nodes:
        return ["No Locks hold at the moment"]
    res = list()
    for locknode in hold_lock_nodes:
        lockstr = locknode.value.nicestr()
        lockstr += " "+str(len(locknode.getCallLocations()))+" calls"
        lockstr += "\n" 
        for loc in locknode.getCallLocations():
            lockstr += str(loc) + "\n"
        res.append(lockstr)
    return res

def printLockInfo(trees,query):
    lock = None
    threadcount = 0
    call_locations = []
    for tree in trees:
        occurrences = tree.findAll(query)
        if occurrences:
            if lock is None:
                lock = occurrences[0].value
            threadcount += 1
            threadstr = "Thread "+nicestr(tree.value)+" called the lock from \n"
            for n in occurrences:
                for loc in n.getCallLocations():
                    threadstr += str(loc) + "\n"
            threadstr += "---------------------------------------------\n"
            call_locations.append(threadstr)
    if lock:
        res = lock.nicestr()+" \n"
        res += str(threadcount)+" Thread call this lock \n"
        res += " ".join(call_locations)
        return res
    else:
        return None
        
def LockNodetoStr(locknode):
        lockstr = locknode.value.nicestr()
        lockstr += " "+str(len(locknode.getCallLocations()))+" calls"
        lockstr += "\n"
        for loc in locknode.getCallLocations():
            lockstr += "  "+str(loc) + "\n"
        return lockstr

def printTree(tree):
    return printSubTree(tree)

def printSubTree(node,prefix=""):
    """ returns string representation of the subTree starting in node"""
    if node is None:
        return ""
    res = prefix+"|--"+nicestr(node.value)+"\n"
    for n in node.children:
        res += printSubTree(n,prefix=prefix+"|  ")
    return res