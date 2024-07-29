import os
import discord
import random
import datetime
import TellDormMeal as TDM
import ConnectMongoDB as CMDB
from discord.ext import tasks
from dotenv import load_dotenv
from server import server_thread


dotenv_path = os.path.join(os.path.dirname(__file__), '../env/.env')
load_dotenv(dotenv_path)

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)
Token = os.getenv("BOT_TOKEN")

@client.event
async def on_ready():
    TDM.NowManual_update()
    TDM.NextManual_update()
    everyday_notice.start()
    if TDM.json_nowWeek_already_update():
        await client.change_presence(status = discord.Status.online, activity=discord.Game(name="今週は表示できるぜ"))
    else:
        await client.change_presence(status = discord.Status.idle, activity=discord.Game(name="今週は表示できないぜ"))



@client.event
async def on_message(message):
    failureReplys = [
        "更新を試みましたが、不可能でした。更新を行う人を応援してあげてください。",
        "更新が不可能でした。寮事務に対して更新を催促することを推奨します。",
        "更新できませんでした。無念です。",
        "知っていましたか？表示がないということは、更新されていないということなのですよ。",
        "更新を試みましたが、不可能でした。魚国が早く更新することを願ってください。",
        "自分で食堂まで確認しに行ってください。",
        "ここで確認をしたならば、ごはんを食べに行きましょう。",
        "多分きっと、何かがそこにはあります。"
    ]
    
    if message.author == client.user:
        return
    else:
        if message.content.startswith("/today"):
            if TDM.json_nowWeek_already_update():
                embed = discord.Embed(
                            title="今日のメニューを表示",
                            color=0x00ff00,
                            )
                date,breakfast,lunchA,lunchB,dinnerA,dinnerB = TDM.today()
                embed.add_field(name="date", value=date, inline=False)
                embed.add_field(name="breakfast", value=breakfast, inline=False)
                embed.add_field(name="lunchA", value=lunchA, inline=False)
                embed.add_field(name="lunchB", value=lunchB, inline=False)
                embed.add_field(name="dinnerA", value=dinnerA, inline=False)
                embed.add_field(name="dinnerB", value=dinnerB, inline=False)
                await message.channel.send(embed=embed)
            else:
                embed = discord.Embed(
                    title="今日の寮食を表示することができません",
                    color=0xff0000,
                    description	= random.choice(failureReplys)
                )
                await message.channel.send(embed=embed)
            
        if message.content.startswith("/tomorrow"):
            weekday = datetime.date.today().weekday()
            if TDM.json_nowWeek_already_update() and weekday != 6:
                embed = discord.Embed(
                        title="明日のメニューを表示",
                        color=0x00ff00,
                        )
                date,breakfast,lunchA,lunchB,dinnerA,dinnerB = TDM.tomorrow()
                embed.add_field(name="date", value=date, inline=False)
                embed.add_field(name="breakfast", value=breakfast, inline=False)
                embed.add_field(name="lunchA", value=lunchA, inline=False)
                embed.add_field(name="lunchB", value=lunchB, inline=False)
                embed.add_field(name="dinnerA", value=dinnerA, inline=False)
                embed.add_field(name="dinnerB", value=dinnerB, inline=False)
                await message.channel.send(embed=embed)
            elif TDM.json_nextWeek_already_update() and weekday == 6:
                embed = discord.Embed(
                        title="明日のメニューを表示",
                        color=0x00ff00,
                        )
                date,breakfast,lunchA,lunchB,dinnerA,dinnerB = TDM.tomorrow()
                embed.add_field(name="date", value=date, inline=False)
                embed.add_field(name="breakfast", value=breakfast, inline=False)
                embed.add_field(name="lunchA", value=lunchA, inline=False)
                embed.add_field(name="lunchB", value=lunchB, inline=False)
                embed.add_field(name="dinnerA", value=dinnerA, inline=False)
                embed.add_field(name="dinnerB", value=dinnerB, inline=False)
                await message.channel.send(embed=embed)
            else:
                embed = discord.Embed(
                    title="明日の寮食を表示することができません",
                    color=0xff0000,
                    description	= random.choice(failureReplys)
                )
                await message.channel.send(embed=embed)
        
        if message.content == "!confMenuAll":
            embed = discord.Embed(
                            title="一週間のメニューを表示",
                            color=0x00ff00,
                            )
            for i in range(7):
                date,breakfast,lunchA,lunchB,dinnerA,dinnerB = TDM.read_Nowjson(i)
                embed.add_field(name="date", value=date, inline=False)
                embed.add_field(name="breakfast", value=breakfast, inline=False)
                embed.add_field(name="lunchA", value=lunchA, inline=False)
                embed.add_field(name="lunchB", value=lunchB, inline=False)
                embed.add_field(name="dinnerA", value=dinnerA, inline=False)
                embed.add_field(name="dinnerB", value=dinnerB, inline=False)
                await message.channel.send(embed=embed)
                embed.clear_fields()
            for i in range(7):
                date,breakfast,lunchA,lunchB,dinnerA,dinnerB = TDM.read_Nextjson(i)
                embed.add_field(name="date", value=date, inline=False)
                embed.add_field(name="breakfast", value=breakfast, inline=False)
                embed.add_field(name="lunchA", value=lunchA, inline=False)
                embed.add_field(name="lunchB", value=lunchB, inline=False)
                embed.add_field(name="dinnerA", value=dinnerA, inline=False)
                embed.add_field(name="dinnerB", value=dinnerB, inline=False)
                await message.channel.send(embed=embed)
                embed.clear_fields()
        
        if message.content == "!confUpdate":
            if TDM.NowManual_update():
                await message.channel.send("今週のメニュー更新完了")
                await client.change_presence(status = discord.Status.online, activity=discord.Game(name="今週は表示できるぜ"))

            else:
                await message.channel.send("今週のメニューはまだ上がってないようです")
                await client.change_presence(status = discord.Status.idle, activity=discord.Game(name="今週は表示できないぜ"))

            
            if TDM.NextManual_update():
                await message.channel.send("来週のメニュー更新完了")
            else:
                await message.channel.send("来週のメニューはまだ上がってないようです")

        if message.content == "!confManualNotice":
            UserChannels = CMDB.Get_UserID()
            if TDM.json_nowWeek_already_update():
                for i in range(len(UserChannels)):
                    ch = client.get_channel(UserChannels[i])

                    embed = discord.Embed(
                                title="今日のメニューを表示",
                                color=0x00ff00,
                                )
                    date,breakfast,lunchA,lunchB,dinnerA,dinnerB = TDM.today()
                    embed.add_field(name="date", value=date, inline=False)
                    embed.add_field(name="breakfast", value=breakfast, inline=False)
                    embed.add_field(name="lunchA", value=lunchA, inline=False)
                    embed.add_field(name="lunchB", value=lunchB, inline=False)
                    embed.add_field(name="dinnerA", value=dinnerA, inline=False)
                    embed.add_field(name="dinnerB", value=dinnerB, inline=False)
                    await ch.send(embed=embed)
            else:
                await message.channel.send("無理でした")
        
        if message.content == "!confGetChannel":
            DevChannels = CMDB.Get_UserID(True)
            for i in range(len(DevChannels)):
                if DevChannels[i] == message.channel.id:
                    embed = discord.Embed(
                        title="登録済みチャンネルを表示します",
                        color=0xf58220
                    )#追記予定
                else:
                    return
        
        if message.content.startswith("!confAddChannel"):
            chID = message.channel.id
            chNAME = message.channel.name
            isAdded = CMDB.Add_user(channelNAME=chNAME, channelID=chID)
            if isAdded:
                await message.channel.send("追加しました。")
            else:
                await message.channel.send("追加済みです。")
        
        if message.content.startswith("!confDelChannel"):
            chID = message.channel.id
            isDelete = CMDB.Del_user(chID)
            if isDelete:
                await message.channel.send("削除しました。")
            else:
                await message.channel.send("存在しません。")
        
        if message.content == "!confHelp":
            embed = discord.Embed(
                        title="コマンド一覧",
                        color=0x00ff00,
                        )
            embed.add_field(name="/today", value="今日一日のメニュー", inline=False)
            embed.add_field(name="/tomorrow", value="明日一日のメニュー", inline=False)
            await message.channel.send(embed=embed)
            embed.clear_fields()
            embed = discord.Embed(
                        title = "自動通知について",
                        color = 0x00ff00
                        )
            embed.add_field(name="追加方法",value="!confAddChannelを追加したいチャンネルに送る",inline=False)
            embed.add_field(name="削除方法",value="!confDelChannelを追加したチャンネルに送る",inline=False)
            await message.channel.send(embed=embed)


