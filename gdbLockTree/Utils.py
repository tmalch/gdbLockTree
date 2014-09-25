

def getTreeForThread(trees,thread):
    for thread_root in trees:
        if thread_root.value == thread:
            return thread_root
    return None

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
    def __str__(self):
        return str(self.info)+":"+str(self.ID)
        
class Lock:
    def __init__(self,lockid,lock_location):
        self.ID = lockid
        self.info = lock_location
    def __eq__(self, other):
        if other == None:
            return False 
        if type(other) != Lock:
            return False
        return self.ID == other.ID
    def __hash__(self):
        return int(self.ID)
    def __str__(self):
        return str(self.ID)

class DeadLock:
    """represents all information about a possible deadlock
        involvednodes: two lists of nodes which locks have triggered the warning
        involvedthreads: the Threads that are involved, list of Thread objects """
    def __init__(self,involvedthreads,involvednodes_thread1,involvednodes_thread2):
        self.involvedthreads = involvedthreads
        self.involvednodes_thread1 = involvednodes_thread1
        self.involvednodes_thread2 = involvednodes_thread2
    def __str__(self):
        involvednodes_thread1 = str(self.involvednodes_thread1[0]) 
        involvednodes_thread1 = involvednodes_thread1+ " "+str([str(n) for n in self.involvednodes_thread1[1]])
        involvednodes_thread2 = str(self.involvednodes_thread2[0]) + " "+str([str(n) for n in self.involvednodes_thread2[1]])
        return "between "+str(self.involvedthreads[0])+" and "+str(self.involvedthreads[1])+" ::\n "+involvednodes_thread1+"\n"+involvednodes_thread2
    def __hash__(self):
        pass
    def __eq__(self, other):
        pass
        
        