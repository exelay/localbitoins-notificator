from time import sleep

from core.loader import lb_client
from core.settings import ALLOWED_USERS, logger
from core.loader import dp


class Notificator:
    notifications_count = 0

    @staticmethod
    async def send_notification(notification):
        message = f"{notification['msg']}\nlocalbitcoins.com{notification['url']}"
        for user in ALLOWED_USERS:
            await dp.bot.send_message(user, message)

    @staticmethod
    async def get_notifications() -> list:
        notifications = lb_client.send_request('/api/notifications/')
        logger.debug(f'Notifications list: {notifications}')
        return notifications

    @staticmethod
    async def get_new_notifications(notifications: list) -> list:
        new_notifications = [notification for notification in notifications if not notification['read']]
        logger.debug(f'New notifications list: {new_notifications}')
        return new_notifications

    async def notify(self):
        notifications = await self.get_notifications()
        new_notifications = await self.get_new_notifications(notifications)

        if len(notifications) > self.notifications_count:
            for notification in new_notifications:
                logger.debug(f'Sends notification: {notification}')
                await self.send_notification(notification)
            self.notifications_count = len(notifications)
        logger.debug(f'Notifications count is: {self.notifications_count}')

    async def run(self):
        while True:
            try:
                await self.notify()
            except Exception as e:
                logger.error(f'Unexpected exception: {e}')
            sleep(10)
