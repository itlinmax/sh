#!/usr/bin/env python3
import urllib.request
from urllib.request import Request
import json
import pprint
url= "http://httpbin.org/get"
USER_AGENT = 'Mozilla/5.0 (Linux; Android 10)  AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.101  Mobile Safari/537.36'
req = Request(url)
req.add_header('User-agent', USER_AGENT)
with urllib.request.urlopen(req) as response_json:
    data_json = json.loads(response_json.read().decode("utf-8"))
    pprint.pprint(data_json)
