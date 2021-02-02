# -*- coding: utf-8 -*-
"""
Created on Wed Jan 27 20:04:00 2021

@author: kevin
"""



import requests
from bs4 import BeautifulSoup
import time


#search_name = input("輸入餐廳名稱:")

start = time.time()



def blogcrawler(search_name):
    
    search_name = search_name.split("_")[0].split(' ')[0].split('-')[0].split('/')[0]

    blog_from=[]
    name_list=[]
    post_url_list=[]
    img_url_list=[]
    name_url_lists = []
    #====周花花====
    web = 'https://tenjo.tw/?s='+'台北 '+ str(search_name)
    
    content = requests.get(web)            
    objSoup = BeautifulSoup(content.text,"html.parser")
    
    objpost = objSoup.find_all('article',class_="blog-post")
        
        
    count=0
    for data in objpost:
        if count==0:
            if search_name in data.text:
                blog_from.append('周花花')
                #print(data.find('a').text)
                name_list.append(data.find('a').text)
                #print(data.find('a').get('href'))
                post_url_list.append(data.find('a').get('href'))
                #print(data.find('img').get('src'))
                img_url_list.append(data.find('img').get('src'))
                #print('---')
                count+=1
    
    
    
   
    
     #====愛吃鬼====
   
    web = 'https://aniseblog.tw/?s='+'台北 '+ str(search_name)

    content = requests.get(web)            
    objSoup = BeautifulSoup(content.text,"html.parser")
    
    objpost = objSoup.find_all('h1',class_='entry-title')
    
    count=0
    for data in objpost:
        if count==0:
            if search_name in data.text:
                blog_from.append('愛吃鬼')
                #print(data.text)
                name_list.append(data.text)
                #print(data.parent.parent.get('href'))
                post_url_list.append(data.parent.parent.get('href'))
                #print(data.parent.find('img').get('src'))
                img_url_list.append(data.parent.find('img').get('src'))
                #print('---')
                count+=1
    
  
   
   
    
     #====艾妮可====

    web = 'https://anikolife.com/?s=' + search_name

    content = requests.get(web)          
    
    
    objSoup = BeautifulSoup(content.text,"html.parser")
    
    obja = objSoup.find_all('a')
    
    
    count=0
    for data in obja:
        
        if search_name in data.text and '台北' in data.text and count==0:
            
            #print(data.text)
            #print(data.get('href'))
            #print(data.parent.parent.find_next_sibling().find('img').get('src'))
            
            blog_from.append('艾妮可')
            name_list.append(data.text)
            post_url_list.append(data.get('href'))
            img_url_list.append('https://image.freepik.com/free-photo/woman-making-photo-meal-her-phone_1303-18328.jpg')
            count+=1
    
        
            
            
            


    #====微笑樂園====
    web = 'https://www.liviatravel.com/2011/10/blog-post_5530.html'

    
    content = requests.get(web)            
    
    objSoup = BeautifulSoup(content.text,"html.parser")
    
    obja = objSoup.find_all('a')
    
    
    count=0
    for data in obja:
        if search_name in data.text and '台北' in data.text and count==0:
            blog_from.append('微笑樂園')
            #print(data.text)
            name_list.append(data.text)
            #print(data.get('href'))
            post_url_list.append(data.get('href'))
            img_url_list.append('https://image.freepik.com/free-photo/making-photograph-english-breakfast_144627-43701.jpg')
            count+=1
       
    for a in range(len(name_list)):
        name_url_list=[]
        #name_url_list.append(a)
        name_url_list.append(blog_from[a])
        name_url_list.append(name_list[a])
        name_url_list.append(post_url_list[a])
        name_url_list.append(img_url_list[a])
        
        name_url_lists.append(name_url_list)
        
   
    
       
        


    #all_dic = dict(zip(blog_from,name_url_lists))
    #print(all_dic)  
    return (name_url_lists)
#print(blogcrawler('一蘭拉麵'))

#print(time.time()-start)
        
              
        
        
        
        
        
        
        
        
        
        
        