
from ..Node import Node
from .. import Utils

class LockNode(Node):
    def __init__(self,lock,call_location=None,parent=None):
        Node.__init__(self, lock, parent)
        self.attributes['callLocations'] = set([call_location])
        
    def addCallLoc(self,call_loc):
        if call_loc is not None:
            self.attributes['callLocations'].update(call_loc)

class ThreadNode(Node): 
    """  represents lockTree of one Thread"""
    def __init__ (self,thread):
        Node.__init__(self, thread, None)
        self.currentNode = self
 
def acquire(trees,thread,lock,call_location=None):
    if lock is None or thread is None:
        return
    treeroot = Utils.getTreeForThread(trees,thread)
    if treeroot is None:
        treeroot = ThreadNode(thread)
        trees.append(treeroot) 

    currentNode = treeroot.currentNode
    #if currentNode.isAbove(lock):
        #print("reentrant lock: Lock "+str(lock)+" is still acquired")
        # reentrant locks get added again
    if currentNode.findChild(lock) != None:
        # follow given path if already taken in the past
        treeroot.currentNode = currentNode.findChild(lock)
    else:
        childnode = LockNode(lock)
        currentNode.addChild(childnode)
        treeroot.currentNode = childnode
    treeroot.currentNode.addCallLoc(call_location)

def release(trees,thread,lock,call_location=None):
    if lock is None or thread is None:
        return
    treeroot = Utils.getTreeForThread(trees,thread)
    if treeroot is None:
        #print("ERROR? thread never acquired lock but releases it")
        treeroot = ThreadNode(thread)
        trees.append(treeroot)      
        
    currentNode = treeroot.currentNode
    if currentNode.value == lock:
        currentNode.addCallLoc(call_location)
        treeroot.currentNode = currentNode.parent
    else:# locks are not nested properly
        if currentNode.isAbove(lock):
            still_acquired = []
            for n in currentNode.getAllParents_G(): 
                if n.value == lock: 
                    releasedNode = n
                    break
                else:
                    still_acquired.append(n)
            releasedNode.addCallLoc(call_location)
            treeroot.currentNode = releasedNode.parent
            still_acquired.reverse()
            #add a copy of all still acquired Locks as children to the Lock above the released one
            for node in still_acquired:
                acquire(trees,thread,node.value)
        else:
            print("ERROR? release not acquired lock"+str(lock))

                