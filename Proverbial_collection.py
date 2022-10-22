import cv2
import numpy as np
import time
from scipy.stats import norm
from datetime import datetime
import os
from pathlib import Path
home = str(os.getcwd())

i = 0
vc = cv2.VideoCapture(0)
path = os.path.join(home, "proverbial", "sampleimages")
path_log = os.path.join(home, "proverbial", "logs")

def wlog(path_log,a):
    p =os.path.join(path_log, 'other_metrics')
    if not os.path.isdir(p):
        # if the demo_folder2 directory is
        # not present then create it.
        os.makedirs(p)
    f = open(os.path.join(p, 'log'  + '.txt'), "a")
    f.write(datetime.now().strftime("%Y%m%d%H%M%S") + ',' + a+'\n')
    f.close()
def wimage(path,sub,im):
    p = os.path.join(path, sub)
    if not os.path.isdir(p):
        os.makedirs(p)
    cv2.imwrite(os.path.join(p, datetime.now().strftime("%Y%m%d%H%M%S") + '.png'), im)

if vc.isOpened(): # try to get the first frame
    rval, frame = vc.read()
while rval:
    i = i+1
    rval, frame = vc.read()

    wimage(path, 'original', frame)
    # cv2.imwrite(os.path.join(path,'original',datetime.now().strftime("%Y%m%d%H%M%S")+'.png'), frame)

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    wimage(path, 'gray', gray)
    # cv2.imwrite(os.path.join(path, 'gray', datetime.now().strftime("%Y%m%d%H%M%S") + '.png'), gray)

    # Noise reduction
    blurred = cv2.GaussianBlur(gray, (3, 3), 0)
    wimage(path, 'blurred', blurred)
    # cv2.imwrite(os.path.join(path, 'blurred', datetime.now().strftime("%Y%m%d%H%M%S") + '.png'), blurred)

    # thresholding
    mean, std = norm.fit(gray)
    thresh_min_value = int(mean + 0*std)
    thresh_max_value = int(mean + 1*std)
    thresh = cv2.threshold(blurred, thresh_min_value, 255, cv2.THRESH_BINARY)[1]
    cv2.imshow("Image", thresh)
    wlog(path_log,'Mean,' + str(mean))
    wlog(path_log,'SD,' + str(std))
    intensity_raw = np.mean(gray)
    wlog(path_log,'intensity weighted,' + str(intensity_raw))
    # print('raw:', intensity_raw)
    intensity = np.mean(gray[thresh])
    wlog(path_log,'intensity raw,' + str(intensity))
    # print(intensity)

    key = cv2.waitKey(20)
    time.sleep(60*15)
    if key == 27 or i == 200:  # exit on ESC
        break
