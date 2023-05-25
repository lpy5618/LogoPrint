from PIL import Image
import easygui
from randomPick import randomPickPics
from dataBase import getPathFromDB


index=1
while(index):
    #background image folder
    # print("please choose the background image folder")
    # backgroundPicFolder=easygui.diropenbox(msg="please choose the background image folder")
    args=input("please input your conditions: color supplier type: ")
    fileNum=int(input("how many pics do you want to get?"))
    print(fileNum)
    # print(backgroundPicFolder)
    # backgroundPicPaths=randomPickPics(backgroundPicFolder,fileNum)
    backgroundPicPaths=getPathFromDB(args,fileNum)
    print(backgroundPicPaths)
    
    #overlay image
    print("please choose the logo")
    logoPicPath=easygui.fileopenbox(msg="please choose the logo")
    logoPic=Image.open(logoPicPath)

    #logo reshape
    width,height=logoPic.size
    rate=int(input("please input the size of the logo: "))
    newWidth=int(width*rate/100)
    newHeight=int(height*rate/100)
    logoPic=logoPic.resize((newWidth,newHeight))

    #result saving folder
    print("please choose the result saving folder")
    saveFolder=easygui.diropenbox(msg="please choose the result saving folder")

    for i in range(len(backgroundPicPaths)):
        #background image
        backgroundPicPath=backgroundPicPaths.pop()
        backgroundPic=Image.open(backgroundPicPath)
        centralPoint=[backgroundPic.size[0]/2,backgroundPic.size[1]/2]#central point of the background pic
        position=tuple((int(centralPoint[0]-newWidth/2),int(centralPoint[1]-newHeight/2)))

        #paste logo to background pic
        backgroundPic.paste(logoPic,position)

    #show the result pic
        # backgroundPic.show()

    #save result pic to file
    
        savePath=saveFolder+"\\"+backgroundPicPath.split("/").pop(-1)
        if savePath:
            backgroundPic.save(savePath)
            print("result pic saved at "+savePath)
    index=int(input("do you wish to continue? input 0 to exit\n"))
