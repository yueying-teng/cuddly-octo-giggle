
import pandas as pd
import urllib.request
from self_portrait_url import *
from color_palette_percentage_bar_from_img import *
import re
import os
import glob
import cv2


# ### parse the table on wiki

# read the html of wikipedia page, the result will be a list
l = pd.read_html('https://en.wikipedia.org/wiki/List_of_works_by_Vincent_van_Gogh') 

# store the result in a dataframe
output = pd.DataFrame(l[0])

# save the info of rows contains self-portrait
portrait_idx_list = []

title = output[2]
for i in range(len(title)):
    if 'Self-Portrait' in title[i]:
        portrait_idx_list.append(i)
        


portrait_df = output.iloc[portrait_idx_list, :]
portrait_df = portrait_df.iloc[:, : 4].rename(columns = {0: 'original_table_index', 2: 'img_name', 3: 'year'})
portrait_df = portrait_df.drop(1, axis =1)
portrait_df.insert(1, 'img_url', self_portrait_url)

portrait_df.to_csv('van_gogh_portrait.csv')

portrait_df.head()


# ### download all self-portraits

exception = []

for i in range(portrait_df.shape[0]):
    
    try:
        url = portrait_df['img_url'].iloc[i]
        img_name = portrait_df['img_name'].iloc[i]
        year_recorded = portrait_df['year'].iloc[i]
        year = re.findall(r'\d{4}', year_recorded)

        name = str(i) + '_' + img_name + '_' + year[0] + '.jpg'

        urllib.request.urlretrieve(url, os.path.join('./self_portrait_van_gogh', name))
        
    except FileNotFoundError:
        
        exception.append(i)


for i in range(len(exception)):
    print (portrait_df.iloc[exception[i]]['img_url'])
    


# ### gerneate palette bar

portraits = glob.glob('./self_portrait_van_gogh/*.jpg')

for i in range(len(portraits)):
    
    img_dir = portraits[i]
    img = cv2.imread(img_dir)

    img_wpalette = generate_palette_plot(img)
    file_name = os.path.join('self_portrait_wcolor_palette', 'palette_' + portraits[i].split('/')[-1])

    plt.imsave(file_name, img_wpalette)
    


# 
# - In 1886, Van Gogh immersed himself in the avant-garde art scene of Paris and experimented with the Pointillist technique, learning to employ the brush to create rhythmic patterns and adopting the use of contrasting hues and complimentary colors that have come to characterize his style.
# 
# - Throughout 1887, Vincent continues his work in Paris. He frequents cafes with other painters and argues about art with Bernard and Gauguin. Over the course of the year, Vincent experiments with some different styles, including Japonaiseries and pointillism.
# 
# - In February of 1888, Van Gogh traveled to Arles to pursue his long-held interest in painting the lives of peasants in the vein of Jean-François Millet and Jules Breton (including his series of the postman, Joseph Roulin, and his family). On Christmas Eve 1888, Van Gogh threatened his friend Paul Gauguin and subsequently cut his own ear in a fit of violent passion.
# 
# - On 8 May 1889, Van Gogh institutionalised himself at the Saint Paul-de-Mausole mental asylum at Saint-Rémy-de-Provence. He found no companionship among the other inmates (many of whom were clinically insane) but began painting once more (his famous series of olive groves and cypresses).
# 
# - On 27 July 1890, Van Gogh returned from the fields covered with blood. This might have been a suicide attempt or an accident. He finally died in his brother Theo’s arms two days later.
# 


