import discord
from dotenv import load_dotenv
import os
from discord import app_commands
import json
from discord.ext import tasks
from operator import itemgetter

load_dotenv()

# constants
TOKEN = os.getenv("DISCORD_CLIENT_TOKEN")
APOLLOSERVER = 1146564374446743683000
STAFFROLES = {
    1146779529730347038:"Founder",
    1147570419629572207:"Commander",
    1189182483963584595:"Lieutenant",
    1175371306510860338:"Admin",
    1225782307281965187:"Moderator",
    1147222722267578489:"Staff",
    1225779210988032103:"Match Checker",
    1225779781585338389:"Rank Fixer"
    }
RANKS = {
    "Bronze":1,
    "Silver":2,
    "Gold":3,
    "Platinum":4,
    "Emerald":5,
    "Diamond":6,
    "Champion":7
}

# initialize client
client = discord.Client(intents=discord.Intents.all())
tree = app_commands.CommandTree(client=client)

# initialise variables
queue = []
matchmakingMessage = discord.Message


# functions
async def matchmake(interaction: discord.Interaction,player1: discord.Member,player2: discord.Member):
    global matchmakingMessage
    global queue

    embed = discord.Embed(title="Matchmaking",colour=discord.Colour.from_rgb(255,255,0)).set_author(name="Match found!").add_field(name="Players",value=f"Player 1: {player1.mention}\nPlayer 2: {player2.mention}").set_footer(text="Project Requiem | Developed by Apollo Systems").set_image(url="https://cdn.discordapp.com/attachments/1206631871228805130/1226871701036470363/project_requiem_player_vs_player_V03_01.png?ex=6626584f&is=6613e34f&hm=31404a82a8c679c717e0af66af0e4a9b6ad5ee07c60e457767654989f5c27fb9&")
    await interaction.followup.send(embed=embed)
    del queue[0:2]

@tasks.loop(minutes=5)
async def timer():
    global queue

    queue = []

