# coding: utf-8
import json
import requests
import numpy as np
from difflib import SequenceMatcher
from base64 import b64encode
from os.path import dirname, join

json_data = open('credentials_vision.json').read()
data = json.loads(json_data)

API_KEY = data['api_key']
PATH_IMAGES = 'static/pictures/'

googleJson = ""


def encode_image(picture):
    with open(PATH_IMAGES + picture, 'rb') as img:
        img_content = img.read()
        enc = b64encode(img_content)
    return enc


def call_vision_api(picture, useBlocks=True):
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

    global googleJson

    # if this is the first try
    if not googleJson:
        r = requests.post(
            url='https://vision.googleapis.com/v1/images:annotate?key={}'
                .format(API_KEY),
            data=json.dumps(request),
            headers={'Content-Type': 'application/json'}

        )
        googleJson = r.text
        # print "Trying blocks"
        return extractBlocks(googleJson)
    else:
        lines = extractLines(googleJson)
        # next time retry with blocks
        googleJson = ""
        # print "trying lines"
        return lines


def extractBlocks(googleJson):
    partial_text = ""
    text = []
    boxsizes = []

    googleDict = json.loads(googleJson)
    blocks = googleDict['responses'][0]['fullTextAnnotation'][
        'pages'][0]['blocks']
    for block in blocks:
        vertices = block['boundingBox']['vertices']
        boxsizes.append(vertices)
        for paragraph in block['paragraphs']:
            words = paragraph['words']
            for word in words:
                symbols = word['symbols']
                for symbol in symbols:
                    partial_text = partial_text + symbol['text']
                partial_text = partial_text + " "
        text.append(partial_text.encode('utf-8').lower().strip())
        partial_text = ""

    # text = text + " --- "

    # for boxsize in boxsizes:
    #     text = text + str(getArea(boxsize)) + ', '

    return text


def extractLines(googleJson):
    partial_text = ""
    text = []

    googleDict = json.loads(googleJson)
    blocks = googleDict['responses'][0]['fullTextAnnotation'][
        'pages'][0]['blocks']
    for block in blocks:
        for paragraph in block['paragraphs']:
            words = paragraph['words']
            for word in words:
                symbols = word['symbols']
                for symbol in symbols:
                    partial_text = partial_text + symbol['text']
                    if (symbol.get('property') and
                            symbol['property'].get('detectedBreak')):

                        detectedBreak = symbol['property']['detectedBreak']

                        if (detectedBreak['type'] == 'LINE_BREAK' or
                                detectedBreak['type'] == 'EOL_SURE_SPACE'):

                            text.append(partial_text.encode('utf-8').lower()
                                        .strip())

                            partial_text = ""
                partial_text = partial_text + " "

    return text


# def getArea(boxsize):
#     x = np.array([])
#     y = np.array([])
#     for vertices in boxsize:
#         x = np.append(x, [vertices['x']])
#         y = np.append(y, [vertices['y']])

#     return 0.5 * np.abs(np.dot(x, np.roll(y, 1)) - np.dot(y, np.roll(x, 1)))


def getStringsDiff(string1, string2):
    return SequenceMatcher(None, string1, string2).ratio()
