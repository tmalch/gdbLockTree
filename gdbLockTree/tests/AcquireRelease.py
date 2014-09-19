import random
import unittest

from gdbLockTree.LockTree import ThreadNode
from gdbLockTree.LockTree import LockNode
from gdbLockTree.LockTree import LockForrest
from gdbLockTree.Utils import Thread

class BasicLockTreeTests(unittest.TestCase):

		def setUp(self):
			self.root = ThreadNode(1234)
			self.l1_0 = LockNode(1)
			self.l1_1 = LockNode(2)
			self.l2_0 = LockNode(10)
			self.l2_1 = LockNode(11)
			self.l3_0 = LockNode(30)
			self.l3_1 = LockNode(31)
			self.l3_1d = LockNode(31)
			
			self.root.addChild(self.l1_0)
			self.root.addChild(self.l1_1)
			self.l1_0.addChild(self.l2_0)
			self.l1_0.addChild(self.l2_1)
			self.l2_1.addChild(self.l3_0)
			self.l2_1.addChild(self.l3_1)
			
			self.l1_1.addChild(self.l3_1d)
			self.root.currentNode = self.root
			
		def test_acquire(self):
			forrest = LockForrest()
			thread = Thread(555)
			forrest.acquire(thread,7)
			forrest.acquire(thread,77)
			self.assertEqual(forrest.trees[thread].currentNode.value,77)
			self.assertEqual(forrest.trees[thread].currentNode.parent.value,7)
			forrest.acquire(thread,None)
			self.assertEqual(forrest.trees[thread].subTreeSize(),3)
			forrest.acquire(thread,77)#reentrant
			self.assertEqual(forrest.trees[thread].subTreeSize(),4)
			self.assertEqual(forrest.trees[thread].currentNode.value,77)
						
		def test_release(self):
			forrest = LockForrest()
			thread = Thread(555)
			forrest.release(thread,99)#release never acquired
			self.assertEqual(forrest.trees[thread].subTreeSize(),1)
			self.assertEqual(forrest.trees[thread].currentNode.value,thread)
			forrest.acquire(thread,7)
			self.assertEqual(forrest.trees[thread].subTreeSize(),2)
			self.assertEqual(forrest.trees[thread].currentNode.value,7)
			forrest.release(thread,99)
			self.assertEqual(forrest.trees[thread].subTreeSize(),2)
			forrest.release(thread,7)
			self.assertEqual(forrest.trees[thread].currentNode.value,None)
			
			
		def test_acquirerelease(self):
			forrest = LockForrest()
			self.root.currentNode = self.root.find(30)
			thread = self.root.value
			forrest.trees[thread] = self.root
			forrest.release(thread,1)
			self.assertEqual(self.root.subTreeSize(),10)
			t = self.root.findAll(30)
			self.assertEqual(len(t),2)
			t = self.root.findAll(11)
			self.assertEqual(len(t),2)
			for n in t:
				if n is not self.l2_1:
					self.assertEqual(n.parent,self.root)

		
		
		
		
		
		
		
		
