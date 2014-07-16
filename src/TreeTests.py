import random
import unittest
from lockForrest import Node

class BasicTreeTests(unittest.TestCase):
		def setUp(self):
			pass

		def test_TreeBasic1(self):
			n = Node(0)
			self.assertTrue(n.isRoot())
			self.assertTrue(n.isLeaf())
    
		def test_TreeBasic2(self):
			root = Node(0)
			l = Node(1)
			root.addChild(l)
			self.assertTrue(root.isRoot())
			self.assertTrue(l.isLeaf())
    
		def test_TreeBasic3(self):
			root = Node(0)
			l = Node(1)
			root.addChild(l)
			self.assertTrue(root.isRoot())
			self.assertTrue(l.isLeaf())
			self.assertIs(root.children[0],l)
		def test_TreeBasic4(self):
			root = Node(0)
			for i in range(10):
				root.addChild(Node(i))
			self.assertEqual(root.getNumChildren(),10)
			
		def test_TreeBasic5(self):
			root = Node(0)
			for i in range(10):
				root.addChild(Node(i))
			n = Node(11)
			root.addChild(n)
			f = root.find(Node(11))
			self.assertIs(n,f)
			self.assertEqual(n,f)
		
		def test_TreeBasic6(self):
			root = Node(0)
			for i in range(10):
				root.addChild(Node(i))
			n = Node(11)
			root.addChild(n)
			f = root.findAll(Node(11))
			self.assertEqual(len(f),1)
			self.assertIs(n,f[0])
			self.assertEqual(n,f[0])
		
		def test_TreeBasic7(self):
			root = Node(0)
			for i in range(10):
				root.addChild(Node(i))
			n = Node(9)
			root.addChild(n)
			f = root.findAll(Node(9))
			self.assertEqual(len(f),2)
			self.assertIn(n,f)
				
		def test_TreeBasic8(self):
			root = Node(0)
			n = Node(11)
			root.addChild(n)
			p = n.getAllParents()
			
			self.assertIs(n,p[0])
			self.assertIs(root,p[1])
			
			cb =  [x for x in root.getAllChildrenBFS_G()]
			self.assertEqual(len(cb),2)
			self.assertIs(root,cb[0])
			self.assertIs(n,cb[1])
			cd =  [x for x in root.getAllChildrenDFS_G()]
			self.assertEqual(len(cd),2)
			self.assertIs(root,cd[0])
			self.assertIs(n,cd[1])
			
		def test_TreeBasic9(self):
			root = Node(0)
			l1_0 = Node(1)
			l1_1 = Node(2)
			l2 = Node(10)
			root.addChild(l1_0)
			root.addChild(l1_1)
			l1_0.addChild(l2)
			
			p = l2.getAllParents()
			self.assertEqual(len(p),3)
			self.assertIs(l2,p[0])
			self.assertIs(l1_0,p[1])
			self.assertIs(root,p[2])
			
			cb =  [x for x in root.getAllChildrenBFS_G()]
			self.assertIs(root,cb[0])
			self.assertIs(l1_0,cb[1])
			self.assertIs(l1_1,cb[2])
			self.assertIs(l2,cb[3])
			
			cd =  [x for x in root.getAllChildrenDFS_G()]
			self.assertIs(root,cd[0])
			self.assertIs(l1_0,cd[1])
			self.assertIs(l2,cd[2])
			self.assertIs(l1_1,cd[3])
			
		def test_TreeBasic10(self):
			size = 15
			root, val = self.buildRandomTree(size)
			self.assertEqual(len(val),size)
			self.assertEqual(len([x for x in root.getAllChildrenBFS_G()]),size)
			self.assertEqual(len([x for x in root.getAllChildrenDFS_G()]),size)
			
			elem = random.choice(val)
			self.assertEqual(len(root.findAll(Node(elem),Node.getAllChildrenDFS_G)),val.count(elem))
			elem = random.choice(val)
			self.assertEqual(len(root.findAll(Node(elem),Node.getAllChildrenBFS_G)),val.count(elem))
		
		def buildRandomTree(self,size):
			s2 = int(size/10)
			s1 = size - s2*2
			values = [ random.randint(1, 1000) for x in range(s1)]
			values.extend(2*[ random.randint(1000,2000) for x in range(s2)])
			root = Node(values[0])
			nodes = [root]
			r = root
			for v in values[1:]:
				n = Node(v)
				nodes.append(n)
				r.addChild(n)
				r = random.choice(nodes)
			return (root,values)
			
