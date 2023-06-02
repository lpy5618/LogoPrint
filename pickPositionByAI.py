from rcnn.frcnn import FRCNN
from PIL import Image

def findPosByAI(inputPosition,logoWidth,logoHeight,inputImgPaths):
    frcnn=FRCNN()
    crop = False
    count = False
    posBox=[]
    for i in range(len(inputImgPaths)):
        img = Image.open(inputImgPaths[i])
        
        
        try:
            classtype,pos=frcnn.detect_image(img, crop = crop, count = count)
            print(pos)
            print(classtype)
            tempPos=[]
            for j in pos:
                if classtype=='dashedcircle':
                    top, left, bottom, right = j
                    centralPoint=tuple(int(left+(right-left)/2),int(top+(bottom-top)/2))
                    tempPos.append(centralPoint)
                elif classtype=='dashedbox':
                    top, left, bottom, right = j
                    if inputPosition=='central':
                        centralPoint=[left+(right-left)/2,top+(bottom-top)/2]#central point of the dashedbox
                        position=tuple((int(centralPoint[0]-logoWidth/2),int(centralPoint[1]-logoHeight/2)))
                        tempPos.append(position)
                    elif inputPosition=="left":
                        position=tuple((int(left),int(top+(bottom-top)/2-logoHeight/2)))#top left position of the logo position
                        tempPos.append(position)
                    elif inputPosition=="top":
                        position=tuple((int(left+(right-left)/2-logoWidth/2),int(top)))#top left position of the logo position
                        tempPos.append(position)
                    elif inputPosition=="right":
                        position=tuple((int(right-logoWidth),int(top+(bottom-top)/2-logoHeight/2)))#top left position of the logo position
                        tempPos.append(position)
                    elif inputPosition=="bottom":
                        position=tuple((int(left+(right-left)/2-logoWidth/2),top+(bottom-top)/2-logoHeight))#top left position of the logo position
                        tempPos.append(position)
            posBox.append(tempPos)

        except:
            posBox.append([])
    return posBox
