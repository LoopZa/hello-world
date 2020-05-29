import numpy as np
import pandas as pd 

import matplotlib.pyplot as plt
import seaborn as sns 
%matplotlib inline
from sklearn.model_selection import train_test_split
import os
import re
from datetime import datetime, timedelta

from sklearn.ensemble import RandomForestRegressor
from sklearn import metrics


RANDOM_SEED = 42
!pip freeze > requirements.txt
df_train = pd.read_csv('./input/main_task.csv')
df_test = pd.read_csv('./input/kaggle_task.csv')
sample_submission = pd.read_csv('./input/sample_submission.csv')

df_train['sample'] = 1 
df_test['sample'] = 0
df_test['Rating'] = 0 

data = df_test.append(df_train, sort=False).reset_index(drop=True)
data.fillna('0',inplace=True)

# Обработка признаков---------------------

# Разнообразие кухонь 
def diversity(x):
    if len(x)<2:
        return(0)
    else:
        x = list(x[1:-1].split(', '))
        return(len(x))
data['Diversity'] = data['Cuisine Style'].apply(lambda x:diversity(x))
#Обработка Price_Range
def price_rev(x):
    if x=='$':
        return(int(1))
    elif x=='$$ - $$$':
        return(int(2))
    elif x=='$$$$':
        return(int(3))
    else:
        return(0)
data['Price Range']=data['Price Range'].apply(lambda x:price_rev(x))

#Столицы
all_list = list(data['City'].unique())
dump_list = 'Oporto,Milan,Munich,Barcelona,Zurich,Lyon,Hamburg,Geneva,Krakow'.split(',')
def cap_dummy(x):
      if x in all_list:
            return(1)
      else:
           return(0)
for x in dump_list:
    if x in all_list:
        all_list.remove(x)
data['Capital']=data['City'].apply(lambda x:cap_dummy(x))
#Dummy по городам
data = pd.get_dummies(data, columns=[ 'City',], dummy_na=True)

# Свежесть времени между последними отзывами
def nonsense(rev_str):
        pattern = re.compile('\d\d\D\d\d\D\d\d\d\d')
        y = pattern.findall(rev_str)
        if (len(y)==2 or len(y)==1):
            return(datetime.strptime(y[0], '%m/%d/%Y'))
        else:
            return(0)
def good_job(rev_str):
     pattern = re.compile('\d\d\D\d\d\D\d\d\d\d')
     y = pattern.findall(rev_str)
     if len(y)==2:
        return(datetime.strptime(y[1], '%m/%d/%Y'))
     elif len(y)==1:
        return(datetime.strptime(y[0], '%m/%d/%Y'))
     else:
         return(0)
data['Last_rev']=data['Reviews'].apply(lambda x:nonsense(x))
data['Prelast_rev']=data['Reviews'].apply(lambda x:good_job(x))
data['Old_time']=0
for num_str in range(0,len(data)):
      try:
            data['Old_time'][num_str] = int((data['Last_rev'][num_str]-data['Prelast_rev'][num_str]).days)
      except:
            None
            
        
# Конец обработки признаков----------------

#Обработка для Kaggle

data.drop(['Restaurant_id','ID_TA',], axis = 1, inplace=True)
data.drop([ 'URL_TA','Reviews','Cuisine Style','Name','Last_rev','Prelast_rev'], axis = 1, inplace=True)
train_data = data.query('sample == 1').drop(['sample'], axis=1)
y = train_data.Rating.values
X = train_data.drop(['Rating'], axis=1)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=RANDOM_SEED)
model = RandomForestRegressor(n_estimators=100, verbose=1, n_jobs=-1, random_state=RANDOM_SEED)
model.fit(X_train, y_train)
y_pred = model.predict(X_test)
print('MAE:', metrics.mean_absolute_error(y_test, y_pred))

test_data = data.query('sample == 0').drop(['sample'], axis=1)
test_data = test_data.drop(['Rating'], axis=1)
predict_submission = model.predict(test_data)
sample_submission['Rating'] = predict_submission
sample_submission.to_csv('solution.csv', index=False)
sample_submission.head()
print(data)
