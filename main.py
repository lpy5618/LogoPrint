from PIL import Image
import easygui
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


index=1
while(index):
    #background image
    backgroundPicPath=easygui.fileopenbox(msg="please choose the background image")
    backgroundPic=Image.open(backgroundPicPath)

    #overlay image
    logoPicPath=easygui.fileopenbox(msg="please choose the logo")
    logoPic=Image.open(logoPicPath)

    #logo reshape
    width,height=logoPic.size
    rate=int(input("please input the size of the logo: "))
    newWidth=int(width*rate/100)
    newHeight=int(height*rate/100)
    logoPic=logoPic.resize((newWidth,newHeight))

    choice=input("which method do you prefer?\n1.input the logo position   2.pick a position by mouse\n")
    if choice=='1':
    #input the logo position
        positionInput=map(int,input("please input the position of the logo: ").split(","))
        position=tuple(positionInput)
    elif choice=='2':
    #pick the logo position by mouse
        windowName="Position Picker"
        position=choosePosition(windowName,backgroundPic)[0]
    else:
        print("wrong option, try again")
        continue

    #paste logo to background pic
    backgroundPic.paste(logoPic,position)

    backgroundPic.show()

    #save result pic to file
    savePath=easygui.filesavebox(msg="where do you want to save this file? ",default="test.png" )
    if savePath:
        backgroundPic.save(savePath)
        print("result pic saved at "+savePath)
    index=int(input("do you wish to continue? input 0 to exit\n"))
