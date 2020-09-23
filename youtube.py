import asyncio
import discord
from discord.ext import commands
import random
from discord.utils import get

app = commands.Bot(command_prefix='~')

@app.event
async def on_ready():
    print("봇 온라인")
    game = discord.Game("사용 가능한 명령어는 ~도움말")
    await app.change_presence(status=discord.Status.online, activity=game)

@app.command(name="팀")
async def _Team(ctx):
    team = ctx.message.content[3:]
    peopleteam = team.split(" / ")
    people = peopleteam[0]
    team = peopleteam[1]
    person = people.split(" ")
    teamname = team.split(" ")
    random.shuffle(teamname)
    await ctx.channel.send("@everyone")
    await ctx.channel.send(":point_right: 팀 정하기 시작~! :point_left:")
    for i in range(0, len(person)):
        await ctx.channel.send(person[i] + " ----> " + teamname[i])

@app.command(name="청소", pass_context=True)
async def _Clean(ctx, amount):
    if ctx.message.author.guild_permissions.change_nickname:
        try:
            if str(amount) >= str(51):
                await ctx.send("50 이하의 수를 입력해 주세요.")
            else:
                await ctx.message.channel.purge(limit=int(amount) + 1)
                await ctx.send(f"**{amount}**개의 메시지를 지웠습니다.")
        except ValueError:
            await ctx.send("청소하실 메시지의 **수**를 입력해 주세요.")
    else:
        await ctx.send("당신은 권한이 없기 때문에 이 명령어를 사용할 수 없습니다")

@app.command(name="숫자뽑기", pass_context=True)
async def _Rn(ctx, n1, n2):
    try:
        pickled = random.randint(int(n1), int(n2))
        await ctx.send(f'뽑힌 숫자는 **{str(pickled)}** 입니다')
    except IndexError:
        await ctx.send("무슨 숫자를 뽑을지 알려주세요")
    except ValueError:
        await ctx.channel.send("정수를 입력해주세요")
    except ZeroDivisionError:
        await ctx.channel.send("0으로 나눌 수 없습니다")


@app.command(name="역할", pass_context=True)
async def _Role(ctx, role, member: discord.Member = None):
    if ctx.message.author.guild_permissions.change_nickname:
        try:
            member = member or ctx.message.author
            await member.add_roles(get(ctx.guild.roles, name=role))
            await ctx.channel.send(str(member) + "에게 역할이 적용되었습니다.")
        except:
            await ctx.channel.send("뭘 잘못 쳤는진 모르겠지만 쨌든 제대로 입력좀")
    else:
        await ctx.channel.send("당신은 권한이 없기 때문에 이 명령어를 사용할 수 없습니다")

@app.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        return
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("값을 입력해주세요")
    elif isinstance(error, commands.BadArgument):
        await ctx.send("올바른 값을 입력해주세요")
    else:
        embed = discord.Embed(title="오류가 발생했습니다", description=" ", color=0xFF0000)
        embed.add_field(name="상세", value=f"```{error}```")
        await ctx.send(embed=embed)

@app.command(name="도움말", pass_context=True)
async def _Help(ctx):
    cmd = ctx.message.content[5:]
    if cmd == "":
        embed = discord.Embed(title="Bedwars Team Shuffle Bot Help", description="베드워즈 내전 팀 나누기 봇 도움말", color=0x00aaaa)
        embed.add_field(name="관리자 전용", value=" `~청소` `~역할`", inline=False)
        embed.add_field(name="기본", value=" `~숫자뽑기` `~팀` \n ", inline=False)
        embed.add_field(name="명령어는 추후 추가될 수 있습니다", value="\n `~도움말 <명령어>` 명령어를 통해 명령어의 상세정보를 확인할 수 있습니다",
                        inline=False)
        await ctx.channel.send(embed=embed)
    elif cmd == "clean":
        embed = discord.Embed(title="명령어 - 청소", description="<숫자> 에 쓰여있는 숫자만큼 밑에서부터 메시지를 삭제합니다", color=0x00aaaa)
        embed.add_field(name="사용법", value="`~청소 <숫자>`")
        await ctx.channel.send(embed=embed)
    elif cmd == "role":
        embed = discord.Embed(title="명령어 - 역할", description="설정한 역할을 멘션한 유저에게 적용합니다", color=0x00aaaa)
        embed.add_field(name="사용법", value="`~역할 <역할 이름> <유저 멘션>`")
        await ctx.channel.send(embed=embed)
    elif cmd == "숫자뽑기":
        embed = discord.Embed(title="명령어 - 숫자뽑기", description="설정한 숫자의 범위 안에서 랜덤한 숫자를 하나 뽑습니다", color=0x00aaaa)
        embed.add_field(name="사용법", value="`~숫자뽑기 <숫자 1> <숫자 2>`")
        await ctx.channel.send(embed=embed)
    elif cmd == "팀":
        embed = discord.Embed(title="명령어 - 팀", description="팀을 랜덤으로 섞어서 뽑습니다", color=0x00aaaa)
        embed.add_field(name="사용법", value="`ex) ~팀 player1 player2 player3 player4 / redteam redteam greenteam greenteam `")
        await ctx.channel.send(embed=embed)
    else:
        await ctx.channel.send("상세정보를 확인할 명령어를 입력해주세요")

access_token = os.environ["BOT_TOKEN"]
app.run(access_token)