import os
from dotenv import load_dotenv
from pymongo import MongoClient
from bson.objectid import ObjectId

dotenv_path = os.path.join(os.path.dirname(__file__), '../env/.env')
load_dotenv(dotenv_path)

uli = os.getenv("ULI")
tlsCertificateKeyFile_path = os.getenv("tlsCertificateKeyFile_PATH")
Mongo_client = MongoClient(uli, tls=True, tlsCertificateKeyFile="./config/X509-cert-5865884892705360989.pem")
db = Mongo_client.TellDormMeal
data = db.Users

def Get_user():
    output = []
    for s in data.find():
        _id = str(s['_id'])
        output.append({'_id':_id, 'ch_name':s['channel_name'], 'ch_id':s['channel_id'], 'isDev':s['Developer']})
    return output

def Get_UserID(*isdev:bool):
    output = Get_user()
    result = []
    if isdev:
        for i in range(len(output)):
            if output[i]["isDev"]:
                result.append(int(output[i]["ch_id"]))
    else:
        for i in range(len(output)):
            result.append(int(output[i]["ch_id"]))
    return result

def Add_user(channelNAME:str, channelID:int):
    output = Get_user()
    for i in range(len(output)):
        if output[i]["ch_id"] == channelID:
            return False
    
    data.insert_one({"channel_name" : channelNAME, "channel_id" : channelID, "Developer" : False})
    return True

def Del_user(channelID:int):
    output = Get_user()
    
    for i in range(len(output)):
        if output[i]["ch_id"] == channelID:
            data.delete_one({'_id' : ObjectId(output[i]["_id"])})
            return True
    return False