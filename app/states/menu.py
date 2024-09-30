from collections import defaultdict

from app.utils.decorators import singleton


@singleton
class UserStateMenu:
    def __init__(self):
        self.queue = defaultdict(list)

    def __repr__(self):
        print("{")
        for k, v in self.queue.items():
            print("\t", k, "=", v)
        print("}")

    def push_menu(self, user_id: str, name_menu: str):
        self.queue[user_id].append(name_menu)

    def back_menu(self, user_id: str, count: int = 1) -> str:
        if user_id in self.queue:
            while count:
                self.queue[user_id].pop()
                count -= 1
            return self.queue[user_id][-1]
        else:
            self.push_menu(user_id, "main_menu")
            return "main_menu"

    def get_menu(self, user_id: str, count: int = 1) -> str:
        if user_id in self.queue:
            return self.queue[user_id][-count]
        self.push_menu(user_id, "main_menu")
        return "main_menu"

    def check_category(self, user_id: str, name: str) -> bool:
        return name in self.queue[user_id]