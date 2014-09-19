

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
    def __init__(self,involvedthreads,involvednodes):
        pass
    def __hash__(self):
        pass
    def __eq__(self, other):
        pass
