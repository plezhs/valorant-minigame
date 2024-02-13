import discord
from discord.ext import commands
from discord.utils import get
import datetime
import random
import requests
import json

def wjson(data,filename='db.json'):
    with open(filename,'r+',encoding='UTF-8') as f:
        file_data = json.load(f)
        file_data["Points"].update(data)
        f.seek(0)
        json.dump(file_data,f,indent=4)
        print(file_data)
        print(data)
def getpoint(id):
    with open('.\\db.json','r',encoding='UTF-8') as f:
        data = json.load(f)
        try:
            p = data['Points'][f'{id}']
        except:
            p = 0
        return p

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
async def 문제(ctx):
    global answer
    global Lresult
    if answer.get(ctx.author) != None:
        await ctx.send("이전문제를 먼저 풀어주세요.\n패널티로 25점이 차감됩니다.")
        ndata = {
            f"{ctx.author.id}": getpoint(ctx.author.id) - 25
        }
        wjson(ndata)
        #로그 메세지 추가필요. 문제 남아있는데도 새로 받았다는 내용 추가.
    else:
        agents =list()
        for k in Lresult[0]:
            agents.append(k)
        random.shuffle(agents)
        tempa = random.sample(range(0,2*(len(Lresult[0])-1)),1)[0]
        i = Lresult[0].index(agents[round(tempa/2)])
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

        r=random.sample(range(0,4),1)[0]
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
async def 정답(ctx,a=None):
    global answer
    if answer.get(ctx.message.author) != None:
        if a.title() == answer.get(ctx.message.author):
            await ctx.send(f"{ctx.author.mention}\n정답입니다!!! 100점이 지급되었습니다.")
            ndata = {
            f"{ctx.author.id}": getpoint(ctx.author.id) + 100
            }
            wjson(ndata)
            with open(f'{rt}.log.txt', 'a',encoding='UTF-8') as f:
                f.write(f"[{time}] {ctx.message.author} got a quiz right. Quiz's answer was {answer.get(ctx.message.author)}. {ctx.author} got 100 points.\n")
            answer.pop(ctx.message.author)
        else:
            await ctx.send(f"{ctx.author.mention}\n아...\n패널티로 50점이 차감되었습니다....")
            ndata = {
            f"{ctx.author.id}": getpoint(ctx.author.id) - 50
            }
            wjson(ndata)
            with open(f'{rt}.log.txt', 'a',encoding='UTF-8') as f:
                f.write(f"[{time}] {ctx.message.author} got a quiz wrong. {ctx.message.author}'s answer was {a}. Quiz's answer was {answer.get(ctx.message.author)}. {ctx.author}'s point decrease 50p.\n")
            # answer.pop(ctx.message.author)
    else:
        await ctx.send(f"{ctx.author.mention}\n먼저 문제를 받아주세요.")
        with open(f'{rt}.log.txt', 'a',encoding='UTF-8') as f:
                f.write(f"[{time}] {ctx.message.author} tried to take the quiz. But there was no quiz\n")

@bot.command()
async def 문제패스(ctx):
    global answer
    player = ctx.author
    if answer.get(player) != None:
        await ctx.send(f"문제를 패스하였습니다.\n 정답은 {answer.pop(player)}였습니다.\n 다음문제를 받아 풀어주세요.\n 패널티로 10점이 차감됩니다.")
        ndata = {
            f"{ctx.author.id}": getpoint(ctx.author.id) - 10
        }
        wjson(ndata)
        with open(f'{rt}.log.txt', 'a',encoding='UTF-8') as f:
            f.write(f"[{time}] {ctx.message.author} passed a quiz. Quiz's answer was {answer.get(ctx.message.author)}. {ctx.author}'s point decrease 10p.\n")
    else:
        await ctx.send("패스할 문제가 없습니다. \"!스킬문제\"로 문제를 받아 풀어보세요.")

@bot.command()
async def 포인트(ctx):
    point = getpoint(ctx.author.id)
    await ctx.send(f"{ctx.author.mention}\n{ctx.message.author.name}님의 잔여 포인트는 {point}점 입니다.")
    with open(f'{rt}.log.txt', 'a',encoding='UTF-8') as f:
        f.write(f"[{time}] {ctx.message.author} checked {ctx.author}'s points. {ctx.author}'s points was {point}.\n")
    

@bot.event
async def on_message(msg):
    await bot.process_commands(msg)

bot.run("")
