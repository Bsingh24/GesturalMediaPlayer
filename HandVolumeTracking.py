import cv2
import numpy as np
import mediapipe
import time
import HandTrackingModule as htm
import math


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






while True:
    success, img = cap.read()
    img = detector.findHands(img)
    lmList = detector.findPosition(img,draw=False)
    if len(lmList) != 0:
        # print(lmList[4],lmList[8])

        x1,y1 = lmList[4][1],lmList[4][2]
        x2,y2 = lmList[8][1],lmList[8][2]
        xc,yc = (x1+x2)//2, (y1+y2)//2



        cv2.circle(img,(x1,y1),15,(255,0,255),cv2.FILLED)
        cv2.circle(img,(x2,y2),15,(255,0,255),cv2.FILLED)
        cv2.line(img,(x1,y1),(x2,y2),(255,0,255),3 )
        cv2.circle(img,(xc,yc),15,(255,0,255),cv2.FILLED)

        length = math.hypot(x2-x1,y2-y1)
        print(length)

        #hand range 300 to 50
        vol = np.interp(length,[50,300],[minVol,maxVol])
        volume.SetMasterVolumeLevel(-20.0, None)

        if length<50:
            cv2.circle(img, (xc, yc), 15, (0, 255, 0), cv2.FILLED)

    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime

    cv2.putText(img, str(int(fps)), (40, 70), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 0), 3)

    cv2.imshow("Img", img)
    cv2.waitKey(1)