from pymongo import MongoClient
from random import sample

def getPathFromDB(args,filenum):
    localDB=MongoClient("mongodb://localhost:27017")
    # print(localDB.list_database_names())
    db=localDB.logoPrint
    bottlesCol=db.bottles
    command=args.split(" ") # color supplier type
    cmd={"color":command[0],"supplier":command[1],"type":command[2]}
    paths=[]
    pathCursor=bottlesCol.find(cmd,{"_id":0,"path":1})
    for i in pathCursor:
        paths.append(i["path"])
    if len(paths)<filenum:
        return paths
    else:
        return sample(paths,filenum)
 
