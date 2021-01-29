# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.
from flask import Config
from botbuilder.ai.qna import QnAMaker, QnAMakerEndpoint, QnAMakerOptions
from botbuilder.ai.luis import LuisApplication, LuisRecognizer, LuisPredictionOptions

from botbuilder.schema import ChannelAccount

from botbuilder.core import ActivityHandler, MessageFactory, TurnContext, CardFactory, RecognizerResult
from botbuilder.schema import ChannelAccount, HeroCard, CardImage, CardAction, Activity, ActivityTypes
from websrestaurantrecom import webcrawl
from restaurant_recom import googlemaps_API, show_photo, googlemaps_search_location, find_position_with_xy
from sql import DB_function
from favorite import my_favorite
from history import add_history, get_history
from blogcrawler import blogcrawler
from translator import detect_translater_language,translate_back
from linebot.models.sources import SourceUser
from azure.cognitiveservices.language.luis.authoring import LUISAuthoringClient
from igcrawler import crawl


class MyBot(ActivityHandler):
    # See https://aka.ms/about-bot-activity-message to learn more about the message and other activity types.

    def __init__(
        self, config: Config
        ):
        self.qna_maker = QnAMaker(
            QnAMakerEndpoint(
                knowledge_base_id=config.QNA_KNOWLEDGEBASE_ID,
                endpoint_key=config.QNA_ENDPOINT_KEY,
                host=config.QNA_ENDPOINT_HOST,
            ), QnAMakerOptions(
                score_threshold = 0.9
            )
        )

        luis_application = LuisApplication(
            config.LUIS_APP_ID,
            config.LUIS_API_KEY,
            "https://" + config.LUIS_API_HOST_NAME,
        )
        luis_options = LuisPredictionOptions(
            include_all_intents=True, include_instance_data=True
        )
        self.recognizer = LuisRecognizer(luis_application, luis_options, True)

        self.db_func = DB_function()
        self.favor = my_favorite()

