import aiohttp
import os
import json


headers = {
    "content-type": "application/json",
    "Authorization": f"Bearer {os.getenv('TOKEN_BACKEND')}",
}


async def create_all_training(name: str, weight: float):
    async with aiohttp.ClientSession() as session:
        url = os.getenv("BACKEND_URL") + "training/create"
        data = {"user_name": name, "weight": weight}
        async with session.post(
            url, data=json.dumps(data), headers=headers
        ) as response:
            return response.status, await response.json()


async def create_trainings(name: str, names: str):
    async with aiohttp.ClientSession() as session:
        url = os.getenv("BACKEND_URL") + "users/create_trainings"
        data = {"user_name": name, "names": names}
        async with session.post(
            url, data=json.dumps(data), headers=headers
        ) as response:
            return response.status


async def update_name_trainings(name: str, names: str):
    async with aiohttp.ClientSession() as session:
        url = os.getenv("BACKEND_URL") + "users/update_name_trainings"
        data = {"user_name": name, "names": names}
        async with session.patch(
            url, data=json.dumps(data), headers=headers
        ) as response:
            return response.status


async def delete_training(name: str):
    async with aiohttp.ClientSession() as session:
        url = f"{os.getenv('BACKEND_URL')}users/delete_trainings/{name}"
        async with session.delete(url, headers=headers) as response:
            return response.status


async def get_name_exercises(name: str, name_train: str):
    async with aiohttp.ClientSession() as session:
        url = os.getenv("BACKEND_URL") + "training/name_exercises"
        data = {"user_name": name, "name_training": name_train}
        async with session.patch(
            url, data=json.dumps(data), headers=headers
        ) as response:
            return response.status, await response.json()
        

async def start_train(name: str, name_train: str):
    async with aiohttp.ClientSession() as session:
        url = os.getenv("BACKEND_URL") + "training/create_train"
        data = {"user_name": name, "name_training": name_train}
        async with session.patch(
            url, data=json.dumps(data), headers=headers
        ) as response:
            return response.status


async def get_last_value(name_training, name_exercise):
    async with aiohttp.ClientSession() as session:
        url = os.getenv("BACKEND_URL") + f"training/{name_training}/{name_exercise}"

        async with session.get(url, headers=headers) as response:
            text = await response.text()
            print("Status:", response.status, "Body:", text)
            return text