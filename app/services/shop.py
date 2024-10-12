import aiohttp
import os
import json


headers = {
    "content-type": "application/json",
    "Authorization": f"Bearer {os.getenv('TOKEN_BACKEND')}",
}


async def get_names_shop_list(username: str):
    async with aiohttp.ClientSession() as session:
        url = os.getenv("BACKEND_URL") + "shop_list/get_names_shop_list"
        async with session.get(
            url, params={"username": username}, headers=headers
        ) as response:
            return response.status, await response.json()


async def get_shop_list(username: str, shop_list_name: str):
    async with aiohttp.ClientSession() as session:
        url = os.getenv("BACKEND_URL") + "shop_list/get_shop_list"
        async with session.get(
            url,
            params={"username": username, "name": shop_list_name},
            headers=headers,
        ) as response:
            return response.status, await response.json()


async def create_shop_list(username: str, name_shop_list: str):
    async with aiohttp.ClientSession() as session:
        url = os.getenv("BACKEND_URL") + "shop_list/create_shop_list"
        data = {"username": username, "name": name_shop_list}
        async with session.post(
            url, data=json.dumps(data), headers=headers
        ) as response:
            return response.status, await response.json()
     

async def user_add_shop_list(username: str, uid: str):
    async with aiohttp.ClientSession() as session:
        url = os.getenv("BACKEND_URL") + "shop_list/user_add_shop_list"
        data = {"username": username, "uid": uid}
        async with session.post(
            url, data=json.dumps(data), headers=headers
        ) as response:
            return response.status, await response.json()


async def get_uid_shop_list(username: str, shop_list_name: str):
    async with aiohttp.ClientSession() as session:
        url = os.getenv("BACKEND_URL") + "shop_list/get_uid_shop_list"
        async with session.get(
            url,
            params={"username": username, "name": shop_list_name},
            headers=headers,
        ) as response:
            return response.status, await response.json()
      

async def delete_shop_list(username: str, shop_list_name: str):
    async with aiohttp.ClientSession() as session:
        url = os.getenv("BACKEND_URL") + "shop_list/delete_shop_list"
        async with session.delete(
            url,
            params={"username": username, "name": shop_list_name},
            headers=headers,
        ) as response:
            return response.status, await response.json()


async def add_items_to_shop_list(username: str, shop_list_name: str, items: str):
    async with aiohttp.ClientSession() as session:
        url = os.getenv("BACKEND_URL") + "shop_list/add_items_to_shop_list"
        data = {"username": username, "name": shop_list_name, "items": items}
        async with session.post(
            url, data=json.dumps(data), headers=headers
        ) as response:
            return response.status, await response.json()
        

async def del_item_from_shop_list(username: str, shop_list_name: str, item: str):
    async with aiohttp.ClientSession() as session:
        url = os.getenv("BACKEND_URL") + "shop_list/del_item_from_shop_list"
        data = {"username": username, "name": shop_list_name, "item": item}
        async with session.delete(
            url, params=data, headers=headers
        ) as response:
            return response.status, await response.json()
