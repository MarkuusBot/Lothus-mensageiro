from utils.configs import  configData
from pymongo import MongoClient
#-----------------------------------------------------------------------------------------------------#
cluster = MongoClient(configData['mongokey'])

db = cluster['LTHC']

adv = db['adv']
mod = db['MOD']
ausen = db['ausente']
tick = db['tickets']
#-----------------------------------------------------------------------------------------------------#
async def advdb(id, qnt, motivo):

    adv.update_one({"_id": id.id}, {"$set": {f"Adv{qnt}": motivo}}, upsert = True)

async def rmvadvdb(id, qnt, motivo):

    adv.update_one({"_id": id.id}, {"$set": {f"Adv{qnt}": motivo}}, upsert = True)
#-----------------------------------------------------------------------------------------------------#
async def ausendb(id, motivo, data):

    ausen.update_one({"_id": id.id}, {"$set": {f"Nome": id.name, f"Motivo": motivo, f"Data": data, "Ausente?": True}}, upsert = True)

    if ausen.find_one({"_id": 'validador'})['valor'] == 0:

        ausen.update_one({"_id": 'validador'}, {"$set": {f"valor": 1}}, upsert = True)

async def desausendb(id):

    ausen.update_one({"_id": id.id}, {"$set": {f"Nome": id.name, f"Motivo": 'None', f"Data": 'None', "Ausente?": False}}, upsert = True)

    if ausen.count_documents({'Ausente?': True}) == 0:

        ausen.update_one({"_id": 'validador'}, {"$set": {f"valor": 0}}, upsert = True)
#-----------------------------------------------------------------------------------------------------#
async def tckdb(id, id2):

    tick.update_one({"_id": id.id}, {"$set": {f"Nome": id.name, "aberto?": True,"fechado?": False, 'msgid': id2}}, upsert = True)

    tick.update_one({"_id": 'validador'}, {"$set": {f"valor": 1}}, upsert = True)

    if tick.find_one({"_id": 'validador'})['valor'] == 0:

        tick.update_one({"_id": 'validador'}, {"$set": {f"valor": 1}}, upsert = True)

async def tckdb2(id, id2):

    tick.update_one({"_id": id.id}, {"$set": {f"Nome": id.name, "aberto?": False,"fechado?": True, "msgid": id2}}, upsert = True)

async def tckdb3(id):

    tick.update_one({"_id": id.id}, {"$set": {f"Nome": id.name, "aberto?": False,"fechado?": False, "msgid": None}}, upsert = True)

    if tick.count_documents({'fechado?': True}) == 0\
    and tick.count_documents({'aberto?': True}) == 0:

        tick.update_one({"_id": 'validador'}, {"$set": {f"valor": 0}}, upsert = True)

def msgtckid(id, guild):

    if id is not None:
        if mod.count_documents({"_id":guild.id}) == 0:
            mod.insert_one({"_id":guild.id, "Nome":guild.name})
        mod.update_one({"_id": guild.id}, {"$set": {"msgtck": id}}, upsert = True)

def msgstf(id, guild):

    if id is not None:
        if mod.count_documents({"_id":guild.id}) == 0:
            mod.insert_one({"_id":guild.id, "Nome":guild.name})
        mod.update_one({"_id": guild.id}, {"$set": {"msgstf": id}}, upsert = True)

#-----------------------------------------------------------------------------------------------------#