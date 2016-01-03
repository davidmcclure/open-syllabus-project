

from flask.ext.cache import Cache


cache = Cache(config=dict(
    CACHE_TYPE = 'redis',
    CACHE_DEFAULT_TIMEOUT = 3600,
    CACHE_KEY_PREFIX = 'osp-www',
))
