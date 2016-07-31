

from flask_cache import Cache


cache = Cache(config=dict(
    CACHE_TYPE = 'redis',
    CACHE_KEY_PREFIX = 'osp.www.flask',
    CACHE_DEFAULT_TIMEOUT = 3600,
))
