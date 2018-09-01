import random
import base64


from claptcha import Claptcha
from claptcha.claptcha import ClaptchaError


chars = '%a1b2cde4#f5ghijk6l8m3nopqr0st9uvwxyzABCDEFG@HIJKLMNOPQR@STUVWXYZ'

def make_gibberish(length=8):
    return ''.join([random.choice(chars) for _ in range(length)])

def make_captcha(text=make_gibberish()):

    try:
        captcha = Claptcha(text, "../../FreeMono.ttf")
    except ClaptchaError as err:
        print (err)
        captcha = Claptcha(text, "src/resources/FreeMono.ttf")
        
    _, img = captcha.bytes
    return text, base64.b64encode(img.read()).decode()

def make_embedded_img(text, img):
    return text, '<img src="data:image/png;base64,{0}" alt="cogcaptcha.png">'.format(img)

def make_a_captcha(length=8, inline=True):
    text = make_gibberish(length)
    text, img = make_captcha(text)
    if inline:
        return make_embedded_img(text, img)
    else:
        return text, img

if __name__ == "__main__":
    text, img = make_captcha()
    print(text, img)
    print(make_embedded_img(text, img))

    with open("index.html", "w") as html_page:
        text, inline_img = make_embedded_img(text, img)
        content = "<html> <body> {0} </body> </html>".format(inline_img)
        html_page.write(content)
        html_page.write("\r\n\r\n" + text)
        html_page.flush()

        
    
