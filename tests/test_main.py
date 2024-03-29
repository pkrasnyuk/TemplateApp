from typing import Any
from unittest import TestCase
from unittest.mock import patch

from pytest import raises

from app.__main__ import main
from app.service_layer.scheduler_service import SchedulerService
from core.helpers.app_handlers import AppHandlers
from core.service_layer.slack_notification_service import SlackNotificationService


class TestMain(TestCase):
    def setUp(self):
        self.__notification_service = SlackNotificationService(
            webhook_url="https://hooks.slack.com/services/Test", token="test_token", channel="test_channel"
        )

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
                handlers=AppHandlers(notification_service=self.__notification_service),
                scheduler_service=SchedulerService(
                    scheduler_job_wrappers=[],
                    notification_service=self.__notification_service,
                ),
            )
