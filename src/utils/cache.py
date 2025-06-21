# src/utils/cache.py
from collections import OrderedDict
from typing import Any, Optional


class LRUCache:
    """
    Basit bir LRU (Least Recently Used) cache sınıfı.
    Maksimum kapasite aşıldığında en eski veri atılır.
    """

    def __init__(self, capacity: int = 100) -> None:
        self.capacity = capacity
        self.cache = OrderedDict()

    def get(self, key: str) -> Optional[Any]:
        if key not in self.cache:
            return None
        self.cache.move_to_end(key)
        return self.cache[key]

    def put(self, key: str, value: Any) -> None:
        if key in self.cache:
            self.cache.move_to_end(key)
        self.cache[key] = value
        if len(self.cache) > self.capacity:
            self.cache.popitem(last=False)

    def clear(self) -> None:
        self.cache.clear()
