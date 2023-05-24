from PIL import Image
import easygui


#background image
backgroundPicPath=easygui.fileopenbox()
img1=Image.open(backgroundPicPath)

#overlay image
logoPicPath=easygui.fileopenbox()
img2=Image.open(logoPicPath)

#logo reshape
img2=img2.resize((270,310))

#paste img2 to img1
img1.paste(img2,(357,762))

img1.show()
