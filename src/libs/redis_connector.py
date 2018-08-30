import redis

from time import sleep


def make_redis_connection(host='localhost', port=6379, db=13):
    try:
        rc = redis.Redis(host, port, db=db)
        rc.set(1, "45")
        rc.get(1)
    except Exception as err:
        print(err)
        return None
    else:
        return rc


def put_captcha(key, value, time=600):
    try:
        rc = make_redis_connection()
        rc.set(key, value)
        rc.expire(key, time)
    except Exception as err:
        print(err)
        return None
    else:
        return key
    
    
def get_captcha(text):
    try:
        key = text.strip()
        rc = make_redis_connection()
        value = rc.get(key)

        if value:
            value = value.decode()
            rc.delete(key)
            
    except Exception as err:
        print(err)
        return None
    else:
        return value

    
if __name__ == "__main__":
    rc = make_redis_connection()

    key = put_captcha("key", "value", time=5)
    print(key)

    value = get_captcha(key)
    print(key, value)

    sleep(10)

    value = get_captcha(key)
    print(key, value)
#    print(rc)
    
