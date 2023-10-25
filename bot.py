import discord, json, numpy, random, datetime
from discord.ext import commands

with open('data/config.json', 'r') as f:
    data = json.load(f)
with open('data/cooldowns.json', 'r') as f1:
    cooldown_list = json.load(f1)
with open('data/distance.json', 'r') as f2:
    distance_list = json.load(f2)
with open('data/mstatus.json', 'r') as f3:
    mstatus_list = json.load(f3)
with open('data/sstatus.json', 'r') as f4:
    sstatus_list = json.load(f4)
with open('data/tstatus.json', 'r') as f5:
    tstatus_list = json.load(f5)
with open('data/smstatus.json', 'r') as f6:
    smstatus_list = json.load(f6)

discord_token = data["token"]
bot = commands.Bot(command_prefix="!", intents=discord.Intents.all(), help_command=None)

# Bot startup and status
@bot.event
async def on_ready():
    await bot.change_presence(status=discord.Status.dnd, activity=discord.Activity(type=discord.ActivityType.watching, name="Races"))
    print("Online")

# Sends cooldown on bot command
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        await ctx.reply(f"{error.retry_after:.2f} seconds to try again", delete_after=3)  

# Joins the racing event
@bot.command()
@commands.cooldown(1, 20, commands.BucketType.user)
async def joinrace(ctx):
    string_author = str(ctx.author)
    if string_author not in cooldown_list:
        cooldown_list[string_author] = 0
        distance_list[string_author] = 0
        mstatus_list[string_author] = False
        smstatus_list[string_author] = False
        tstatus_list[string_author] = False
        sstatus_list[string_author] = False
        with open("data/cooldowns.json", "w") as outfile:
            json.dump(cooldown_list, outfile)
        with open("data/distance.json", "w") as outfile2:
            json.dump(distance_list, outfile2)
        with open("data/mstatus.json", "w") as outfile3:
            json.dump(mstatus_list, outfile3)
        with open("data/smstatus.json", "w") as outfile4:
            json.dump(smstatus_list, outfile4)
        with open("data/sstatus.json", "w") as outfile5:
            json.dump(sstatus_list, outfile5)
        with open("data/tstatus.json", "w") as outfile6:
            json.dump(tstatus_list, outfile6)
        embed = discord.Embed(title="Welcome to the Big Race!", color=discord.Colour.dark_gold())
        await ctx.reply(embed=embed)
    else:
        embed = discord.Embed(title="You already joined", color=discord.Colour.dark_red())
        await ctx.reply(embed=embed)

