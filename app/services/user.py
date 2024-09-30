import aiohttp
import os
import json
from datetime import datetime

headers = {
    "content-type": "application/json",
    "Authorization": f"Bearer {os.getenv('TOKEN_BACKEND')}",
}


async def create_user(username: str):
    async with aiohttp.ClientSession() as session:
        url = os.getenv("BACKEND_URL") + "users/create"
        data = {
            "user_name": username,
            "last_date_license": datetime.now().isoformat(),
        }
        async with session.post(
            url, data=json.dumps(data), headers=headers
        ) as response:
            html = await response.text()
            print("users/create", "Status:", response.status, "Body:", html)
            return response
