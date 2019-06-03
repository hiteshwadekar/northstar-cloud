from unittest import mock
from testtools import testcase


class BaseTest(testcase.TestCase):
    def setUp(self):
        super(BaseTest, self).setUp()
        self.addCleanup(mock.patch.stopall)
