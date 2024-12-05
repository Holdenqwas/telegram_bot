import os
from telebot.asyncio_filters import SimpleCustomFilter


class AdminFilter(SimpleCustomFilter):
    """
    Filter for admin users
    """

    key = "admin"

    async def check(self, message):
        return message.from_user.id == os.getenv("MY_NAME")
