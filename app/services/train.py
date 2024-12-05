import aiohttp
import os
import json


DEBUG = os.environ.get("DEBUG")
verify_ssl = not DEBUG

headers = {
    "content-type": "application/json",
    "Authorization": f"Bearer {os.getenv('TOKEN_BACKEND')}",
}


async def create_all_training(name: str, weight: float):
    async with aiohttp.ClientSession() as session:
        url = os.getenv("BACKEND_URL") + "training/create"
        data = {"user_id": name, "weight": weight}
        async with session.post(
            url, data=json.dumps(data), headers=headers, verify_ssl=verify_ssl
        ) as response:
            return response.status, await response.json()


async def create_trainings(name: str, names: str):
    async with aiohttp.ClientSession() as session:
        url = os.getenv("BACKEND_URL") + "users/create_trainings"
        data = {"user_id": name, "names": names}
        async with session.post(
            url, data=json.dumps(data), headers=headers, verify_ssl=verify_ssl
        ) as response:
            return response.status


async def update_name_trainings(name: str, names: str):
    async with aiohttp.ClientSession() as session:
        url = os.getenv("BACKEND_URL") + "users/update_name_trainings"
        data = {"user_id": name, "names": names}
        async with session.patch(
            url, data=json.dumps(data), headers=headers, verify_ssl=verify_ssl
        ) as response:
            return response.status


async def update_name_exercises(user_id: str, name_train: str, name_exers: str):
    async with aiohttp.ClientSession() as session:
        url = os.getenv("BACKEND_URL") + "users/update_name_exercises"
        data = {
            "user_id": user_id,
            "name_train": name_train,
            "names": name_exers,
        }
        async with session.patch(
            url, data=json.dumps(data), headers=headers, verify_ssl=verify_ssl
        ) as response:
            return response.status


async def delete_training(name: str):
    async with aiohttp.ClientSession() as session:
        url = f"{os.getenv('BACKEND_URL')}users/delete_trainings/{name}"
        async with session.delete(
            url, headers=headers, verify_ssl=verify_ssl
        ) as response:
            return response.status


async def get_name_trainings(name: str):
    async with aiohttp.ClientSession() as session:
        url = os.getenv("BACKEND_URL") + f"training/name_trainings/{name}"
        async with session.get(
            url, headers=headers, verify_ssl=verify_ssl
        ) as response:
            return response.status, await response.json()


async def get_name_exercises(name: str, name_train: str):
    async with aiohttp.ClientSession() as session:
        url = os.getenv("BACKEND_URL") + "training/name_exercises"
        data = {"user_id": name, "name_training": name_train}
        async with session.post(
            url, data=json.dumps(data), headers=headers, verify_ssl=verify_ssl
        ) as response:
            return response.status, await response.json()


async def start_train(name: str, name_train: str):
    async with aiohttp.ClientSession() as session:
        url = os.getenv("BACKEND_URL") + "training/create_train"
        data = {"user_id": name, "name_training": name_train}
        async with session.post(
            url, data=json.dumps(data), headers=headers, verify_ssl=verify_ssl
        ) as response:
            return response.status


async def get_last_value(name: str, name_training, name_exercise):
    async with aiohttp.ClientSession() as session:
        url = os.getenv("BACKEND_URL") + "exercise/last_exercise"
        data = {
            "user_id": name,
            "name_training": name_training,
            "name_exercise": name_exercise,
        }
        async with session.post(
            url, data=json.dumps(data), headers=headers, verify_ssl=verify_ssl
        ) as response:
            text = await response.text()
            return text


async def write_exercise(name: str, name_training, name_exercise, value):
    async with aiohttp.ClientSession() as session:
        url = os.getenv("BACKEND_URL") + "exercise/write_exercise"
        data = {
            "user_id": name,
            "name_training": name_training,
            "name_exercise": name_exercise,
            "value": value,
        }
        async with session.post(
            url, data=json.dumps(data), headers=headers, verify_ssl=verify_ssl
        ) as response:
            text = await response.text()
            return text
