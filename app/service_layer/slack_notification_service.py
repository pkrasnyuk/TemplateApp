import logging
from typing import List, Optional

from slack_sdk import WebClient, WebhookClient
from slack_sdk.errors import SlackApiError
from slack_sdk.http_retry.builtin_handlers import RateLimitErrorRetryHandler
from slack_sdk.web import SlackResponse
from slack_sdk.webhook import WebhookResponse


class SlackNotificationService:
    def __init__(self, webhook_url: str, token: str, channel: str):
        self.__logger = logging.getLogger(f"{__name__}.{self.__class__.__name__}")
        self.__webhook_client = WebhookClient(
            url=webhook_url, logger=self.__logger, retry_handlers=[RateLimitErrorRetryHandler(max_retry_count=5)]
        )
        self.__client = WebClient(
            token=token, logger=self.__logger, retry_handlers=[RateLimitErrorRetryHandler(max_retry_count=5)]
        )
        self.__channel = channel

    def send_webhook_message(self, message: str) -> None:
        response: WebhookResponse = self.__webhook_client.send(text=message)
        if response.status_code != 200:
            self.__logger.error(
                f"A request to slack returned an error {response.status_code}, the response is: {response.body}"
            )

    def send_webhook_messages(self, messages: List[str]) -> None:
        if len(messages) > 0:
            for message in messages:
                self.send_webhook_message(message=message)

    def send_client_message(
        self, message: str, user_name: Optional[str] = None, thread_ts: Optional[str] = None
    ) -> Optional[str]:
        ts: Optional[str] = None
        try:
            response: SlackResponse = self.__client.chat_postMessage(
                channel=self.__channel, text=message, username=user_name, thread_ts=thread_ts
            )
            if response.status_code != 200:
                self.__logger.error(
                    f"A request to slack returned an error {response.status_code}, the response is: {response.data}"
                )
            else:
                ts = response.data["ts"] if "ts" in response.data else None
        except SlackApiError as err:
            self.__logger.error(f"""A request to slack returned an error {err.response["error"]}""")
        return ts

    def send_notification_message(self, message: str) -> None:
        self.send_client_message(message=message, user_name="Notification")

    def send_notification_messages(self, messages: List[str]) -> None:
        if len(messages) > 0:
            paging_items_count: int = 20
            for i in range(0, len(messages), paging_items_count):
                self.send_notification_message(message="\n".join(messages[i : i + paging_items_count]))

    def send_error_message(self, message: str, ex: Optional[Exception] = None, traceback: Optional[str] = None) -> None:
        thread_ts: Optional[str] = self.send_client_message(message=message, user_name="Error Notification")
        if thread_ts is not None:
            if ex is not None:
                self.send_client_message(message=str(ex), user_name="Exception Details", thread_ts=thread_ts)
            if traceback is not None:
                self.send_client_message(message=traceback, user_name="Stack Trace", thread_ts=thread_ts)