class RankManager:
    def updateData_win(player):
        RankManager.addUser(str(player))

        with open("data.json","r") as f:
            data = json.load(f)

        data[player]["Points"] = int(data[player]["Points"])
        data[player]["Division"] = int(data[player]["Division"])

        match data[player]["Rank"]:
            case "Bronze":
                data[player]["Points"] += 30
            case "Silver":
                data[player]["Points"] += 32
            case "Gold":
                data[player]["Points"] += 34
            case "Platinum":
                data[player]["Points"] += 36
            case "Emerald":
                data[player]["Points"] += 38
            case "Diamond":
                data[player]["Points"] += 40
            case "Champion":
                data[player]["Points"] += 42
            
        if data[player]["Points"] >= 100:
            data[player]["Points"] = 0
            if data[player]["Division"] == 1 and data[player]["Rank"] != "Champion":
                with open("data.json","w") as f:
                    data[player]["Points"] = str(data[player]["Points"])
                    data[player]["Division"] = "5"
                    json.dump(data,f)
                RankManager.promote(player)
            else:
                data[player]["Division"] -= 1
                with open("data.json","w") as f:
                    data[player]["Points"] = str(data[player]["Points"])
                    data[player]["Division"] = str(data[player]["Division"])
                    json.dump(data,f)
        else:
            with open("data.json","w") as f:
                data[player]["Points"] = str(data[player]["Points"])
                data[player]["Division"] = str(data[player]["Division"])
                json.dump(data,f)
                


    def updateData_loss(player):
        RankManager.addUser(str(player))

        with open("data.json","r") as f:
            data = json.load(f)

        data[player]["Points"] = int(data[player]["Points"])
        data[player]["Division"] = int(data[player]["Division"])


        match data[player]["Rank"]:
            case "Bronze":
                data[player]["Points"] -= 14
            case "Silver":
                data[player]["Points"] -= 28
            case "Gold":
                data[player]["Points"] -= 36
            case "Platinum":
                data[player]["Points"] -= 44
            case "Emerald":
                data[player]["Points"] -= 52
            case "Diamond":
                data[player]["Points"] -= 60
            case "Champion":
                data[player]["Points"] -= 68
    
        if data[player]["Points"] < 0:
            data[player]["Points"] = 0
            if data[player]["Division"] == 5:
                data[player]["Division"] = 1
                with open("data.json","w") as f:
                    data[player]["Points"] = str(data[player]["Points"])
                    data[player]["Division"] = str(data[player]["Division"])
                    json.dump(data,f)
                RankManager.demote(player)
            else:
                data[player]["Division"] += 1
                with open("data.json","w") as f:
                    data[player]["Points"] = str(data[player]["Points"])
                    data[player]["Division"] = str(data[player]["Division"])
                    json.dump(data,f)
        else:
            with open("data.json","w") as f:
                data[player]["Points"] = str(data[player]["Points"])
                data[player]["Division"] = str(data[player]["Division"])
                json.dump(data,f)
        
        


    def promote(player):
        with open("data.json","r") as f:
            data = json.load(f)

        match data[player]["Rank"]:
            case "Bronze":
                data[player]["Rank"] = "Silver"
            case "Silver":
                data[player]["Rank"] = "Gold"
            case "Gold":
                data[player]["Rank"] = "Platinum"
            case "Platinum":
                data[player]["Rank"] = "Emerald"
            case "Emerald":
                data[player]["Rank"] = "Diamond"
            case "Diamond":
                data[player]["Rank"] = "Champion"

        with open("data.json","w") as f:
            json.dump(data,f)

    def demote(player):
        with open("data.json","r") as f:
            data = json.load(f)

        match data[player]["Rank"]:
            case "Bronze":
                data[player]["Division"] = 1
            case "Silver":
                data[player]["Rank"] = "Bronze"
            case "Gold":
                data[player]["Rank"] = "Silver"
            case "Platinum":
                data[player]["Rank"] = "Gold"
            case "Emerald":
                data[player]["Rank"] = "Platinum"
            case "Diamond":
                data[player]["Rank"] = "Emerald"
            case "Champion":
                data[player]["Rank"] = "Diamond"

        with open("data.json","w") as f:
            json.dump(data,f)

    def addUser(player):
        with open("data.json","r") as f:
            data = json.load(f)
        
        try:
            data[player]
        except KeyError:
            data[player] = {"Rank":"Bronze","Division":"5","Points":"0"}
        
        with open("data.json","w") as f:
            json.dump(data,f)

# events
@client.event
async def on_ready():
    print("ready")
    await tree.sync()
    await client.change_presence(status=discord.Status.online,activity=discord.CustomActivity(name="System Online"))
            


# commands
@tree.command(name="queue-match",description="Queue matchmaking")
async def queuematch(interaction: discord.Interaction):
    if interaction.guild_id != APOLLOSERVER:
        RankManager.addUser(str(interaction.user.id))

        await interaction.response.defer()
        if interaction.user in queue:
            embed = discord.Embed(title="Matchmaking",colour=discord.Colour.from_rgb(255,255,0)).add_field(name="Error",value="Already in matchmaking queue!").set_footer(text="Project Requiem | Developed by Apollo Systems").set_image(url="https://cdn.discordapp.com/attachments/1206631871228805130/1226871635798134956/project_requiem_queuing_v02.png?ex=66265840&is=6613e340&hm=2705e2c7105d2b43d6c89030018c55cf72cca7e91f5f0ce412631f94eff76e2b&")
            await interaction.followup.send(embed=embed)
        elif len(queue) >= 1:
            queue.append(interaction.user)
            await matchmake(interaction,queue[0],queue[1])
        else:
            queue.append(interaction.user)
            embed = discord.Embed(title="Matchmaking",colour=discord.Colour.from_rgb(255,255,0)).add_field(name="Queue",value=f"Successfully added {interaction.user.mention} to matchmaking queue!").set_footer(text="Project Requiem | Developed by Apollo Systems").set_image(url="https://cdn.discordapp.com/attachments/1206631871228805130/1226871635798134956/project_requiem_queuing_v02.png?ex=66265840&is=6613e340&hm=2705e2c7105d2b43d6c89030018c55cf72cca7e91f5f0ce412631f94eff76e2b&")
            await interaction.followup.send(embed=embed)
            try: 
                if not timer.is_running:
                    timer.start()
            except Exception:
                print(Exception)

