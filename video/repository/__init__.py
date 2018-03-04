LRU_CACHE_MAXSIZE = 128
LRU_CACHE_MAXSIZE = LRU_CACHE_MAXSIZE if LRU_CACHE_MAXSIZE > 0 else None


class NoCacheValueException(Exception):
    """lru_cacheにキャッシュをさせたくないときに投げる例外"""

    def __init__(self, *args, **kwargs):
        super().__init__()
        self.value = kwargs.get('value')
