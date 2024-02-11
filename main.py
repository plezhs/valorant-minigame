import discord
from discord.ext import commands
from discord.utils import get
import datetime
import random
import requests
import json

time = datetime.datetime.now()

rt =str(time)[0:10]
with open(f'{rt}.log.txt', 'a') as f:
    f.write(f"[{time}]--------------------------------------------------\n[{time}]Bot Started\n[{time}]--------------------------------------------------\n")

bot = commands.Bot(command_prefix="!",intents=discord.Intents.all())

global Lresult

def isQ(agent):
    if agent['abilities'][0]['slot'] == "Ability1":
        return agent['abilities'][0]['displayIcon']
    elif agent['abilities'][1]['slot'] == "Ability1":
        return agent['abilities'][1]['displayIcon']
    elif agent['abilities'][2]['slot'] == "Ability1":
        return agent['abilities'][2]['displayIcon']
    elif agent['abilities'][3]['slot'] == "Ability1":
        return agent['abilities'][3]['displayIcon']
def isE(agent):
    if agent['abilities'][0]['slot'] == "Ability2":
        return agent['abilities'][0]['displayIcon']
    elif agent['abilities'][1]['slot'] == "Ability2":
        return agent['abilities'][1]['displayIcon']
    elif agent['abilities'][2]['slot'] == "Ability2":
        return agent['abilities'][2]['displayIcon']
    elif agent['abilities'][3]['slot'] == "Ability2":
        return agent['abilities'][3]['displayIcon']
def isC(agent):
    if agent['abilities'][0]['slot'] == "Grenade":
        return agent['abilities'][0]['displayIcon']
    elif agent['abilities'][1]['slot'] == "Grenade":
        return agent['abilities'][1]['displayIcon']
    elif agent['abilities'][2]['slot'] == "Grenade":
        return agent['abilities'][2]['displayIcon']
    elif agent['abilities'][3]['slot'] == "Grenade":
        return agent['abilities'][3]['displayIcon']
def isX(agent):
    if agent['abilities'][0]['slot'] == "Ultimate":
        return agent['abilities'][0]['displayIcon']
    elif agent['abilities'][1]['slot'] == "Ultimate":
        return agent['abilities'][1]['displayIcon']
    elif agent['abilities'][2]['slot'] == "Ultimate":
        return agent['abilities'][2]['displayIcon']
    elif agent['abilities'][3]['slot'] == "Ultimate":
        return agent['abilities'][3]['displayIcon']

@bot.event
async def on_ready():
    global Lresult
    print(f"Logged in as {bot.user}")
    await bot.change_presence(activity=discord.Game(name="발로란트 스킬 이름 맟추기"))
    Lname = list()
    Licon = list()
    Limg = list()
    Lresult = list()
    IconabilistiesQ = list()
    IconabilistiesE = list()
    IconabilistiesC = list()
    IconabilistiesX = list()
    abilistiesQ = list()
    abilistiesE = list()
    abilistiesC = list()
    abilistiesX = list()
    url = "https://valorant-api.com/v1/agents"
    parameters = {"isPlayableCharacter": "true"}

    response = requests.get(url, params=parameters)
    data = response.json()["data"]
    with open('.\\agent.json','r',encoding='UTF-8') as f:
        dbdata = json.load(f)
    for agent in data:
        Lname.append(agent["displayName"])
        abilistiesQ.append(dbdata["Agents"][agent["displayName"]]['abQ'])
        abilistiesE.append(dbdata["Agents"][agent["displayName"]]['abE'])
        abilistiesC.append(dbdata["Agents"][agent["displayName"]]['abC'])
        abilistiesX.append(dbdata["Agents"][agent["displayName"]]['abX'])
        Licon.append(agent["displayIcon"])
        Limg.append(agent["bustPortrait"])
        IconabilistiesQ.append(isQ(agent))
        IconabilistiesE.append(isE(agent))
        IconabilistiesC.append(isC(agent))
        IconabilistiesX.append(isX(agent))
    Lresult.append(Lname)
    Lresult.append(abilistiesQ)
    Lresult.append(abilistiesE)
    Lresult.append(abilistiesC)
    Lresult.append(abilistiesX)
    Lresult.append(Licon)
    Lresult.append(IconabilistiesQ)
    Lresult.append(IconabilistiesE)
    Lresult.append(IconabilistiesC)
    Lresult.append(IconabilistiesX)

