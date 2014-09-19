from collections import deque


class Node:
    def __init__(self,value,parent=None):
        self.parent = parent
        self.children = []
        self.value = value
        self.attributes = {}
    def isRoot(self):
        return self.parent == None
    def isLeaf(self):
        return len(self.children) == 0
    def getNumChildren(self):
        return len(self.children)
    def findChild(self,query):
        for child in self.children:
            if child.value == query:
                return child
        return None #not found
    def addChild(self,childnode):
        childnode.parent = self
        self.children.append(childnode)
    def __str__(self):
        return str(self.value)
        
# Methods operating on the SubTree
    def subTreeSize(self):
        return len([0 for i in self.getAllChildrenDFS_G()])
    def printSubTree(self,prefix=""):
        """ returns string representation of the subTree starting in self"""
        res = prefix+"|--"+str(self.value)+"\n"
        for n in self.children:
            res += n.printSubTree(prefix=prefix+"|  ")
        return res
   
    def getAllChildrenBFS_G(self):
        """ a Generator that returns all children of this node in BFS order
                this node as first"""  
        yield from self.filterSubtreeBFS(lambda n: True)  
            
    def filterSubtreeBFS(self,query):
        queue = deque([self])
        while len(queue) > 0:
            n = queue.popleft()
            if query(n) == True:
                yield n
            queue.extend(n.children)
            
    def filterSubtreeDFS(self,query): 
        if query(self):
            yield self
        for child in self.children:
            yield from child.filterSubtreeDFS(query)

    def mapSubtree(self,function): 
        yield function(self)
        for child in self.children:
            yield from child.mapSubtree(function) 
    
        
    def getAllChildrenDFS_G(self):
        """ a Generator that returns all children of this node in DFS order
                this node as first"""    
        yield from self.filterSubtreeDFS(lambda n: True)

    getAllChildren = getAllChildrenDFS_G

    def find(self,query,order = getAllChildrenBFS_G):
        """find the node of first occurrences of value 'query'; Breadth First Search """
        for node in order(self):
            if node.value == query:
                return node
        
    def findAll(self,query,order = getAllChildrenBFS_G):
        """find all Nodes in which the value 'query' occurs; Breadth First Search """
        occurrences = []
        for node in order(self):
            if node.value == query:
                occurrences.append(node)
        return occurrences

    def getAllParents(self):
        """returns list of all parents of this node up to the Root element"""
        return [node for node in self.getAllParents_G() ]

    def getAllParents_G(self):
        """a Generator which returns all parents of this node up to (including) the Root element
                this node as first"""
        yield self
        if not self.isRoot():
            yield from self.parent.getAllParents_G()

    def branch_G(self):
        """ returns all branches of the subtree rooted in this node as lists"""
        branch = []
        prev_branch = []
        for n in self.getAllChildrenDFS_G():
            if n.parent in prev_branch:
                branch = prev_branch[:prev_branch.index(n.parent)+1]
            branch.append(n)
            if n.isLeaf():
                yield branch
                prev_branch = branch 
                branch = []
         
    def isAbove(self,query):
        """returns True if this Node or any parent Node has requested value"""
        for p in self.getAllParents_G():
            if p.value == query:
                return True
        return False
    def isBelow(self,query):
        """returns True if this Node or any descendent Node has requested value (wrapper for find)"""
        r = self.find(query)
        if r == None:
            return False
        else:
            return True

