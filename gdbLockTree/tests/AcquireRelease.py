import random
import unittest

from ..commands import AcquireRelease
from ..commands.AcquireRelease import ThreadNode
from ..commands.AcquireRelease import LockNode
from gdbLockTree.Utils import Thread
from gdbLockTree import Utils

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
			thread = Thread(555)
			trees = []
			AcquireRelease.acquire(trees,thread,7)
			AcquireRelease.acquire(trees,thread,77)
			throot = Utils.getTreeForThread(trees,thread)
			self.assertEqual(throot.currentNode.value,77)
			self.assertEqual(throot.currentNode.parent.value,7)
			AcquireRelease.acquire(trees,thread,None)
			self.assertEqual(throot.subTreeSize(),3)
			AcquireRelease.acquire(trees,thread,77)#reentrant
			self.assertEqual(throot.subTreeSize(),4)
			self.assertEqual(throot.currentNode.value,77)
						
		def test_acquirerelease(self):
			thread = Thread(555)
			trees = []
			AcquireRelease.release(trees,thread,99)#release never acquired
			throot = Utils.getTreeForThread(trees,thread)
			self.assertEqual(throot.subTreeSize(),1)
			self.assertEqual(throot.currentNode.value,thread)
			AcquireRelease.acquire(trees,thread,7)
			self.assertEqual(throot.subTreeSize(),2)
			self.assertEqual(throot.currentNode.value,7)
			AcquireRelease.release(trees,thread,99)
			self.assertEqual(throot.subTreeSize(),2)
			AcquireRelease.release(trees,thread,7)
			self.assertEqual(throot.currentNode.value,thread)
			
			
		def test_release(self):
			self.root.currentNode = self.root.find(30)
			thread = self.root.value
			trees = [self.root]
			AcquireRelease.release(trees,thread,1)
			self.assertEqual(self.root.subTreeSize(),10)
			t = self.root.findAll(30)
			self.assertEqual(len(t),2)
			t = self.root.findAll(11)
			self.assertEqual(len(t),2)
			for n in t:
				if n is not self.l2_1:
					self.assertEqual(n.parent,self.root)

		
		
		
		
		
		
		
		
