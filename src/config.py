# src/config.py
import os
import json
from typing import Optional
from cryptography.fernet import Fernet

CONFIG_PATH = os.path.expanduser("~/.ai_hub_config.json")
KEY_PATH = os.path.expanduser("~/.ai_hub_key")


def generate_key() -> bytes:
    """Generates and stores a key for encryption."""
    key = Fernet.generate_key()
    with open(KEY_PATH, "wb") as f:
        f.write(key)
    return key


def load_key() -> bytes:
    """Loads the encryption key from the key file."""
    if not os.path.exists(KEY_PATH):
        return generate_key()
    with open(KEY_PATH, "rb") as f:
        return f.read()


class Config:
    """
    Manages configuration and encrypted API keys.
    Supports multiple profiles (dev, staging, prod).
    """

    def __init__(self, profile: str = "default") -> None:
        self.profile = profile
        self._key = load_key()
        self._fernet = Fernet(self._key)
        self._data = self._load_config()

    def _load_config(self) -> dict:
        if os.path.exists(CONFIG_PATH):
            with open(CONFIG_PATH, "r") as f:
                return json.load(f)
        return {}

    def _save_config(self) -> None:
        with open(CONFIG_PATH, "w") as f:
            json.dump(self._data, f, indent=4)

    def set_api_key(self, service: str, key: str) -> None:
        encrypted_key = self._fernet.encrypt(key.encode()).decode()
        self._data.setdefault(self.profile, {})[f"{service}_key"] = encrypted_key
        self._save_config()

    def get_api_key(self, service: str) -> Optional[str]:
        try:
            encrypted_key = self._data.get(self.profile, {}).get(f"{service}_key")
            if encrypted_key:
                return self._fernet.decrypt(encrypted_key.encode()).decode()
        except Exception:
            return None
        return None

    def delete_api_key(self, service: str) -> None:
        if f"{service}_key" in self._data.get(self.profile, {}):
            del self._data[self.profile][f"{service}_key"]
            self._save_config()

    def switch_profile(self, new_profile: str) -> None:
        self.profile = new_profile
        self._data.setdefault(new_profile, {})
        self._save_config()

    def get_all_profiles(self) -> list:
        return list(self._data.keys())
