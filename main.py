import sys
import os
import glob
from PIL import Image
from PIL import ImageOps
from PIL import ImageStat
import numpy as np
import matplotlib.pyplot as plt

"""

test numbers overview:
    original image - 1960x1960px
    tile size - 28x28px
    1960/28 = 70

"""



#Declare root directory name. Still a lot of repitition bc main.py under heavy construction
rootDir = 'pictures'

#makes everything in pictures directory small
for dirName, subdirList, fileList in os.walk(rootDir):
    for fname in fileList:
        imgpath = dirName+"\\"+fname
        im = Image.open(imgpath)
        im = im.resize((28,28), resample = Image.BILINEAR)
        im.save(dirName+"\\"+fname,"JPEG")

#helper function to merge two lists of same size into one list of tuples
#returns merged list
def merge(list1, list2):
    merged_list = [(list1[i], list2[i]) for i in range(0, len(list1))]
    return merged_list

#helper function to calculate rmb brightness of image
#returns float value
def brightness( im_file ):
   im = Image.open(im_file)
   stat = ImageStat.Stat(im)
   r,g,b = stat.rms
   return ((0.299*(r**2) + 0.587*(g**2) + 0.114*(b**2)))**(1/2)

#helper function to find the closest match in a list to a number
#returns index of list
def closest_match(list, target):
    curr = list[0][0]
    ans = 0
    for i in range (len(list)):
        if abs(target - list[i][0]) < abs(target - curr):
            curr = list[i][0]
            ans = i
    return ans


#size down the profile image and save as result.jpg
img = Image.open("test-gradient.jpg")
result = img.resize((70,70), resample=Image.BILINEAR)
result.save("result.jpg")

#TODO
#calculate the brightness of each pixel in result.jpg
im = Image.open("result.jpg").convert('L')
print(np.shape(im))
profile_brightness = np.zeros((70,70))
imarr = im.getdata()
imarr = np.array(imarr)
imarr = np.reshape(imarr, (70,70))
print(imarr)
rgb_count = 0
for i in range(70):
    for j in range(70):
        profile_brightness[i][j]= imarr[i][j]
print("")
print("profile_brightness:")
print(np.array(profile_brightness[0].astype(int)))


#return result.jpg to regular size
result = result.resize(img.size, Image.NEAREST)
result.save("result.jpg")
#print(np.shape(result))

#resize all images

#make a sorted list of rmb brightness and filenames
allimg_names = []
for i in os.walk("pictures"):
    for j in glob.glob(os.path.join(i[0], "*.jpg")):
        allimg_names.append(j)
allimg_brightness = []
for i in range(len(allimg_names)):
    b = brightness(allimg_names[i])
    allimg_brightness.append(b)
allimg = merge(allimg_brightness, allimg_names)
allimg = sorted(allimg)
print(allimg[len(allimg)-1])



#create a placement_ref array whos values are the allimg index that best matches the profile image brightness at each coordinate
placement_ref = np.zeros((70,70))
for i in range(70):
    for j in range(70):
        placement_ref[i][j] = closest_match(allimg, profile_brightness[i][j])
placement_ref = placement_ref.astype(int)
print("")
print("placement_ref:")
print(placement_ref[0])



tilecount = 0
final_mosaic = np.zeros((1960,1960,3))
print("BUILDING MOSAIC (Window will pop up when complete)")

#iterate through placement_ref
for i in range(70):
    y_offset = (i*28)%1960
    for j in range(70):
        x_offset = (j*28)%1960
        tilepath = allimg[placement_ref[i][j]][1]
        tile = Image.open(tilepath)
        tile = tile.getdata()
        tile_array = np.array(tile)
        tile_array = np.reshape(tile_array, (28,28,3))
        #fill in a tile
        for i in range(28):
            for j in range(28):
                for k in range(3):
                    final_mosaic[i+x_offset][j+y_offset][k] = tile_array[i][j][k]
        print(str(tilecount+1)+"/4900 tiles...", end = '\r')
        tilecount+=1
print("")
print("Mosaic finished - displaying...")
#(1960, 1960, 3)
plt.imshow(final_mosaic/255)
plt.show()
print("END OF PROGRAM")




"""
arr = np.zeros((120,120,3))
imarr = result.getdata()
finalimg = np.array(imarr)
finalimg = np.reshape(finalimg, (60,60,3))
#print(np.shape(finalimg))
for i in range(60):
    for j in range(60):
        for k in range(3):
            arr[i][j][k] = finalimg[i][j][k]
print(arr)
plt.imshow(arr/255)
plt.show()"""
#print(finalimg)


"""
test1 = ['h', 'e', 'l', 'l', 'o']
test2 = [4, 2, 3, 1, 0]
test3 = merge(test2, test1)
heapq.heapify(test3)
print(test3)
test3.pop()
print(test3)
test3.pop()
print(test3)

test3 = merge(test2, test1)
sorted(test3)
print(test3)"""
