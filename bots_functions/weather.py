import requests
from bs4 import BeautifulSoup
import urllib.parse
import random

def todaytop3eat():
    try:
        response = requests.get("https://www.google.com/search?Aw&q=台北今日天氣")
        soup = BeautifulSoup(response.text, "html.parser")
        today = soup.find('div',{"class": "BNeawe tAd8D AP7Wnd"})
        today_des = today.text.replace("\n","")
        degree = int("".join(list(today_des.split("：")[-1][:2])))
        
    except:
        degree = 13
    weatherfood = { "cold":['火鍋', '薑母鴨', '湯圓', '熱炒', '四物湯', '羊肉爐', '鴛鴦鍋', '關東煮', '麻油雞', '蚵仔麵線'],
                    "warm":['燉飯', '油飯', '披薩', '速食', '火鍋', '便當', '牛肉麵', '泡麵', '迴轉壽司', '自助餐'],
                    "hot":['涼麵', '炸雞', '三明治', '沙拉', '咖哩飯', '御飯糰', '關東煮', '烏龍麵', '壽司', '麵包'],
                    }
    if degree <= 17:
        food = weatherfood["cold"]
    elif 17 < degree <= 22:
        food = weatherfood["warm"]
    else:
        food = weatherfood["hot"]
    
    ii = random.sample(food, k=3)
    print(degree, ii)
    tod = [degree, ii]
    return tod


