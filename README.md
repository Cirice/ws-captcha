# A webservice for creation and verification of captcha images

### To start the webservice please do as follow:
    1. ./manage.sh redis-start
    2. ./manage.sh gunicorn-start
    3. ./mange.sh nginx-start

### Alternatively you can do the following:
    - ./manage.sh start-all

### To test the captcha webservice api use the following scripts
    1. src/resources/client/get_captcha.sh # it should return
    
### Endpoints
    1. [http://localhost/api/captcha/1/generate](http://localhost/api/captcha/1/generate)
    2. [http://localhost/api/captcha/2/generate](http://localhost/api/captcha/2/generate)
    3. [http://localhost/api/captcha/1/verify?captcha_text={CAPTCHA_TEXT}](http://localhost/api/captcha/1/verify?captcha_text={CAPTCHA_TEXT})
    4. [http://localhost/api/captcha/1/pass?client_token={CLIENT_TOKEN}](http://localhost/api/captcha/1/pass?client_token={CLIENT_TOKEN})
    5. 

