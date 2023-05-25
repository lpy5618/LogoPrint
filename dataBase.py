from pymongo import MongoClient
from random import sample

def getPathFromDB(args,filenum):
    localDB=MongoClient("mongodb://localhost:27017")
    paths=[]
    # print(localDB.list_database_names())
    db=localDB.logoPrint
    bottlesCol=db.bottles
    bagsCol=db.bags
    command=args.split(" ") # item color supplier type
    cmd={"color":command[1],"supplier":command[2],"type":command[3]}
    if command[0]=="bottles":
        pathCursor=bottlesCol.find(cmd,{"_id":0,"path":1})
    elif command[0]=="bags":
        pathCursor=bagsCol.find(cmd,{"_id":0,"path":1})
    for i in pathCursor:
        paths.append(i["path"])
    if len(paths)<filenum:
        return paths
    else:
        return sample(paths,filenum)
 
