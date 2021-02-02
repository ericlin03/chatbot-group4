# 爬美食記
import requests
from bs4 import BeautifulSoup
import urllib.parse

def webcrawl(usertypein):

    usertypein = usertypein.split("_")[0]

    response = requests.get("https://ifoodie.tw/explore/台北市/list/"+usertypein)
    soup = BeautifulSoup(response.text, "html.parser")

    restaurants = soup.find_all('a',{"class": "jsx-2133253768 title-text"})
    imgs = soup.find_all('div',{"class": "jsx-2133253768 restaurant-info"})
    restaurant_name_list = []
    restaurant_post_list = []
    restaurant_img_list = []
    for r in restaurants:
        restaurant_name_list.append(r.text)
        posturl = "https:/ifoodie.tw" + urllib.parse.unquote(r.get("href"))
        restaurant_post_list.append(posturl) 
    for i in imgs:
        # print(i)
        if i.find('img',{"class":"jsx-2133253768 cover lazyload"}) == None:
            imgurl = i.find('img',{"class":"jsx-2133253768 cover"}) 
            
            restaurant_img_list.append(imgurl.get("src"))
        else:
            imgurl = i.find('img',{"class":"jsx-2133253768 cover lazyload"})
            restaurant_img_list.append(imgurl.get("data-src"))
    url_lists = []
    for a in range(len(restaurant_post_list)):
        url_list=[]
        url_list.append(restaurant_post_list[a])
        url_list.append(restaurant_img_list[a])
        url_lists.append(url_list)
    try:
        li = []
        li.append(restaurant_name_list[0])
        li.append(restaurant_post_list[0])
        li.append(restaurant_img_list[0])
        dic = {"愛食記":li}

        return (dic)
    except:
        return False


# print(webcrawl("一蘭拉麵"))
