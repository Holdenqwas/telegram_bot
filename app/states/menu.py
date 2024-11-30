from collections import defaultdict

from app.utils.decorators import singleton


def create_dict():
    return {"menu": []}


@singleton
class UserStateMenu:
    def __init__(self):
        self.mem = defaultdict(create_dict)

    def __repr__(self):
        print("{")
        for k, v in self.mem.items():
            print("\t", k, "=", v)
        print("}")

    def clear_mem(self, user_id):
        self.mem[user_id] = {"menu": ["main_menu"]}

    def push_menu(self, user_id: str, name_menu: str):
        self.mem[user_id]["menu"].append(name_menu)

    def back_menu(self, user_id: str, count: int = 1) -> str:
        if user_id in self.mem:
            while count:
                self.mem[user_id]["menu"].pop()
                count -= 1
            return self.mem[user_id]["menu"][-1]
        else:
            self.push_menu(user_id, "main_menu")
            return "main_menu"

    def get_menu(self, user_id: str, count: int = 1) -> str:
        if user_id in self.mem:
            return self.mem[user_id]["menu"][-count]
        self.push_menu(user_id, "main_menu")
        return "main_menu"

    def check_category(self, user_id: str, name: str) -> bool:
        return name in self.mem[user_id]["menu"]

    def set_cookie(self, user_id, key, value):
        self.mem[user_id][key] = value

    def get_cookie(self, user_id, key):
        if key in self.mem[user_id]:
            return self.mem[user_id][key]
        return None
