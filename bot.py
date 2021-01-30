# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.
from flask import Config
from botbuilder.ai.qna import QnAMaker, QnAMakerEndpoint, QnAMakerOptions
from botbuilder.ai.luis import LuisApplication, LuisRecognizer, LuisPredictionOptions
from botbuilder.core import ActivityHandler, MessageFactory, TurnContext, CardFactory, RecognizerResult
from botbuilder.schema import ChannelAccount, HeroCard, CardImage, CardAction, Activity, ActivityTypes
from websrestaurantrecom import webcrawl
from restaurant_recom import googlemaps_API, show_photo, googlemaps_search_location, find_position_with_xy, googlemaps_search_nearby
from sql import DB_function
from favorite import my_favorite
from history import history
from blogcrawler import blogcrawler
from linebot.models.sources import SourceUser
from azure.cognitiveservices.language.luis.authoring import LUISAuthoringClient
import opendata_earth 
import opendata_vegetable 
from azure.cognitiveservices.language.luis.runtime.models import LuisResult
from weather import todaytop3eat
import re
import json

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
        self.history = history()

# define what we response
    async def on_message_activity(self, turn_context: TurnContext):
        turn_context.activity.address=''
        ## DB insert old user
        id_res = self.db_func.DB_query('SELECT ID FROM user_info')
        user_id = turn_context.activity.recipient.id
