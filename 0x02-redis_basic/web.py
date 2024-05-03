#!/usr/bin/env python3

import redis
import requests
from functools import wraps
from typing import Callable

redis_store = redis.Redis()
'''The module-level Redis instance.
'''

def data_cache(method: Callable) -> Callable:
    '''Decorator to cache the output of fetched data.'''
    @wraps(method)
    def wrapper(url: str) -> str:
        '''Wrapper function for caching the output.'''
        count_key = f'count:{url}'
        result_key = f'result:{url}'
        
        redis_store.incr(count_key)
        
        cached_result = redis_store.get(result_key)
        if cached_result:
            return cached_result.decode('utf-8')
        
        result = method(url)
        redis_store.setex(result_key, 10, result)
        
        return result
    return wrapper

@data_cache
def get_page(url: str) -> str:
    '''Returns the content of a URL after caching the request's response.'''
    response = requests.get(url)
    response.raise_for_status()
    return response.text
