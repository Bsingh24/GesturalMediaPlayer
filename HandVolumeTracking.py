import cv2
import numpy as np
import mediapipe
import time
import HandTrackingModule as htm
import math
import pyautogui

import os
from playsound import playsound


from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

################

wcam = 1280
hcam = 720


################

cap = cv2.VideoCapture(0)
cap.set(3,wcam)
cap.set(4,hcam)
pTime = 0

detector = htm.handDetector(detectionCon=0.7)



devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))
#volume.GetMute()
#volume.GetMasterVolumeLevel()
volRange = volume.GetVolumeRange()
minVol = volRange[0]
maxVol = volRange[1]
val = 0
volBar = 400


globTF = 0
playpauseTF = 0
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



while True:
    success, img = cap.read()
    img = detector.findHands(img)
    lmList = detector.findPosition(img,draw=False)
    if len(lmList) != 0:
        x1,y1 = lmList[4][1],lmList[4][2] #Thumb
        x2,y2 = lmList[8][1],lmList[8][2] #Index Finger
        x3,y3 = lmList[12][1],lmList[12][2] #Middle Finger
        x4,y4 = lmList[16][1],lmList[16][2] #Ring Finger
        x5,y5 = lmList[20][1],lmList[20][2] #Pinky Finger

        cv2.circle(img, (x1, y1), 15, (255, 0, 255), cv2.FILLED)
        cv2.circle(img, (x2, y2), 15, (255, 0, 255), cv2.FILLED)
        cv2.circle(img, (x3, y3), 15, (255, 0, 255), cv2.FILLED)
        cv2.circle(img, (x4, y4), 15, (255, 0, 255), cv2.FILLED)
        cv2.circle(img, (x5, y5), 15, (255, 0, 255), cv2.FILLED)

        xc,yc = (x1+x2)//2, (y1+y2)//2

        print(y1)
        print(y2)
        #making a full open hand be the reset
        if (y2 < y1) and (y3 < y1) and (y4 < y1) and (y5 < y1):
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

        #these are the lower the level
        if (y2 > y1) and (y3 < y1) and (y4 < y1) and (y5 < y1): #index finder
            pyautogui.hotkey('volumedown')
        elif (y3 > y1) and (y2 < y1) and (y4 < y1) and (y5 < y1): #middle finger
            pyautogui.hotkey('volumeup')
        elif (y4 > y1) and (y2 < y1) and (y3 < y1) and (y5 < y1): #ring finger
            pyautogui.hotkey('stop')
        elif (y5 > y1) and (y2 < y1) and (y3 < y1) and (y4 < y1): #pinky finger
            if(playpauseTF == 0):
                pyautogui.hotkey('playpause')
                playpauseTF = 1

        #something a little more advanced
        #hold hand like a gun with y2 and y3 in the air, with y4 and y5 pointed down. Then move y1 upwards to hand. to cancel just move hand or release hand.
        if(y2 < y1) and (y3 < y1) and (y4 > y1) and (y5 > y1):
            #keeps track where the values are at before hand
            if (globTF == 0):
                tempy1 = y1
                tempy2 = y2
                tempy3 = y3
                tempy4 = y4
                tempy5 = y5
                tempx1 = x1
                tempx2 = x2
                tempx3 = x3
                tempx4 = x4
                tempx5 = x5
                globTF = 1
            if(y2 < y1) and (y3 < y1) and (y4 > y1) and (y5 > y1) and (x5 < tempx1) and (x1 > tempx5):
                if(y2 < (tempy2)-15):
                    print("gun too high!")
                elif(y3 < (tempy3)-15):
                    print("gun too high!")
                elif(y1 < (tempy1)-20):
                    audio_file = os.path.dirname(__file__) + '/sounds/gunshot.mp3'
                    playsound(audio_file)
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

        #skip videos (at least on youtube). Next is shift + n, and last is shift + p.
        #hand symbol for this is all fingers down(aside from thumb). Then drag hand left to go back, and right to skip video. right now it is using short cuts...
        #so might need to change it.
        if(y2 > y1) and (y3 > y1) and (y4 > y1) and (y5 > y1):
                if (globTF == 0):
                    tempy1 = y1
                    tempy2 = y2
                    tempy3 = y3
                    tempy4 = y4
                    tempy5 = y5
                    tempx1 = x1
                    tempx2 = x2
                    tempx3 = x3
                    tempx4 = x4
                    tempx5 = x5
                    globTF = 1
                if (y2 > y1) and (y3 > y1) and (y4 > y1) and (y5 > y1):
                #if (y2 < y1) and (y3 < y1) and (y4 < y1):
                    #if (y5 > y1) and (y5 < y1 + 10):
                    if(x1 < tempx1 - 100):
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
                    if(x1 > tempx1 + 100):
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



        length = math.hypot(x2-x1,y2-y1)
        print(length)

        #hand range 300 to 50
        # vol = np.interp(length,[50,300],[minVol,maxVol])
        # volBar = np.interp(length,[50,300],[400,150])
        # volume.SetMasterVolumeLevel(vol, None)

        if length<50:
            cv2.circle(img, (xc, yc), 15, (0, 255, 0), cv2.FILLED)

    cv2.rectangle(img,(50,150), (85,400), (0,255,0), 3)
    cv2.rectangle(img,(50,int(volBar)), (85,400), (0,255,0), cv2.FILLED)

    # prevlength = length
    # while length <= 500 and length >= 0:
    #     if length > prevlength:
    #         pyautogui.hotkey('volume up')
    #     elif length < prevlength:
    #         pyautogui.hotkey('volume down')
    #     else:
    #         pass
    #     prevlength = length

    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime

    cv2.putText(img, str(int(fps)), (40, 70), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 0), 3)

    cv2.imshow("Img", img)
    cv2.waitKey(1)
    print("tempy is at ", tempy1)
