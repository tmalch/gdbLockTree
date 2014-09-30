import random
import unittest

from gdbLockTree.Node import Node
from gdbLockTree.tests import Utils


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
			f = root.find(11)
			self.assertIs(n,f)
			self.assertEqual(n,f)
		
		def test_TreeBasic6(self):
			root = Node(0)
			for i in range(10):
				root.addChild(Node(i))
			n = Node(11)
			root.addChild(n)
			f = root.findAll(11)
			self.assertEqual(len(f),1)
			self.assertIs(n,f[0])
			self.assertEqual(n,f[0])
		
		def test_TreeBasic7(self):
			root = Node(0)
			for i in range(10):
				root.addChild(Node(i))
			n = Node(9)
			root.addChild(n)
			f = root.findAll(9)
			self.assertEqual(len(f),2)
			self.assertIn(n,f)
				
		def test_TreeBasic8(self):
			root = Node(0)
			n = Node(11)
			root.addChild(n)
			p = list(n.getAllParents())
			
			self.assertIs(n,p[0])
			self.assertIs(root,p[1])
			
			cb =  [x for x in root.getDescendantsBFS_G()]
			self.assertEqual(len(cb),2)
			self.assertIs(root,cb[0])
			self.assertIs(n,cb[1])
			cd =  [x for x in root.getDescendantsDFS_G()]
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
			
			p = list(l2.getAllParents_G())
			self.assertEqual(len(p),3)
			self.assertIs(l2,p[0])
			self.assertIs(l1_0,p[1])
			self.assertIs(root,p[2])
			
			cb =  [x for x in root.getDescendantsBFS_G()]
			self.assertIs(root,cb[0])
			self.assertIs(l1_0,cb[1])
			self.assertIs(l1_1,cb[2])
			self.assertIs(l2,cb[3])
			
			cd =  [x for x in root.getDescendantsDFS_G()]
			self.assertIs(root,cd[0])
			self.assertIs(l1_0,cd[1])
			self.assertIs(l2,cd[2])
			self.assertIs(l1_1,cd[3])
			
		def test_TreeBasic9_1(self):
			root = Node(0)
			l1_0 = Node(1)
			l1_1 = Node(2)
			l2_0 = Node(10)
			l2_1 = Node(11)
			l3_0 = Node(30)
			l3_1 = Node(31)
			l3_1d = Node(31)
			
			root.addChild(l1_0)
			root.addChild(l1_1)
			l1_0.addChild(l2_0)
			l1_0.addChild(l2_1)
			l2_1.addChild(l3_0)
			l2_1.addChild(l3_1)
			
			l1_1.addChild(l3_1d)
			
			f = root.find(Node(5555),Node.getDescendantsBFS_G)
			self.assertEqual(f,None)
			f = root.find(Node(5555),Node.getDescendantsDFS_G)
			self.assertEqual(f,None)
			
			f = root.findAll(Node(5555))
			self.assertEqual(len(f),0)
			self.assertEqual(f,[])
			f = root.findAll(Node(5555))
			self.assertEqual(len(f),0)
			self.assertEqual(f,[])
			
			f = root.find(None,Node.getDescendantsBFS_G)
			self.assertEqual(f,None)
			f = root.find(None,Node.getDescendantsDFS_G)
			self.assertEqual(f,None)
			
			f = root.findAll(None)
			self.assertEqual(len(f),0)
			self.assertEqual(f,[])

			
			f = root.find(9,Node.getDescendantsBFS_G)
			self.assertEqual(f,None)
			f = root.find(9,Node.getDescendantsDFS_G)
			self.assertEqual(f,None)
			
			f = root.findAll(9)
			self.assertEqual(len(f),0)
			self.assertEqual(f,[])
			
		def test_TreeBasic10(self):
			size = 15
			root, val,dval = self.buildRandomTree(size)
			self.assertEqual(len(val),size)
			self.assertEqual(len([x for x in root.getDescendantsBFS_G()]),size)
			self.assertEqual(len([x for x in root.getDescendantsDFS_G()]),size)
			
			elem = random.choice(val)
			self.assertEqual(len(root.findAll(elem)),val.count(elem))
			elem = random.choice(val)
			self.assertEqual(len(root.findAll(elem)),val.count(elem))
		
		def test_TreeBasic11(self):
			size = 100
			root, val, dval = self.buildRandomTree(size)
			self.assertEqual(len(val),size)
			self.assertEqual(len([x for x in root.getDescendantsBFS_G()]),size)
			self.assertEqual(len([x for x in root.getDescendantsDFS_G()]),size)
						
			elem = random.choice(val)
			f = root.find(elem,Node.getDescendantsDFS_G)
			self.assertEqual(f.value,elem)
			f = root.find(elem,Node.getDescendantsBFS_G)
			self.assertEqual(f.value,elem)
			
			elem = random.choice(val)
			oc = root.findAll(elem)
			self.assertEqual(len(oc),val.count(elem))
			self.assertEqual(oc[0].value,elem)
			elem = random.choice(val)
			oc = root.findAll(elem)
			self.assertEqual(len(oc),val.count(elem))
			self.assertEqual(oc[0].value,elem)
			
			elem = random.choice(dval)
			oc = root.findAll(elem)
			self.assertEqual(len(oc),val.count(elem))
			self.assertEqual(oc[0].value,elem)
			self.assertEqual(oc[1].value,elem)			
			
			elem = random.choice(dval)
			oc = root.findAll(elem)
			self.assertEqual(len(oc),val.count(elem))
			self.assertEqual(oc[0].value,elem)
			self.assertEqual(oc[1].value,elem)
		
		def test_TreeBasic12(self):
			root = Node(0)
			l1_0 = Node(1)
			l1_1 = Node(2)
			l2_0 = Node(10)
			l2_1 = Node(11)
			l3_0 = Node(30)
			l3_1 = Node(31)
			l3_1d = Node(31)
			
			root.addChild(l1_0)
			root.addChild(l1_1)
			l1_0.addChild(l2_0)
			l1_0.addChild(l2_1)
			l2_1.addChild(l3_0)
			l2_1.addChild(l3_1)
			
			l1_1.addChild(l3_1d)
			
			f = root.find(30)
			self.assertIs(l3_0,f)
			self.assertEqual(f.value,30)
			
			f = l2_1.find(30)
			self.assertIs(l3_0,f)
			self.assertEqual(f.value,30)
			
			f = root.find(55)
			self.assertEqual(f,None)
			
			f = root.find(None)
			self.assertEqual(f,None)
			
			f = root.find(31,Node.getDescendantsDFS_G)
			self.assertIs(l3_1,f)
			self.assertEqual(f.value,31)
			f = root.find(31,Node.getDescendantsBFS_G)
			self.assertIs(l3_1d,f)
			self.assertEqual(f.value,31)
			
			f = root.findAll(31)
			self.assertEqual(len(f),2)
			
			p = list(l3_1.getAllParents())
			self.assertEqual(len(p),4)
			self.assertIs(p[0],l3_1)
			self.assertIs(p[1],l2_1)
			self.assertIs(p[2],l1_0)
			self.assertIs(p[3],root)
			
		def test_TreeBasic13(self):
			root = Node(0)
			l1_0 = Node(1)
			l1_1 = Node(2)
			l2_0 = Node(10)
			l2_1 = Node(None)
			l3_0 = Node(30)
			l3_1 = Node(31)
			l3_1d = Node(31)
			
			root.addChild(l1_0)
			root.addChild(l1_1)
			l1_0.addChild(l2_0)
			l1_0.addChild(l2_1)
			l2_1.addChild(l3_0)
			l2_1.addChild(l3_1)
			
			l1_1.addChild(l3_1d)
			
			f = root.find(30)
			self.assertIs(l3_0,f)
			self.assertEqual(f.value,30)
			
			f = l2_1.find(30)
			self.assertIs(l3_0,f)
			self.assertEqual(f.value,30)
			
			f = root.find(31,Node.getDescendantsDFS_G)
			self.assertIs(l3_1,f)
			self.assertEqual(f.value,31)
			f = root.find(31,Node.getDescendantsBFS_G)
			self.assertIs(l3_1d,f)
			self.assertEqual(f.value,31)
			
			f = root.findAll(31)
			self.assertEqual(len(f),2)
			
			p = list(l3_1.getAllParents())
			self.assertEqual(len(p),4)
			self.assertIs(p[0],l3_1)
			self.assertIs(p[1],l2_1)
			self.assertIs(p[2],l1_0)
			self.assertIs(p[3],root)
		def test_Treebranch(self):
			root = Node(0)
			l1_0 = Node(1)
			l1_1 = Node(2)
			l2_0 = Node(10)
			l2_1 = Node(None)
			l3_0 = Node(30)
			l3_1 = Node(31)
			l3_1d = Node(31)
			
			root.addChild(l1_0)
			root.addChild(l1_1)
			l1_0.addChild(l2_0)
			l1_0.addChild(l2_1)
			l2_1.addChild(l3_0)
			l2_1.addChild(l3_1)
			l2_0.addChild(l3_1d)
			
			b0 = [root, l1_0,l2_0,l3_1d] # 0, 1, 10, 31
			b1 = [root, l1_0,l2_1,l3_0]  # 0, 1, None, 30
			b2 = [root, l1_0,l2_1,l3_1]  # 0, 1, None, 31
			b3 = [root, l1_1] 			# 0, 2
			branches = [b for b in root.branch_G()]

			self.assertIn(b0, branches)
			self.assertIn(b1, branches)
			self.assertIn(b2, branches)
			self.assertIn(b3, branches)
			self.assertTrue(len(branches) == 4)
		def test_Treebranch2(self):
			root = Node(0)
			l1_0 = Node(10)
			l1_1 = Node(11)
			l2_0 = Node(20)
			l2_1 = Node(21)
			l3_0 = Node(30)
			l3_1 = Node(31)
			l3_1d = Node(31)
			
			root.addChild(l1_0)
			root.addChild(l1_1)
			l1_0.addChild(l2_0)
			l1_0.addChild(l2_1)
			l2_1.addChild(l3_0)
			
			b0 = [root, l1_0,l2_0] # 0, 1, 10, 31
			b1 = [root, l1_0,l2_1,l3_0]  # 0, 1, None, 30
			b2 = [root, l1_1] 			# 0, 2
			branches = [b for b in root.branch_G()]

			self.assertIn(b0, branches)
			self.assertIn(b1, branches)
			self.assertIn(b2, branches)
			self.assertTrue(len(branches) == 3)
		def test_Treebranch3(self):
			root = Node(0)
			l1_0 = Node(10)
			l1_1 = Node(11)
			l2_0 = Node(20)
			l2_1 = Node(21)
			l3_0 = Node(30)
			l3_1 = Node(31)
			l3_1d = Node(31)
			
			root.addChild(l1_0)
			root.addChild(l1_1)
			l1_0.addChild(l2_0)
			l1_1.addChild(l2_1)
			l2_0.addChild(l3_0)
			l2_1.addChild(l3_1)
			
			b0 = [root, l1_0,l2_0,l3_0] # 0, 1, 10, 31
			b1 = [root, l1_1,l2_1,l3_1]  # 0, 1, None, 30
			branches = [b for b in root.branch_G()]

			self.assertIn(b0, branches)
			self.assertIn(b1, branches)
			self.assertTrue(len(branches) == 2)
		def test_Treebranch4(self):
			root = Node(0)
			l1_0 = Node(10)
			l1_1 = Node(11)
			l2_0 = Node(20)
			l2_1 = Node(21)
			l3_0 = Node(30)
			l3_1 = Node(31)
			l3_1d = Node(31)
			
			root.addChild(l1_0)
			root.addChild(l1_1)
			l1_0.addChild(l2_0)
			l1_0.addChild(l2_1)
			l2_0.addChild(l3_0)
			l2_0.addChild(l3_1)
			
			b0 = [root, l1_0,l2_0,l3_0] # 0, 1, 10, 31
			b1 = [root, l1_0,l2_0,l3_1]  # 0, 1, None, 30
			b2 = [root, l1_0,l2_1]
			b3 = [root, l1_1]
			branches = [b for b in root.branch_G()]

			self.assertIn(b0, branches)
			self.assertIn(b1, branches)
			self.assertIn(b2, branches)
			self.assertIn(b3, branches)
			self.assertTrue(len(branches) == 4)
		def test_clone1(self):
			tree = Node(0)
			newtree = Utils.cloneTree(tree)
			nodelist1 = [n for n in tree.getDescendants()]
			nodelist2 = [n for n in newtree.getDescendants()]
			for i, j in zip(nodelist1, nodelist2):
				if i.value != j.value:
					self.assertTrue(False)
		def test_clone2(self):
			(tree,_) = Utils.randomTree(30)
			newtree = Utils.cloneTree(tree)
			nodelist1 = [n for n in tree.getDescendants()]
			nodelist2 = [n for n in newtree.getDescendants()]
			for i, j in zip(nodelist1, nodelist2):
				if i.value != j.value:
					self.assertTrue(False)
		def test_clone3(self):
			(tree,_) = Utils.randomTree(100)
			newtree = Utils.cloneTree(tree)
			nodelist1 = [n for n in tree.getDescendants()]
			nodelist2 = [n for n in newtree.getDescendants()]
			for i, j in zip(nodelist1, nodelist2):
				if i.value != j.value:
					self.assertTrue(False)
		def buildRandomTree(self,size):
			s2 = int(size/10)
			s1 = size - s2*2
			values = [ random.randint(1, 1000) for x in range(s1)]
			doublevalues = 2*[ random.randint(1000,2000) for x in range(s2)]
			values.extend(doublevalues)
			root = Node(values[0])
			nodes = [root]
			r = root
			for v in values[1:]:
				n = Node(v)
				nodes.append(n)
				r.addChild(n)
				r = random.choice(nodes)
			return (root,values,doublevalues)
			
