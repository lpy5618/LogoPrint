# from rcnn.frcnn import FRCNN
import math
import boto3
import io
from PIL import Image, ImageDraw, ExifTags, ImageColor, ImageFont
def detectByAWS(imagePath):
    resBox=[]
    # print(imagePath)
    bucket='custom-labels-console-ap-southeast-2-866d8ab204'
    model='arn:aws:rekognition:ap-southeast-2:686239894582:project/logoPrint/version/logoPrint.2023-06-15T17.29.07/1686814148965'
    min_confidence=50
    client=boto3.client('rekognition')

    #Call DetectCustomLabels
    response = client.detect_custom_labels(Image={'S3Object': {'Bucket': bucket, 'Name': imagePath}},
        MinConfidence=min_confidence,
        ProjectVersionArn=model)
    # Load image from S3 bucket
    s3_connection = boto3.resource('s3')

    s3_object = s3_connection.Object(bucket,imagePath)
    s3_response = s3_object.get()

    stream = io.BytesIO(s3_response['Body'].read())
    image=Image.open(stream)
    imageName=imagePath.split('/')[-1]
    print('imageName:',imageName)

    # Ready image to draw bounding boxes on it.
    imgWidth, imgHeight = image.size
    # draw = ImageDraw.Draw(image)

    # calculate and display bounding boxes for each detected custom label
    print('Detected custom labels for ' + imagePath)
    for customLabel in response['CustomLabels']:
        print('Label ' + str(customLabel['Name']))
        label=str(customLabel['Name'])
        print('Confidence ' + str(customLabel['Confidence']))
        if 'Geometry' in customLabel:
            box = customLabel['Geometry']['BoundingBox']
            left = imgWidth * box['Left']
            top = imgHeight * box['Top']
            width = imgWidth * box['Width']
            height = imgHeight * box['Height']
            right=left+width
            bottom=top+height

#             fnt = ImageFont.truetype('/Library/Fonts/Arial.ttf', 50)
            # fnt = ImageFont.truetype('arial.ttf', 50)
            # draw.text((left,top), customLabel['Name'], fill='#00d400', font=fnt)

            print('Left: ' + '{0:.0f}'.format(left))
            print('Top: ' + '{0:.0f}'.format(top))
            print('Label Width: ' + "{0:.0f}".format(width))
            print('Label Height: ' + "{0:.0f}".format(height))

            # points = (
            #     (left,top),
            #     (left + width, top),
            #     (left + width, top + height),
            #     (left , top + height),
            #     (left, top))
            # draw.line(points, fill='#00d400', width=5)
            resBox.append([label,[top, left, bottom, right]])

    return resBox,image,imageName

def findPosByAWS(inputPosition,logoWidth,logoHeight,inputImgPaths):
    posBox=[]
    for i in inputImgPaths:
        posDic={}
        try:
            resBox,image,imageName=detectByAWS(i)
            tempPos=[]
            for j in resBox:
                classtype,pos=j
                print('classtype:',classtype)
                print('pos:',pos)
                if classtype=='dashedcircle':
                    top, left, bottom, right = pos
                    posWidth = int(right - left)
                    posHeight = int(bottom - top)
                    if posWidth>posHeight:
                        d=posHeight
                    else:
                        d=posWidth

                    alpha=math.atan2(logoHeight,logoWidth)
                    newWidth=int(d*math.cos(alpha))
                    newHeight=int(d*math.sin(alpha))
                    centralPoint=tuple((int(left+(right-left)/2),int(top+(bottom-top)/2)))
                    location=tuple((int(centralPoint[0]-newWidth/2),int(centralPoint[1]-newHeight/2)))
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
            # tempPos.append(image)
            # posBox.append(tempPos)
            posDic['pos']=tempPos
            posDic['image']=image
            posDic['imageName']=imageName
        except Exception as ex:
            print(ex)
            posDic['pos']=[]
            posDic['image']=image
            posDic['imageName']=imageName
        posBox.append(posDic)
    return posBox
        
# def findPosByAI(inputPosition,logoWidth,logoHeight,inputImgPaths):
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
                    posWidth = int(right - left)
                    posHeight = int(bottom - top)
                    if posWidth>posHeight:
                        d=posHeight
                    else:
                        d=posWidth

                    alpha=math.atan2(logoHeight,logoWidth)
                    newWidth=int(d*math.cos(alpha))
                    newHeight=int(d*math.sin(alpha))
                    centralPoint=tuple((int(left+(right-left)/2),int(top+(bottom-top)/2)))
                    location=tuple((int(centralPoint[0]-newWidth/2),int(centralPoint[1]-newHeight/2)))
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
