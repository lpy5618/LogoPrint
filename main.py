from PIL import Image
import easygui
import os
# from randomPick import randomPickPics
from dataBase import getPathFromDB
from pickPositionByAI import findPosByAI,findPosByAWS

def main():
    index=1
    while(index):
        #background image folder
        # print("please choose the background image folder")
        # backgroundPicFolder=easygui.diropenbox(msg="please choose the background image folder")
        # args=input("please input your conditions: item color supplier type: ")
        # print(fileNum)
        # print(backgroundPicFolder)
        # backgroundPicPaths=randomPickPics(backgroundPicFolder,fileNum)
        backgroundPicPaths=getPathFromDB()
        # print(backgroundPicPaths)
        
        #overlay image
        print("please choose the logo")
        logoPicPath=easygui.fileopenbox(msg="please choose the logo")
        logoPic=Image.open(logoPicPath)

        #logo shape
        width,height=logoPic.size
        # rate=int(input("please input the size of the logo: "))
        # newWidth=int(width*rate/100)
        # newHeight=int(height*rate/100)
        # logoPic=logoPic.resize((newWidth,newHeight))

        #logo position
        inputPosition=input("please choose the position of the logo: ")
        
        #result saving folder
        print("please choose the result saving folder")
        saveFolder=easygui.diropenbox(msg="please choose the result saving folder")

        # positionBox=findPosByAI(inputPosition,width,height,backgroundPicPaths)
        positionBox=findPosByAWS(inputPosition,width,height,backgroundPicPaths)
        try:
            for j in positionBox:
                backgroundPic=j['image']
                posList=j['pos']
                imageName=j['imageName']
                print('poslist:',posList)
                print('backPic:',backgroundPic)
                for k in posList:
                    if len(k):
                        #paste logo to background pic, according to AI
                        location,newWidth,newHeight=k
                        # posBox,backgroundPic=j
                        # location,newWidth,newHeight=posBox
                        logoPic=logoPic.resize((newWidth,newHeight))
                        backgroundPic.paste(logoPic,location)
                # backgroundPic.show()
                #save result pic to file
                savePath=os.path.join(saveFolder,imageName)
                if savePath:
                    backgroundPic.save(savePath)
                    print("result pic saved at "+savePath)
        except Exception as ex:
            print(ex)        
            
        index=int(input("do you wish to continue? input 0 to exit\n"))

if __name__=="__main__":
    main()