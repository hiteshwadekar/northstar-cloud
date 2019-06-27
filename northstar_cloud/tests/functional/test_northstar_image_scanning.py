import os
import mock
import pytest

from northstar_cloud.tests import base
from northstar_cloud.common import utils as c_utils

DEFAULT_LOGGING_FILE_NAME = "etc/logging.ini"
ROOT_DIR = os.path.abspath(os.curdir)


class TestNorthStarImageScanning(base.BaseTest):
    def setUp(self):
        super(TestNorthStarImageScanning, self).setUp()
        self.service = mock.Mock()