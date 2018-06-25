# coding: utf-8
import json
import requests
from difflib import SequenceMatcher
from base64 import b64encode
from os.path import dirname, join

json_data = open('credentials_vision.json').read()
data = json.loads(json_data)

API_KEY = data['api_key']
PATH_IMAGES = 'static/pictures/'


def encode_image(picture):
    with open(PATH_IMAGES + picture, 'rb') as img:
        img_content = img.read()
        enc = b64encode(img_content)
    return enc


def call_vision_api(picture):
    request = {
               "requests": [
                {
                 "image": {
                    "content": encode_image(picture)
                          },
                 "features": [
                    {
                     "type": "TEXT_DETECTION"
                    }
                             ]
                }
                            ]
            }

    # JSON for a request with an URL ###
    # request = {
    #         "requests": [
    #             {
    #                 "image": {
    #                     "source": {
    #                         "imageUri": url
    #                     }
    #                 },
    #                 "features": [
    #                     {
    #                         "type": "LOGO_DETECTION",
    #                         "maxResults": 1
    #                     }
    #                 ]
    #             }
    #         ]
    #     }

    r = requests.post(
        url='https://vision.googleapis.com/v1/images:annotate?key={}'
            .format(API_KEY),
        data=json.dumps(request),
        headers={'Content-Type': 'application/json'}
        )

    return r.text


def getStringsDiff(string1, string2):
    return SequenceMatcher(None, string1, string2).ratio()

if __name__ == '__main__':
    print getStringsDiff(
        "Harry Potter e la pietra filosofale",
        "Harty Potter e la pietra filosofale")