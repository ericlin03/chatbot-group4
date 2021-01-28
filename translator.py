# -*- coding: utf-8 -*-
"""
Created on Fri Jan 29 01:11:30 2021

@author: kevin
"""

import requests, uuid, json

# Add your subscription key and endpoint
subscription_key = "be69f5f9d9184a339ee454e3b52904a6"
constructed_url = "https://api.cognitive.microsofttranslator.com/translate"

# Add your location, also known as region. The default is global.
# This is required if using a Cognitive Services resource.
location = "southeastasia"

#path = '/translate'
#constructed_url = endpoint + path
headers = {
        'Ocp-Apim-Subscription-Key': subscription_key,
        'Ocp-Apim-Subscription-Region': location,
        'Content-type': 'application/json',
        'X-ClientTraceId': str(uuid.uuid4())
    }

#text = input("type in here:")

# You can pass more than one object in body.




def detect_translater_language(text):
    
    body = [{
    'text': text
    }]
    params = {
    'api-version': '3.0',
    #'from': 'en',
    'to': ['zh-Hant']
    }
    
    request = requests.post(constructed_url, params=params, headers=headers, json=body)
    response = request.json()
    
    #print(json.dumps(response, sort_keys=True, ensure_ascii=False, indent=4, separators=(',', ': ')))
    
    return([response[0]['detectedLanguage']['language'],response[0]['translations'][0]['text']])
    
#def translater(text):
    
    
#print(detect_language(text))

def translate_back(text,language_type):
    body = [{
    'text': text
    }]
    params = {
    'api-version': '3.0',
    'from': "zh-Hant",
    'to': [language_type]
    }
    
    request = requests.post(constructed_url, params=params, headers=headers, json=body)
    response = request.json()
    
    #print(json.dumps(response, sort_keys=True, ensure_ascii=False, indent=4, separators=(',', ': ')))
    
    return(response[0]["translations"][0]["text"])

#print(translate_back('目前不支援', 'en'))
    

    

