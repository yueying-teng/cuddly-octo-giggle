
# https://en.wikipedia.org/wiki/List_of_works_by_Vincent_van_Gogh

from bs4 import BeautifulSoup
from urllib import request
import os, glob, re
import pandas as pd
import numpy as np



url = "https://en.wikipedia.org/wiki/List_of_works_by_Vincent_van_Gogh"

html = request.urlopen(url).read()
soup = BeautifulSoup(html, "html.parser")

table = soup.find_all('tr')
base_url = "https://en.wikipedia.org"


# save high resolution images to local dir
# save high resolution image links

img_link_list = []

for i, t in enumerate(table):
    print (i)
    
    try:
        link = t.find('a')
        link = link['href']
        new_url = base_url + link
        
        # click on the image link found in the table again 
        sub_html = request.urlopen(new_url)
        sub_soup = BeautifulSoup(sub_html, 'html.parser')
        sub_link = sub_soup.find('div', {'class': 'fullImageLink'})
        img_link = "https:" + sub_link.a['href']
        img_link_list.append(img_link)
        
        name = '_' + sub_link.a['href'].split('/')[-1]
        file_name = os.path.join('all_paintings', str(i) + name)
        request.urlretrieve(url = img_link, filename = file_name)
      
    except:
        print('error')
        continue

    

# parse the table form wiki where all info of all van gogh's work is stored
# read the html of wikipedia page, the result will be a list
l = pd.read_html('https://en.wikipedia.org/wiki/List_of_works_by_Vincent_van_Gogh') 

# store the result in a dataframe
output = pd.DataFrame(l[0])
output.columns = output.iloc[0, :]
output = output.iloc[1:, :]

# add img_link column
output.insert(1, 'img_link', img_link_list)
output = output.drop('Image', axis = 1)
output = output[['No.', 'img_link', 'Title', 'Year']].rename(columns = {'No.': 'original index', 'Title': 'img_name'})

# concise year
year_recorded = output['Year'].apply(lambda x: re.findall(r'\d{4}', x)[0])

output['year'] = year_recorded
output = output.drop('Year', axis = 1)


# add img_dir column
img_dir = [str(i + 1) + '_' + output['img_link'].iloc[i].split('/')[-1] for i in range(output.shape[0])]
img_dir = ['./all_paintings/' + img_dir[i] for i in range(len(img_dir))]

output.insert(2, 'img_dir', img_dir)
output.to_csv('./all_painting_list.csv', index = None)


