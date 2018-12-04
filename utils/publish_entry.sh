#!/usr/bin/env bash

URL="127.0.0.1"
PORT="8000"
SECRET="123456789"

curl \
    --data-urlencode "secret=$SECRET" \
    --data-urlencode "title=Test" \
    --data-urlencode "link=https://conno.ddns.net/" \
    --data-urlencode "description=<h1>This is a description</h1><br>And this + this is actual content.<br>&_^-~+" \
    --data-urlencode "author=der_conno" \
    http://$URL:$PORT/appendToFeed