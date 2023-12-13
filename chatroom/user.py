import threading


class UserManager:
    """
    用户管理类：单例模式，用于管理所有客户端
    """
    _lock = threading.Lock()
    _instance = None

    def __new__(cls):           # 双重检验
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super(UserManager, cls).__new__(cls)
                    cls._users = dict()         # 保存用户信息需要的字典
        return cls._instance

    def add_user(self, user_name, user_addr):
        with self._lock:
            if user_name not in self._users:
                self._users[user_name] = user_addr

    def remove_user(self, user_name):
        with self._lock:
            if user_name in self._users:
                del self._users[user_name]

    def get_all_user(self):
        with self._lock:
            return self._users

    def is_exists(self, user_name) -> bool:
        with self._lock:
            return user_name in self._users
