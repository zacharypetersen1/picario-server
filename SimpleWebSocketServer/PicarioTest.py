import unittest
from PicarioServer import *

class MessageTestCase(unittest.TestCase):
    def setUp(self):
        initTest()

class DefaultWidgetSizeTestCase(MessageTestCase):
    def runTest(self):
        self.assertEqual(1, 1)

class WidgetResizeTestCase(MessageTestCase):
    def runTest(self):
        self.assertEqual(1, 1)