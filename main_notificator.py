from asyncio import get_event_loop

from core.types import Notificator


if __name__ == '__main__':
    loop = get_event_loop()
    notificator = Notificator()
    coroutine = notificator.run()

    loop.run_until_complete(coroutine)

