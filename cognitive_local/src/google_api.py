# coding: utf-8
import json
import requests
import numpy as np
from difflib import SequenceMatcher
from base64 import b64encode
from os.path import dirname, join

API_KEY = 'AIzaSyDUVomcGLoMCZHUnEqo0nRGwOCb66v-e0A'
PATH_IMAGES = 'cognitive_local/static/pictures/'

def encode_image(picture):
    with open(PATH_IMAGES + picture,'rb') as img:
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
                    "type": "DOCUMENT_TEXT_DETECTION"
                    }
                ]
                }
            ]
            }

    ### JSON for a request with an URL ###
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

    # print type(json.dumps(extractBlocks(r.text)))
    # print type(r.text)
    return extractBlocks(r.text)
    # return r.text

def extractBlocks(googleJson):
    text = ""
    boxsizes = []

    googleDict = json.loads(googleJson)
    blocks = googleDict['responses'][0]['fullTextAnnotation']['pages'][0]['blocks']
    for block in blocks:
        vertices = block['boundingBox']['vertices']
        boxsizes.append(vertices)
        for paragraph in block['paragraphs']:            
            words = paragraph['words']
            for word in words:
                symbols = word['symbols']
                for symbol in symbols:
                    text = text + symbol['text']
                text = text + " "
        text = text + '<br /> ' 

    text = text + " --- "
    
    for boxsize in boxsizes:
        text = text + str(getArea(boxsize)) + ', '

    return text

def getArea(boxsize):
    x = np.array([])
    y = np.array([])
    for vertices in boxsize:
        x = np.append(x,[vertices['x']])
        y = np.append(y,[vertices['y']])

    return 0.5*np.abs(np.dot(x,np.roll(y,1))-np.dot(y,np.roll(x,1)))


def getStringsDiff(string1, string2):
    return SequenceMatcher(None,string1,string2).ratio()

if __name__ == '__main__':
    print getStringsDiff(
        "Harry Potter e la pietra filosofale",
        "Harty Potter e la pietra filosofale")