from collections import deque


class Node:
    def __init__(self,value,parent=None):
        self.parent = parent
        self.children = []
        self.value = value
    def __eq__(self, other):        
        if other == None:
            return False 
        if type(other) != Node:
            return False 
        return self.value == other.value
    def isRoot(self):
        return self.parent == None
    def isLeaf(self):
        return len(self.children) == 0
    def getNumChildren(self):
        return len(self.children)
    def getChild(self,query):
        for child in self.children:
            if child == query:
                return child
        #not found
        return None
    def addChild(self,childnode):
        childnode.parent = self
        self.children.append(childnode)
    def printNode(self,prefix=""):
        """ returns string representation of the subTree starting in self"""
        res = prefix+"|--"+str(self.value)+"\n"
        for n in self.children:
            res += n.printNode(prefix=prefix+"|  ")
        return res
    def __str__(self):
        return self.printNode()
        
        
        
    def getAllChildrenBFS_G(self):
        """ a Generator that returns all children of this node in BFS order
                this node as first"""    
        queue = deque([self])
        while len(queue) > 0:
            n = queue.popleft()
            yield n
            queue.extend(n.children)
            
            
    def find(self,query,order = getAllChildrenBFS_G):
        """find first occurence of query; Breadth First Search """
        for node in order(self):
            if node == query:
                return node
        
    def findAll(self,query,order = getAllChildrenBFS_G):
        """find all occurence of query; Breadth First Search """
        occurences = []
        for node in order(self):
            if node == query:
                occurences.append(node)
        return occurences

    def getAllParents(self):
        """returns list of all parents of this node up to the Root element"""
        return [node for node in self.getAllParents_G() ]

    def getAllParents_G(self):
        """a Generator which returns all parents of this node up to the Root element
                this node as first"""
        yield self
        if not self.isRoot():
            yield from self.parent.getAllParents_G()

    def getAllChildrenDFS_G(self):
        """ a Generator that returns all children of this node in DFS order
                this node as first"""    
        yield self
        for child in self.children:
            yield from child.getAllChildrenDFS_G()
            
    def isAbove(self,query):
        """returns True if this Node or any parent Node has requested value"""
        for p in self.getAllParents_G():
            if p == query:
                return True
        return False
    def isBelow(self,query):
        """returns True if this Node or any descendent Node has requested value (wrapper for find)"""
        r = self.find(query)
        if r == None:
            return False
        else:
            return True

