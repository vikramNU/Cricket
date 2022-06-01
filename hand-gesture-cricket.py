import cv2,math
import matplotlib.pyplot as plt
import numpy as np

blurValue = 35
bow = 10
Score = 0
Fianl_Score = 0
Comp_Score=0
Final_Score=0
xin=0
side=0
choosestate=[1,2]
state = np.random.choice(choosestate)
OddEven=0
print('you will need a webcam to play this.')
print('\n')
print('Press Esc to quit.')

cap = cv2.VideoCapture(0)
while True:
    ret, img = cap.read()
    cv2.rectangle(img,(400,400),(100,100),(0,255,0),0)
    crop = img[100:400, 100:400]
    grey = cv2.cvtColor(crop, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(grey, (blurValue, blurValue), 0)
    _, thresh1 = cv2.threshold(blurred, 127, 255,
                               cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)
    cv2.imshow('Thresholded', thresh1)
    contours, hierarchy = cv2.findContours(thresh1.copy(),cv2.RETR_TREE,cv2.CHAIN_APPROX_NONE)
    max_area = -1
    for i in range(len(contours)):
        cnt=contours[i]
        area = cv2.contourArea(cnt)
        if(area>max_area):
            max_area=area
            ci=i
    cnt=contours[ci]    
    x,y,w,h = cv2.boundingRect(cnt)
    cv2.rectangle(crop,(x,y),(x+w,y+h),(0,0,255),0)
    hull = cv2.convexHull(cnt)
    drawing = np.zeros(crop.shape,np.uint8)
    cv2.drawContours(drawing,[cnt],0,(255,255,0),0)
    cv2.drawContours(drawing,[hull],0,(0,255,255),0)
    hull = cv2.convexHull(cnt,returnPoints = False)
    defects = cv2.convexityDefects(cnt,hull)
    count_defects = 0
    cv2.drawContours(thresh1, contours, -1, (0,255,0), 3)
    for i in range(defects.shape[0]):
        s,e,f,d = defects[i,0]
        start = tuple(cnt[s][0])
        end = tuple(cnt[e][0])
        far = tuple(cnt[f][0])
        # cv2.line(drawing,start,end,[0,255,0],2)
        # cv2.circle(drawing,far,5,[0,0,255],-1)
        a = math.sqrt((end[0] - start[0])**2 + (end[1] - start[1])**2)
        b = math.sqrt((far[0] - start[0])**2 + (far[1] - start[1])**2)
        c = math.sqrt((end[0] - far[0])**2 + (end[1] - far[1])**2)
        angle = math.acos((b**2 + c**2 - a**2)/(2*b*c)) * 57
        if angle <= 90:
            count_defects += 1
            cv2.circle(crop,far,1,[255,0,255],-1)
        #dist = cv2.pointPolygonTest(cnt,far,True)
        cv2.line(crop,start,end,[255,255,0],2)
        #cv2.circle(crop,far,5,[0,0,255],-1)
    if count_defects == 1:
        cv2.putText(img,"Your Score - One", (75,50), cv2.FONT_HERSHEY_DUPLEX, 1,1)
    elif count_defects == 2:
        cv2.putText(img,"Your Score - Two", (75,50), cv2.FONT_HERSHEY_DUPLEX, 1,1)
    elif count_defects == 3:
        cv2.putText(img,"Your Score - Three", (75,50), cv2.FONT_HERSHEY_DUPLEX, 1,1)
    elif count_defects == 4:
        cv2.putText(img,"Your Score - Four", (75,50), cv2.FONT_HERSHEY_DUPLEX, 1,1)
    elif count_defects == 5:
        cv2.putText(img,"Your Score - Five", (75,50), cv2.FONT_HERSHEY_DUPLEX, 1, 1)
    else:
        cv2.putText(img,"Your Score - Zero", (75,50),cv2.FONT_HERSHEY_DUPLEX, 1, 1)
    cv2.putText(img,"Computer score: %d"%xin, (75,150), cv2.FONT_HERSHEY_DUPLEX, 1, 1)
    cv2.putText(img,"Total score: %d"%Score, (75,250), cv2.FONT_HERSHEY_DUPLEX, 1, 1)
    if choosestate==1:
        cv2.putText(img,"The computer has fixed odd state", (75,350), cv2.FONT_HERSHEY_DUPLEX, 1, 1)
    else:
        cv2.putText(img,"The computer has fixed even state", (75,350), cv2.FONT_HERSHEY_DUPLEX, 1, 1)

    cv2.putText(img,"Odd Even Results: %s"%OddEven, (75,450), cv2.FONT_HERSHEY_DUPLEX, 1, 1)

    cv2.imshow('Drawing', drawing)
    cv2.imshow('end', crop)
    cv2.imshow('Gesture', img)
    k = cv2.waitKey(10)
    # print(k)
    if k == 27:
        break

    if k=='q':
        side=1

    elif k == ord('s'):
        randStart = np.random.randint(5)+1
        print('Outcomes:',randStart,count_defects+1)
        if (randStart+count_defects+1)%2==state:
            OddEven = "You have won press 1 to bat and 2 to bowl"
            side=2
        else:
            decisionstate=['ball',"bat"]
            decision=str(np.random.choice(decisionstate))
            OddEven = ("You have lost, Bot has choosen to "+decision)
            bow=decisionstate.index(decision)
            side=2

    elif k == ord('b'):
        if side==1:
            print("Batting")
            if bow == 1:
                    print("Round 2")
                    xin = np.random.randint(5)+1
                    print('Outcomes:',xin,count_defects+1)
                    if xin != count_defects+1:
                        print('Run',count_defects+1)
                        Score = Score+count_defects+1
                        print('Computers_New_Score:',Score)
                        if Score > Final_Score:
                            print('Computer Wins')
                    else:
                        print('Out!')
                        Comp_Score = Score
                        print('Final_Computer_Score',Comp_Score)
                        print('Your_Final_Score_was',Final_Score)
                        if Final_Score>Comp_Score:
                            print('you win by ',Final_Score-Comp_Score,' Runs.')
                            break
                        else:
                            print('This is a Draw.')
                            break
            if bow == 0:
                print("Round 1")
                xin = np.random.randint(5)+1
                print('Opponent',xin)
                print('Outcomes:',xin,count_defects+1)
                if xin != count_defects+1 :
                    print( 'Run:',count_defects+1)
                    Score = Score+count_defects+1
                    print( 'New_Score:',Score)
                else:
                    print('Out!')
                    Final_Score = Score
                    Score = 0
                    print( 'Final Score',Final_Score)
                    print('Now your bowling turn')
                    bow = 1
        if side==2:
            print("Bowling")
            if bow == 1:
                    print("Round 2")
                    xin = np.random.randint(5)+1
                    print('Outcomes:',xin,count_defects+1)
                    if xin != count_defects+1:
                        print('Run',count_defects+1)
                        Score = Score+count_defects+1
                        print('Computers_New_Score:',Score)
                        if Score > Final_Score:
                            print('Computer Wins')
                    else:
                        print('Out!')
                        Comp_Score = Score
                        print('Final_Computer_Score',Comp_Score)
                        print('Your_Final_Score_was',Final_Score)
                        if Final_Score>Comp_Score:
                            print('you win by ',Final_Score-Comp_Score,' Runs.')
                            break
                        else:
                            print('This is a Draw.')
                            break
            if bow == 0:
                print("Round 1")
                xin = np.random.randint(5)+1
                print('Opponent',xin)
                print('Outcomes:',xin,count_defects+1)
                if xin != count_defects+1 :
                    print( 'Run:',count_defects+1)
                    Score = Score+count_defects+1
                    print( 'New_Score:',Score)
                else:
                    print('Out!')
                    Final_Score = Score
                    Score = 0
                    print( 'Final Score',Final_Score)
                    print('Now your bowling turn')
                    bow = 1

cap.release()
cv2.destroyAllWindows()