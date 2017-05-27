from decorators import async
import requests
import json


@async
def send_async_request(url, payload):
    r = requests.post(url, data = json.dumps(payload))

def send_request(url, payload):
    send_async_request(url, payload)
