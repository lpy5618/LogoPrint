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
    productColor = input("please input product color:")
    productCategory = input("please input product category:")
    productPrintType = input("please input product print type:")
    fileNum=int(input("how many pics do you want to get?"))
    args['color'] = productColor
    args['category'] = productCategory
    args['printtype'] = productPrintType

    query = {}
    if args['color'] != '':
        query['ColourPart1Des'] = re.compile(args['color'],re.IGNORECASE)
    if args['category'] != '':
        query['category'] = re.compile(args['category'],re.IGNORECASE)
    if args['printtype'] != '':
        query['printtype'] = re.compile(args['printtype'],re.IGNORECASE)
    # if command[0]=="bottles":
    #     pathCursor=bottlesCol.find(cmd,{"_id":0,"imagePath":1})
    # elif command[0]=="bags":
    #     pathCursor=bagsCol.find(cmd,{"_id":0,"imagePath":1})
    projection = {"_id": 0, "imagePath": 1}
    pathCursor=productsCol.find(query, projection)
    for i in pathCursor:
        paths.append(i["imagePath"])
    if len(paths)<fileNum:
        return paths
    else:
        return sample(paths,fileNum)
 
