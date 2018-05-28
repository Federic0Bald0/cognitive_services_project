# coding: utf-8
import json
import requests

API_KEY = 'AIzaSyDUVomcGLoMCZHUnEqo0nRGwOCb66v-e0A'


def call_vision_api(url):
    request = {
            "requests": [
                {
                    "image": {
                        "source": {
                            "imageUri": url
                        }
                    },
                    "features": [
                        {
                            "type": "LOGO_DETECTION",
                            "maxResults": 1
                        }
                    ]
                }
            ]
        }

    r = requests.post(
        url='https://vision.googleapis.com/v1/images:annotate?key={}'
            .format(API_KEY),
        data=json.dumps(request),
        headers={'Content-Type': 'application/json'}
        )

    return r.text