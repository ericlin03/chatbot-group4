import numpy as np
import pandas as pd
import re

def get_vege_data():
    data = pd.read_csv('台北素食.csv', encoding='utf-8')
    data = data.iloc[:,0].values.tolist()
    for a in range(len(data)):
        item = data[a].split('.')[1]
        item=re.sub(r'[\':\s ,]*｜', '', item)
        data[a] = item
    return data

#print(get_vege_data())