# Travels a certain amount of distance
@bot.command()
@commands.cooldown(1, 5, commands.BucketType.user)
async def race(ctx):
    string_author = str(ctx.author)
    name, pfp = ctx.author.display_name, ctx.author.display_avatar
    if string_author in distance_list:
        presentDate = datetime.datetime.now()
        unix_timestamp = datetime.datetime.timestamp(presentDate)*1000
        if cooldown_list[string_author] <= unix_timestamp:
            presentDate = datetime.datetime.now()
            cooldown_list[string_author] = ((datetime.datetime.timestamp(presentDate)*1000) + 82800000)
            with open("data/cooldowns.json", "w") as outfile:
                json.dump(cooldown_list, outfile)
            travel_distance = random.randint(1, 100)
            if tstatus_list[string_author] == True:
                travel_distance = random.randint(1, 20)
            if mstatus_list[string_author] == True:
                travel_distance += 20
                mstatus_list[string_author] = False
                embed = discord.Embed(title="You used a speed mushroom!", color=discord.Colour.brand_red())
                embed.set_author(name=f"{name}", icon_url=f"{pfp}")
                await ctx.reply(embed=embed)
            if smstatus_list[string_author] == True:
                travel_distance += 100
                smstatus_list[string_author] = False
                embed = discord.Embed(title="You used a warp speed mushroom!", color=discord.Colour.dark_gold())
                embed.set_author(name=f"{name}", icon_url=f"{pfp}")
                await ctx.reply(embed=embed)
            distance_list[string_author] += travel_distance
            with open("data/distance.json", "w") as outfile2:
                json.dump(distance_list, outfile2)
            power_up_probability = random.randint(1, 100)
            if power_up_probability <= 5: 
                mstatus_list[string_author] = True
                embed = discord.Embed(title="You picked up a speed mushroom!", color=discord.Colour.brand_red())
                embed.set_author(name=f"{name}", icon_url=f"{pfp}")
                await ctx.reply(embed=embed)
            elif power_up_probability >= 30 and power_up_probability < 45:
                sstatus_list[string_author] = True
                embed = discord.Embed(title="You picked up a trip shield!", color=discord.Colour.dark_gray())
                embed.set_author(name=f"{name}", icon_url=f"{pfp}")
                await ctx.reply(embed=embed)
            elif power_up_probability >= 91:
                keys, values = list(distance_list.keys()), list(distance_list.values())
                sorted_value_index = numpy.argsort(values)
                sorted_dict = {keys[i]: values[i] for i in sorted_value_index}
                key_list = list(sorted_dict.keys())
                key_list = list(reversed(key_list))
                value_list = list(sorted_dict.values())
                value_list = list(reversed(value_list))
                rank_number = key_list.index(string_author) + 1
                participant_num = len(key_list)
                if ((participant_num/4)*3) < rank_number:
                    smstatus_list = True
                    embed = discord.Embed(title="You picked up a warp speed mushroom!", color=discord.Colour.dark_gold())
                    embed.set_author(name=f"{name}", icon_url=f"{pfp}")
                    await ctx.reply(embed=embed)
            with open("data/mstatus.json", "w") as outfile3:
                json.dump(mstatus_list, outfile3)
            with open("data/smstatus.json", "w") as outfile4:
                json.dump(smstatus_list, outfile4)
            with open("data/sstatus.json", "w") as outfile5:
                json.dump(sstatus_list, outfile5)
            embed = discord.Embed(title=f"You ran {travel_distance} meters!", color=discord.Colour.dark_green())
            embed.set_author(name=f"{name}", icon_url=f"{pfp}")
            embed.set_image(url="https://i.seadn.io/gcs/files/b9f21b5c8a24edb5bdc91fc129d5e411.gif?auto=format&dpr=1&w=1000")
            await ctx.reply(embed=embed)
        else:
            await ctx.reply(f"You can race again at <t:{round(cooldown_list[string_author] / 1000)}>")
    else:
        embed = discord.Embed(title="You have not joined the race yet", color=discord.Colour.dark_red())
        embed.set_author(name=f"{name}", icon_url=f"{pfp}")
        await ctx.reply(embed=embed)

# Attempt to trip a player
@bot.command()
@commands.cooldown(1, 5, commands.BucketType.user)
async def trip(ctx, member:discord.Member = None):
    string_member = str(member)
    string_author = str(ctx.author)
    name, pfp = ctx.author.display_name, ctx.author.display_avatar
    if string_member in distance_list:
        if string_author in distance_list:
            presentDate = datetime.datetime.now()
            unix_timestamp = datetime.datetime.timestamp(presentDate)*1000
            if cooldown_list[string_author] <= unix_timestamp:
                if tstatus_list[string_member] == False:
                    trip_success = random.randint(1, 100)
                    if trip_success <= 50:
                        if sstatus_list[string_member] == True:
                            sstatus_list[string_member] = False
                            with open("data/sstatus.json", "w") as outfile6:
                                json.dump(sstatus_list, outfile6)
                            embed = discord.Embed(title=f"{string_member} has been protected by a trip shield.", color=discord.Colour.dark_orange())
                            embed.set_author(name=f"{name}", icon_url=f"{pfp}")
                            await ctx.reply(embed=embed)
                        else:
                            tstatus_list[string_member] = True
                            with open("data/tstatus.json", "w") as outfile6:
                                json.dump(tstatus_list, outfile6)
                            presentDate = datetime.datetime.now()
                            cooldown_list[string_author] = ((datetime.datetime.timestamp(presentDate)*1000) + 82800000)
                            with open("data/cooldowns.json", "w") as outfile:
                                json.dump(cooldown_list, outfile)
                            embed = discord.Embed(title=f"{string_member} has been tripped", color=discord.Colour.dark_green())
                            embed.set_author(name=f"{name}", icon_url=f"{pfp}")
                            embed.set_image(url="https://i.seadn.io/gcs/files/01bbebc0cec8f6ef0e4744fcd9561a2e.gif?auto=format&dpr=1&w=1000")
                            await ctx.reply(embed=embed)
                    else:
                        presentDate = datetime.datetime.now()
                        cooldown_list[string_author] = ((datetime.datetime.timestamp(presentDate)*1000) + 82800000)
                        with open("data/cooldowns.json", "w") as outfile:
                            json.dump(cooldown_list, outfile)
                        embed = discord.Embed(title=f"You failed to trip {string_member}", color=discord.Colour.dark_red())
                        embed.set_author(name=f"{name}", icon_url=f"{pfp}")
                        await ctx.reply(embed=embed)
                else:
                    embed = discord.Embed(title=f"{string_member} has already been tripped today, leave them alone!", color=discord.Colour.dark_red())
                    embed.set_author(name=f"{name}", icon_url=f"{pfp}")
                    await ctx.reply(embed=embed)
            else:
                await ctx.reply(f"You can race again at <t:{round(cooldown_list[string_author] / 1000)}>")
        else:
            embed = discord.Embed(title="You not joined the race yet", color=discord.Colour.dark_red())
            embed.set_author(name=f"{name}", icon_url=f"{pfp}")
            await ctx.reply(embed=embed)
    else:
        embed = discord.Embed(title=f"{string_member} have not joined the race yet", color=discord.Colour.dark_red())
        await ctx.reply(embed=embed)

