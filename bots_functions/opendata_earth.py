import numpy as np
import pandas as pd
import re

def get_earth_data():
    data = pd.read_csv('臺北市自備餐具優惠業者清單.csv', encoding='big5')
    data = data.iloc[:,0].values.tolist()
    for a in range(len(data)):
        item=re.sub(r'[\':\s ,]*?', '', data[a])
        data[a] = item
    return data


#data = get_earth_data()
data = get_earth_data()


