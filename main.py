import tweepy
import cv2
import os
import random
import json
import sys
from PIL import Image

CONSUMER_KEY = 'CONSUMER_KEY'
CONSUMER_SECRET = 'CONSUMER_SECRET'
ACCESS_TOKEN = 'ACCESS_TOKEN'
ACCESS_TOKEN_SECRET = 'ACCESS_TOKEN_SECRET'

seasonpath = None
postvar = None
colors = 0
original_stdout = sys.stdout

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

api = tweepy.API(auth, wait_on_rate_limit=True)


def get_frame_number(filename):
    cap = cv2.VideoCapture(filename)
    frame_no = cap.get(cv2.CAP_PROP_FRAME_COUNT)
    return int(frame_no)


def get_random_frame(framen):
    numframes = framen
    randomfn = random.randint(0, numframes)
    return randomfn


def get_season_number():
    randoms = random.randint(1, 3)
    global seasonpath
    seasonpath = randoms
    return randoms


def get_episode_number(s):
    if (s == 1):
        randome = random.randint(1, 20)
    if (s == 2):
        randome = random.randint(1, 20)
    if (s == 3):
        randome = random.randint(1, 21)
    return randome


def get_filename():
    season = get_season_number()
    ep = get_episode_number(season)
    filename = 's{}e{:02d}.mp4'.format(season, ep)
    return filename


# def get_filepath(seasonp):
    # if seasonp == 1:
       # return '/Volumes/atladrive1/s1/'
    #if seasonp == 2:
        #return '/Volumes/atladrive1/s2/'
    #if seasonp == 3:
        #return '/Volumes/atladrive1/s3/'
    #else:
        #return ''


def get_filepath(seasonp):
    if seasonp == 1:
        return '/media/pi/atladrive1/s1/'
    if seasonp == 2:
        return '/media/pi/atladrive1/s2/'
    if seasonp == 3:
        return '/media/pi/atladrive1/s3/'
    else:
        return ''

def get_image_from_fn(filename, totf, rf):
    cap = cv2.VideoCapture(str(filename))
    totalf = totf
    randf = rf
    if randf >= 0 and randf <= totalf:
        cap.set(1, randf)
        ret, frame = cap.read()
        cv2.imwrite('/home/pi/Documents/everyatlaframetwitter/frametemp.jpg', frame)
    cap.release()
    cv2.destroyAllWindows()

def check_if_grayscale(filename):
    img = Image.open(str(filename))
    global colors
    clrs = img.getcolors(img.size[0] * img.size[1])
    colors = len(clrs)
    if len(clrs) < 256:
        return True
    else:
        return False

def post_frame(filename):
    media = api.media_upload(str(filename))
    global postvar
    postvar = api.update_status(status='', media_ids=[media.media_id])

try:
    os.remove('/home/pi/Documents/everyatlaframetwitter/frametemp.jpg')
except:
    pass

def get_var_value(filename="/home/pi/Documents/everyatlaframetwitter/rejectstore.dat"):
    with open(filename, "a+") as f:
        f.seek(0)
        if grayscale == True:
            val = int(f.read() or 0) + 1
        else:
            val = int(f.read() or 0)
        f.seek(0)
        f.truncate()
        f.write(str(val))
        return val

file = ''
filep = ''
fullfilepath = ''
filenomp4 = ''
fn = 0
framesstring = ''
frametopost = None
grayscale = None

def create_frame():
    try:
        os.remove('/home/pi/Documents/everyatlaframetwitter/frametemp.jpg')
    except:
        pass
    global file, filep, fullfilepath, fn, filenomp4, framesstring, frametopost, grayscale
    file = get_filename()
    filep = get_filepath(seasonpath)
    #file = 's2e02.mp4'
    #filep = '/Users/issaahmed/Code/everyatlaframetwitter/'
    fullfilepath = str(filep) + str(file)
    filenomp4 = os.path.splitext(file)[0]
    fn = get_frame_number(str(fullfilepath))
    rf = get_random_frame(fn)
    # rf = 14753
    framesstring = '{}/{}'.format(rf, fn)
    frametopost = get_image_from_fn(str(fullfilepath), fn, rf)
    grayscale = check_if_grayscale('/home/pi/Documents/everyatlaframetwitter/frametemp.jpg')

create_frame()
rejected = get_var_value()

while grayscale == True:
    with open('rejects.txt', 'a') as f:
        sys.stdout = f
        print("[Avatar: The Last Airbender; {}; Frame {}; Colors: {}]".format(filenomp4.upper(), (str(framesstring)), str(colors)))
        sys.stdout = original_stdout
    create_frame()
    rejected = get_var_value()


if grayscale == False:
    #print("[Avatar: The Last Airbender; {}; Frame {}; Colors: {}]".format(filenomp4.upper(), (str(framesstring)), str(colors)))
    post_frame('/home/pi/Documents/everyatlaframetwitter/frametemp.jpg')
    reply = api.update_status("[Avatar: The Last Airbender; {}; Frame {}; Colors: {}]".format(filenomp4.upper(), (str(framesstring)), str(colors)),
                              in_reply_to_status_id=postvar._json["id"], auto_populate_reply_metadata=True)
