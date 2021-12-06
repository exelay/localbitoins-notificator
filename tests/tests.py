from asyncio import get_event_loop

from unittest import TestCase
from unittest.mock import patch, AsyncMock

from tests.objects import notifications, new_notification
from core.types import Notificator, Notification


class TestNotificator(TestCase):

    def test_get_notifications(self):
        loop = get_event_loop()
        expected_answer = [Notification(**raw_notification) for raw_notification in notifications]

        with patch('core.types.lb_client.send_request', return_value=notifications):
            notificator = Notificator()
            coroutine = notificator.get_notifications()
            answer = loop.run_until_complete(coroutine)

            self.assertEqual(answer, expected_answer)

    def test_get_last_notification(self):
        loop = get_event_loop()
        expected_answer = Notification(**new_notification)

        with patch('core.types.lb_client.send_request', return_value=notifications):
            notificator = Notificator()
            coroutine = notificator.get_notifications()
            returned_notifications = loop.run_until_complete(coroutine)
            coroutine = notificator.get_last_notification(returned_notifications)
            answer = loop.run_until_complete(coroutine)

            self.assertEqual(answer, expected_answer)

    def test_update_last_notification(self):
        loop = get_event_loop()
        expected_answer = Notification(**new_notification)
        mocked_send_notification = AsyncMock()

        with patch('core.types.lb_client.send_request', return_value=notifications):
            with patch('core.types.Notificator.send_notification', return_value=mocked_send_notification):
                notificator = Notificator()
                coroutine = notificator.notify()
                loop.run_until_complete(coroutine)
                answer = notificator.last_notification

                self.assertEqual(answer, expected_answer)
