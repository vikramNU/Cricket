import cv2
import time
import os
import HandTrackingModule as htm
import numpy as np

wCam, hCam = 640, 480
bow = 0
Score = 0
Fianl_Score = 0
Comp_Score=0
cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)

pTime = 0

detector = htm.handDetector(0.7, 0.5)

tipIds = [4, 8, 12, 16, 20]
turn = None
out = None
while True:
    success, img = cap.read()
    img = detector.findHands(img)
    lmList = detector.findPosition(img, draw=False)

    if len(lmList) != 0:
        fingers = []

        # Thumb
        if lmList[tipIds[0]][1] > lmList[tipIds[0] - 1][1]:
            fingers.append(1)
        else:
            fingers.append(0)

        # 4 Fingers
        for id in range(1, 5):
            if lmList[tipIds[id]][2] < lmList[tipIds[id] - 2][2]:
                fingers.append(1)
            else:
                fingers.append(0)

        # print(fingers)
        totalFingers = fingers.count(1)
        #print(totalFingers)

#         h, w, c = overlayList[totalFingers - 1].shape
#         img[0:h, 0:w] = overlayList[totalFingers - 1]

        #cv2.rectangle(img, (20, 225), (170, 425), (0, 255, 0), cv2.FILLED)
        cv2.putText(img, str(totalFingers), (100, 175), cv2.FONT_HERSHEY_PLAIN,
                    10, (255, 0, 0), 25)
    
    
    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime

    k = cv2.waitKey(10)
    
    if k == 27:
        break
    
    elif k == ord('s'):
        randStart = np.random.randint(5)+1
        print('Outcomes:',randStart,count_defects+1)
        if (randStart+count_defects+1)%2==state:
            OddEven = "You have won press 1 to bat and 2 to bowl"
        else:
            decisionstate=['ball',"bat"]
            decision=str(np.random.choice(decisionstate))
            OddEven = ("You have lost, Bot has choosen to "+decision)
            bow=decisionstate.index(decision)
    
    elif k == ord('b'):
        print(bow)
        if bow == 1:
                turn = 'You are bowling'
                x = np.random.randint(5)+1

                guess = cv2.imread('%d.jpg' % x)
                cv2.imshow('Desktop',guess)
                print('Outcomes:',x,totalFingers)
                out_string = str(x) + '  ' + str(totalFingers)
#                 cv2.putText(img, out_string, (400, 70), cv2.FONT_HERSHEY_PLAIN,
                #3, (255, 0, 0), 3)
               
                if x != totalFingers:
                    print( 'comp_Run',totalFingers)
                    Score = Score+totalFingers
                    print( 'Computers_New_Score:',Score)
                    if Score > Final_Score:
                        print('Computer Wins.')
                else:
                    print('Out!')
                    Comp_Score = Score
                    print('Final_Computer_Score',Comp_Score)
                    print('Your_Final_Score_was',Final_Score)
                    out = 'Computer is out!'
                    outPic = cv2.imread('OUT.png')
                    cv2.imshow("Image", outPic)
                    if Final_Score>Comp_Score:
                        print('you win by ',Final_Score-Comp_Score,' Runs.')
                        break
                    else:
                        print('This is a Draw.')
                        break

        if bow == 0:
            turn = 'You are batting'
            x = np.random.randint(5)+1
            guess = cv2.imread('%d.jpg' % x)
            cv2.imshow('Desktop',guess)
            out_string = 'computer - ' + str(x) + '  '+ 'player - ' + str(totalFingers)

#             cv2.putText(img, out_string, (400, 70), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 0), 3)
               
            print('Outcomes:',x,totalFingers)

            if x != totalFingers :
                print( 'Run:',totalFingers)
                Score = Score+totalFingers
#                 cv2.putText(img, str(Score), (800, 70), cv2.FONT_HERSHEY_PLAIN,3, (255, 0, 0), 3)
                

                print( 'New_Score:',Score)
            else:
                print('Out!')
                out = 'You are out!'
                outPic = cv2.imread('OUT.png')
                cv2.imshow("Image", outPic)
                Final_Score = Score
                Score = 0
                print( 'Final Score',Final_Score)
                print('Now your bowling turn')
                bow = 1
    
    cv2.putText(img, turn, (100, 70), cv2.FONT_HERSHEY_PLAIN,3, (255, 0, 0), 3)
    cv2.putText(img, str(Score), (100, 140), cv2.FONT_HERSHEY_PLAIN,3, (255, 0, 0), 3)
    cv2.putText(img, out, (100,100 ), cv2.FONT_HERSHEY_PLAIN,3, (255, 0, 0), 3)
    cv2.imshow("Image", img)

cap.release()
cv2.destroyAllWindows()