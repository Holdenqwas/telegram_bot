import aiohttp
import os
import json
from datetime import datetime


DEBUG = os.environ.get("DEBUG")
verify_ssl = not DEBUG

headers = {
    "content-type": "application/json",
    "Authorization": f"Bearer {os.getenv('TOKEN_BACKEND')}",
}


async def create_user(user_id: int, username: str):
    async with aiohttp.ClientSession() as session:
        url = os.getenv("BACKEND_URL") + "users/create"
        data = {
            "user_id": user_id,
            "username": username,
            "last_date_license": datetime.now().isoformat(),
        }

        async with session.post(
            url, data=json.dumps(data), headers=headers, verify_ssl=verify_ssl
        ) as response:
            # html = await response.text()
            return response