# Displays top 10 players on the race leader board
@bot.command(aliases=["rlb", "rleaderboard"])
@commands.cooldown(1, 5, commands.BucketType.user)
async def raceleaderboard(ctx):
    string_author = str(ctx.author)
    name, pfp = ctx.author.display_name, ctx.author.display_avatar
    rank1, rank2, rank3, rank4, rank5 = '', '', '', '', ''
    rank1score, rank2score, rank3score, rank4score, rank5score = 0, 0, 0, 0, 0
    rank6, rank7, rank8, rank9, rank10 = '', '', '', '', ''
    rank6score, rank7score, rank8score, rank9score, rank10score = 0, 0, 0, 0, 0

    keys, values = list(distance_list.keys()), list(distance_list.values())
    sorted_value_index = numpy.argsort(values)
    sorted_dict = {keys[i]: values[i] for i in sorted_value_index}
    key_list = list(sorted_dict.keys())
    key_list = list(reversed(key_list))
    value_list = list(sorted_dict.values())
    value_list = list(reversed(value_list))
    rank_number = key_list.index(string_author) + 1

    if len(sorted_dict) >= 1:
        rank1, rank1score = key_list[0], value_list[0]
        if len(sorted_dict) >= 2:
            rank2, rank2score = key_list[1], value_list[1]
            if len(sorted_dict) >= 3:
                rank3, rank3score = key_list[2], value_list[2]
                if len(sorted_dict) >= 4:
                    rank4, rank4score = key_list[3], value_list[3]
                    if len(sorted_dict) >= 5:
                        rank5, rank5score = key_list[4], value_list[4]
                        if len(sorted_dict) >= 6:
                            rank6, rank6score = key_list[5], value_list[5]
                            if len(sorted_dict) >= 7:
                                rank7, rank7score = key_list[6], value_list[6]
                                if len(sorted_dict) >= 8:
                                    rank8, rank8score = key_list[7], value_list[7]
                                    if len(sorted_dict) >= 9:
                                        rank9, rank9score = key_list[8], value_list[8]

    embed = discord.Embed(title="The Great Race", description="*Top 9 Distances*", color=discord.Colour.dark_gold())
    embed.add_field(name=f"**1st. **{rank1} :first_place:", value=f"{rank1score} meters", inline='true')
    embed.add_field(name=f"**2nd. **{rank2} :second_place:", value=f"{rank2score} meters", inline='true')
    embed.add_field(name=f"**3rd. **{rank3} :third_place:", value=f"{rank3score} meters", inline='true')
    embed.add_field(name=f"**4th. **{rank4}", value=f"{rank4score} meters", inline='true')
    embed.add_field(name=f"**5th. **{rank5}", value=f"{rank5score} meters", inline='true')
    embed.add_field(name=f"**6th. **{rank6}", value=f"{rank6score} meters", inline='true')
    embed.add_field(name=f"**7th. **{rank7}", value=f"{rank7score} meters", inline='true')
    embed.add_field(name=f"**8th. **{rank8}", value=f"{rank8score} meters", inline='true')
    embed.add_field(name=f"**9th. **{rank9}", value=f"{rank9score} meters", inline='true')
    embed.add_field(name="Your Rank", value=f"#{rank_number}", inline='false')
    embed.set_author(name=f"{name}", icon_url=f"{pfp}")
    await ctx.send(embed=embed)

