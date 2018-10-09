import sys
import os
import hashlib


from time import sleep
from flask import Flask, jsonify, request
from os.path import dirname
from time import sleep


sys.path.append(dirname(__file__))

from libs.make_captcha import make_a_captcha
from libs.redis_connector import put_captcha, get_captcha
from libs.redis_connector import put_kv, get_v


DEBUG = os.getenv("CAPTCHA_DEBUG", None)
app = Flask(__name__)


def normalize_text(text):
    return text.strip().lower()

def find_client_ip(request):
    print(request.headers)
    if request.environ.get('HTTP_X_FORWARDED_FOR'):
        return request.environ['HTTP_X_FORWARDED_FOR']
    else:
        return request.environ['REMOTE_ADDR']

def make_client_token(raw_token='', length=12):
    return hashlib.sha1(raw_token.encode()).hexdigest()[0:length]
    
@app.route("/webservice/api/captcha/1/generate", methods=["GET"])
def generate_captcha_img():
    text, img = make_a_captcha(inline=False)
    key = put_captcha(key=normalize_text(text), value=img)
    if key:
        if DEBUG:
            return jsonify({"debug": 1, "captcha-text": key,
                            "captcha-image": img}), 200
        else:
            return jsonify({"captcha-image": img}), 200
    else:
        return jsonify({"error": "captcha creation failed!"}), 810
    
@app.route("/webservice/api/captcha/2/generate", methods=["GET"])
def generate_captcha_inline_img():
    text, img = make_a_captcha()
    key = put_captcha(key=normalize_text(text), value=img)
    if key:
        if DEBUG:
            return jsonify({"debug": 1, "captcha-text": key,
                            "inline-captcha-image": img, "debug": 1}), 200
        else:
            return jsonify({"inline-captcha-image": img}), 200
    else:
        return jsonify({"error": "captcha creation failed"}), 820

@app.route("/webservice/api/captcha/1/verify", methods=["GET"])
def verify_captcha():
    try:
        captcha_text = normalize_text(request.args.get("captcha_text"))
        token = normalize_text(make_client_token(find_client_ip(request).strip()))
        if captcha_text:
            img = get_captcha(captcha_text)
        else:
            return jsonify({"error": "invalid captcha text"}), 835
    except Exception as err:
        print(err)
        if DEBUG:
            return jsonify({"error": "error in validating the captcha",
                            "stack-tarce": str(err), "debug": 1,
                            #"request-headers": str(request.environ),
                            "text": str((find_client_ip(request),
                            [(k, v) for k, v in request.args.items()])),
                            #"X": find_client_ip(request).strip()
                            }), 835
        else:
            return jsonify({"error": "error in validating the captcha"}), 835
    else:
        if img:
            if put_kv(token, captcha_text):
                return jsonify({"captcha-text": captcha_text ,
                                "client-token": token}), 200
            else:
                return jsonify({"error": "internal error"}), 895
        else:
            return jsonify({"error": "captcha may not exist or maybe expired"}), 845

@app.route("/webservice/api/captcha/1/pass", methods=["GET"])
def pass_client():
    try:
        #if DEBUG:
        #    token = make_client_token(find_client_ip(request).strip())
        #    return jsonify({"client-token": token, "debug": 1}), 200
        token = normalize_text(request.args.get("client_token"))
        sleep(0.5)
        if get_v(token):
            return jsonify({"client-token": token}), 200
        else:
            return jsonify({"error": "invalid or expired token",
                            "client-token": token}), 865
        
    except Exception as err:
        print(err)
        if DEBUG:
            return jsonify({"error": "you shall not pass!",
                            "stack-trace": str(err), "debug": 1}), 855
        else:
            return jsonify({"error": "you shall not pass!"}), 855
                                

if __name__ == "__main__":
    #text, img = make_a_captcha()
    #key = put_captcha(text, img)
    #sleep(3)
    #value = get_captcha(key)
    #print(key, value)
    #print(text)
    app.run(host="0.0.0.0", port=87, debug=True, threaded=False)
    
    
