#!/usr/bin/env bash

FILE=./data/exchange.html
echo 'Crawling... ('$FILE')'

curl "http://community.fxkeb.com/fxportal/jsp/RS/DEPLOY_EXRATE/22264_0.html" -H "Accept-Encoding: gzip, deflate, sdch" -H "Accept-Language: en-US,en;q=0.8,ko;q=0.6" -H "User-Agent: Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.90 Safari/537.36" -H "Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8" -H "Cache-Control: max-age=0" -H "If-None-Match: W/""4808-1430200839000""" -H "Connection: keep-alive" -H "If-Modified-Since: Tue, 28 Apr 2015 06:00:39 GMT" --compressed  | iconv -f euc-kr -t utf-8 > $FILE

python ./run.py $FILE