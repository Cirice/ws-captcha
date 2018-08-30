import sys

from time import sleep
from flask import Flask, jsonify, request
from os.path import dirname

sys.path.append(dirname(__file__))

from libs.make_captcha import make_a_captcha
from libs.redis_connector import put_captcha, get_captcha


app = Flask(__name__)

@app.route("/api/captcha/1/generate", methods=["GET"])
def generate_captcha_img():
    text, img = make_a_captcha(inline=False)
    key = put_captcha(key=text, value=img)
    if key:
        return jsonify({"ok": key}), 200
    else:
        return jsonify({"error": "captcha creation failed"}), 810

    
@app.route("/api/captcha/2/generate", methods=["GET"])
def generate_captcha_inline_img():
    text, img = make_a_captcha()
    key = put_captcha(key=text, value=img)
    if key:
        return jsonify({"ok": key}), 200
    else:
        return jsonify({"error": "captcha creation failed"}), 820

    
@app.route("/api/captcha/1/verify", methods=["GET"])
def verify_captcha():
    try:
        captcha_text = request.args.get("captcha_text")
        if captcha_text.strip():
            img = get_captcha(captcha_text)
        else:
            return jsonify({"error": "invalid captcha text"}), 830   
    except Exception as err:
        print(err)
        return jsonify({"error": "error in validating the captcha"}), 835
    else:
        if img:
            return jsonify({"captcha": img}), 840
        else:
            return jsonify({"captcha": "captcha may not exist or maybe expired"}), 845


if __name__ == "__main__":
    #text, img = make_a_captcha()
    #key = put_captcha(text, img)
    #sleep(3)
    #value = get_captcha(key)
    #print(key, value)
    #print(text)
    app.run(host="0.0.0.0", port=80, debug=True, threaded=False)
    
    
