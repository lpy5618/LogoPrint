from pymongo import MongoClient
from random import sample
import re

def getPathFromDB():
    localDB=MongoClient("mongodb://localhost:27017")
    paths=[]
    # print(localDB.list_database_names())
    db=localDB.logoPrint
    # bottlesCol=db.bottles
    # bagsCol=db.bags
    productsCol=db.products
    # command=args.split(" ") # item color supplier type
    # cmd={"color":command[1],"supplier":command[2],"type":command[3]}
    args = {}
    args['color'] = input("please input product color:")
    args['category']= input("please input product category:")
    args['printtype'] = input("please input product print type:")
    fileNum=int(input("how many pics do you want to get?"))
    
    query = {}
    if args['color'] != '':
        query['ColourPart1Des'] = re.compile(args['color'],re.IGNORECASE)
    elif args['category'] != '':
        query['category'] = re.compile(args['category'],re.IGNORECASE)
    elif args['printtype'] != '':
        query['printtype'] = re.compile(args['printtype'],re.IGNORECASE)
    else:
        pass
    # if command[0]=="bottles":
    #     pathCursor=bottlesCol.find(cmd,{"_id":0,"imagePath":1})
    # elif command[0]=="bags":
    #     pathCursor=bagsCol.find(cmd,{"_id":0,"imagePath":1})
    projection = {"_id": 0, "imagePath": 1}
    if len(query)==0:
        pathCursor=productsCol.find({}, projection)
    else:
        pathCursor=productsCol.find(query, projection)
    for i in pathCursor:
        try:
            paths.append(i["imagePath"])
        except:
            continue
    if len(paths)<fileNum:
        return paths
    else:
        return sample(paths,fileNum)
 
