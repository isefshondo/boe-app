from flask_caching import Cache

cache = Cache()

def configurationCache(app):
    cache.init_app(app, config={
        "CACHE_TYPE": "simple"
    })