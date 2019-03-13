

import cv2
import numpy as np
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
get_ipython().run_line_magic('matplotlib', 'inline')
import seaborn as sns

# reference
# https://www.pyimagesearch.com/2014/05/26/opencv-python-k-means-color-clustering/



clusters = 6
bordersize = 60


def image_resize(image, width = None, height = None, inter = cv2.INTER_AREA):
    '''
    resize function that keeps the aspect ratio
    '''
    
    dim = None
    (h, w) = image.shape[: 2]
    
    if width is None and height is None:
        return image
    
    if width is None:
        r = height / float(h)
        dim = (int(w * r), height)
    else:
        r = width / float(w)
        dim = (width, int(h * r))
    
    resized = cv2.resize(image, dim, interpolation=inter)
    
    return resized



def centroid_histogram(clt):
    
    # grab the number of different clusters and create a histogram based on the number of pixels assigned to each cluster
    numLabels = np.arange(0, len(np.unique(clt.labels_)) + 1)
    (hist, _) = np.histogram(clt.labels_, bins = numLabels)

    # normalize the histogram, such that it sums to one
    hist = hist.astype("float")
    hist /= hist.sum()

    return hist



def plot_colors(hist, centroids):
    
    # initialize the bar chart representing the relative frequency of each of the colors
    bar = np.zeros((50, 300, 3), dtype = "uint8")
    startX = 0
    
    # Sort the centroids to form a gradient color look
    k = sorted(zip(hist, centroids), key = lambda x: sum(x[1]))
    percentage = [k[i][0] for i in range(len(k))]
    color = [k[i][1] for i in range(len(k))]
    
    # loop over the percentage of each cluster and the color of each cluster
    for (percent, color) in zip(percentage, color):
        # plot the relative percentage of each cluster
        endX = startX + (percent * 300)

        endX = startX + (percent * 300)
        cv2.rectangle(bar, (int(startX), 0), (int(endX), 50),
            color.astype("uint8").tolist(), -1)
        startX = endX

    return bar


def get_bar_img(img):
    
    # Since K-means algorithm is very labour intensive, need to do it on a smaller image copy
    # copy of the resized image
    img_copy = image_resize(cv2.cvtColor(img, cv2.COLOR_BGR2RGB), width = 100)
    # reshape the image to be a list of pixels
    pixel_img = img_copy.reshape((img_copy.shape[0] * img_copy.shape[1], 3))
    plt.imshow(img_copy)

    # use K-Means algorithm to find the color histogram
    clt = KMeans(n_clusters = clusters)
    clt.fit(pixel_img)

    # build a histogram of clusters and then create a figure representing the number of pixels labeled to each color
    hist = centroid_histogram(clt)

    # color palette bar
    bar = plot_colors(hist, clt.cluster_centers_)

    # Resize the palette bar to be even width with the source image 
    bar_img = image_resize(bar, width = int(img.shape[1]))
    
    return bar_img


def generate_palette_plot(img):
    
    bar_img = get_bar_img(img)

    # This is just a whitespace to put between the image and the color bar
    im = np.zeros((int(bordersize/ 2), int(img.shape[1]), 3), np.uint8)
    cv2.rectangle(im, (0, 0), (int(img.shape[1]), int(bordersize/ 2)), (255, 255, 255), -1)

    # Now we combine the video frame and the color bar into one image
    new_img = np.concatenate([cv2.cvtColor(img, cv2.COLOR_BGR2RGB), im, bar_img], axis = 0)
    
    return new_img


'''
# example 

img_dir = './monet/the_terrace.jpg'
img2 = cv2.imread(img_dir)

img2_palette = generate_palette_plot(img2)

'''



# pie chart 
# zipped = zip(hist, centroids)
# k = sorted(zipped, key = lambda x: sum(x[1]))

# percentage = [k[i][0] for i in range(len(k))]
# color = [k[i][1] for i in range(len(k))]

# fig, ax = plt.subplots()
# ax.pie(percentage, startangle = 90, colors = [color[i]/ 255 for i in range(len(color))])
# ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

# plt.show()

