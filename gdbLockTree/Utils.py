

def getTreeForThread(trees,thread):
    """returns the first node with thread as value from list trees
        None if it doesn't exist """
    for thread_root in trees:
        if thread_root.value == thread:
            return thread_root
    return None

def completeFromList(word,list):
    """returns list of possible completions of word out of list"""
    return [elem for elem in list if elem.startswith(word)]

def nicestr(obj):
    if hasattr(obj, "nicestr"):
        return obj.nicestr()
    else:
        return str(obj)
class Thread:
    def __init__(self,thread_id,thread_info=""):
        self.ID = thread_id
        self.info = thread_info

    def __eq__(self, other):
        if other == None:
            return False 
        if type(other) != Thread:
            return False
        return self.ID == other.ID
    def __hash__(self):
        return int(self.ID)
    def nicestr(self):
        res = str(self.ID)
        if self.info is not None:
            res += " -- ("+str(self.info)+")"
        return res
    def __str__(self):
        return str(self.ID)
        
class Lock:
    def __init__(self,lockid,lock_location):
        """lockid: an unique integer identifying the lock (most likely the address)"""
        self.ID = int(lockid)
        self.info = lock_location
    def __eq__(self, other):
        if other == None:
            return False 
        if type(other) != Lock:
            return False
        return self.ID == other.ID
    def __hash__(self):
        return self.ID
    def nicestr(self):
        lockstr = str(hex(self.ID))
        if self.info is not None:
            lockstr += " -- ("+str(self.info)+")"
        return lockstr
    def __str__(self):
        return str(hex(self.ID))

class DeadLock:
    """represents all information about a possible deadlock
        involvednodes: a tuple for each thread containing first the locknode that was checked
                        and second the list of nodes which trigger the deadlock with the first lock
        threads: the two Threads that are involved, tuple of Thread objects """
    def __init__(self,involvedthreads,involvednodes_thread0,involvednodes_thread1):
        assert involvedthreads[0] != involvedthreads[1]
        assert involvednodes_thread0[0].value == involvednodes_thread1[0].value

        self.threads = (involvedthreads[0],involvedthreads[1])
        self.locknodes = (involvednodes_thread0[0],involvednodes_thread1[0])
        self.locknode_sets = (involvednodes_thread0[1],involvednodes_thread1[1])

        self.lock = self.locknodes[0].value
        lockset0 = frozenset([n.value for n in self.locknode_sets[0]])
        lockset1 = frozenset([n.value for n in self.locknode_sets[1]])
        assert lockset0 == lockset1 #both nodesets must have the same locks
        self.lockset = lockset0
    def __str__(self):
        res = "between "+str(self.threads[0])+" and "+str(self.threads[1])+"::"+"\n"
        res += str(self.lock)+" with "+str([i for i in self.lockset])+"\n"
        return res
    def __hash__(self):
        return hash((self.threads,self.lock,self.lockset) )
    def __eq__(self, other):
        """ 2 deadlocks are equal if the same threads are involved and
            the same lock has a deadlock with the same other locks (lockset) """
        if other == None:
            return False 
        if type(other) != DeadLock:
            return False
        if self.threads[0] not in other.threads or self.threads[1] not in other.threads:
            return False
        if self.lock != other.lock:
            return False
        
        return (self.lockset == other.lockset)

        
        
        
        
        
        