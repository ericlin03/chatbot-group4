#!/usr/bin/env python3
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

import os

class DefaultConfig:
    """ Bot Configuration """

    PORT = 3978
    APP_ID = os.environ.get("MicrosoftAppId", "")
    APP_PASSWORD = os.environ.get("MicrosoftAppPassword", "")

    QNA_KNOWLEDGEBASE_ID = os.environ.get("QnAKnowledgebaseId", "aa9a8da0-a395-4047-9c3d-9838fc1d9a6c")
    QNA_ENDPOINT_KEY = os.environ.get("QnAEndpointKey", "cd7b25b5-973c-436f-a7f6-887047b6dd3a")
    QNA_ENDPOINT_HOST = os.environ.get("QnAEndpointHostName", "https://restaurant-recom-qna.azurewebsites.net/qnamaker")

    # LUIS_APP_ID = os.environ.get("LuisAppId", "cc1ccd7e-f2e6-4ad5-be28-22dc51f946f8")   
    LUIS_APP_ID = os.environ.get("LuisAppId", "bee2730d-b196-4b6f-980d-3a70f47077ba")  
    LUIS_API_KEY = os.environ.get("LuisAPIKey", "20511052d473458ba2f09c6639ab820e")

    # LUIS endpoint host name, ie "westus.api.cognitive.microsoft.com"
    LUIS_API_HOST_NAME = os.environ.get("LuisAPIHostName", "westus.api.cognitive.microsoft.com")
