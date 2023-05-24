from PIL import Image
import easygui


#background image
backgroundPicPath=easygui.fileopenbox(msg="please choose the background image")
img1=Image.open(backgroundPicPath)

#overlay image
logoPicPath=easygui.fileopenbox(msg="please choose the logo")
img2=Image.open(logoPicPath)

#logo reshape
width,height=img2.size
rate=int(input("please input the size of the logo: "))
newWidth=int(width*rate/100)
newHeight=int(height*rate/100)
img2=img2.resize((newWidth,newHeight))

#paste img2 to img1
positionInput=map(int,input("please input the position of the logo: ").split(","))
position=tuple(positionInput)
img1.paste(img2,position)

img1.show()

#save result pic to file
savePath=easygui.filesavebox(msg="where do you want to save this file? ",default="test.png" )
if savePath:
    img1.save(savePath)
