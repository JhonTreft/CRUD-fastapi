from .connection import redis_client
from redis.exceptions import ResponseError

def save_hash(key:str,data:dict):
    try:
        redis_client.hset(name=key,mapping=data)
    except ResponseError as e:
        print(e)
        


def get_hash(key:str):
    try:
        return redis_client.hgetall(name=key)
    except ResponseError as e:
        print(e)
        

def delete_hash(key:str, keys: list):
    try:
        redis_client.hdel(key,*keys)
    except ResponseError as e:
        print(e)
    
def save_multiple_products(data: list):
    try:
         for product in data:
            product_id = product["id"]
            # Verifica si el producto ya existe en Redis antes de guardarlo nuevamente
            if not redis_client.hexists(product_id, product_id):
                redis_client.hset(name=product_id, mapping=product)
    except ResponseError as e:
        print(e)