#    if userid not in our db, add it        
        if user_id not in id_res:
            insert_query = 'INSERT INTO user_info (ID, counter) VALUES (\'' + user_id + '\', 0);'
            self.db_func.DB_insert(insert_query)
            self.db_func.DB_commit()

        ## QnA Maker's response
        response = await self.qna_maker.get_answers(turn_context)
            
    # check if user typing in qna maker
        if response and len(response) > 0 and (turn_context.activity.text != response[0].answer):
            await turn_context.send_activity(MessageFactory.text(response[0].answer))
    # 個人化推薦
        elif turn_context.activity.text == '個人化推薦':
            await turn_context.send_activity('success in')
            todayrecom = todaytop3eat()
            await turn_context.send_activity("今天最低溫為 %s, 為您推薦以下料理："%todayrecom[0])
            todaylist = []
            for tt in range(3):
                restaurants_dict = googlemaps_API("北車", 3, todayrecom[1][tt])
                todaylist.append(
                            CardFactory.hero_card(
                                HeroCard(
                                    title=restaurants_dict[0]['name'], text='推薦指數 : ' + str(restaurants_dict[0]['rating']), 
                                    images=[CardImage(url=show_photo(restaurants_dict[0]['photo_reference']))], 
                                    buttons=[CardAction(type="openUrl",title="地圖",
                                    value="https://www.google.com/maps/search/?api=1&query=" + str(restaurants_dict[0]['location_x']) + "," + str(restaurants_dict[0]['location_y']) +"&query_place_id="+str(restaurants_dict[0]['place_id'])), 
                                    CardAction(type="imBack",title="點此看評論",value=restaurants_dict[0]['name']+"_評論"), 
                                    CardAction(type="imBack",title="加入我的最愛",value=restaurants_dict[0]['name']+"_加入最愛")]
                                )
                            )
                        )
            msg = MessageFactory.carousel(todaylist)
            await turn_context.send_activity(msg)
        elif "加入最愛" in turn_context.activity.text: ## add favorite button
            rest_name = turn_context.activity.text.split("_")[0]
            message = self.favor.add_favorite(user_id, rest_name)
            await turn_context.send_activity(message)
        elif turn_context.activity.text == '瀏覽紀錄':
            res = self.history.get_history(user_id)
            if (res == []):
                await turn_context.send_activity("還沒有瀏覽紀錄，趕快搜尋餐廳吧~GOGO")
            else:
                history_list = []
                for length in range(len(res)):
                    rest_name = res[length]
                    rest_location = find_position_with_xy(rest_name)
                    (x, y) = googlemaps_search_location(rest_name)
                    history_list.append(CardFactory.hero_card(HeroCard(title=rest_name, subtitle=rest_location, buttons=[CardAction(type="openUrl",title="地圖",
                                value="https://www.google.com/maps/search/?api=1&query=" + str(x)+ ',' + str(y))])))
                message = MessageFactory.carousel(history_list)                   
                await turn_context.send_activity(message)
        elif turn_context.activity.text == '我的最愛':
            res = self.favor.get_favorite(user_id)
            if (res == []):
                await turn_context.send_activity("還沒有最愛的餐廳，趕快搜尋餐廳並加入最愛吧~GOGO")
            else:
                fav_list = []
                for length in range(len(res)):
                    rest_name = res[length]
                    rest_location = find_position_with_xy(rest_name)
                    (x, y) = googlemaps_search_location(rest_name)
                    fav_list.append(CardFactory.hero_card(HeroCard(title=rest_name, subtitle=rest_location, buttons=[CardAction(type="openUrl",title="地圖",
                                value="https://www.google.com/maps/search/?api=1&query=" + str(x)+ ',' + str(y))])))
                message = MessageFactory.carousel(fav_list)   
                await turn_context.send_activity(message)                
        elif "加入最愛" in turn_context.activity.text: ## add favorite button
            rest_name = turn_context.activity.text.split("_")[0]
            message = self.favor.add_favorite(user_id, rest_name)
            await turn_context.send_activity(message)
        # 歷史紀錄
        elif turn_context.activity.text == '瀏覽紀錄':
            res = self.history.get_history(user_id)
            print(user_id)
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
        # IG
        elif "_IG" in turn_context.activity.text:
            hashtag = turn_context.activity.text.split("_")[0].split(' ')[0].split('-')[0].split('/')[0].split("'")[0].split('&')[0]
            url = 'https://www.instagram.com/explore/tags/'+hashtag

            await turn_context.send_activity("稍等一下唷! 美食公道伯正在幫你尋找餐廳的IG熱門貼文...")
            message = MessageFactory.carousel([
                CardFactory.hero_card(HeroCard(title=hashtag+'的IG熱門文章',images=[CardImage(url='https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQB1DfQKJ-vfC16ybbNPP0N7FVVV6bNEC3W9Q&usqp=CAU')], buttons=[CardAction(type="openUrl",title="前往IG熱門文章",value=url)]))
            ])                   

            await turn_context.send_activity(message) 
        # 找評論

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
            self.history.add_history(user_id, rest_name)

            message = MessageFactory.carousel(review_list)                   
            await turn_context.send_activity(message)

            # 書文的func

            # line address
        elif ("{" in turn_context.activity.text and "}" in turn_context.activity.text):
            line_address_json = json.loads(turn_context.activity.text)
            print('line_address_json', line_address_json)
            x = line_address_json['latitude']
            y = line_address_json['longitude']
            restaurants_dict = googlemaps_search_nearby(x ,y ,'steak')
            # 沒有餐廳的狀況
            if(len(restaurants_dict) == 0):
                message = "您附近沒有相對應的餐廳可以推薦呦，輸入『吃』來繼續👀"   
            else:
                restaurants_list=[]
                for i in range(len(restaurants_dict)):
                    restaurants_list.append(
                        CardFactory.hero_card(
                            HeroCard(
                                title=restaurants_dict[i]['name'], text='推薦指數 : ' + str(restaurants_dict[i]['rating'])+ "👍", 
                                images=[CardImage(url=show_photo(restaurants_dict[i]['photo_reference']))], 
                                buttons=[CardAction(type="openUrl",title="地圖",
                                value="https://www.google.com/maps/search/?api=1&query=" + str(restaurants_dict[i]['location_x']) + "," + str(restaurants_dict[i]['location_y']) +"&query_place_id="+str(restaurants_dict[i]['place_id'])), 
                                CardAction(type="imBack",title="點此看評論",value=restaurants_dict[i]['name']+"_評論"), 
                                CardAction(type="imBack",title="加入我的最愛",value=restaurants_dict[i]['name']+"_加入最愛")]
                            )
                    ))
                    if(i==10):
                        break

                message = MessageFactory.carousel(restaurants_list)                   
                await turn_context.send_activity(message)
        else:
            ## LUIS's result & intent
            recognizer_result = await self.recognizer.recognize(turn_context)
            # parse intent and entity 
            intent = LuisRecognizer.top_intent(recognizer_result)
            print(intent)
            ## get user input and make response
            luis_result = recognizer_result.properties["luisResult"]
            entity=''
            if luis_result.entities:
                entities_list =[]
                for ll in luis_result.entities:
                    print(turn_context.activity.text)
                    print(ll)
                    ll.entity = ll.entity.replace(" ",'')
                    entities_list.append(ll.entity)
                print(entities_list)
                print(len(entities_list))
                if len(entities_list) == 1:
                    entity = entities_list[0]
                # two entites situation
                else:
                    entity = entities_list[0]+'^'+entities_list[1]
                    print("double entity:", entity)
            entity = entity.replace("\x08",'')
            
            if intent == "使用者食物類別" and "_$" not in turn_context.activity.text and "_IG" not in turn_context.activity.text:      

                message = MessageFactory.carousel([
                        CardFactory.hero_card(
                          HeroCard(title='您想吃的食物為：' + str(entity)
                        , subtitle= '請選擇您的預算區間： 🤑'
                        , buttons=[CardAction(type="imBack",title="$$$",value="我想吃"+str(entity)+"_$$$")
                        , CardAction(type="imBack",title="$$",value="我想吃"+str(entity)+"_$$")
                        , CardAction(type="imBack",title="$",value="我想吃"+str(entity)+"_$")]
                        ))
                ])
                await turn_context.send_activity(message)

                # msg = '請輸入您目前的地點或是附近的景點 🧐（例如：北車、公館）（小提示：點擊Line的+號可以傳地址上來呦!）'
       
                # await turn_context.send_activity(msg)

            elif intent == "使用者地理位置" and "_$" not in turn_context.activity.text and "_IG" not in turn_context.activity.text:
                if entity == "":
                    entity = turn_context.activity.text 
                    print(entity)             
                message = MessageFactory.carousel([
                        CardFactory.hero_card(
                        HeroCard(title='您的所在位置為：' + str(entity)
                        , subtitle= '請選擇您的預算區間： 🤑'
                        , buttons=[CardAction(type="imBack",title="$$$",value="我在" + str(entity) + "_$$$")
                        , CardAction(type="imBack",title="$$",value="我在" + str(entity) + "_$$")
                        , CardAction(type="imBack",title="$",value="我在" + str(entity) + "_$")]
                        ))
                ])
                await turn_context.send_activity(message)

            # find 2 entites in sequence
            elif "^" in entity:
                entity = entity.split("^")
                food = entity[0]
                location = entity[1]
                restaurants_dict = googlemaps_API(location, 2, food)
        
                 # 沒有餐廳的狀況
                if(len(restaurants_dict) == 0):
                    message = "您附近沒有相對應的餐廳可以推薦呦，輸入『我想吃...』來繼續👀"   
                else:
                    restaurants_list=[]
                    for i in range(len(restaurants_dict)):
                        restaurants_list.append(
                            CardFactory.hero_card(
                                HeroCard(
                                    title=restaurants_dict[i]['name'], text='推薦指數 : ' + str(restaurants_dict[i]['rating'])+ "👍", 
                                    images=[CardImage(url=show_photo(restaurants_dict[i]['photo_reference']))], 
                                    buttons=[CardAction(type="openUrl",title="地圖",
                                    value="https://www.google.com/maps/search/?api=1&query=" + str(restaurants_dict[i]['location_x']) + "," + str(restaurants_dict[i]['location_y']) +"&query_place_id="+str(restaurants_dict[i]['place_id'])), 
                                    CardAction(type="imBack",title="點此看評論",value=restaurants_dict[i]['name']+"_評論"), 
                                    CardAction(type="imBack",title="加入我的最愛",value=restaurants_dict[i]['name']+"_加入最愛")]
                                )
                        ))
                        if(i==10):
                            break

                    message = MessageFactory.carousel(restaurants_list)                   
                    await turn_context.send_activity(message)
                

            elif('_$' in turn_context.activity.text):
                money_status = 1
                msg = turn_context.activity.text    
                # 判斷price_level
                if('_$$' in turn_context.activity.text):
                    money_status = 2
                    msg = msg.replace('_$$', '')
                elif('_$$$' in turn_context.activity.text):
                    money_status = 3
                    msg = msg.replace('_$$$', '')
                msg = msg.replace('_$', '')
                msg = msg.replace('_', '')
                msg = msg.replace('我想吃', '')
                msg = msg.replace('我想喝', '')
                msg = msg.replace('我要吃', '')
                msg = msg.replace('我要喝', '')
                msg = msg.replace('我在', '')
                if(intent == '使用者食物類別'):
                    restaurants_dict = googlemaps_API("北車", money_status, msg)
                    print(restaurants_dict)
                elif(intent == '使用者地理位置'):
                    restaurants_dict = googlemaps_API(msg, money_status, '')
                    print(restaurants_dict)
                print('money_status:', money_status)
                print('msg:', msg)
                # 沒有餐廳的狀況
                if not restaurants_dict:
                    message = "您附近沒有相對應的餐廳可以推薦呦，輸入『我想吃...』來繼續👀" 
                    await turn_context.send_activity(message)  
                else:
                    # good_list = opendata_earth.get_earth_data()
                    # vegetable_list = opendata_vegetable.get_vege_data()

                    restaurants_list=[]
                    for i in range(len(restaurants_dict)):
                        restaurants_list.append(
                            CardFactory.hero_card(
                                HeroCard(
                                    title=restaurants_dict[i]['name'], text='推薦指數 : ' + str(restaurants_dict[i]['rating'])+" 👍", 
                                    images=[CardImage(url=show_photo(restaurants_dict[i]['photo_reference']))], 
                                    buttons=[CardAction(type="openUrl",title="地圖",
                                    value="https://www.google.com/maps/search/?api=1&query=" + str(restaurants_dict[i]['location_x']) + "," + str(restaurants_dict[i]['location_y']) +"&query_place_id="+str(restaurants_dict[i]['place_id'])), 
                                    CardAction(type="imBack",title="點此看IG熱門貼文",value=restaurants_dict[i]['name']+"_IG"),
                                    CardAction(type="imBack",title="點此看評論",value=restaurants_dict[i]['name']+"_評論"), 
                                    CardAction(type="imBack",title="加入我的最愛",value=restaurants_dict[i]['name']+"_加入最愛")]
                                )
                            )
                        )
              
                        
       
                        if(i == 10):
                            break

                    message = MessageFactory.carousel(restaurants_list)                   
                    await turn_context.send_activity(message)
                
            elif turn_context.activity.address!='':
                turn_context.send_activity(turn_context.activity.address)
            # non-type
            else:
                message = MessageFactory.carousel([
                    CardFactory.hero_card(
                    HeroCard( title="無法了解您的需求，美食公道伯在這邊先推薦幾家給您😉"
                    , subtitle= '請選擇您想吃的類型： 😗'
                    , buttons=[CardAction(type="imBack",title="咖啡廳",value="我想吃咖啡廳")
                    , CardAction(type="imBack",title="牛排",value="我想吃牛排")
                    , CardAction(type="imBack",title="火鍋",value="我想吃火鍋")]
                    ))
                ])
                await turn_context.send_activity(message)

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
                await turn_context.send_activity("美食公道伯在此🧙‍♂️，請輸入『我想吃...』以繼續")