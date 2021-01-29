import googlemaps
import opendata
# 餐具友善餐廳列表
good_list = opendata.get_data()
# Client initialization
API_key = 'AIzaSyAPtgFF8msgOfa_CK_FevErxHxH6HGZ8EM'
gmaps = googlemaps.Client(key=API_key)

def googlemaps_search_location(place):
# 尋找位置的經緯度
# http形式： https://maps.googleapis.com/maps/api/geocode/json?address=%E5%8C%97%E8%BB%8A&key=AIzaSyAPtgFF8msgOfa_CK_FevErxHxH6HGZ8EM
    geocode_result = gmaps.geocode(place)
    x = geocode_result[0]['geometry']['location']['lat']
    y = geocode_result[0]['geometry']['location']['lng']
    # print('經緯度', x, y)
    return (x, y)

def googlemaps_search_nearby(x,y):
    location = (x, y)
    radius = 1000    #1km
    place_type = 'restaurant'
    result = gmaps.places_nearby(location, radius, type=place_type, language='zh-TW')

    restaurants = result['results']
    restaurants_list=[]
    # sort the restaurant by its rating
    for i in restaurants:
        # 先過濾掉沒有rating的商店, 且使用者rating至少有50則
        if('rating' in i and 'price_level' in i and i['user_ratings_total'] > 50):
            place_id=''
            price_level= i['price_level']
            rating= i['rating']
            business_status=''
            location_x=''
            location_y=''
            name=''
            photo_reference=''
            user_ratings_total=''
            address=''
            if('place_id' in i):
                place_id = i['place_id']
            if('business_status' in i):
                business_status = i['business_status']
            if('geometry' in i):
                location_x = i['geometry']['location']['lat']
                location_y = i['geometry']['location']['lng']
            if('name' in i):
                name = i['name']
            if('photos' in i):
                photo_reference = i['photos'][0]['photo_reference']
            if('user_ratings_total' in i):
                user_ratings_total = i['user_ratings_total']
            if('vicinity' in i):
                address = i['vicinity']
            # create each restaurant dict
            restaurant = {            
                'place_id':place_id,
                'price_level':price_level,
                'rating' : rating,
                'business_status':business_status,
                'location_x':location_x,
                'location_y':location_y,
                'name':name,
                'photo_reference':photo_reference,
                'user_ratings_total':user_ratings_total,
                'address':address
            }
            restaurants_list.append(restaurant)

    # 以rating排序restaurant_list
    restaurants_list = sorted(restaurants_list, key=lambda k: k['rating'], reverse=True)
    # print(restaurants_list)
    # print('餐廳總數：', len(restaurants_list))
    return restaurants_list
  
# 供外界call的function，回傳格式：[{},{},...,{}]
def googlemaps_API(place, money_status):
    x, y = googlemaps_search_location(place)
    restaurants = googlemaps_search_nearby(x,y)
    if(money_status == 1):
        restaurants = list(filter(lambda x: x['price_level']==1, restaurants))
    elif(money_status == 2):
        restaurants = list(filter(lambda x: x['price_level']==2 or x['price_level']==1, restaurants))
    else:
        restaurants = list(filter(lambda x: x['price_level']==3 or x['price_level']==2 or x['price_level']==1, restaurants))

    return restaurants

# show photo of restaurant
def show_photo(ref):
    url = 'https://maps.googleapis.com/maps/api/place/photo?maxwidth=400&photoreference='+ ref +'&key='+API_key
    return url
