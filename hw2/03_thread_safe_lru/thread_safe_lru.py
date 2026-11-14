"""Потокобезопасный LRU-кеш фиксированной ёмкости. Условие — в README.md.

API:
    cache: LRUCache[str, int] = LRUCache(capacity=100)
    cache.put("key", 42)
    val = cache.get("key")                 # 42
    miss = cache.get("no", default=-1)     # -1
    size = len(cache)
    "key" in cache                         # bool
"""

from collections import OrderedDict
import threading


class LRUCache[K, V]:
    """Потокобезопасный LRU-кеш.

    Инварианты:
    - `len(cache) <= capacity` всегда;
    - при переполнении удаляется least recently used ключ (тот, к которому дольше всех не обращались);
    - успешный `get(key)` делает key самым свежим (MRU);
    - `put(key)` делает key самым свежим — и для нового ключа, и для обновления.
    """

    def __init__(self, capacity: int) -> None:
        # TODO:
        # 1. Если capacity < 1 — raise ValueError("capacity должен быть >= 1").
        # 2. Сохранить capacity в self._capacity.
        # 3. self._data: OrderedDict[K, V] = OrderedDict()  — хранилище;
        #    порядок ключей = порядок использования (в начале самый старый, в конце самый свежий).
        # 4. self._lock = threading.RLock()  — один замок на все операции.
        if capacity < 1:
            raise ValueError("capacity должен быть >= 1")
        self._capacity = capacity
        self._data: OrderedDict[K, V] = OrderedDict()
        self._lock = threading.RLock()

    @property
    def capacity(self) -> int:
        # TODO: вернуть self._capacity.
        return self._capacity

    def put(self, key: K, value: V) -> None:
        # TODO: всё тело — внутри `with self._lock:`
        # 1. Записать значение: self._data[key] = value.
        # 2. Сделать ключ самым свежим: self._data.move_to_end(key).
        # 3. Если len(self._data) > self._capacity — удалить самый старый:
        #    self._data.popitem(last=False).
        with self._lock:
            self._data[key] = value
            self._data.move_to_end(key)
            if len(self._data) > self.capacity:
                self._data.popitem(last=False)


    def get(self, key: K, default: V | None = None) -> V | None:
        # TODO: всё тело — внутри `with self._lock:`
        # 1. Если ключа нет — вернуть default (порядок НЕ трогать).
        # 2. Иначе сделать ключ самым свежим (move_to_end) и вернуть значение.
        with self._lock:
            if key not in self._data:
                return default
            else:
                self._data.move_to_end(key)
                return self._data[key]

    def __len__(self) -> int:
        # TODO: под замком вернуть len(self._data).
        with self._lock:
            return len(self._data)

    def __contains__(self, key: object) -> bool:
        # TODO: под замком вернуть key in self._data (порядок НЕ трогать).
        with self._lock:
            return key in self._data
