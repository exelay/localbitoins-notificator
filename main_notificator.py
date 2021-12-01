from time import sleep
from asyncio import get_event_loop

from core.loader import lb_client
from core.settings import ALLOWED_USERS
from core.loader import dp


class Notificator:
    notifications_count = 0

    @staticmethod
    async def send_notification(notification):
        message = f"{notification['msg']}\nlocalbitcoins.com{notification['url']}"
        for user in ALLOWED_USERS:
            await dp.bot.send_message(user, message)

    async def notify(self):
        notifications = lb_client.send_request('/api/notifications/')
        new_notifications = [notification for notification in notifications if not notification['read']]

        if len(notifications) > self.notifications_count:
            for notification in new_notifications:
                await self.send_notification(notification)
            self.notifications_count = len(notifications)

    async def run(self):
        while True:
            await self.notify()
            sleep(60)


if __name__ == '__main__':
    loop = get_event_loop()
    notificator = Notificator()
    coroutine = notificator.run()

    loop.run_until_complete(coroutine)

