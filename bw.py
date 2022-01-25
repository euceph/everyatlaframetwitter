import cv2
from PIL import Image
from matplotlib import pyplot as plt
import numpy as np
from colormap import rgb2hex

colors = None
pixeln = None

def check_if_grayscale(filename):
    img = Image.open(str(filename))
    global colors
    colors = img.getcolors(img.size[0] * img.size[1])
    global pixeln
    pixeln = img.size[0] * img.size[1]
    return colors
    #if len(clrs) < 256:
        #return True
    #else:
        #return False

def get_clrs_summed(filename):
    img = Image.open(str(filename))
    clrs = img.getcolors(img.size[0] * img.size[1])
    sumaq = 0
    for clr in clrs:
        sumaq += clr[0]
    return sumaq

def get_clrs_sorted(filename):
    img = Image.open(str(filename))
    global colors
    colors = img.getcolors(img.size[0] * img.size[1])
    global pixeln
    pixeln = img.size[0] * img.size[1]
    sumaq = 0
    for clr in colors:
        sumaq += clr[0]
    sorted_pixels = sorted(colors, key=lambda t: t[0], reverse=True)
    return sorted_pixels


# echo -e '\033[38;2;R;G;Bmtext\033[0;00m'

#print("expected: false | got: " + str(check_if_grayscale('bw/bwtest.jpeg')).lower() + " | colors: " + str(len(clrs))) # false
#print("expected: false | got: " + str(check_if_grayscale('bw/bwtest2.jpeg')).lower() + " | colors: " + str(len(clrs)))# false
#print("expected: false | got: " + str(check_if_grayscale('bw/bwtest3.jpeg')).lower() + " | colors: " + str(len(clrs))) # false
#print("expected: false | got: " + str(check_if_grayscale('bw/bwtest4.jpeg')).lower() + " | colors: " + str(len(clrs))) # false
#print("expected: false | got: " + str(check_if_grayscale('bw/bwtest5.jpeg')).lower() + " | colors: " + str(len(clrs))) # false
#print("expected: false | got: " + str(check_if_grayscale('bw/clrtest.jpeg')).lower() + " | colors: " + str(len(clrs))) # false
#print("expected: false | got: " + str(check_if_grayscale('bw/clrtest2.jpeg')).lower() + " | colors: " + str(len(clrs))) # false
#print("expected: true | got: " + str(check_if_grayscale('bw/bscreen.jpg')).lower() + " | colors: " + str(len(clrs))) # true
#print("expected: true | got: " + str(check_if_grayscale('bw/wscreen.jpeg')).lower() + " | colors: " + str(len(clrs))) # true
#print("expected: true | got: " + str(check_if_grayscale('bw/wscreen2.png')).lower() + " | colors: " + str(len(clrs))) # true
#print("expected: true | got: " + str(check_if_grayscale('bw/wscreen3.jpeg')).lower() + " | colors: " + str(len(clrs))) # true

f = 'bw/avtrtest3.jpeg'
#f = 'frametemp.jpg'
sclrs = get_clrs_sorted(f)

clrcnt = [0] * len(sclrs)
rgbarr = [''] * len(sclrs)
hexarr = [''] * len(sclrs)
clrcntr = 0
rgbcntr = 0
hexcntr = 0
rarr = [0] * len(rgbarr)
garr = [0] * len(rgbarr)
barr = [0] * len(rgbarr)


for clr in colors:
    clrcnt[clrcntr] = clr[0]
    rgbarr[clrcntr] = clr[1]
    clrcntr += 1
    #print(str(clr[1][0]) + " | " + str(clr[1][1]) + " | " + str(clr[1][2]))

for rgb in rgbarr:
    rarr[rgbcntr] = rgb[0]
    garr[rgbcntr] = rgb[1]
    barr[rgbcntr] = rgb[2]
    rgbcntr += 1

for rgb in rgbarr:
    hexarr[hexcntr] = rgb2hex(rarr[hexcntr], garr[hexcntr], barr[hexcntr])
    hexcntr += 1

sclrs.reverse()

print("colors: ")
for i in range (len(sclrs)):
    print(str(sclrs[i]))
print("filename: " + f + "\npixel num: " + str(pixeln) + "\nadded color count: " + str(get_clrs_summed(f)) + "\nnum colors: " + str(len(colors))) # false
#fig = plt.figure(figsize=(20,14))
#plt.pie(clrcnt, colors=hexarr)
#plt.show()