# Displays distance and rank of a player
@bot.command()
@commands.cooldown(1, 5, commands.BucketType.user)
async def distance(ctx, member:discord.Member = None):
    if member is None:
        string_member = str(ctx.author)
        name, pfp = ctx.author.display_name, ctx.author.display_avatar
    else: 
        string_member = str(member)
        name, pfp = member.display_name, member.display_avatar
    if string_member in distance_list:
        total_distance = distance_list[string_member]
        embed = discord.Embed(title=f"{total_distance} meters ", color=discord.Colour.dark_gold())
        embed.set_author(name=f"{name}", icon_url=f"{pfp}")
        await ctx.reply(embed=embed)
    else:
        embed = discord.Embed(title="Not in the event", color=discord.Colour.dark_red())
        embed.set_author(name=f"{name}", icon_url=f"{pfp}")
        await ctx.reply(embed=embed)

# Displays power-up status of a player
@bot.command()
@commands.cooldown(1, 5, commands.BucketType.user)
async def status(ctx, member:discord.Member = None):
    if member is None:
        string_member = str(ctx.author)
        name, pfp = ctx.author.display_name, ctx.author.display_avatar
    else: 
        string_member = str(member)
        name, pfp = member.display_name, member.display_avatar
    if string_member in distance_list:
        s_status = sstatus_list[string_member]
        m_status = mstatus_list[string_member]
        sm_status = smstatus_list[string_member]
        embed = discord.Embed(title=f"{name}'s Power-Ups", color=discord.Colour.dark_gold())
        embed.set_author(name=f"{name}", icon_url=f"{pfp}")
        if s_status == True:
            embed.add_field(name="Trip Shield (:shield:)", value=":green_circle:", inline='false')
        else:
            embed.add_field(name="Trip Shield (:shield:)", value=":red_circle:", inline='false')
        if m_status == True:
            embed.add_field(name="Speed Mushroom (:mushroom:)", value=":green_circle:", inline='false')
        else:
            embed.add_field(name="Speed Mushroom (:mushroom:)", value=":red_circle:", inline='false')
        if sm_status == True:
            embed.add_field(name="Warp Speed Mushroom (:comet:)", value=":green_circle:", inline='false')
        else:
            embed.add_field(name="Warp Speed Mushroom (:comet:)", value=":red_circle:", inline='false')
        await ctx.reply(embed=embed)
    else:
        embed = discord.Embed(title="Not in the event", color=discord.Colour.dark_red())
        embed.set_author(name=f"{name}", icon_url=f"{pfp}")
        await ctx.reply(embed=embed)

# Displays commands related to the event
@bot.command()
@commands.cooldown(1, 5, commands.BucketType.user)
async def rhelp(ctx, member:discord.Member = None):
    embed = discord.Embed(title="Help Menu", description="*To participate in the race event you must first use !joinrace to be able to use the commands.*", color=discord.Colour.dark_green())
    embed.add_field(name="> !joinrace", value="Joins the Great Race", inline='false')
    embed.add_field(name="> !race", value="Moves a certain distance forward, may gain power-ups", inline='false')
    embed.add_field(name="> !trip <target>", value="Attempts to reduce another player's max travelable distance from !race", inline='false')
    embed.add_field(name="> !status <target>", value="Displays the power-ups currently held by a player", inline='false')
    embed.add_field(name="> !distance <target>", value="Displays distance traveled so far by a player", inline='false')
    embed.add_field(name="> !raceleaderboard", value="Displays the top 10 players by distance", inline='false')
    await ctx.reply(embed=embed)

if __name__ == '__main__':
    bot.run(discord_token)