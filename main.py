from PIL import Image
import easygui


#background image
backgroundPicPath=easygui.fileopenbox()
img1=Image.open(backgroundPicPath)

#overlay image
logoPicPath=easygui.fileopenbox()
img2=Image.open(logoPicPath)

#logo reshape
width,height=img2.size
rate=int(input("please input the size of the logo: "))
newWidth=int(width*rate/100)
newHeight=int(height*rate/100)
img2=img2.resize((newWidth,newHeight))

#paste img2 to img1
img1.paste(img2,(357,762))

img1.show()

#save result pic to file
savePath=easygui.filesavebox(msg="where do you want to save this file? ",default="test.png" )
img1.save(savePath)
