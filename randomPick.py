import random
import os

def randomPickPics(folderPath,fileNum):
    filePaths=[]
    files=os.listdir(folderPath)
    
    sample=random.sample(files,fileNum)
    for name in sample:
        filePaths.append(os.path.join(folderPath,name))
    # totalNum=len(files)
    
    # randomNum=[]
    # while(1):
    #     ran=random.randint(0,totalNum-1)
    #     if ran in randomNum:
    #         continue
    #     else:
    #         randomNum.append(ran)
    #     if len(randomNum)==fileNum:
    #         break
    # for i in range(fileNum):
    #     filePath=folderPath+"/"+str(randomNum.pop())+".png"
    #     filePaths.append(filePath)
    return filePaths


# folderpath='H://LogoPrint//LogoPrint//pictures//bag//'
# filenum=10

# filepaths=randomPickPics(folderpath,filenum)
# for i in range(filenum):
#     print(filepaths.pop())