@tree.command(name="match-result",description="Register the result of a match")
@app_commands.describe(player1="Player 1",player2="Player 2",result="Match winner ('1' OR '2')")
async def matchresult(interaction: discord.Interaction,player1: discord.Member,player2: discord.Member,result: int):
    if interaction.guild_id != APOLLOSERVER:
        staff = False
        for role in interaction.user.roles:
            if role.id in STAFFROLES or interaction.user.id==610020302692417546:
                staff = True
                break

        if not staff:
            await interaction.response.send_message("Not authorized.")
        else:
            embed = discord.Embed(title="Match Results",description="The results for a match have been added by a staff member.",colour=discord.Colour.from_rgb(255,255,0))

            if result == 1:
                embed.add_field(name="Player 1",value=f"{player1.mention} - Win").add_field(name="Player 2",value=f"{player2.mention} - Loss").set_footer(text="Project Requiem | Developed by Apollo Systems")
                RankManager.updateData_win(str(player1.id))
                RankManager.updateData_loss(str(player2.id))
            elif result == 2:
                embed.add_field(name="Player 1",value=f"{player1.mention} - Loss").add_field(name="Player 2",value=f"{player2.mention} - Win").set_footer(text="Project Requiem | Developed by Apollo Systems")
                RankManager.updateData_win(str(player2.id))
                RankManager.updateData_loss(str(player1.id))

            await interaction.response.send_message(embed=embed)

@tree.command(name="check-rank",description="Check the rank and division of a user!")
@app_commands.describe(user="User to check")
async def checkrank(interaction: discord.Interaction,user: discord.Member=None):
    if not user:
        user = interaction.user
    
    RankManager.addUser(str(user.id))

    with open("data.json","r") as f:
        data = json.load(f)

    division,rank,points = data[str(user.id)]["Division"],data[str(user.id)]["Rank"],data[str(user.id)]["Points"]
    embed = discord.Embed(title="Check Rank",description=f"Information on {user.display_name}'s current rank, division, and points values.",colour=discord.Colour.from_rgb(255,255,0)).set_footer(text="Project Requiem | Developed by Apollo Systems").set_image(url="https://cdn.discordapp.com/attachments/1206631871228805130/1226880696115789874/project_requiem_banner_rank_info.png?ex=662660b0&is=6613ebb0&hm=d187fa40c4f2ee5f95173199f65408388abf61fee4b6291fad693f2c298045e2&")
    embed.add_field(name="Rank",value=rank)
    embed.add_field(name="Division",value=division)
    embed.add_field(name="Points",value=f"Progress to next rank: {points}%")

    await interaction.response.send_message(embed=embed)

@tree.command(name="reset-data",description="Reset the points, rank, and division for all users or a specific user.")
@app_commands.describe(user="User to reset",foreveryone="Apply to everyone? DANGEROUS - DO NOT USE UNLESS YOU ARE SURE")
async def resetdata(interaction:discord.Interaction,user: discord.Member=None,foreveryone:bool=False):
    for role in interaction.user.roles:
        if role.id in STAFFROLES or interaction.user.id == 610020302692417546:
            role = role.id
            if interaction.user.id==610020302692417546 or STAFFROLES[role] == "Founder":
                with open("data.json","r") as f:
                    data = json.load(f)
                
                if user:
                    data[user.id] = {"Rank":"Bronze","Division":"5","Points":"0"}
                elif foreveryone:
                    for userid in data:
                        if userid == "lorem ipsum":
                            continue

                        data[userid] = {"Rank":"Bronze","Division":"5","Points":"0"}
                        
                with open("data.json","w") as f:
                    data = json.dump(data,f)

                await interaction.response.send_message("Done.")
                return
            
    await interaction.response.send_message("Not authorized.")
    
