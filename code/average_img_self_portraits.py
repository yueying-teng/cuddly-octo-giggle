
# coding: utf-8

# In[24]:


import pandas as pd
import numpy as np
import re
import os
import glob
from PIL import Image
import matplotlib.pyplot as plt
get_ipython().run_line_magic('matplotlib', 'inline')
import cv2


# In[113]:


df = pd.read_csv('van_gogh_portrait.csv').iloc[:, 1: ]

year_created = []
file_name_list = []

for i in range(df.shape[0]):
    year = re.findall(r'\d{4}', df['year'].iloc[i])
    img_name = df.iloc[i]['img_name']
    name = str(i) + '_' + img_name + '_' + year[0] + '.jpg'
    year_created.append(year[0])
    file_name_list.append(name)
    


# In[114]:


df = df.drop('year', axis =1)
df['year'] = year_created
df['file_name'] = file_name_list
df.head()


# In[115]:



def image_resize(image, width, height, inter = cv2.INTER_AREA):
    '''
    resize the image to the size given without keeping the aspect ratio
    img is image np.array 
    '''
    
    dim = (width, height)
    resized = cv2.resize(image, dim, interpolation = inter)
    
    return resized


# In[116]:


gp = df.groupby('year')

years = []
yearly_df_list = []
for group, yearly_df in gp:
    years.append(group)
    yearly_df_list.append(yearly_df)
    


# In[ ]:


# genrate average self-portraits in each year 

width = 792
height = 1024

for i in range(len(years)):
    
    blank_arr = np.zeros((height, width , 3), np.float)

    df18 = yearly_df_list[i]
    img_list18 = [os.path.join('self_portrait_van_gogh', df18['file_name'].iloc[k]) for k in range(df18.shape[0])]
    n = len(img_list18)

    for j in range(len(img_list18)):
        
        img_arr = cv2.imread(img_list18[j])
        img_arr = cv2.cvtColor(img_arr, cv2.COLOR_BGR2RGB)

        resized_img_arr = image_resize(img_arr, width, height)

        blank_arr += resized_img_arr/ n
    
    filename = os.path.join('avg_self_portraits', years[i] + '_avg_portraits.jpg')
     
    print (years[i] + ' done')
    
    plt.imsave(filename, blank_arr/ 255.)
    

