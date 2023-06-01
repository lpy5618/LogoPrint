from rcnn.frcnn import FRCNN
from PIL import Image
import copy

def findPosByAI(inputImgPaths):
    frcnn=FRCNN()
    crop = False
    count = False
    paths=copy.deepcopy(inputImgPaths)
    posBox=[]
    for i in range(len(inputImgPaths)):
        img = Image.open(paths[i])
        pos=frcnn.detect_image(img, crop = crop, count = count)
        try:
            if len(pos):
                posBox.append(pos)
        except:
            posBox.append([])
    
    # try:
    #     image = Image.open(img)
    # except:
    #     print('Open Error! Try again!')
    # else:
    #     posBox = frcnn.detect_image(image, crop = crop, count = count)
    return posBox
