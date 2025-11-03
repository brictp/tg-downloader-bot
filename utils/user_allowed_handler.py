import json
from pathlib import Path

ALLOWED_FILE = Path("allowed_users.json")


class UserHandler:
    def __init__(self):
        self.data = self._load_data()

    # === BASE ===
    def _load_data(self):
        """Cargar archivo JSON o crear estructura por defecto"""
        if not ALLOWED_FILE.exists():
            data = {"admins": [], "users": []}
            self._save_data(data)
            return data

        with open(ALLOWED_FILE, "r") as f:
            return json.load(f)

    def _save_data(self, data=None):
        """Guardar datos en JSON"""
        if data is None:
            data = self.data
        with open(ALLOWED_FILE, "w") as f:
            json.dump(data, f, indent=4)

    # === CRUD ADMIN ===
    def add_admin(self, user_id: int):
        if user_id not in self.data["admins"]:
            self.data["admins"].append(user_id)
            self._save_data()

    def remove_admin(self, user_id: int):
        if user_id in self.data["admins"]:
            self.data["admins"].remove(user_id)
            self._save_data()

    def is_admin(self, user_id: int) -> bool:
        return user_id in self.data["admins"]

    def list_admins(self):
        return self.data["admins"]

    # === CRUD USERS ===
    def add_user(self, user_id: int):
        if user_id not in self.data["users"]:
            self.data["users"].append(user_id)
            self._save_data()

    def remove_user(self, user_id: int):
        if user_id in self.data["users"]:
            self.data["users"].remove(user_id)
            self._save_data()

    def is_user_allowed(self, user_id: int) -> bool:
        """Verifica si el usuario está autorizado"""
        return user_id in self.data["users"] or user_id in self.data["admins"]

    def list_users(self):
        return self.data["users"]
