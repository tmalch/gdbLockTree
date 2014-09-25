import random
from ..LockTree import LockNode


def randomTree(size,valrange=(1,100),root=None):
    values = [ random.randint(valrange[0],valrange[1]) for _ in range(size)]
    if root is None:
        root = LockNode(values[0])
        values = values[1:]
    nodelist = [root]
    for lid in values:
        rnd_parent = random.choice(nodelist)
        new_node = LockNode(lid)
        rnd_parent.addChild(new_node)
        nodelist.append(new_node)
    return (root,nodelist)

def cloneTree(root):
    import copy
    return copy.deepcopy(root)