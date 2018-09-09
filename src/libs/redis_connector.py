import redis

from time import sleep


def make_redis_connection(host='localhost', port=6379, db=1):
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

    
def put_kv(k, v, db=2, timeout=600):
    try:
        rc = make_redis_connection(db=db)
        rc.set(k, v)
        rc.expire(k, timeout)
        
    except Exception as err:
        print(err)
        return None
    else:
        return k

    
def get_v(k, db=2):
    try:
        key =  k.strip()
        rc = make_redis_connection(db=db)
        v = rc.get(k)

        if v:
            v = v.decode()
            rc.delete(k)
            
    except Exception as err:
        print(err)
        return None
    else:
        return v              

    
if __name__ == "__main__":
    rc = make_redis_connection()

    key = put_captcha("key", "value", time=5)
    print(key)

    value = get_captcha(key)
    print(key, value)

    sleep(10)

    value = get_captcha(key)
    print(key, value)
    #print(rc)

    k = put_kv("192.168.1.100", "ok", timeout=90)

    sleep(5)
    
    if k:
        v = get_v(k)
        print(v)
        

        
