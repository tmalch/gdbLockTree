
#use graphviz for visualization of tree - disadvantage: non-interactive 
import os
import subprocess
import tempfile
from .. import Utils
from ..Node import Node as Node
import threading


def startGraphvizProcess(filename):
    p = subprocess.Popen(["dot","-Tx11", filename],
        stderr=subprocess.PIPE,
        shell=False,
        universal_newlines=True
    )
    return p

def renderDotCode(dotcode):
    """takes a graph description in dot language and executes the dot command for hierarchical rendering and displaying the result.
        is non-blocking"""
    try:
        with tempfile.NamedTemporaryFile(mode='w',delete=False) as f:
            f.write(dotcode)
        p = startGraphvizProcess(f.name)# has to be in a own functions because otherwise p.wait() would block the window because of any obscure reason i cannot determine
        (_, error) = p.communicate()
        if p.returncode != 0:
            print("graphviz dot command reported an error: " + error)
    except OSError as exc:
        print("an error occurred while executing graphviz's dot command (not installed?): "+ str(exc))
    except Exception as exc:
        print("an error occurred while starting graphviz process: "+ str(exc))
    finally:
        os.unlink(f.name)

def NodetoDot(node):
    if not isinstance(node, Node):
        return ""
    label = str(node.value)
    if node.value.info:
        label += "<BR/><FONT POINT-SIZE=\"8\" COLOR=\"grey\">"+node.value.info+"</FONT>"
    node_id = str(id(node))
    dot_node = "\""+node_id+"\"[label=<"+label+"> ];\n"
    if node.isRoot():
        return dot_node
    parent_node_id = str(id(node.parent))
    edge = "\""+parent_node_id+"\""+" -- "+"\""+node_id+"\";\n"
    return dot_node+edge

def generateDotCode(root):
    """ print the current locktree for the given ThreadID with graphviz"""
    if root is None:
        return
    dotCode = "graph G7 { \n node [fontsize=\"10\"];"
    for edge in root.mapSubtree(NodetoDot):
        dotCode += edge
    dotCode += "}"
    graphviz_thread = threading.Thread(target=renderDotCode,kwargs={'dotcode':dotCode})
    graphviz_thread.setDaemon(True)
    graphviz_thread.start()
    
    
