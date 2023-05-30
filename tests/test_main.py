from typing import Any
from unittest import TestCase
from unittest.mock import patch

from pytest import raises

from app.__main__ import main
from app.helpers.app_handlers import AppHandlers
from app.service_layer.scheduler_service import SchedulerService
from app.service_layer.slack_notification_service import SlackNotificationService


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
        with patch.object(SchedulerService, "run", side_effect=SystemExit), raises(SystemExit):
            main(
                handlers=AppHandlers(),
                scheduler_service=SchedulerService(
                    scheduler_job_wrappers=[],
                    notification_service=SlackNotificationService(
                        webhook_url="https://hooks.slack.com/services/Test", token="test_token", channel="test_channel"
                    ),
                ),
            )