# define what we response
    async def on_message_activity(self, turn_context: TurnContext):

        language_type=detect_translater_language(turn_context.activity.text)[0]
        
        if language_type == 'en' or 'review' in turn_context.activity.text : #如果使用者輸入的是英文
            #將英文轉中文輸入
            turn_context.activity.text = detect_translater_language(turn_context.activity.text)[1]

            response = await self.qna_maker.get_answers(turn_context)
            if response and len(response) > 0 and (turn_context.activity.text != response[0].answer):
                await turn_context.send_activity(MessageFactory.text(response[0].answer))
            else:
                if turn_context.activity.text == "wait":
                    return await turn_context.send_activities([
                        Activity(
                            type=ActivityTypes.typing
                        ),
                        Activity(
                            type="delay",
                            value=3000
                        ),
                        Activity(
                            type=ActivityTypes.message,
                            text="Finished Typing"
                        )
                    ])
                elif turn_context.activity.text == "test sql":
                    output = DB_query("Select ID from user_info")
                    for i in range(0, len(output), 2):
                        await turn_context.send_activity(output[i] + ' ' + output[i+1])
                # elif turn_context.activity.text == "get my id":
                #     await turn_context.send_activity(self.user_id)
                elif "評論"in turn_context.activity.text or "review"in turn_context.activity.text :
                    await turn_context.send_activity(translate_back("稍等一下唷! 美食公道伯正在幫你尋找餐廳評論...",'en'))
                    # 展宏的func
                    re = webcrawl(turn_context.activity.text)
                    # 佑誠的func
                    blog_re=[]
                    blog_re = blogcrawler(turn_context.activity.text)
    
                    review_list = []
    
                    for index in range(len(blog_re)):
                        review_list.append(CardFactory.hero_card(HeroCard(title=blog_re[index][1], images=[CardImage(url=blog_re[index][3])], buttons=[CardAction(type="openUrl",title="Check This",value=blog_re[index][2])])))
                                    
                    if re:
                        review_list.append(CardFactory.hero_card(HeroCard(title=re["愛食記"][0], images=[CardImage(url=re["愛食記"][2])], buttons=[CardAction(type="openUrl",title="Check This",value=re["愛食記"][1])])))
                    
                    
                    message = MessageFactory.carousel(review_list)   
                    
                    await turn_context.send_activity(message)
    
                else:
    
                    restaurants_dict = googlemaps_API(turn_context.activity.text)
                    # 書文的func
                    re = webcrawl(turn_context.activity.text)
                    
                    message = MessageFactory.carousel([
                            CardFactory.hero_card(HeroCard(title=restaurants_dict[0]['name'], text='Recommendation : ' + str(restaurants_dict[0]['rating']), images=[CardImage(url=show_photo(restaurants_dict[0]['photo_reference']))], buttons=[CardAction(type="openUrl",title="Map",value="https://www.google.com/maps/search/?api=1&query=" + str(restaurants_dict[0]['location_x']) + "," + str(restaurants_dict[0]['location_y']) +"&query_place_id="+str(restaurants_dict[0]['place_id'])), CardAction(type="imBack",title="Click to Watch Review",value=restaurants_dict[0]['name']+"_review")])),
                            CardFactory.hero_card(HeroCard(title=restaurants_dict[1]['name'], text='Recommendation : ' + str(restaurants_dict[1]['rating']), images=[CardImage(url=show_photo(restaurants_dict[1]['photo_reference']))], buttons=[CardAction(type="openUrl",title="Map",value="https://www.google.com/maps/search/?api=1&query=" + str(restaurants_dict[1]['location_x']) + "," + str(restaurants_dict[1]['location_y']) +"&query_place_id="+str(restaurants_dict[1]['place_id'])), CardAction(type="imBack",title="Click to Watch Review",value=restaurants_dict[0]['name']+"_review")])),
                            CardFactory.hero_card(HeroCard(title=restaurants_dict[2]['name'], text='Recommendation : ' + str(restaurants_dict[2]['rating']), images=[CardImage(url=show_photo(restaurants_dict[2]['photo_reference']))], buttons=[CardAction(type="openUrl",title="Map",value="https://www.google.com/maps/search/?api=1&query=" + str(restaurants_dict[2]['location_x']) + "," + str(restaurants_dict[2]['location_y']) +"&query_place_id="+str(restaurants_dict[2]['place_id'])), CardAction(type="imBack",title="Click to Watch Review",value=restaurants_dict[2]['name']+"_review")])),
                            CardFactory.hero_card(HeroCard(title=restaurants_dict[3]['name'], text='Recommendation : ' + str(restaurants_dict[3]['rating']), images=[CardImage(url=show_photo(restaurants_dict[3]['photo_reference']))], buttons=[CardAction(type="openUrl",title="Map",value="https://www.google.com/maps/search/?api=1&query=" + str(restaurants_dict[3]['location_x']) + "," + str(restaurants_dict[3]['location_y']) +"&query_place_id="+str(restaurants_dict[3]['place_id'])), CardAction(type="imBack",title="Click to Watch Review",value=restaurants_dict[3]['name']+"_review")])),
                            CardFactory.hero_card(HeroCard(title=restaurants_dict[4]['name'], text='Recommendation : ' + str(restaurants_dict[4]['rating']), images=[CardImage(url=show_photo(restaurants_dict[4]['photo_reference']))], buttons=[CardAction(type="openUrl",title="Map",value="https://www.google.com/maps/search/?api=1&query=" + str(restaurants_dict[4]['location_x']) + "," + str(restaurants_dict[4]['location_y']) +"&query_place_id="+str(restaurants_dict[4]['place_id'])), CardAction(type="imBack",title="Click to Watch Review",value=restaurants_dict[4]['name']+"_review")])),
                            # CardFactory.hero_card(HeroCard(title=re["愛食記"][0], images=[CardImage(url=re["愛食記"][2])], buttons=[CardAction(type="openUrl",title="前往網頁",value=re["愛食記"][1])])),
                            # CardFactory.hero_card(HeroCard(title=re["愛食記"][0], images=[CardImage(url=re["愛食記"][2])], buttons=[CardAction(type="openUrl",title="前往網頁",value=re["愛食記"][1])])),
                            # CardFactory.hero_card(HeroCard(title=re["愛食記"][0], images=[CardImage(url=re["愛食記"][2])], buttons=[CardAction(type="openUrl",title="前往網頁",value=re["愛食記"][1])]))
                        ])#, buttons=[CardAction(title='button3')
                    await turn_context.send_activity(message)
    
                    # await (
                    #     turn_context.send_activity(
                    #         MessageFactory.content_url(url= re["愛食記"][2], content_type='image/jpg', text="There's the restaurants we find"))
                    # )
                    # await (
                    #     turn_context.send_activity(
                    #         MessageFactory.text(text= re["愛食記"][0])
                    #     )
                    # )
        elif language_type == 'zh-Hant' or '評論' in turn_context.activity.text: #如果是中文
        
            response = await self.qna_maker.get_answers(turn_context)
            if response and len(response) > 0 and (turn_context.activity.text != response[0].answer):
                await turn_context.send_activity(MessageFactory.text(response[0].answer))
            else:
                if turn_context.activity.text == "wait":
                    return await turn_context.send_activities([
                        Activity(
                            type=ActivityTypes.typing
                        ),
                        Activity(
                            type="delay",
                            value=3000
                        ),
                        Activity(
                            type=ActivityTypes.message,
                            text="Finished Typing"
                        )
                    ])
                elif turn_context.activity.text == "test sql":
                    output = DB_query("Select ID from user_info")
                    for i in range(0, len(output), 2):
                        await turn_context.send_activity(output[i] + ' ' + output[i+1])
                # elif turn_context.activity.text == "get my id":
                #     await turn_context.send_activity(self.user_id)
                elif "評論"in turn_context.activity.text or "review"in turn_context.activity.text :
                    await turn_context.send_activity("稍等一下唷! 美食公道伯正在幫你尋找餐廳評論...")
                    # 展宏的func
                    re = webcrawl(turn_context.activity.text)
                    # 佑誠的func
                    blog_re=[]
                    blog_re = blogcrawler(turn_context.activity.text)
    
                    review_list = []
    
                    for index in range(len(blog_re)):
                        review_list.append(CardFactory.hero_card(HeroCard(title=blog_re[index][1], images=[CardImage(url=blog_re[index][3])], buttons=[CardAction(type="openUrl",title="前往網頁",value=blog_re[index][2])])))
                                    
                    if re:
                        review_list.append(CardFactory.hero_card(HeroCard(title=re["愛食記"][0], images=[CardImage(url=re["愛食記"][2])], buttons=[CardAction(type="openUrl",title="前往網頁",value=re["愛食記"][1])])))
                    
                    
                    message = MessageFactory.carousel(review_list)   
                    
                    await turn_context.send_activity(message)
    
                else:
    
                    restaurants_dict = googlemaps_API(turn_context.activity.text)
                    # 書文的func
                    re = webcrawl(turn_context.activity.text)

            response = await self.qna_maker.get_answers(turn_context)

            ## LUIS's result & intent
            recognizer_result = await self.recognizer.recognize(turn_context)
            intent = LuisRecognizer.top_intent(recognizer_result)
        # check if user typing in qna maker
            if response and len(response) > 0 and (turn_context.activity.text != response[0].answer):
                await turn_context.send_activity(MessageFactory.text(response[0].answer))
            else:
                if turn_context.activity.text == '我的最愛':
                    res = self.favor.get_favorite()
                    if (res is None):
                        await turn_context.send_activity("還沒有最愛的餐廳，趕快搜尋餐廳並加入最愛吧~")
                    else:
                        fav_list = []
                        for length in range(len(res)):
                            rest_name = res[length]
                            rest_location = find_position_with_xy(rest_name)
                            fav_list.append(CardFactory.hero_card(HeroCard(title=rest_name, subtitle=rest_location)))
                        message = MessageFactory.carousel(fav_list)                   
                        await turn_context.send_activity(message)
                elif "加入最愛" in turn_context.activity.text: ## add favorite button
                    rest_name = turn_context.activity.text.split("_")[0]
                    message = self.favor.add_favorite(user_id, rest_name)
                    await turn_context.send_activity(message)
                elif turn_context.activity.text == '歷史紀錄':
                    res = get_history(user_id)
                    if (res is None):
                        await turn_context.send_activity("還沒有瀏覽紀錄，趕快搜尋餐廳吧~")
                    else:
                        history_list = []
                        for length in range(len(res)):
                            rest_name = res[length]
                            rest_location = find_position_with_xy(rest_name)
                            history_list.append(CardFactory.hero_card(HeroCard(title=rest_name, subtitle=rest_location)))
                        message = MessageFactory.carousel(history_list)                   
                        await turn_context.send_activity(message)
                elif "評論"in turn_context.activity.text:
                    await turn_context.send_activity("稍等一下唷! 美食公道伯正在幫你尋找餐廳評論...")
                    # 展宏的func
                    re = webcrawl(turn_context.activity.text)
                    # 佑誠的func
                    blog_re=[]
                    blog_re = blogcrawler(turn_context.activity.text)


                    review_list = []
                    for index in range(len(blog_re)):
                        review_list.append(CardFactory.hero_card(HeroCard(title=blog_re[index][1], images=[CardImage(url=blog_re[index][3])], buttons=[CardAction(type="openUrl",title="前往網頁",value=blog_re[index][2])])))
                                    
                    if re:
                        review_list.append(CardFactory.hero_card(HeroCard(title=re["愛食記"][0], images=[CardImage(url=re["愛食記"][2])], buttons=[CardAction(type="openUrl",title="前往網頁",value=re["愛食記"][1])])))
                    
                    if len(review_list)!=0:
                        message = MessageFactory.carousel(review_list)   
                    else:
                        message = "未查詢到這間餐廳的相關評論文章喔～ 歡迎您發布首則評論！"
                    rest_name = turn_context.activity.text.split("_")[0]
                    add_history(user_id, rest_name)

                    message = MessageFactory.carousel(review_list)                   
                    await turn_context.send_activity(message)
            # # add restaurant to my favorite
            #     elif "加入我的最愛"in turn_context.activity.text:
            #         add_name = turn_context.activity.text.split("_")[0]
            #         insert_myfav = 'INSERT INTO user_info (ID, favorite) VALUES (\'' + user_id + '\', %s);'%(add_name)
            #         self.db_func.DB_insert(insert_myfav)
            
                elif turn_context.activity.text == "get my id":
                    user_id = turn_context.activity.recipient.id
                    await turn_context.send_activity(user_id)
                
                # 書文的func
                elif intent == "使用者食物類別": 

                    msg = '請輸入您目前的地點或是附近的景點 🧐（例如：北車、公館）（小提示：點擊Line的+號可以傳地址上來呦!）'
        
                    await turn_context.send_activity(msg)
                # elif(turn_context.activity.text.message.type=='location'):
                #     print('work')

                elif('_$' in turn_context.activity.text):
                    money_status = 1
                    # 判斷price_level
                    if('_$$' in turn_context.activity.text):
                        money_status = 2
                    elif('_$$$' in turn_context.activity.text):
                        money_status = 3
                        
                    restaurants_dict = googlemaps_API(turn_context.activity.text, money_status)
                    print('money_status:', money_status)
                    # 沒有餐廳的狀況
                    if(len(restaurants_dict) == 0):
                        message = "您附近沒有相對應的餐廳可以推薦呦，輸入『吃』來繼續👀"   

                    elif(len(restaurants_dict) >= 5):

                        message = MessageFactory.carousel([
                                CardFactory.hero_card(HeroCard(title=restaurants_dict[0]['name'], text='推薦指數 : ' + str(restaurants_dict[0]['rating']), images=[CardImage(url=show_photo(restaurants_dict[0]['photo_reference']))], buttons=[CardAction(type="openUrl",title="地圖",value="https://www.google.com/maps/search/?api=1&query=" + str(restaurants_dict[0]['location_x']) + "," + str(restaurants_dict[0]['location_y']) +"&query_place_id="+str(restaurants_dict[0]['place_id'])), CardAction(type="imBack",title="點此看評論",value=restaurants_dict[0]['name']+"_評論"), CardAction(type="imBack",title="加入我的最愛",value=restaurants_dict[0]['name']+"_加入最愛")])),
                                CardFactory.hero_card(HeroCard(title=restaurants_dict[1]['name'], text='推薦指數 : ' + str(restaurants_dict[1]['rating']), images=[CardImage(url=show_photo(restaurants_dict[1]['photo_reference']))], buttons=[CardAction(type="openUrl",title="地圖",value="https://www.google.com/maps/search/?api=1&query=" + str(restaurants_dict[1]['location_x']) + "," + str(restaurants_dict[1]['location_y']) +"&query_place_id="+str(restaurants_dict[1]['place_id'])), CardAction(type="imBack",title="點此看評論",value=restaurants_dict[1]['name']+"_評論"), CardAction(type="imBack",title="加入我的最愛",value=restaurants_dict[1]['name']+"_加入最愛")])),
                                CardFactory.hero_card(HeroCard(title=restaurants_dict[2]['name'], text='推薦指數 : ' + str(restaurants_dict[2]['rating']), images=[CardImage(url=show_photo(restaurants_dict[2]['photo_reference']))], buttons=[CardAction(type="openUrl",title="地圖",value="https://www.google.com/maps/search/?api=1&query=" + str(restaurants_dict[2]['location_x']) + "," + str(restaurants_dict[2]['location_y']) +"&query_place_id="+str(restaurants_dict[2]['place_id'])), CardAction(type="imBack",title="點此看評論",value=restaurants_dict[2]['name']+"_評論"), CardAction(type="imBack",title="加入我的最愛",value=restaurants_dict[2]['name']+"_加入最愛")])),
                                CardFactory.hero_card(HeroCard(title=restaurants_dict[3]['name'], text='推薦指數 : ' + str(restaurants_dict[3]['rating']), images=[CardImage(url=show_photo(restaurants_dict[3]['photo_reference']))], buttons=[CardAction(type="openUrl",title="地圖",value="https://www.google.com/maps/search/?api=1&query=" + str(restaurants_dict[3]['location_x']) + "," + str(restaurants_dict[3]['location_y']) +"&query_place_id="+str(restaurants_dict[3]['place_id'])), CardAction(type="imBack",title="點此看評論",value=restaurants_dict[3]['name']+"_評論"), CardAction(type="imBack",title="加入我的最愛",value=restaurants_dict[3]['name']+"_加入最愛")])),
                                CardFactory.hero_card(HeroCard(title=restaurants_dict[4]['name'], text='推薦指數 : ' + str(restaurants_dict[4]['rating']), images=[CardImage(url=show_photo(restaurants_dict[4]['photo_reference']))], buttons=[CardAction(type="openUrl",title="地圖",value="https://www.google.com/maps/search/?api=1&query=" + str(restaurants_dict[4]['location_x']) + "," + str(restaurants_dict[4]['location_y']) +"&query_place_id="+str(restaurants_dict[4]['place_id'])), CardAction(type="imBack",title="點此看評論",value=restaurants_dict[4]['name']+"_評論"), CardAction(type="imBack",title="加入我的最愛",value=restaurants_dict[4]['name']+"_加入最愛")])),
                        ])
                    elif len(restaurants_dict) == 4:
                        message = MessageFactory.carousel([
                                CardFactory.hero_card(HeroCard(title=restaurants_dict[0]['name'], text='推薦指數 : ' + str(restaurants_dict[0]['rating']), images=[CardImage(url=show_photo(restaurants_dict[0]['photo_reference']))], buttons=[CardAction(type="openUrl",title="地圖",value="https://www.google.com/maps/search/?api=1&query=" + str(restaurants_dict[0]['location_x']) + "," + str(restaurants_dict[0]['location_y']) +"&query_place_id="+str(restaurants_dict[0]['place_id'])), CardAction(type="imBack",title="點此看評論",value=restaurants_dict[0]['name']+"_評論"), CardAction(type="imBack",title="加入我的最愛",value=restaurants_dict[0]['name']+"_加入最愛")])),
                                CardFactory.hero_card(HeroCard(title=restaurants_dict[1]['name'], text='推薦指數 : ' + str(restaurants_dict[1]['rating']), images=[CardImage(url=show_photo(restaurants_dict[1]['photo_reference']))], buttons=[CardAction(type="openUrl",title="地圖",value="https://www.google.com/maps/search/?api=1&query=" + str(restaurants_dict[1]['location_x']) + "," + str(restaurants_dict[1]['location_y']) +"&query_place_id="+str(restaurants_dict[1]['place_id'])), CardAction(type="imBack",title="點此看評論",value=restaurants_dict[1]['name']+"_評論"), CardAction(type="imBack",title="加入我的最愛",value=restaurants_dict[1]['name']+"_加入最愛")])),
                                CardFactory.hero_card(HeroCard(title=restaurants_dict[2]['name'], text='推薦指數 : ' + str(restaurants_dict[2]['rating']), images=[CardImage(url=show_photo(restaurants_dict[2]['photo_reference']))], buttons=[CardAction(type="openUrl",title="地圖",value="https://www.google.com/maps/search/?api=1&query=" + str(restaurants_dict[2]['location_x']) + "," + str(restaurants_dict[2]['location_y']) +"&query_place_id="+str(restaurants_dict[2]['place_id'])), CardAction(type="imBack",title="點此看評論",value=restaurants_dict[2]['name']+"_評論"), CardAction(type="imBack",title="加入我的最愛",value=restaurants_dict[2]['name']+"_加入最愛")])),
                                CardFactory.hero_card(HeroCard(title=restaurants_dict[3]['name'], text='推薦指數 : ' + str(restaurants_dict[3]['rating']), images=[CardImage(url=show_photo(restaurants_dict[3]['photo_reference']))], buttons=[CardAction(type="openUrl",title="地圖",value="https://www.google.com/maps/search/?api=1&query=" + str(restaurants_dict[3]['location_x']) + "," + str(restaurants_dict[3]['location_y']) +"&query_place_id="+str(restaurants_dict[3]['place_id'])), CardAction(type="imBack",title="點此看評論",value=restaurants_dict[3]['name']+"_評論"), CardAction(type="imBack",title="加入我的最愛",value=restaurants_dict[3]['name']+"_加入最愛")])),
                        ])
                    elif len(restaurants_dict) == 3:
                        message = MessageFactory.carousel([
                                CardFactory.hero_card(HeroCard(title=restaurants_dict[0]['name'], text='推薦指數 : ' + str(restaurants_dict[0]['rating']), images=[CardImage(url=show_photo(restaurants_dict[0]['photo_reference']))], buttons=[CardAction(type="openUrl",title="地圖",value="https://www.google.com/maps/search/?api=1&query=" + str(restaurants_dict[0]['location_x']) + "," + str(restaurants_dict[0]['location_y']) +"&query_place_id="+str(restaurants_dict[0]['place_id'])), CardAction(type="imBack",title="點此看評論",value=restaurants_dict[0]['name']+"_評論"), CardAction(type="imBack",title="加入我的最愛",value=restaurants_dict[0]['name']+"_加入最愛")])),
                                CardFactory.hero_card(HeroCard(title=restaurants_dict[1]['name'], text='推薦指數 : ' + str(restaurants_dict[1]['rating']), images=[CardImage(url=show_photo(restaurants_dict[1]['photo_reference']))], buttons=[CardAction(type="openUrl",title="地圖",value="https://www.google.com/maps/search/?api=1&query=" + str(restaurants_dict[1]['location_x']) + "," + str(restaurants_dict[1]['location_y']) +"&query_place_id="+str(restaurants_dict[1]['place_id'])), CardAction(type="imBack",title="點此看評論",value=restaurants_dict[1]['name']+"_評論"), CardAction(type="imBack",title="加入我的最愛",value=restaurants_dict[1]['name']+"_加入最愛")])),
                                CardFactory.hero_card(HeroCard(title=restaurants_dict[2]['name'], text='推薦指數 : ' + str(restaurants_dict[2]['rating']), images=[CardImage(url=show_photo(restaurants_dict[2]['photo_reference']))], buttons=[CardAction(type="openUrl",title="地圖",value="https://www.google.com/maps/search/?api=1&query=" + str(restaurants_dict[2]['location_x']) + "," + str(restaurants_dict[2]['location_y']) +"&query_place_id="+str(restaurants_dict[2]['place_id'])), CardAction(type="imBack",title="點此看評論",value=restaurants_dict[2]['name']+"_評論"), CardAction(type="imBack",title="加入我的最愛",value=restaurants_dict[2]['name']+"_加入最愛")])),
                        ])
                    elif len(restaurants_dict) == 2:
                        message = MessageFactory.carousel([
                                CardFactory.hero_card(HeroCard(title=restaurants_dict[0]['name'], text='推薦指數 : ' + str(restaurants_dict[0]['rating']), images=[CardImage(url=show_photo(restaurants_dict[0]['photo_reference']))], buttons=[CardAction(type="openUrl",title="地圖",value="https://www.google.com/maps/search/?api=1&query=" + str(restaurants_dict[0]['location_x']) + "," + str(restaurants_dict[0]['location_y']) +"&query_place_id="+str(restaurants_dict[0]['place_id'])), CardAction(type="imBack",title="點此看評論",value=restaurants_dict[0]['name']+"_評論"), CardAction(type="imBack",title="加入我的最愛",value=restaurants_dict[0]['name']+"_加入最愛")])),
                                CardFactory.hero_card(HeroCard(title=restaurants_dict[1]['name'], text='推薦指數 : ' + str(restaurants_dict[1]['rating']), images=[CardImage(url=show_photo(restaurants_dict[1]['photo_reference']))], buttons=[CardAction(type="openUrl",title="地圖",value="https://www.google.com/maps/search/?api=1&query=" + str(restaurants_dict[1]['location_x']) + "," + str(restaurants_dict[1]['location_y']) +"&query_place_id="+str(restaurants_dict[1]['place_id'])), CardAction(type="imBack",title="點此看評論",value=restaurants_dict[1]['name']+"_評論"), CardAction(type="imBack",title="加入我的最愛",value=restaurants_dict[1]['name']+"_加入最愛")])),
                        ])
                    elif len(restaurants_dict) == 1:
                        message = MessageFactory.carousel([
                                CardFactory.hero_card(HeroCard(title=restaurants_dict[0]['name'], text='推薦指數 : ' + str(restaurants_dict[0]['rating']), images=[CardImage(url=show_photo(restaurants_dict[0]['photo_reference']))], buttons=[CardAction(type="openUrl",title="地圖",value="https://www.google.com/maps/search/?api=1&query=" + str(restaurants_dict[0]['location_x']) + "," + str(restaurants_dict[0]['location_y']) +"&query_place_id="+str(restaurants_dict[0]['place_id'])), CardAction(type="imBack",title="點此看評論",value=restaurants_dict[0]['name']+"_評論"), CardAction(type="imBack",title="加入我的最愛",value=restaurants_dict[0]['name']+"_加入最愛")])),
                        ])
                        

                    await turn_context.send_activity(message)

                elif turn_context.activity.address!='':
                    turn_context.send_activity(turn_context.activity.address)
                    

                elif intent == "使用者地理位置" :              
                    message = MessageFactory.carousel([
                            CardFactory.hero_card(
                            HeroCard(title='您的所在位置為：' + str(turn_context.activity.text)
                            , subtitle= '請選擇您的預算區間： 🤑'
                            , buttons=[CardAction(type="imBack",title="$$$",value=str(turn_context.activity.text) + "_$$$")
                            , CardAction(type="imBack",title="$$",value=str(turn_context.activity.text) + "_$$")
                            , CardAction(type="imBack",title="$",value=str(turn_context.activity.text) + "_$")]
                            ))
                    
                    ])
                    await turn_context.send_activity(message)

                elif turn_context.activity.text == 'get id':
                    await turn_context.send_activity(turn_context.activity.recipient.id)
                # non-type
                else:
                    message = '不好意思，我聽不太明白，請說的具體一點'
                    await turn_context.send_activity(message)

        else:
            return_text = '很抱歉, 目前尚未支援您所使用的語言, 目前僅支援中文及英文'
            await turn_context.send_activity(translate_back(return_text,language_type))

# say hello at the beginning

    async def on_members_added_activity(
        self,
        members_added: ChannelAccount,
        turn_context: TurnContext
    ):
        for member_added in members_added:
            if member_added.id != turn_context.activity.recipient.id:
                ## DB insert new user
                id_res = self.db_func.DB_query('SELECT ID FROM user_info')
                user_id = turn_context.activity.recipient.id
                if user_id not in id_res:
                    insert_query = 'INSERT INTO user_info (ID, counter) VALUES (\'' + user_id + '\', 0);'
                    self.db_func.DB_insert(insert_query)
                    self.db_func.DB_commit()
                await turn_context.send_activity("美食公道伯在此🧙‍♂️，請輸入『我要大吃特吃』以繼續")