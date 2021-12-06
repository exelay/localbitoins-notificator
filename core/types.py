from time import sleep
from typing import List, Optional
from dataclasses import dataclass

from core.loader import lb_client
from core.settings import ALLOWED_USERS, logger
from core.loader import dp


@dataclass
class Notification:
    read: bool
    created_at: str
    msg: str
    url: str
    id: str
    contact_id: Optional[int] = None

    def __eq__(self, other):
        return self.created_at == other.created_at

    def __gt__(self, other):
        return self.created_at > other.created_at

    def __lt__(self, other):
        return self.created_at < other.created_at

    def __ge__(self, other):
        return self.created_at >= other.created_at

    def __le__(self, other):
        return self.created_at <= other.created_at


class Notificator:
    last_notification: Optional[Notification] = None

    @staticmethod
    async def send_notification(notification: Notification):
        message = f"{notification.msg}\nlocalbitcoins.com{notification.url}"
        for user in ALLOWED_USERS:
            await dp.bot.send_message(user, message)

    @staticmethod
    async def get_notifications() -> List[Notification]:
        raw_notifications = lb_client.send_request('/api/notifications/')
        notifications = [Notification(**raw_notification) for raw_notification in raw_notifications]
        logger.debug(f'Notifications list: {notifications}')
        return notifications

    async def get_last_notification(self, notifications: List[Notification]) -> Optional[Notification]:
        last_notification = max(notifications)
        if not self.last_notification or self.last_notification != last_notification:
            self.last_notification = last_notification
            return last_notification
        elif last_notification == self.last_notification:
            return

    async def notify(self):
        notifications = await self.get_notifications()
        last_notification = await self.get_last_notification(notifications)
        if last_notification:
            logger.debug(f'Sends notification: {last_notification}')
            await self.send_notification(last_notification)
        logger.debug(f'Last notification is: {self.last_notification}')

    async def run(self):
        while True:
            try:
                await self.notify()
            except Exception as e:
                logger.error(f'Unexpected exception: {e}')
            sleep(10)