@tasks.loop(seconds=60)
async def everyday_notice():
    now = datetime.datetime.now().strftime("%H:%M")
    day = datetime.date.today().weekday()
    failureReplys = [
        "更新を試みましたが、不可能でした。更新を行う人を応援してあげてください。",
        "更新が不可能でした。寮事務に対して更新を催促することを推奨します。",
        "更新できませんでした。無念です。",
        "知っていましたか？表示がないということは、更新されていないということなのですよ。",
        "更新を試みましたが、不可能でした。魚国が早く更新することを願ってください。",
        "自分で食堂まで確認しに行ってください。",
        "ここで確認をしたならば、ごはんを食べに行きましょう。",
        "多分きっと、何かがそこにはあります。"
    ]

    if day == 0 and now == "00:00":
        DevChannels = CMDB.Get_UserID(True)
        if TDM.get_NowMealData():
            TDM.make_Nowjson()
            for i in range(len(DevChannels)):
                ch = client.get_channel(DevChannels[i])
                await ch.send("今週分を獲得しました。")
                await client.change_presence(status = discord.Status.online, activity=discord.Game(name="今週は表示できるぜ"))
                if TDM.get_NextMealData():
                    TDM.make_Nextjson()
                    for i in range(len(DevChannels)):
                        ch = client.get_channel(DevChannels[i])
                        await ch.send("来週分を獲得しました。")
                else:
                    for i in range(len(DevChannels)):
                        ch = client.get_channel(DevChannels[i])
                        await ch.send("来週分を獲得できませんでした。")
            UserChannels = CMDB.Get_UserID()
            for i in range(len(UserChannels)):
                ch = client.get_channel(UserChannels[i])

                embed = discord.Embed(
                            title="今日のメニューを表示",
                            color=0x00ff00,
                            )
                date,breakfast,lunchA,lunchB,dinnerA,dinnerB = TDM.today()
                embed.add_field(name="date", value=date, inline=False)
                embed.add_field(name="breakfast", value=breakfast, inline=False)
                embed.add_field(name="lunchA", value=lunchA, inline=False)
                embed.add_field(name="lunchB", value=lunchB, inline=False)
                embed.add_field(name="dinnerA", value=dinnerA, inline=False)
                embed.add_field(name="dinnerB", value=dinnerB, inline=False)
                await ch.send(embed=embed)
        else:
            await ch.send("獲得できませんでした。更新されていないようです。")
            await client.change_presence(status = discord.Status.idle, activity=discord.Game(name="今週は表示できないぜ"))
    
    elif now == "00:00":
        UserChannels = CMDB.Get_UserID()
        if TDM.json_nowWeek_already_update():
            for i in range(len(UserChannels)):
                ch = client.get_channel(UserChannels[i])

                embed = discord.Embed(
                            title="今日のメニューを表示",
                            color=0x00ff00,
                            )
                date,breakfast,lunchA,lunchB,dinnerA,dinnerB = TDM.today()
                embed.add_field(name="date", value=date, inline=False)
                embed.add_field(name="breakfast", value=breakfast, inline=False)
                embed.add_field(name="lunchA", value=lunchA, inline=False)
                embed.add_field(name="lunchB", value=lunchB, inline=False)
                embed.add_field(name="dinnerA", value=dinnerA, inline=False)
                embed.add_field(name="dinnerB", value=dinnerB, inline=False)
                await ch.send(embed=embed)
        else:
            for i in range(len(UserChannels)):
                ch = client.get_channel(UserChannels[i])
                embed = discord.Embed(
                            title="今日のメニューを表示することができません",
                            color=0xff0000,
                            description	= random.choice(failureReplys)
                            )
                await ch.send(embed=embed)


server_thread()
client.run(Token)