global answer
answer = dict()
@bot.command(aliases=[""])
async def 스킬문제(ctx):
    global answer
    global Lresult
    i = random.sample(range(0,len(Lresult[0])-1),1)[0]
    agentsIcon = Lresult[5][i]

    abilityQ = Lresult[1]
    abilityE = Lresult[2]
    abilityC = Lresult[3]
    abilityX = Lresult[4]

    ability = list()
    ability.append(abilityQ)
    ability.append(abilityE)
    ability.append(abilityC)
    ability.append(abilityX)

    IconabilityQ = Lresult[6]
    IconabilityE = Lresult[7]
    IconabilityC = Lresult[8]
    IconabilityX = Lresult[9]
    
    Iconability = list()
    Iconability.append(IconabilityQ)
    Iconability.append(IconabilityE)
    Iconability.append(IconabilityC)
    Iconability.append(IconabilityX)

    r=random.sample(range(0,3),1)[0]
    temp = ability[r][i]
    aw = temp.replace(" ","")
    name = ctx.message.author.name
    answer[ctx.message.author] = aw
    name = name.title()
    embed1 = discord.Embed(timestamp=ctx.message.created_at, colour=discord.Colour.red(),description=f"{name}님의 문제입니다.",title=f"이스킬의 이름은?")
    embed1.set_image(url=Iconability[r][i])
    embed1.set_thumbnail(url=agentsIcon)
    embed1.add_field(name="※주의 사항※",value=f"띄어쓰기는 생략해주세요.\n(이 게임에 도움을 준 사람: 유건우)", inline=False) #inline이 False라면 다음줄로 넘깁니다.
    await ctx.send(embed=embed1)
    with open(f'{rt}.log.txt', 'a',encoding='UTF-8') as f:
        f.write(f"[{time}] {ctx.message.author} received a quiz. Quiz's answer was {aw}.\n")
@bot.command()
async def 스킬정답(ctx,a=None):
    global answer
    if answer.get(ctx.message.author) != None:
        if a.title() == answer.get(ctx.message.author):
            await ctx.send("정답입니다!!!")
            with open(f'{rt}.log.txt', 'a',encoding='UTF-8') as f:
                f.write(f"[{time}] {ctx.message.author} got a quiz right. Quiz's answer was {answer.get(ctx.message.author)}.\n")
            with open('.\\db.json','r+',encoding='UTF-8') as f:
                jjj = json.load(f)
                nnn = {
                    f"{ctx.author.id}":{"points":100}
                }
                try:
                    dump = jjj["Points"][f"{ctx.author.id}"]["points"] + 100
                    abc = {}
                    abc[f"{ctx.author.id}"] = []
                    abc['Points'].append({f"{ctx.author.id}":{"points":dump}})
                except KeyError:
                    dump = 100
                    abc = {}
                    abc["Points"] = []
                    abc['Points'].append(nnn)
                f.seek(0)
                print(abc)
                json.dump(abc, f, indent=4)
            answer.pop(ctx.message.author)
        else:
            await ctx.send(f"아...\n정답은 {answer.get(ctx.message.author)} 이었습니다...")
            with open(f'{rt}.log.txt', 'a',encoding='UTF-8') as f:
                f.write(f"[{time}] {ctx.message.author} got a quiz wrong. {ctx.message.author}'s answer was {a}. Quiz's answer was {answer.get(ctx.message.author)}.\n")
            answer.pop(ctx.message.author)
    else:
        await ctx.send("먼저 문제를 받아주세요.")
        with open(f'{rt}.log.txt', 'a',encoding='UTF-8') as f:
                f.write(f"[{time}] {ctx.message.author} tried to take the quiz. But there was no quiz\n")

@bot.event
async def on_message(msg):
    await bot.process_commands(msg)

bot.run("")
