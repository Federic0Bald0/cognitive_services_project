# coding: utf-8
from googleapiclient import discovery
from oauth2client.client import GoogleCredentials

def get_language_service():
    credentials = GoogleCredentials.get_application_default()
    return discovery.build('vison', 'v1', credentials=credentials)

# def call_vision_api(img):
#     service = get_language_service()
#     request =