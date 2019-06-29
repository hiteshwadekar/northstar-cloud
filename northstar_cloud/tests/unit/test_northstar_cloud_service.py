import mock
import pytest

from northstar_cloud.tests import base
from northstar_cloud.common import utils as c_utils


class TestNorthStarUserCloudService(base.BaseTest):
    def setUp(self):
        super(TestNorthStarUserCloudService, self).setUp()
        self.service = mock.Mock()

    @pytest.skip("fixing")
    def test_getting_images(self):
        pass

    @pytest.skip("fixing")
    def test_predict_fire_from_image(self):
        pass