# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.
from flask import Config
from botbuilder.ai.qna import QnAMaker, QnAMakerEndpoint, QnAMakerOptions
# from botbuilder.schema import ChannelAccount
from botbuilder.core import ActivityHandler, MessageFactory, TurnContext, CardFactory
from botbuilder.schema import ChannelAccount, HeroCard, CardImage, CardAction
from websrestaurantrecom import webcrawl
from restaurant_recom import googlemaps_API, show_photo 
from sql import DB_query
from linebot.models.sources import SourceUser
from blogcrawler import blogcrawler
from translator import detect_translater_language,translate_back

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
        # self.user_id = str(SourceUser.sender_id())

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
                    
                    message = MessageFactory.carousel([
                            CardFactory.hero_card(HeroCard(title=restaurants_dict[0]['name'], text='推薦指數 : ' + str(restaurants_dict[0]['rating']), images=[CardImage(url=show_photo(restaurants_dict[0]['photo_reference']))], buttons=[CardAction(type="openUrl",title="地圖",value="https://www.google.com/maps/search/?api=1&query=" + str(restaurants_dict[0]['location_x']) + "," + str(restaurants_dict[0]['location_y']) +"&query_place_id="+str(restaurants_dict[0]['place_id'])), CardAction(type="imBack",title="點此看評論",value=restaurants_dict[0]['name']+"_評論")])),
                            CardFactory.hero_card(HeroCard(title=restaurants_dict[1]['name'], text='推薦指數 : ' + str(restaurants_dict[1]['rating']), images=[CardImage(url=show_photo(restaurants_dict[1]['photo_reference']))], buttons=[CardAction(type="openUrl",title="地圖",value="https://www.google.com/maps/search/?api=1&query=" + str(restaurants_dict[1]['location_x']) + "," + str(restaurants_dict[1]['location_y']) +"&query_place_id="+str(restaurants_dict[1]['place_id'])), CardAction(type="imBack",title="點此看評論",value=restaurants_dict[0]['name']+"_評論")])),
                            CardFactory.hero_card(HeroCard(title=restaurants_dict[2]['name'], text='推薦指數 : ' + str(restaurants_dict[2]['rating']), images=[CardImage(url=show_photo(restaurants_dict[2]['photo_reference']))], buttons=[CardAction(type="openUrl",title="地圖",value="https://www.google.com/maps/search/?api=1&query=" + str(restaurants_dict[2]['location_x']) + "," + str(restaurants_dict[2]['location_y']) +"&query_place_id="+str(restaurants_dict[2]['place_id'])), CardAction(type="imBack",title="點此看評論",value=restaurants_dict[2]['name']+"_評論")])),
                            CardFactory.hero_card(HeroCard(title=restaurants_dict[3]['name'], text='推薦指數 : ' + str(restaurants_dict[3]['rating']), images=[CardImage(url=show_photo(restaurants_dict[3]['photo_reference']))], buttons=[CardAction(type="openUrl",title="地圖",value="https://www.google.com/maps/search/?api=1&query=" + str(restaurants_dict[3]['location_x']) + "," + str(restaurants_dict[3]['location_y']) +"&query_place_id="+str(restaurants_dict[3]['place_id'])), CardAction(type="imBack",title="點此看評論",value=restaurants_dict[3]['name']+"_評論")])),
                            CardFactory.hero_card(HeroCard(title=restaurants_dict[4]['name'], text='推薦指數 : ' + str(restaurants_dict[4]['rating']), images=[CardImage(url=show_photo(restaurants_dict[4]['photo_reference']))], buttons=[CardAction(type="openUrl",title="地圖",value="https://www.google.com/maps/search/?api=1&query=" + str(restaurants_dict[4]['location_x']) + "," + str(restaurants_dict[4]['location_y']) +"&query_place_id="+str(restaurants_dict[4]['place_id'])), CardAction(type="imBack",title="點此看評論",value=restaurants_dict[4]['name']+"_評論")])),
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
        else:
            return_text = '很抱歉, 目前尚未支援您所使用的語言, 目前僅支援中文及英文'
            await turn_context.send_activity(translate_back(return_text,language_type))

# say helllo at the beginning
    async def on_members_added_activity(
        self,
        members_added: ChannelAccount,
        turn_context: TurnContext
    ):
        for member_added in members_added:
            if member_added.id != turn_context.activity.recipient.id:
                await turn_context.send_activity("Hello and welcome!")