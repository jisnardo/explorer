from .memory import memory
import flask_caching

application_cache = flask_caching.Cache(config = memory.application_cache_config)