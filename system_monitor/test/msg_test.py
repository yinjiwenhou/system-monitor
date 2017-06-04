import unittest
import os
import sys
project_path = os.path.split(os.path.realpath('__file__'))[0] + '../..'
project_path = os.path.normpath(project_path)
sys.path.append(project_path)

from SystemMonitor import os_msg

class TestMsg(unittest.TestCase):
	"""docstring for TestMsg"""
	def setUp(slef):
		pass

	def tearDown(slef):
		pass

	def test_os_process(self):
		p = os_msg.get_os_process()
		self.assertNotEqual(len(p), 0)

if __name__ == '__main__':	
	unittest.main()