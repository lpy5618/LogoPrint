import cv2 as cv
import numpy as np
def choosePosition(windowName,img):
    points=[]
    img=np.array(img)
    def onMouse(event,x,y,flags,param):
        if event==cv.EVENT_LBUTTONDOWN:
            cv.circle(temp_img,(x,y),5,(102,217,239),-1)
            points.append((x,y))
            cv.imshow(windowName,temp_img)
    
    temp_img=img.copy()
    cv.namedWindow(windowName,cv.WINDOW_NORMAL)
    cv.imshow(windowName,temp_img)
    cv.setMouseCallback(windowName,onMouse)
    key=cv.waitKey(0)
    if key==13:           #Enter
        del temp_img
        cv.destroyAllWindows()
        return points
    elif key==27:           #ESC
        del temp_img
        cv.destroyAllWindows()
        return
    else:
        return choosePosition(windowName,img)

  # choice=input("which method do you prefer?\n1.input the logo position   2.pick a position by mouse   3.central point of background pic\n")
    # if choice=='1':
    # #input the logo position
    #     positionInput=map(int,input("please input the position of the logo: ").split(","))
    #     position=tuple(positionInput)
    # elif choice=='2':
    # #pick the logo position by mouse
    #     windowName="Position Picker"
    #     position=choosePosition(windowName,backgroundPic)[0]
    # elif choice=='3':
    # #paste logo at central point
    #     centralPoint=[backgroundPic.size[0]/2,backgroundPic.size[1]/2]#central point of the background pic
    #     position=tuple((int(centralPoint[0]-newWidth/2),int(centralPoint[1]-newHeight/2)))
    # else:
    #     print("wrong option, try again")
    #     continue