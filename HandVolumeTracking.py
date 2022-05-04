import cv2
import numpy as np
import mediapipe
import time
import HandTrackingModule as htm
import math
import pyautogui

import os
#from playsound import playsound

from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

################

wcam = 1280
hcam = 720
midcam = hcam / 2

################

cap = cv2.VideoCapture(0)
cap.set(3, wcam)
cap.set(4, hcam)
pTime = 0

detector = htm.handDetector(detectionCon=0.7)


globTF = 0
playpauseTF = 0
shiftTF = 0
xylock = 0
muteTF = 0
tempy1 = 0
tempy2 = 0
tempy3 = 0
tempy4 = 0
tempy5 = 0
tempx1 = 0
tempx2 = 0
tempx3 = 0
tempx4 = 0
tempx5 = 0

t = time.perf_counter()
while True:
    success, img = cap.read()
    img = detector.findHands(img)
    lmList = detector.findPosition(img, draw=False)
    if len(lmList) != 0:
        palmx, palmy = lmList[0][1], lmList[0][2]
        thumbx, thumby = lmList[4][1], lmList[4][2]  # Thumb
        index_x, index_y = lmList[8][1], lmList[8][2]  # Index Finger
        middle_x, middle_y = lmList[12][1], lmList[12][2]  # Middle Finger
        ring_x, ring_y = lmList[16][1], lmList[16][2]  # Ring Finger
        pinky_x, pinky_y = lmList[20][1], lmList[20][2]  # Pinky Finger
        
        thumbkx, thumbky = lmList[2][1], lmList[2][2]  # Thumb knuckle
        index_kx, index_ky = lmList[6][1], lmList[6][2]  # Index Finger knuckle
        middle_kx, middle_ky = lmList[10][1], lmList[10][2]  # Middle Finger knuckle
        ring_kx, ring_ky = lmList[14][1], lmList[14][2]  # Ring Finger knuckle
        pinky_kx, pinky_ky = lmList[18][1], lmList[18][2]  # Pinky Finger knuckle


        cv2.circle(img, (thumbx, thumby), 15, (255, 0, 0), cv2.FILLED)
        cv2.circle(img, (index_x, index_y), 15, (255, 0, 0), cv2.FILLED)
        cv2.circle(img, (middle_x, middle_y), 15, (255, 0, 0), cv2.FILLED)
        cv2.circle(img, (ring_x, ring_y), 15, (255, 0, 0), cv2.FILLED)
        cv2.circle(img, (pinky_x, pinky_y), 15, (255, 0, 0), cv2.FILLED)

        xc, yc = (thumbx + index_x) // 2, (thumby + index_y) // 2

        #lock reset
        if (index_y < thumby) and (middle_y < thumby) and (ring_y < thumby) and (pinky_y < thumby) and index_y < index_ky and (middle_y < middle_ky) and (ring_y < ring_ky) and (pinky_y < pinky_ky):
            tempy1 = 0
            tempy2 = 0
            tempy3 = 0
            tempy4 = 0
            tempy5 = 0
            tempx1 = 0
            tempx2 = 0
            tempx3 = 0
            tempx4 = 0
            tempx5 = 0
            globTF = 0
            playpauseTF = 0
            shiftTF = 0
            xylock = 0
            muteTF = 0


        # play/pause, using  
        if (index_y < thumby) and (middle_y > thumby) and (ring_y > thumby) and (pinky_y > thumby):
            if(playpauseTF == 0):
                pyautogui.hotkey('playpause')
                playpauseTF = 1

        if (index_y < thumby) and (middle_y < thumby) and (ring_y > thumby) and (pinky_y > thumby):
            pyautogui.hotkey('stop')

        # # skip videos (at least on youtube). Next is shift + n, and last is shift + p.
        # # hand symbol for this is all fingers down(aside from thumb). Then drag hand left to go back, and right to skip video. right now it is using short cuts...
        # # so might need to change it.
        if (index_y > thumby) and (middle_y > thumby) and (ring_y > thumby) and (pinky_y > thumby):
            if (globTF == 0):
                tempy1 = thumby
                tempy2 = index_y
                tempy3 = middle_y
                tempy4 = ring_y
                tempy5 = pinky_y
                tempx1 = thumbx
                tempx2 = index_x
                tempx3 = middle_x
                tempx4 = ring_x
                tempx5 = pinky_x
                globTF = 1
                
            if (index_y > thumby) and (middle_y > thumby) and (ring_y > thumby) and (pinky_y > thumby):
                if (thumbx < tempx1 - 75 and shiftTF == 0):
                    pyautogui.keyDown('shift')
                    pyautogui.press('p')
                    pyautogui.keyUp('shift')
                    globTF = 0
                    tempy1 = 0
                    tempy2 = 0
                    tempy3 = 0
                    tempy4 = 0
                    tempy5 = 0
                    tempx1 = 0
                    tempx2 = 0
                    tempx3 = 0
                    tempx4 = 0
                    tempx5 = 0
                    shiftTF = 1
                if (thumbx > tempx1 + 75 and shiftTF == 0):
                    pyautogui.keyDown('shift')
                    pyautogui.press('n')
                    pyautogui.keyUp('shift')
                    globTF = 0
                    tempy1 = 0
                    tempy2 = 0
                    tempy3 = 0
                    tempy4 = 0
                    tempy5 = 0
                    tempx1 = 0
                    tempx2 = 0
                    tempx3 = 0
                    tempx4 = 0
                    tempx5 = 0
                    shiftTF = 1

        


        lengthfist = math.hypot(index_x - thumbx, index_y - thumby)
        if (lengthfist < 50 and muteTF == 0):
            muteTF = 1
            pyautogui.hotkey('volumemute')
            t = time.perf_counter()


        # if all tips are on the same x-axis, fast-forward or rewind mode
        # move flat hand left for rewind, right for fast forward
        if (index_x <= thumbx + 5 or index_x >= thumbx - 5) and (middle_x <= thumbx + 5 or middle_x >= thumbx - 5) and (
                ring_x <= thumbx + 5 or ring_x >= thumbx - 5) and (
                pinky_x <= thumbx + 5 or pinky_x >= thumbx - 5)  and (index_y < thumby) and (middle_y < thumby) and (ring_y < thumby) and (index_y < pinky_y):
            # cv2.putText(img, "FFW or RWD", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 2,(0,0,255), 2)
            if (globTF == 0):
                tempy1 = thumby
                tempy2 = index_y
                tempy3 = middle_y
                tempy4 = ring_y
                tempy5 = pinky_y
                tempx1 = thumbx
                tempx2 = index_x
                tempx3 = middle_x
                tempx4 = ring_x
                tempx5 = pinky_x
                globTF = 1

            if (index_x <= thumbx + 5 or index_x >= thumbx - 5) and (
                    middle_x <= thumbx + 5 or middle_x >= thumbx - 5) and (
                    ring_x <= thumbx + 5 or ring_x >= thumbx - 5) and (pinky_x <= thumbx + 5 or pinky_x >= thumbx - 5):
                if (thumbx > tempx1 + 50):
                    # cv2.putText(img, "RWD", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 2,(0,0,255), 2)
                    pyautogui.press('left')

                    globTF = 0
                    tempy1 = 0
                    tempy2 = 0
                    tempy3 = 0
                    tempy4 = 0
                    tempy5 = 0
                    tempx1 = 0
                    tempx2 = 0
                    tempx3 = 0
                    tempx4 = 0
                    tempx5 = 0
                    xylock = 0
                    
                if (thumbx < tempx1 - 50):
                    # cv2.putText(img, "RWD", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 2,(0,0,255), 2)
                    # pyautogui.press('left')
                    pyautogui.press('right')
                    globTF = 0
                    tempy1 = 0
                    tempy2 = 0
                    tempy3 = 0
                    tempy4 = 0
                    tempy5 = 0
                    tempx1 = 0
                    tempx2 = 0
                    tempx3 = 0
                    tempx4 = 0
                    tempx5 = 0
                    xylock = 0

        # if all tips are on the same y-axis, we increase or decrease the volume
        # move flat hand left for rewind, right for fast forward
        if (index_y <= thumby + 5 or index_y >= thumby - 5) and (middle_y <= thumby + 5 or middle_y >= thumby - 5) and (
                ring_y <= thumby + 5 or ring_y >= thumby - 5) and (pinky_y > thumby) and (pinky_y > middle_y) and (pinky_y > ring_y) and xylock == 0: 
            # cv2.putText(img, "FFW or RWD", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 2,(0,0,255), 2)

            if (globTF == 0):
                tempy1 = thumby
                tempy2 = index_y
                tempy3 = middle_y
                tempy4 = ring_y
                tempy5 = pinky_y
                tempx1 = thumbx
                tempx2 = index_x
                tempx3 = middle_x
                tempx4 = ring_x
                tempx5 = pinky_x
                globTF = 1
                xylock = 1
            if (index_y <= thumby + 3 or index_y >= thumby - 3) and (
                    middle_y <= thumby + 3 or middle_y >= thumby - 3) and (
                    ring_y <= thumby + 3 or ring_y >= thumby - 3) and (pinky_y <= thumby + 3 or pinky_y >= thumby - 3):
                if (thumby > tempy1 + 20):
                    # cv2.putText(img, "RWD", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 2,(0,0,255), 2)
                    pyautogui.hotkey('volumedown')
                    pyautogui.hotkey('volumedown')
                    globTF = 0
                    tempy1 = 0
                    tempy2 = 0
                    tempy3 = 0
                    tempy4 = 0
                    tempy5 = 0
                    tempx1 = 0
                    tempx2 = 0
                    tempx3 = 0
                    tempx4 = 0
                    tempx5 = 0
                    xylock = 0
                if (thumby < tempy1 - 20):
                    # cv2.putText(img, "RWD", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 2,(0,0,255), 2)
                    # pyautogui.press('left')
                    pyautogui.hotkey('volumeup')
                    pyautogui.hotkey('volumeup')
                    globTF = 0
                    tempy1 = 0
                    tempy2 = 0
                    tempy3 = 0
                    tempy4 = 0
                    tempy5 = 0
                    tempx1 = 0
                    tempx2 = 0
                    tempx3 = 0
                    tempx4 = 0
                    tempx5 = 0
                    xylock = 0

        if lengthfist < 50:
            cv2.circle(img, (xc, yc), 15, (0, 255, 0), cv2.FILLED)


    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime

    cv2.putText(img, str(int(fps)), (40, 70), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 0), 3)

    cv2.imshow("Img", img)
    cv2.waitKey(1)
