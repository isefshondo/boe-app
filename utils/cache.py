from flask_caching import Cache

cache = Cache()

def configCache(app):
    cache.init_app(app, config={
        'CACHE_TYPE': 'simple'
    })