@tree.command(name="leaderboard",description="Display the player leaderboard")
@app_commands.describe(page="Page to view")
async def leaderboard(interaction:discord.Interaction,page:int=1):
    if interaction.guild_id != APOLLOSERVER:
        await interaction.response.defer()
        embed = discord.Embed(title="Leaderboard",description=f"Page {page}",colour=discord.Colour.from_rgb(255,255,0)).set_footer(text="Project Requiem | Developed by Apollo Systems").set_thumbnail(url="https://cdn.discordapp.com/attachments/1206631871228805130/1245009030825381949/PR_Project_Requiem.png?ex=66573084&is=6655df04&hm=7c59a2e003d0c6a0cae5f5c1714aafafcfd5aeaa901b137bde4fe929ca1e30d5&").set_image(url="https://cdn.discordapp.com/attachments/1206631871228805130/1245018733408288828/leaderboards_1.png?ex=6657398d&is=6655e80d&hm=fff5c75e03c705d55d440635709887c2b840232be2593ff9e830d44643370042&")
        
        organised_data = {}
        sorted_data = {}

        with open("data.json","r") as f:
            data = json.load(f)
        
        for user in data:
            rank = data[user]["Rank"]
            division = data[user]["Division"]

            try: organised_data[f"{rank}{division}"]
            except KeyError: organised_data[f"{rank}{division}"] = {}
            
            organised_data[f"{rank}{division}"][user] = data[user]
        
        try:sorted_data.update(organised_data["Diamond5"])
        except KeyError:pass
        try:sorted_data.update(organised_data["Diamond4"])
        except KeyError:pass
        try:sorted_data.update(organised_data["Diamond3"])
        except KeyError:pass
        try:sorted_data.update(organised_data["Diamond2"])
        except KeyError:pass
        try:sorted_data.update(organised_data["Diamond1"])
        except KeyError:pass
        try:sorted_data.update(organised_data["Emerald5"])
        except KeyError:pass
        try:sorted_data.update(organised_data["Emerald4"])
        except KeyError:pass
        try:sorted_data.update(organised_data["Emerald3"])
        except KeyError:pass
        try:sorted_data.update(organised_data["Emerald2"])
        except KeyError:pass
        try:sorted_data.update(organised_data["Emerald1"])
        except KeyError:pass
        try:sorted_data.update(organised_data["Platinum5"])
        except KeyError:pass
        try:sorted_data.update(organised_data["Platinum4"])
        except KeyError:pass
        try:sorted_data.update(organised_data["Platinum3"])
        except KeyError:pass
        try:sorted_data.update(organised_data["Platinum2"])
        except KeyError:pass
        try:sorted_data.update(organised_data["Platinum1"])
        except KeyError:pass
        try:sorted_data.update(organised_data["Gold5"])
        except KeyError:pass
        try:sorted_data.update(organised_data["Gold4"])
        except KeyError:pass
        try:sorted_data.update(organised_data["Gold3"])
        except KeyError:pass
        try:sorted_data.update(organised_data["Gold2"])
        except KeyError:pass
        try:sorted_data.update(organised_data["Gold1"])
        except KeyError:pass
        try:sorted_data.update(organised_data["Silver5"])
        except KeyError:pass
        try:sorted_data.update(organised_data["Silver4"])
        except KeyError:pass
        try:sorted_data.update(organised_data["Silver3"])
        except KeyError:pass
        try:sorted_data.update(organised_data["Silver2"])
        except KeyError:pass
        try:sorted_data.update(organised_data["Silver1"])
        except KeyError:pass
        try:sorted_data.update(organised_data["Bronze5"])
        except KeyError:pass
        try:sorted_data.update(organised_data["Bronze4"])
        except KeyError:pass
        try:sorted_data.update(organised_data["Bronze3"])
        except KeyError:pass
        try:sorted_data.update(organised_data["Bronze2"])
        except KeyError:pass
        try:sorted_data.update(organised_data["Bronze1"])
        except KeyError:pass

        for i,user in enumerate(sorted_data):
            if i < page*10 and i >= ((page-1)*10)-1:
                rank = sorted_data[user]["Rank"]
                division = sorted_data[user]["Division"]
                member:discord.Member = await client.fetch_user(user)
                embed.add_field(name=f"{i+1}. {member.display_name}",value=f"Rank: {rank}\nDivision: {division}",inline=False)

        await interaction.followup.send(embed=embed)

    else:
        await interaction.response.send_message("NOT AUTHORIZED")
        



client.run(TOKEN)