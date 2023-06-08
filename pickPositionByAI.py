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
            resBox=frcnn.detect_image(img, crop = crop, count = count)
            tempPos=[]
            for j in resBox:
                classtype,pos=j
                print('classtype:',classtype)
                print('pos:',pos)
                if classtype=='dashedcircle':
                    top, left, bottom, right = pos
                    centralPoint=tuple((int(left+(right-left)/2),int(top+(bottom-top)/2)))
                    location=tuple((int(centralPoint[0]-logoWidth/2),int(centralPoint[1]-logoHeight/2)))
                    newWidth=logoWidth
                    newHeight=logoHeight
                    temp=[]
                    temp.append(location)
                    temp.append(newWidth)
                    temp.append(newHeight)
                    tempPos.append(temp)
                elif classtype=='dashedbox':
                    top, left, bottom, right = pos
                    posWidth = int(right - left)
                    posHeight = int(bottom - top)
                    if inputPosition == 'central':
                        newWidth = int(logoWidth * posHeight / logoHeight)
                        newHeight = posHeight
                        if newWidth>posWidth:
                            newWidth=posWidth
                            newHeight=int(logoHeight*posWidth/logoWidth)
                        centralPoint=[left+(right-left)/2,top+(bottom-top)/2]#central point of the dashedbox
                        location=tuple((int(centralPoint[0]-newWidth/2),int(centralPoint[1]-newHeight/2)))
                        temp=[]
                        temp.append(location)
                        temp.append(newWidth)
                        temp.append(newHeight)
                        tempPos.append(temp)

                    elif inputPosition == "left":
                        newWidth = int(logoWidth * posHeight / logoHeight)
                        newHeight = posHeight
                        location = tuple((int(left), int(top)))
                        if newWidth>posWidth:
                            newWidth=posWidth
                            newHeight=int(logoHeight*posWidth/logoWidth)
                            location=tuple((int(left),int(top+(bottom-top)/2-newHeight/2)))
                        temp=[]
                        temp.append(location)
                        temp.append(newWidth)
                        temp.append(newHeight)
                        tempPos.append(temp)
                            
                    elif inputPosition == "top":
                        newWidth=posWidth
                        newHeight=int(logoHeight*posWidth/logoWidth)
                        location=tuple((int(left), int(top)))
                        if newHeight>posHeight:
                            newHeight=posHeight
                            newWidth=int(logoWidth * posHeight / logoHeight)
                            location=tuple((int(left+(right-left)/2-newWidth/2),int(top)))
                        temp=[]
                        temp.append(location)
                        temp.append(newWidth)
                        temp.append(newHeight)
                        tempPos.append(temp)
                            
                    elif inputPosition == "right":
                        newWidth = int(logoWidth * posHeight / logoHeight)
                        newHeight = posHeight
                        location = tuple((int(right-newWidth),int(top)))
                        if newWidth>posWidth:
                            newWidth=posWidth
                            newHeight=int(logoHeight*posWidth/logoWidth)
                            location=tuple((int(right-newWidth),int(top+(bottom-top)/2-newHeight/2)))
                        temp=[]
                        temp.append(location)
                        temp.append(newWidth)
                        temp.append(newHeight)
                        tempPos.append(temp)
                            
                    elif inputPosition == "bottom":
                        newWidth=posWidth
                        newHeight=int(logoHeight*posWidth/logoWidth)
                        location=tuple((int(left), int(bottom-newHeight)))
                        if newHeight>posHeight:
                            newHeight=posHeight
                            newWidth=int(logoWidth * posHeight / logoHeight)
                            location=tuple((int(left+(right-left)/2-newWidth/2),int(bottom-newHeight)))
                        temp=[]
                        temp.append(location)
                        temp.append(newWidth)
                        temp.append(newHeight)
                        tempPos.append(temp)
                    # if inputPosition=='central':
                    #     centralPoint=[left+(right-left)/2,top+(bottom-top)/2]#central point of the dashedbox
                    #     position=tuple((int(centralPoint[0]-logoWidth/2),int(centralPoint[1]-logoHeight/2)))
                    #     tempPos.append(position)
                    # elif inputPosition=="left":
                    #     position=tuple((int(left),int(top+(bottom-top)/2-logoHeight/2)))#top left position of the logo position
                    #     tempPos.append(position)
                    # elif inputPosition=="top":
                    #     position=tuple((int(left+(right-left)/2-logoWidth/2),int(top)))#top left position of the logo position
                    #     tempPos.append(position)
                    # elif inputPosition=="right":
                    #     position=tuple((int(right-logoWidth),int(top+(bottom-top)/2-logoHeight/2)))#top left position of the logo position
                    #     tempPos.append(position)
                    # elif inputPosition=="bottom":
                    #     position=tuple((int(left+(right-left)/2-logoWidth/2),int(bottom-logoHeight)))#top left position of the logo position
                    #     tempPos.append(position)
            posBox.append(tempPos)

        except:
            posBox.append([])
    return posBox
