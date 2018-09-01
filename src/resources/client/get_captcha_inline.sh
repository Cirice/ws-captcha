#!/usr/bin/env sh


HOST_PORT="localhost:80"
URI="/api/captcha/2/generate"
CURL="/usr/bin/curl"


$CURL $HOST_PORT$URI
