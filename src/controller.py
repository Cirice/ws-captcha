import urllib
import hashlib
import sys
import os

from os.path import dirname

sys.path.append(dirname(__file__))
from main import make_client_token


cognos_login_uri = "/ibmcognos/cgi-bin/cognos.cgi"
pass_endpoint = "http://localhost:87/api/captcha/1/pass?client_token="

def find_client_ip(flow):
    try:
        return flow.request.headers['X-Forwarded-For']
    except Exception as err:
        print(err)
        return flow.request.headers['X-Real-Ip']
    return ''

def pass_client(client_token=''):
    try:
        url = pass_endpoint
        print(url+client_token)
        r = urllib.request.urlopen(url+client_token)
    except urllib.error.HTTPError as err:
        print(err.read())
        return err.code
    except Exception as err:
        print(err)
        return -1
    else:
        print(r.read(), r.code)
        return r.code
    
def request(flow):
    if flow.request.method in ('POST') and flow.request.url.endswith(cognos_login_uri):
        try:
            client_ip = find_client_ip(flow)
            token = make_client_token(client_ip)
            print("client token is %s" % token)
            if pass_client(client_token=token) != 200:
                contents = flow.request.content.decode()
                #contents = contents.replace("CAMNamespace", "FakeNamespace")
                contents = contents.replace("CAMUsername=", "FakeUsername=")
                contents = contents.replace("CAMPassword=", "FakePassword=")
                flow.request.content = contents.encode()
        except Exception as err:
            print(err)
