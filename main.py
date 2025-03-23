import discord
from discord.ext import commands
from pymongo import MongoClient

mongo = MongoClient("mongodb+srv://")
db = mongo.OwO
noti = db.noti

#Channel
OWO_TICKET_CHANNEL = 822972235996201021
TOKEN = ""

bot = commands.Bot(command_prefix="#",self_bot = True)



def extract(content):
    content = content.lower()

    if "stock:" in content:
        stock_part = content.split("stock:")[1].strip()
    elif "stocks:" in content:
        stock_part = content.split("stocks:")[1].strip()
    elif "stock " in content:
        stock_part = content.split("stock ")[1].strip()
    elif "stocks " in content:
        stock_part = content.split("stocks ")[1].strip()
    else:
        raise ValueError("Error extract")

    stock_info = stock_part.split()[0]  
    stock_info = "".join(c for c in stock_info if c.isdigit())

    if stock_info:
        return int(stock_info)



@bot.event
async def on_ready():
    print(f"{bot.user}")
    await sync()

async def sync():
    channel = bot.get_channel(OWO_TICKET_CHANNEL)
    if channel:
        noti.update_one(
            {"_id": "stock_tracker"},
            {"$set": {"message_ids": [], "stocks": []}},
            upsert=True
        )
        print("Deleted data")

        async for message in channel.history(limit=10): 
            if "stock" in message.content.lower() or "stocks" in message.content.lower():
                stock_info = extract(message.content)
                if stock_info == None:
                    continue
                    
                db = noti.find_one({"_id": "stock_tracker"}) or {}
                message_id = db.get("message_ids", [])
                stock = db.get("stocks", [])
                    
                message_id.append(message.id)
                stock.append(stock_info)
                    
                noti.update_one(
                    {"_id": "stock_tracker"},
                    {"$set": {"ticket": True, "message_ids": message_id, "stocks": stock}},
                    upsert=True
                )
                print(f"Sync: Stock: {stock_info}, Message ID: {message.id}")
                    

@bot.event
async def on_message(message):
    if message.channel.id == OWO_TICKET_CHANNEL:
        if "stock" in message.content.lower() or "stocks" in message.content.lower(): 
            try:
                stock_info = extract(message.content)
                db = noti.find_one({"_id": "stock_tracker"}) or {}
                message_id = db.get("message_ids", [])
                stock = db.get("stocks", [])
                
                message_id.append(message.id)
                stock.append(stock_info)
                
                noti.update_one(
                    {"_id": "stock_tracker"},
                    {"$set": {"ticket": True, "message_ids": message_id, "stocks": stock}},
                    upsert=True
                )
                print(f"Save: Stock: {stock_info}, Message ID: {message.id}")
            except (IndexError, ValueError) as e:
                print(f"Error save: {e}")
    
    await bot.process_commands(message)

@bot.event
async def on_raw_message_edit(payload):
    channel = bot.get_channel(payload.channel_id)
    if channel.id == OWO_TICKET_CHANNEL:
        after = await channel.fetch_message(payload.message_id)
        if "stock" in after.content.lower() or "stocks" in after.content.lower():
            try:
                stock_info = extract(after.content)
                db = noti.find_one({"_id": "stock_tracker"}) or {}
                message_id = db.get("message_ids", [])
                stock = db.get("stocks", [])
                
                if after.id in message_id:
                    index = message_id.index(after.id)
                    stock[index] = stock_info
                else:
                    message_id.append(after.id)
                    stock.append(stock_info)
                
                noti.update_one(
                    {"_id": "stock_tracker"},
                    {"$set": {"ticket": True, "message_ids": message_id, "stocks": stock}},
                    upsert=True
                )
                print(f"Save update: Stock: {stock_info}, Message ID: {after.id}")
            except (discord.NotFound, discord.Forbidden, discord.HTTPException) as e:
                print(f"Error update: {e}")



@bot.event
async def on_raw_message_delete(payload):
    channel = bot.get_channel(payload.channel_id)
    if channel.id == OWO_TICKET_CHANNEL:
        db = noti.find_one({"_id": "stock_tracker"}) or {}
        message_id = db.get("message_ids", [])
        stock = db.get("stocks", [])
        
        if payload.message_id in message_id:
            index = message_id.index(payload.message_id)
            del message_id[index]
            del stock[index]
            
            noti.update_one(
                {"_id": "stock_tracker"},
                {"$set": {"message_ids": message_id, "stocks": stock}},
                upsert=True
            )
            print(f"Deleted: {payload.message_id}")


bot.run(TOKEN)