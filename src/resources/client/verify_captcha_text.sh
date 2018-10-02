#!/usr/bin/env sh


HOST_PORT="localhost:80"
URI="/api/captcha/1/verify?captcha_text=$1"
CURL="/usr/bin/curl"


$CURL $HOST_PORT$URI
