import random
import unittest
from lockForrest import LockTree
from lockForrest import Node
class BasicLockTreeTests(unittest.TestCase):

		def setUp(self):
			self.root = Node(None)
			self.l1_0 = Node(1)
			self.l1_1 = Node(2)
			self.l2_0 = Node(10)
			self.l2_1 = Node(11)
			self.l3_0 = Node(30)
			self.l3_1 = Node(31)
			self.l3_1d = Node(31)
			
			self.root.addChild(self.l1_0)
			self.root.addChild(self.l1_1)
			self.l1_0.addChild(self.l2_0)
			self.l1_0.addChild(self.l2_1)
			self.l2_1.addChild(self.l3_0)
			self.l2_1.addChild(self.l3_1)
			
			self.l1_1.addChild(self.l3_1d)
			self.l = LockTree(1234)
			self.l.root = self.root
			self.l.actualNode = self.root
			
		def test_acquire(self):
			self.l.printTree()
			tree = LockTree(555)
			tree.acquire(7)
			tree.acquire(77)
			self.assertEqual(tree.actualNode.value,77)
			self.assertEqual(tree.actualNode.parent.value,7)
			tree.acquire(None)
			self.assertEqual(tree.size(),3)
			tree.acquire(77)#reentrant
			self.assertEqual(tree.size(),3)
			self.assertEqual(tree.actualNode.value,77)
						
		def test_release(self):
			tree = LockTree(555)
			tree.release(99)#release never acquired
			self.assertEqual(tree.size(),1)
			self.assertEqual(tree.actualNode.value,None)
			tree.acquire(7)
			self.assertEqual(tree.size(),2)
			self.assertEqual(tree.actualNode.value,7)
			tree.release(99)
			self.assertEqual(tree.size(),2)
			tree.release(7)
			self.assertEqual(tree.actualNode.value,None)
			
			
		def test_acquirerelease(self):
			self.l.actualNode = self.root.find(Node(30))
			self.l.release(1)
			self.assertEqual(self.l.size(),10)
			t = self.root.findAll(Node(30))
			self.assertEqual(len(t),2)
			t = self.root.findAll(Node(11))
			self.assertEqual(len(t),2)
			for n in t:
				if n is not self.l2_1:
					self.assertEqual(n.parent,self.root)

		
		def test_above(self):
			t = self.l.getAllHoldLocks(None)
			self.assertEqual(len(t),0)
			t = self.l.getAllHoldLocks(1)

			self.assertEqual(len(t),0)
						
			t = self.l.getAllHoldLocks(10)
			self.assertEqual(t,set([1]))

			t = self.l.getAllHoldLocks(31)
			self.assertTrue(t == set([11,2,1]))
			self.assertTrue(11 in t)
			self.assertTrue(1 in t)
			self.assertTrue(2 in t)
			
		def test_below(self):
			t = self.l.getAllLocksBelow(None)

			self.assertEqual(t,set([1,2,10,11,31,30]))
			
			t = self.l.getAllLocksBelow(30)
			self.assertEqual(len(t),0)
			t = self.l.getAllLocksBelow(31)
			self.assertEqual(len(t),0)
			
			t = self.l.getAllLocksBelow(1)
			self.assertEqual(t,set([10,11,30,31]))
		
		
		
		
		
		
		
		