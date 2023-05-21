from typing import Any
from unittest import TestCase
from unittest.mock import patch

from pytest import raises

from app.__main__ import main
from app.helpers.app_handlers import AppHandlers
from app.service_layer.data_processing_service import DataProcessingService


class TestMain(TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    @patch("app.__main__", return_value=None)
    def test_handler(self, __handler):
        self.assertIsNone(__handler(Any, Any))

    @patch("app.__main__", return_value=None)
    def test_main(self, main):
        self.assertIsNone(main(handlers=Any, scheduler_service=Any))

    def test_main_2(self):
        with patch.object(DataProcessingService, "processing", side_effect=SystemExit), raises(SystemExit):
            main(handlers=AppHandlers(), service=DataProcessingService())
