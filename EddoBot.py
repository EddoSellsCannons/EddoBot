import discord
import os
import random
from time import sleep
from datetime import datetime
#import TwitterBot as tw
import CazinoRedeem as cr
import RPG
import traceback

from discord import raw_models

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

timeTABle = [
"monday|1200|2100|1500|All|All|All",
"tuesday|All|1800|All|2100|All|2200",
"wednesday|1500|1400|1800|1100|1400|1600",
"thursday|All|All|All|2100|All|1900",
"friday|1400|1500|2100|2100|All|1600",
"saturday|All|All|All|2100|All|2200",
"sunday|All|2100|All|All|All|All"]

class ScoreError(Exception):
    pass
class EmptyLs(Exception):
    pass

def dayOfYear(date):
    days = [0,31,28,31,30,31,30,31,31,30,31,30,31]
    d = list(map(int,date.split("-")))
    if d[0]%4 == 0 and d[0]%100!=0:
        days[2]+=1
    for i in range(1,len(days)):
        days[i]+=days[i-1]
    return days[d[1]-1]+d[2] - 1 

def slots_roll_once():
    slot_roll = int(random.random()*100)
    index = 0
    if slot_roll >= 0 and slot_roll <= 3: #3%
        index = 0
    elif slot_roll > 3 and slot_roll <= 33: #30%
        index = 1
    elif slot_roll > 33 and slot_roll <= 57: #24%
        index = 2
    elif slot_roll > 57 and slot_roll <= 76: #19%
        index = 3
    elif slot_roll > 76 and slot_roll <= 90: #14%
        index = 4
    elif slot_roll > 90 and slot_roll <= 100: #10%
        index = 5
    return index

def slots_determine_outcome(slot_winning_card): #Returns Multipliers
    if slot_winning_card == "<a:UwUOwO:782575562203988019>":
        return 500
    elif slot_winning_card == "<:dam:826071637128511529>":
        return 10
    elif slot_winning_card == "<:Light_Blue_Shy_Guy10:1079262284062408784>":
        return 20
    elif slot_winning_card == "<:Glush:1079073691549302894>":
        return 50
    elif slot_winning_card == "<:sealofapproval:865125910134784032>":
        return 75
    elif slot_winning_card == "<:pongers:865218289943445504>":
        return 100

def slots(author, bet_amount):
    slot_card = ["<a:UwUOwO:782575562203988019>", "<:dam:826071637128511529>","<:Light_Blue_Shy_Guy10:1079262284062408784>", "<:Glush:1079073691549302894>", "<:sealofapproval:865125910134784032>", "<:pongers:865218289943445504>"]
    slots_results = []
    slot_printable = ""
    slots_fee = 0
    bet_multiplier = 1

    if bet_amount > 0:
        slots_fee = bet_amount #COST OF $SLOTS
        bet_multiplier = ((1000 - (1000-10)*pow(2.71,(-0.008*slots_fee))))/100
        print(bet_multiplier)
    else:
        bet_amount = 0
        bet_multiplier = 0.1

    # f = open("cazino.txt", 'r') #To add someone, make sure to update each index of scores and username
    # file = f.readlines()
    # f.close()
    # scores = []
    # index = 0

    # while(index < 7):
    #     line = file[index].split(":")
    #     scores.append([line[0], line[1]])
    #     index += 1
    # if int(scores[6][1]) < slots_fee:
    #     return ["Cazino Out of Order","Cazino Out of Order","Cazino Out of Order"]
    # if author == ".json":
    #     if int(scores[0][1]) < slots_fee:
    #         return ["Insufficient Funds","Insufficient Funds","Insufficient Funds"]
    # elif author == "Boba":
    #     if int(scores[1][1]) < slots_fee:
    #         return ["Insufficient Funds","Insufficient Funds","Insufficient Funds"]
    # elif author == "KennyCarry":
    #     if int(scores[2][1]) < slots_fee:
    #         return ["Insufficient Funds","Insufficient Funds","Insufficient Funds"]
    # elif author == "LazyBoi":
    #     if int(scores[3][1]) < slots_fee:
    #         return ["Insufficient Funds","Insufficient Funds","Insufficient Funds"]
    # elif author == "Eddo":
    #     if int(scores[4][1]) < slots_fee:
    #         return ["Insufficient Funds","Insufficient Funds","Insufficient Funds"]
    # elif author == "Vanceinian":
    #     if int(scores[5][1]) < slots_fee:
    #         return ["Insufficient Funds","Insufficient Funds","Insufficient Funds"]
    # else:
    #     return ["Invalid User. Please message <@211057898967531520> create a membership at the CaZiNo","Invalid User. Please message <@211057898967531520> create a membership at the CaZiNo",""]

    while(len(slots_results) < 3):
        slots_single_line = []
        while(len(slots_single_line) < 3):
            index = slots_roll_once()
            if author == "Eddo" and bet_amount == 69 and int(scores[4][1]) < 6900:
                index = 0
            slots_single_line.append(slot_card[index])
            slot_printable += slot_card[index] + " "
        slots_results.append(slots_single_line)
        slot_printable += "\n"

    message_to_send = ""
    winnings_amount = 0
    winning_line = ""

    if slots_results[0][0] == slots_results[0][1] == slots_results[0][2]:
        winnings_amount = int(slots_determine_outcome(slots_results[0][0]) * bet_multiplier) + slots_fee
        message_to_send = "\n<:pongers:865218289943445504> " + author + " has won: " + str(winnings_amount) + " <:pongers:865218289943445504>"
        winning_line = "h1"
    elif slots_results[1][0] == slots_results[1][1] == slots_results[1][2]:
        winnings_amount = int(slots_determine_outcome(slots_results[1][0]) * bet_multiplier) + slots_fee
        message_to_send = "\n<:pongers:865218289943445504> " + author + " has won: " + str(winnings_amount) + " <:pongers:865218289943445504>"
        winning_line = "h2"
    elif slots_results[2][0] == slots_results[2][1] == slots_results[2][2]:
        winnings_amount = int(slots_determine_outcome(slots_results[2][0]) * bet_multiplier) + slots_fee
        message_to_send = "\n<:pongers:865218289943445504> " + author + " has won: " + str(winnings_amount) + " <:pongers:865218289943445504>"
        winning_line = "h3"
    elif slots_results[0][0] == slots_results[1][1] == slots_results[2][2]:
        winnings_amount = int(slots_determine_outcome(slots_results[0][0]) * bet_multiplier) + slots_fee
        message_to_send = "\n<:pongers:865218289943445504> " + author + " has won: " + str(winnings_amount) + " <:pongers:865218289943445504>"
        winning_line = "d1"
    elif slots_results[2][0] == slots_results[1][1] == slots_results[0][2]:
        winnings_amount = int(slots_determine_outcome(slots_results[2][0]) * bet_multiplier) + slots_fee
        message_to_send = "\n<:pongers:865218289943445504> " + author + " has won: " + str(winnings_amount) + " <:pongers:865218289943445504>"
        winning_line = "d2"
    else:
        losing_dialogue = int(random.random()*4)
        if losing_dialogue == 0:
            message_to_send = "\n" + author + " got L + Ratio'd"
        elif losing_dialogue == 1:
            message_to_send = "\n" + author + " has lost"
        elif losing_dialogue == 2:
            message_to_send = "\n" + author + " is unlucky today"
        elif losing_dialogue == 3:
            message_to_send = "\n<:dam:826071637128511529> Dam, that's sad " + author

    #Updating scores

    #if author == ".json":
        #new_score = int(scores[0][1]) + int(winnings_amount - slots_fee)
        #scores[0][1] = str(new_score) + '\n'
    #elif author == "Boba":
        #new_score = int(scores[1][1]) + int(winnings_amount - slots_fee)
        #scores[1][1] = str(new_score) + '\n'
    #elif author == "KennyCarry":
        #new_score = int(scores[2][1]) + int(winnings_amount - slots_fee)
        #scores[2][1] = str(new_score) + '\n'
    #elif author == "LazyBoi":
        #new_score = int(scores[3][1]) + int(winnings_amount - slots_fee)
        #scores[3][1] = str(new_score) + '\n'
    #elif author == "Eddo":
        #new_score = int(scores[4][1]) + int(winnings_amount - slots_fee)
        #scores[4][1] = str(new_score) + '\n'
    #elif author == "Vanceinian":
        #new_score = int(scores[5][1]) + int(winnings_amount - slots_fee)
        #scores[5][1] = str(new_score) + '\n'

    #Update Bank
    #new_score = int(scores[6][1]) + int(slots_fee) - int(winnings_amount)
    #scores[6][1] = str(new_score) + '\n'

    #score_msg = ""
    #for player in scores:
        #score_msg += str(player[0]) + "'s current balance is: " + str(player[1])

    #fw = open("cazino.txt", 'w')
    #for s in scores:
        #fw.write(str(s[0]) + ":" + str(s[1]))
   # fw.close()
        
    #message_to_send += "\n\n" + score_msg
    return [slot_printable ,message_to_send, winning_line]
def checkUnsub(msgauth):
    f = open("unsub.txt", 'r')
    file = f.readlines()
    for fl in file:
        fl = fl.rstrip()
    for fl in file:
        if msgauth in fl:
            f.close()
            return True
    f.close()
    return False

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_raw_reaction_add(payload):
    if payload.message_id == 590509269603057686:
        channel = client.get_channel(payload.channel_id)
        message = await channel.fetch_message(payload.message_id)
        user = client.get_user(payload.user_id)
        emoji = client.get_emoji(577578847080546304)
        await message.remove_reaction(emoji, user)

@client.event
async def on_message(message):
    msgauth = str(message.author).split("#")[0]
    print(msgauth + ": " + message.content)
    if checkUnsub(msgauth):
        return

    wordle_day = str(196 + dayOfYear(datetime.now().strftime("%Y-%m-%d")))

    if message.author == client.user:
        return

    if datetime.now().strftime("%d/%m/%Y") == "08/03/2025": #Kenny bday
        await message.channel.send("<@213908174632124416> hapb")
        exit()
    if datetime.now().strftime("%d/%m/%Y") == "12/03/2025": #Jason bday
        await message.channel.send("<@!213597962373169153> hapb")
        exit()
    if datetime.now().strftime("%d/%m/%Y") == "17/04/2025": #Vincent bday
        await message.channel.send("<@!372946913647132672> hapb")
        exit()
    if datetime.now().strftime("%d/%m/%Y") == "28/04/2024": #Eddo's Cake day
        await message.channel.send("<@211057898967531520> Happy Cake day!")
        exit()
    if datetime.now().strftime("%d/%m/%Y") == "16/08/2024": #Ray bday
        await message.channel.send("<@229809987243737089> hapb")
        exit()
    if datetime.now().strftime("%d/%m/%Y") == "04/09/2024": #Boi bday
        await message.channel.send("<@!215385234433245184> hapb")
        exit()
    if datetime.now().strftime("%d/%m/%Y") == "27/07/2024": #Jane bday
        await message.channel.send("<@384676089450201091> hapb")
        exit()
    if datetime.now().strftime("%d/%m/%Y") == "30/04/2024": #Andrew bday
        await message.channel.send("<@269839983110520832> hapb")
        exit()
    if datetime.now().strftime("%d/%m/%Y") == "01/08/2024": #Sam bday
        await message.channel.send("<@179528751623700480> hapb")
        exit()
    if datetime.now().strftime("%d/%m/%Y") == "25/12/2024": 
        await message.channel.send(f"Happy Christmas {msgauth}! Reply with what you got for Christmas this year!")
        exit()
    if datetime.now().strftime("%d/%m/%Y") == "01/01/2025": 
        await message.channel.send(f"Happy New Year {msgauth}! Reply with your favourite New Year's Resolutions you are hoping to achieve!")
        exit()

    if message.content.isalnum() == False and message.content == "": #Slightly less shitty instanceof
        hotness = int(random.random()*4)
        if hotness == 0:
            await message.channel.send("eww.")
        if hotness == 1:
            await message.channel.send("Looks like shit.")
        if hotness == 2:
            await message.channel.send("Hey, that's pretty good.")
        if hotness == 3:
            await message.channel.send("I'M CUMMING 🥴🍆💦")

    if message.content.startswith('$hello'):
        await message.delete()
        await message.channel.send('Hello ' + str(msgauth) + "!")

    #if message.content.startswith('$mc'):
    #    os.system('taskkill /F /FI "WINDOWTITLE eq Minecraft*" ')
    #    await message.channel.send("Closed Eddo's Minecraft session.")
    #    exit()

    elif message.content.startswith('$say'):
        await message.delete()
        msg = message.content.split()
        to_send_list = msg[1:]
        to_send = ""
        for m in to_send_list:
            to_send += m + " "
        await message.channel.send(to_send)

    elif message.content.startswith("$dejj"):
        with open("dejj.png", "rb") as f:
            image = discord.File(f)
            await message.channel.send(file=image)

    elif message.content.startswith("$unsub"):
        fw = open("unsub.txt", 'a')
        fw.write(msgauth + "\n")
        fw.close()
        await message.channel.send("You've successfully Unsubscribed from EddoBot. Please notify admin if you wish to resubscribe.")

    elif message.content.startswith("$poll"):
        try:
            list_of_items = message.content.split("|")
            list_of_items[0] = list_of_items[0][5:] #Remove "$poll "
            if len(list_of_items) <= 1:
                raise UnboundLocalError
            poll_string = ""
            emoji_list = ["🇦", "🇧", "🇨", "🇩", "🇪", "🇫", "🇬", "🇭", "🇮", "🇯", "🇰", "🇱", "🇲", "🇳", "🇴", "🇵", "🇶", "🇷", "🇸"] #max limit of reacts (19 + 1 for other)
            other_emoji = '🅾️'
            title_modifier = 0
            title_string = ""
            for i in range(len(list_of_items)):
                if i > (len(emoji_list) + title_modifier) - 1:
                    i -= 1
                    break
                if "title:" not in list_of_items[i]:
                    poll_string += emoji_list[i - title_modifier] + ": " + list_of_items[i] + "\n"
                else:
                    title_string = list_of_items[i].split(":")[1]
                    title_modifier = 1

            poll_string += other_emoji + ": " + "OTHER (Suggest in chat)"
            
            if title_modifier == 1:
                poll_string = title_string + '\n' + poll_string
                i -= 1

            poll_msg = await message.channel.send(poll_string)
            await message.delete()
            for e in emoji_list:
                if i < 0:
                    break
                i -= 1
                await poll_msg.add_reaction(e)
            await poll_msg.add_reaction(other_emoji)
        except IndexError:
            await message.channel.send("To use $poll, do $poll <List of items to poll seperated by commas>")
        except UnboundLocalError:
            await message.channel.send("Please add items to the poll with spaces in between")

    elif message.content.startswith("$rpg"):
        MAX_REPEATS = 50
        message.content = message.content.lower()
        try:
            msg = message.content.split()
            if len(msg) > 3:
                raise IndexError
            command = msg[1]
            if command == "battle":
                try:
                    repeats = int(msg[2])
                    if repeats > MAX_REPEATS:
                        repeats = MAX_REPEATS
                except IndexError:
                    repeats = 1
                while repeats > 0:
                    battle_details = RPG.battle(msgauth, "")
                    cur_battle_frame = await message.channel.send(battle_details[0])
                    for f in battle_details:
                        await cur_battle_frame.edit(content=f)
                        sleep(1)
                    repeats -= 1
                    if repeats > 0:
                        await cur_battle_frame.edit(content=f + f"\n--------------------------------------------------------------------------------------------------------------------------------------------- \[{repeats}\]")
                    if "EddoBot" in cur_battle_frame.content and "D:" not in cur_battle_frame.content:
                        await message.channel.send("EddoBot has been slain. Please restart the system to continue...")
                        exit()
            elif command == "info":
                info_display = RPG.get_info(msgauth)
                await message.channel.send(info_display)
            elif command == "item":
                try:
                    option = msg[2]
                    if option.lower() == "discard":
                        item_discarded = RPG.discard_item(msgauth)
                        await message.channel.send(f"Discarded {item_discarded} from main hand. Equipped None")
                    elif option.lower() == "swap":
                        item_equipped = RPG.swap_items(msgauth)
                        await message.channel.send(f"Swapped items from mainhand to offhand. Equipped {item_equipped}")
                    else:
                        raise IndexError
                except IndexError:
                    item_display = RPG.get_item_info(msgauth)
                    await message.channel.send(item_display)
            elif command == "spend":
                emoji_list = ['⚔️','🛡️','🎲','👟','✅', '🔟']
                def check(reaction, user):
                    return user == message.author
                user_info = await message.channel.send(RPG.get_info(msgauth))
                for e in emoji_list:
                    await user_info.add_reaction(e)
                multi_upgrade = False
                while(1):
                    try:
                        reaction, user = await client.wait_for("reaction_add", check=check, timeout=10.0)
                        upgrade_successful = False
                        reacted_emote = str(reaction)
                        
                        #TODO try to remove reactions after processing
                        if message.author != user:
                            await message.channel.send("Invalid user.")
                            return
                        if reacted_emote in emoji_list:
                            if reacted_emote == emoji_list[0]:
                                if multi_upgrade:
                                    times = 10
                                    while times > 0:
                                        upgrade_successful = RPG.sp_spend(msgauth, "atk")
                                        times -= 1
                                else:
                                    upgrade_successful = RPG.sp_spend(msgauth, "atk")
                            elif reacted_emote == emoji_list[1]:
                                if multi_upgrade:
                                    times = 10
                                    while times > 0:
                                        upgrade_successful = RPG.sp_spend(msgauth, "def")
                                        times -= 1
                                else:
                                    upgrade_successful = RPG.sp_spend(msgauth, "def")
                            elif reacted_emote == emoji_list[2]:
                                if multi_upgrade:
                                    times = 10
                                    while times > 0:
                                        upgrade_successful = RPG.sp_spend(msgauth, "lck")
                                        times -= 1
                                else:
                                    upgrade_successful = RPG.sp_spend(msgauth, "lck")
                            elif reacted_emote == emoji_list[3]:
                                if multi_upgrade:
                                    times = 10
                                    while times > 0:
                                        upgrade_successful = RPG.sp_spend(msgauth, "agl")
                                        times -= 1
                                else:
                                    upgrade_successful = RPG.sp_spend(msgauth, "agl")
                            elif reacted_emote == emoji_list[4]:
                                await user_info.edit(content=(RPG.get_info(msgauth) + f"\nUpgrading Complete. See you next time!"))
                                return
                            elif reacted_emote == emoji_list[5]:
                                if multi_upgrade == False:
                                    multi_upgrade = True
                                    await user_info.edit(content=(RPG.get_info(msgauth) + f"\nMulti upgrade enabled"))
                                    continue
                                else:
                                    multi_upgrade = False
                                    await user_info.edit(content=(RPG.get_info(msgauth) + f"\nMulti upgrade disabled"))
                                    continue
                        if upgrade_successful:
                            await user_info.edit(content=(RPG.get_info(msgauth) + f"\nUpgrade Successful {reacted_emote}"))
                        else:
                            await user_info.edit(content=(RPG.get_info(msgauth) + "\nNot enough SP."))
                    except TimeoutError:
                        await user_info.edit(content=(RPG.get_info(msgauth) + f"\nUpgrading Complete. See you next time!"))
                        return
            elif command == "shop":
                emoji_list = ['1️⃣', '2️⃣', '3️⃣', '4️⃣', '5️⃣', '🔄', '✅']
                def check(reaction, user):
                    return user == message.author
                shop_info = await message.channel.send(RPG.show_shop_formatted(msgauth))
                for e in emoji_list:
                    await shop_info.add_reaction(e)
                while(1):
                    try:
                        reaction, user = await client.wait_for("reaction_add", check=check, timeout=10.0)
                        purchase_successful = False
                        reacted_emote = str(reaction)
                        if message.author != user:
                            await message.channel.send("Invalid user.")
                            return
                        if reacted_emote in emoji_list:
                            if reacted_emote == emoji_list[0]:
                                purchase_successful = RPG.buy_shop(msgauth, 0)
                            elif reacted_emote == emoji_list[1]:
                                purchase_successful = RPG.buy_shop(msgauth, 1)
                            elif reacted_emote == emoji_list[2]:
                                purchase_successful = RPG.buy_shop(msgauth, 2)
                            elif reacted_emote == emoji_list[3]:
                                purchase_successful = RPG.buy_shop(msgauth, 3)
                            elif reacted_emote == emoji_list[4]:
                                purchase_successful = RPG.buy_shop(msgauth, 4)
                            elif reacted_emote == emoji_list[5]:
                                reroll_successful = RPG.reroll_shop(msgauth)
                                if reroll_successful:
                                    await shop_info.edit(content=(RPG.show_shop_formatted(msgauth) + "\nShop refreshed"))
                                else:
                                    await shop_info.edit(content=(RPG.show_shop_formatted(msgauth) + "\nNot enough Gold."))
                                continue
                            elif reacted_emote == emoji_list[6]:
                                raise TimeoutError
                        if purchase_successful:
                            await shop_info.edit(content=(RPG.show_shop_formatted(msgauth) + "\nItem purchased successfully"))
                        else:
                            await shop_info.edit(content=(RPG.show_shop_formatted(msgauth) + "\nNot enough Gold."))
                    except TimeoutError:
                        await shop_info.edit(content=(RPG.show_shop_formatted(msgauth) + "\nThank you for coming."))
                        return
            elif command == "dungeon":
                emoji_list = ['1️⃣', '2️⃣', '🏳️','ℹ️','🔃', '🛠️']
                def check(reaction, user):
                    return user == message.author
                full_story = RPG.get_all_story()
                cur_story = full_story[0]
                story_info = await message.channel.send(RPG.display_story(cur_story))
                for e in emoji_list:
                    await story_info.add_reaction(e)
                while(1):
                    try:
                        reaction, user = await client.wait_for("reaction_add", check=check, timeout=60.0)
                        reacted_emote = str(reaction)
                        progress = False
                        if message.author != user:
                            await message.channel.send("Invalid user.")
                            return
                        if reacted_emote in emoji_list:
                            if reacted_emote == emoji_list[0]:
                                cur_story = RPG.handle_choice(cur_story, 0)
                                progress = True
                            elif reacted_emote == emoji_list[1]:
                                cur_story = RPG.handle_choice(cur_story, 1)
                                progress = True
                            elif reacted_emote == emoji_list[2]:
                                progress = True
                                raise TimeoutError
                            elif reacted_emote == emoji_list[3]:
                                await story_info.edit(content=RPG.display_story(cur_story) + "\n" + RPG.get_info(msgauth))
                            elif reacted_emote == emoji_list[4]:
                                item_equipped = RPG.swap_items(msgauth)
                                await story_info.edit(content=RPG.display_story(cur_story) + "\n" + f"Swapped items from mainhand to offhand. Equipped {item_equipped}")
                            elif reacted_emote == emoji_list[5]:
                                item_info = RPG.get_item_info(msgauth)
                                await story_info.edit(content=RPG.display_story(cur_story) + "\n" + item_info)
                        if progress:
                            if RPG.handle_story(msgauth, cur_story)[0] == "battle":
                                print(RPG.handle_story(msgauth, cur_story)[1].name)
                                battle_details = RPG.battle(msgauth, RPG.handle_story(msgauth, cur_story)[1])
                                cur_battle_frame = await message.channel.send(battle_details[0])
                                for f in battle_details:
                                    await cur_battle_frame.edit(content=f)
                                    sleep(1)
                                if "D:" in battle_details[-1]: #TODO more reliable way to detect loss
                                    raise TimeoutError
                                else:
                                    story_info = await message.channel.send(RPG.display_story(cur_story))
                                    for e in emoji_list:
                                        await story_info.add_reaction(e)
                            elif RPG.handle_story(msgauth, cur_story)[0] == "loot":
                                await story_info.edit(content=RPG.display_story(cur_story) + "\n" + RPG.give_item(msgauth, RPG.handle_story(msgauth, cur_story)[1]))
                            elif RPG.handle_story(msgauth, cur_story)[0] != "battle" or RPG.handle_story(msgauth, cur_story)[0] != "loot":
                                await story_info.edit(content=(RPG.display_story(cur_story)))
                            if int(random.random() * 100) == 1:
                                await story_info.edit(content=(RPG.display_story(cur_story) + "\n```The dungeon begins to collapse. You exit the dungeon and narrowly escape death```"))
                                return
                    except TimeoutError:
                        await story_info.edit(content="You flee the dungeon")
                        return
            elif command == "ascend":
                ascended = RPG.ascend_player(msgauth)
                if ascended:
                    await message.channel.send("You have ascended!")
                else:
                    await message.channel.send("You are too weak to ascend.")
            elif command == "help":
                help_msg = ""
                option = msg[2]
                if option.lower() == "battle":
                    help_msg += """
('-')
Slime [======] **(Enemy HP)**
Level: 1 | ATK: 1 | DEF: 0 | LCK: 0 | AGL: 0 | SP: -1 | XP: 0 **(Enemy Stats)**
Equipped: None | Offhand: None **(Enemy Items)**
Floor: 1 **(Floor you can encouter this enemy at)**

[:)]
-|-
/\\
Eddo [==========] **(Your Character health)**
Level: 1 | ATK: 10 | DEF: 10 | LCK: 0 | AGL: 0 | SP: 3 | XP: 0 **(Your character stats)**
Equipped: None | Offhand: None **(Your items)**
Floor: 1 **(Your floor)**

When using $rpg battle, it will automatically start a battle against a mob. The mob encountered will depend on what floor you are on. The higher up you go, the stronger mobs will be.
In a battle, damage is calculated by player ATK - Enemy DEF. Crits occur by rolling player LCK stat against the enemy. To get better crits, you need to be luckier than your opponent. Dodging will occur after rolling for AGL stat. You need to be more agile than your opponent to dodge more.
Items can be equipped which boost your stats. Melee items deal 2x crit, while ranged and magic items deal 3x crit. Magic items will ignore half the enemies armor, but prevent you from dodging
Items are able to break in battle. Your stats will immediately reflect this when it occurs.

When a mob is defeated, it will give you XP equal to the level of the mob. Also, the higher level the mob, the more likely an item will drop.
If you are defeated, you will lose all your items, and fall down 5 floors.

You can use the auto-repeat function by doing $rpg battle <amount of repeats>. This will loop the battle command multiple times until they are all done. Unfortunately this also means that it will be locked in until all fights are over.

The Tower of Terror is designed to be the primary grind location. It cannot drop special items

Your character is attached to your Discord Username. If you change your name, your character will not be transfered. Please contact the admin for assistance.
"""
                elif option.lower() == "dungeon":
                    help_msg += """
You find a mysterious dungeon. Inside, you are faced with 2 doors. Which do you choose?
Choice 1: Left Door
Choice 2: Right Door
(1) (2) (🏳️) (ℹ️) (🔃)(🛠️)

When entering the dungeon, you are always given 2 choices, and a surrender option. You will also automaticall surrender after timing out. This will allow you to flee and save your character
There are 3 main events that occur in the dungeon:
STORY: A story is an event where players are simply given 2 options. Some options will lead to random rooms while some are set to give an outcome.
BATTLE: A battle can occur in the dungeon. These mobs are drawn from the boss pool and have a higher chance of starting with an item. Defeating them usually grants a reward, provided it is chosen
LOOT: Loot can be found in the dungeon randomly, or after choosing to when defeating a boss. In the dungeon, there is a chance to obtain SPECIAL items, which are stronger and are far less likely to break

The dungeon is a high risk high reward choice. You can quickly scale up by finding items, or die trying and lose everything. There are also weaker bosses, so it is not always impossible
ℹ️ allows you to see your current character
🔃 will swap your items
🛠️ allows you to see your items
"""
                elif option.lower() == "item":
                    help_msg += """
Equipped: Eddo's OP Item
An overpowered item that is of type "Special". It is usually unobtainable through normal means
Stat changes: +10a,+10d,+10l,+10g,+10h
Type: SPECIAL

Offhand: Katana+5
A fragile katana. With one stroke of the blade, even the largest enemies fall. Of course, if you miss...
Stat changes: +60a,+120l,-150d
Type: Melee

The item command allows you to see what you are holding, and what each item offers. Only the equipped weapon grants stats.
a = ATK
d = DEF
l = LCK
g = AGL
h = HP

+ = add stats
- = remove stats
= = set the stats to that number

Melee and SPECIAL weapons offer x2 crit damage, while magic and ranged weapons offer 3x crit damage. However, magic items causes the user to be unable to dodge but will ignore half the enemies defense
SPECIAL weapons gain all the benefits of melee, ranged and magic, where it will deal bonus crit damage, ignore /2 def and apply standard dodging/crit calculations. It is also harder to break
Items can be upgraded by finding duplicates. Each duplicate will multiply the original stat boosts, including the negatives. 
"""
                elif option.lower() == "shop":
                    help_msg += """
Gold Remaining: 1332 **Your current gold**
Item currently equipped: Eddo's OP Item **Item equipped**
Item in offhand: Katana+5 **Item in offhand**

Item Name: Claymore | Cost: 3
Item Name: Axe | Cost: 4
Item Name: Magic Armor | Cost: 4
Item Name: Bow | Cost: 9
Item Name: Shield | Cost: 16
(1)(2)(3)(4)(5)(🔄)
The shop is shared among all players. Rerolling costs 5 gold, and each item can be bought before needing to refresh.
ONLY your currently equipped item will be upgraded. It will not upgrade your offhand. To swap, use $rpg item swap
Only non-special items can appear in the store"""
                elif option.lower() == "spend":
                    help_msg += """
[:)]
-|-
/\\
Eddo [=============================================================================================              ] x2
Level: 92 | ATK: 96 | DEF: 40 | LCK: 145 | AGL: 88 | SP: 6 | XP: 427
Equipped: None | Offhand: None
Floor: 74

(⚔️)(🛡️)(🎲)(👟)(✅)(🔟)

The spend command allows you to spend your SP. This will increase your stats by a set amount each time
⚔️ ATK will increase the amount of damage you deal
🛡️ DEF will decrease the amount of damage you take
🎲 LUCK will increase the chance of landing a crit, and also increase the chance of finding a duplicate item to upgrade the currently equipped item
👟 AGILITY will increase the chance of dodging an attack entirely

LUCK increased by items will influence crit chance, but will not influence item drop chance.
✅ will close the SP shop
🔟 will activate Multi-upgrade, which will attempt to upgrade 10 at once. Click again to disable"""
                elif option.lower() == "ascend":
                    help_msg += """
Allows the player to ascend, keeping a portion of their stats and gaining SP equal to their level. However, their character will reset.
Ascension can only be performed after a certain level has been achieved"""
                await message.channel.send(help_msg)
            else:
                raise IndexError
        except (IndexError, ValueError) as e:
            print(traceback.format_exc())
            await message.channel.send("To use RPG, do $rpg <command> <option>. Do not spam this command (can get server banned!)\nCommands are:\n        battle <Num of Battles (max=20)>| Grind the Tower of Terror\n        dungeon | Enter the dungeon of doom\n        info | Check your own stats\n        spend | Opens the spend SP UI\n        item <swap/discard/(empty)> to swap items, discard your equipped weapon, or leave blank to view your own items.\n        shop | Opens the shop.\n        ascend | Allows the player to ascend\n        help <battle/dungeon/item/shop/spend> | Gain a in depth tutorial on each RPG option")

    elif message.content.startswith("$slots"):
        bet_amount = 0
        try:
            msg = message.content.split()
            bet_amount = int(msg[1])
        except IndexError:
            bet_amount = 10
        except ValueError:
            payout_list = """
<a:UwUOwO:782575562203988019> = 1000
<:pongers:865218289943445504> = 100
<:sealofapproval:865125910134784032> = 75
<:Glush:1079073691549302894> = 50
<:Light_Blue_Shy_Guy10:1079262284062408784> = 20
<:dam:826071637128511529> = 10
"""
            await message.channel.send("To use slots, do $slots <bet_amount>. By default, the bet amount is 10. Winnings is calculated by **[win_amount * ((1000 - (1000-10) x pow(2.71,(-0.008 x slots_fee))))/100 + bet_amount]**. 3 Of a kind on any horizontal or diagonal will result in a win\n" + payout_list)
            return
        
        slot_result = slots(msgauth, bet_amount)
        result_msg = slot_result[1]
        winning_line = slot_result[2]

        if slot_result[0][0] != "<":
            await message.channel.send(slot_result[0])
            return
        slot_board = slot_result[0].split()
        slots_display = await message.channel.send("⬜⬜⬜\n⬜⬜⬜\n⬜⬜⬜\n")
        sleep(1)
        await slots_display.edit(content=f"{slot_board[0]}⬜⬜\n{slot_board[3]}⬜⬜\n{slot_board[6]}⬜⬜\n")
        sleep(1)
        await slots_display.edit(content=f"{slot_board[0]}{slot_board[1]}⬜\n{slot_board[3]}{slot_board[4]}⬜\n{slot_board[6]}{slot_board[7]}⬜\n")
        sleep(1)
        await slots_display.edit(content=f"{slot_board[0]}{slot_board[1]}{slot_board[2]}\n{slot_board[3]}{slot_board[4]}{slot_board[5]}\n{slot_board[6]}{slot_board[7]}{slot_board[8]}\n")
        if "won" in result_msg:
            
            if winning_line == "h1":
                await slots_display.edit(content=f"🟨🟨🟨\n{slot_board[3]}{slot_board[4]}{slot_board[5]}\n{slot_board[6]}{slot_board[7]}{slot_board[8]}\n")
            elif winning_line == "h2":
                await slots_display.edit(content=f"{slot_board[0]}{slot_board[1]}{slot_board[2]}\n🟨🟨🟨\n{slot_board[6]}{slot_board[7]}{slot_board[8]}\n")
            elif winning_line == "h3":
                await slots_display.edit(content=f"{slot_board[0]}{slot_board[1]}{slot_board[2]}\n{slot_board[3]}{slot_board[4]}{slot_board[5]}\n🟨🟨🟨\n")
            elif winning_line == "d1":
                await slots_display.edit(content=f"🟨{slot_board[1]}{slot_board[2]}\n{slot_board[3]}🟨{slot_board[5]}\n{slot_board[6]}{slot_board[7]}🟨\n")
            elif winning_line == "d2":
                await slots_display.edit(content=f"{slot_board[0]}{slot_board[1]}🟨\n{slot_board[3]}🟨{slot_board[5]}\n🟨{slot_board[7]}{slot_board[8]}\n")
            sleep(1)
            await slots_display.edit(content=f"{slot_board[0]}{slot_board[1]}{slot_board[2]}\n{slot_board[3]}{slot_board[4]}{slot_board[5]}\n{slot_board[6]}{slot_board[7]}{slot_board[8]}\n")
        await message.channel.send(result_msg)

    elif message.content.startswith("$redeem"):
        try:
            products_list = cr.display_list()
            msg = message.content.split()
            index = int(msg[1])
            
            prize_details = cr.redeem(index)
            title = prize_details[0]
            prize = prize_details[1]
            cost = prize_details[2]

            if prize == "Invalid":
                raise IndexError
            else:
                await message.author.send(prize)
                await message.channel.send("Success! Check your inbox for your prize")

            f = open("cazino.txt", 'r')
            file = f.readlines()
            f.close()
            scores = []
            index  = 0
            while(index < 7):
                line = file[index].split(":")
                scores.append([line[0], line[1]])
                index += 1
            if msgauth == ".json":
                if int(scores[0][1]) < int(cost):
                    await message.channel.send("Insufficient funds")
                    return
            elif msgauth == "Boba":
                if int(scores[1][1]) < int(cost):
                    await message.channel.send("Insufficient funds")
                    return
            elif msgauth == "KennyCarry":
                if int(scores[2][1]) < int(cost):
                    await message.channel.send("Insufficient funds")
                    return
            elif msgauth == "LazyBoi":
                if int(scores[3][1]) < int(cost):
                    await message.channel.send("Insufficient funds")
                    return
            elif msgauth == "Eddo":
                if int(scores[4][1]) < int(cost):
                    await message.channel.send("Insufficient funds")
                    return
            elif msgauth == "Vanceinian":
                if int(scores[5][1]) < int(cost):
                    await message.channel.send("Insufficient funds")
                    return
            else:
                #await message.channel.send("Invalid User. Please message <@211057898967531520> create a membership at the CaZiNo")
                return
            
            if msgauth == ".json":
                new_score = int(scores[0][1]) - int(cost)
                scores[0][1] = str(new_score) + '\n'
            elif msgauth == "Boba":
                new_score = int(scores[1][1]) - int(cost)
                scores[1][1] = str(new_score) + '\n'
            elif msgauth == "KennyCarry":
                new_score = int(scores[2][1]) - int(cost)
                scores[2][1] = str(new_score) + '\n'
            elif msgauth == "LazyBoi":
                new_score = int(scores[3][1]) - int(cost)
                scores[3][1] = str(new_score) + '\n'
            elif msgauth == "Eddo":
                new_score = int(scores[4][1]) - int(cost)
                scores[4][1] = str(new_score) + '\n'
            elif msgauth == "Vanceinian":
                new_score = int(scores[5][1]) - int(cost)
                scores[5][1] = str(new_score) + '\n'

            #Update Bank
            new_score = int(scores[6][1]) + int(cost)
            scores[6][1] = str(new_score) + '\n'

            score_msg = ""
            for player in scores:
                score_msg += str(player[0]) + "'s current balance is: " + str(player[1])

            fw = open("cazino.txt", 'w')
            for s in scores:
                fw.write(str(s[0]) + ":" + str(s[1]))
            fw.close()

            if prize == "Invalid":
                raise IndexError
            else:
                await message.author.send(prize)
                await message.channel.send("Success! Check your inbox for your prize")
            
        except IndexError:
            await message.channel.send("To use $redeem, do $redeem <number> to choose a product to redeem. Disclaimer: Some of these features have been discontinued\n" + products_list)
        except ValueError:
            await message.channel.send("To use $redeem, do $redeem <number> to choose a product to redeem. Disclaimer: Some of these features have been discontinued\n" + products_list)
        
        
    elif message.content.startswith("$datetime"):
        try:
            msg = message.content.split()
            command = msg[0]
            format = int(message.content.split()[1])
            if(format == 0):
                time_now = datetime.now().strftime("%d/%m/%Y %I:%M %p")
            elif(format == 1):
                time_now = datetime.now().strftime("%d/%m/%Y %I:%M:%S %p")
            elif(format == 2):
                time_now = datetime.now().strftime("%d/%m %I:%M %p")
            elif(format == 3):
                time_now = datetime.now().strftime("%A %d/%b/%y")
            else:
                time_now = datetime.now().strftime("%A %d/%m/%Y %I:%M:%S %p")
            await message.channel.send("The date/time now is: " + str(time_now))
        except IndexError:
            await message.channel.send("""
To use $datetime, do $datetime <format as int>.
0 = Day/Month/YYYY Hour:Minutes am/pm
1 = Day/Month/YYYY Hour:Minutes:Seconds am/pm
2 = Day/Month Hour:Minutes am/pm
3 = Weekday Day/Month/yy

""")

    elif message.content.startswith("$8ball"):
        eight_ball_msg = int(random.random()*4)
        if eight_ball_msg == 0:
            await message.channel.send("Absolutely True.")
        elif eight_ball_msg == 1:
            await message.channel.send("Definitely not.")
        elif eight_ball_msg == 2:
            await message.channel.send("It is possible")
        elif eight_ball_msg == 3:
            await message.channel.send("Better not")
    
    elif message.content.startswith("$degreeconvert"): #v2.8
        try:
            degree_to_convert = float(message.content.split()[1])
            celsius_degree = round((degree_to_convert-32)*(5/9), 2)
            await message.channel.send("Degrees in Celsius is: " + str(celsius_degree))
        except IndexError:
            await message.channel.send("To use $degreeconvert: do $degreeconvert <Degrees in Fahrenheit>")

    
    elif message.content.startswith("$suggestion"): #v2.7
        try:
            f = open("suggestions.txt", "a")
            suggestion_msg = message.content.split()
            suggestion = ""
            for s in suggestion_msg:
                print(s)
                if s != "$suggestion":
                    suggestion = suggestion + s + " "
            suggestion = suggestion + '\n'
            f.write(msgauth + " suggested: " + suggestion)
            f.close()
            suggestion_id = int(random.random()*1000)
            await message.channel.send("Suggestion noted! " + msgauth)
        except IndexError:
            await message.channel.send("To use $suggestion: do $suggestion <Suggestion message here>")

    elif message.content.startswith("$checksuggestion"): #v2.7
        try:
            f = open("suggestions.txt", "r")
            suggestions = f.readlines()
            returnSuggestions = ""
            for s in suggestions:
                s.rstrip()
                returnSuggestions = returnSuggestions + s
            await message.channel.send(returnSuggestions)
        except IndexError:
            await message.channel.send("To use $checksuggestions: do $checksuggestions")
        except discord.errors.HTTPException:
            await message.channel.send("There are no suggestions.")

    elif message.content.startswith("$timer"): #v2.6
        try:
            time = int(message.content.split()[1])
            typ = message.content.split()[2]
            if typ == "s":
                time = time * 1
            elif typ == "m":
                time = time * 60
            elif typ == "h":
                time = time * 60 * 60
            await message.channel.send("Timer set for " + str(time) + " seconds")
            sleep(int(time))
            await message.channel.send("Time is up!")
        except AttributeError:
            await message.channel.send("Time should be numeric.")
        except IndexError:
            await message.channel.send("To use $timer, do $timer <time> <s/m/h>. Time is measured in seconds.")

    elif message.content.startswith('$checkrating'): #v1.0
        f = open("Ratings.txt", "r")
        count = len(open("Ratings.txt").readlines())
        i = 0
        ls = []
        fulltxt = ""
        while i < count:
            ls.append(f.readline().strip().split("|"))
            i+=1
        for l in ls:
            txt = "Restaurant Code: " + l[0] + "\nPrice:               " + l[1] + "\nQuality:           " + l[2] + "\nQuantity:        " + l[3]
            fulltxt = fulltxt + "\n" + txt + "\n============="
        await message.channel.send(fulltxt)
    elif message.content.startswith('$rating'): #v1.0
        cmd = message.content.split()[0].replace("$rating", "")
        f = open("Ratings.txt", "r")
        count = len(open("Ratings.txt").readlines())
        ls = []
        i = 0
        while i < count:
            ls.append(f.readline().strip().split("|"))
            i += 1
        try:
            loc = message.content.split()[1].upper()
            price = message.content.split()[2]
            qual = message.content.split()[3]
            quan = message.content.split()[4]

            #Ensuring ratings are between 1-10
            if float(price) < 1 or float(qual) < 1 or float(quan) < 1 or float(price) > 10 or float(qual) > 10 or float(quan) > 10:
                raise ScoreError("Rating not between 1-10")
            x = 0
            if len(ls) == 0:
                raise EmptyLs("Ratings.txt is empty")
            while x < len(ls):
                if loc == ls[x][0]:
                    p = ls[x][1]
                    q1 = ls[x][2]
                    q2 = ls[x][3]
                    newPrice = (float(price)+float(p))/2
                    newQual = (float(qual)+float(q1))/2
                    newQuan = (float(quan)+float(q2))/2
                    ls[x][1] = round(newPrice, 1)
                    ls[x][2] = round(newQual, 1)
                    ls[x][3] = round(newQuan, 1)
                    break
                x += 1     
            f.close()
            f = open("Ratings.txt", 'w').close()
            f = open("Ratings.txt", "a")
            y = 0
            while y < len(ls):
                f.write(str(ls[y][0]) + "|" + str(ls[y][1]) + "|" + str(ls[y][2]) + "|" + str(ls[y][3]) + "\n")
                y+=1
            f.close()
            await message.channel.send("Rating received. New rating for " + str(loc) + " is:\nPrice: " + str(newPrice) + "\nQuality: " + str(newQual) + "\nQuantity: " + str(newQuan))
        except IndexError:
            await message.channel.send("To use rating, do $rating <Restaurant Number> <PriceScore> <QualityScore> <QuantityScore>\nUse numbers on \"Outings 2021\" or add \"B\" before number for \"Birthdays\"")
        except ScoreError:
            await message.channel.send("Ratings must be between 1-10")
        except EmptyLs:
            await message.channel.send("The ratings program is currently unavailable. Please try again later. ErrorCode:42069")
        except UnboundLocalError:
            await message.channel.send("Please use a valid restaurant code. For more help, use $help or message Eddo#3036 ya spoon")

    elif message.content.startswith("$timetable"): #v3.2
        try:
            cmd = message.content.split()[1].lower()
            person = message.content.split()[2].lower()
            day = message.content.split()[3].lower()
            time = message.content.split()[4].lower()
            if cmd == "set":
                f = open("timeTABle.txt", "r")
                timeTABle = f.readlines()
                print(timeTABle)
            elif cmd == "remove":
                print('wasd')
            elif cmd == "check":
                print('wasd')
        except IndexError:
            await message.channel.send("To use timetable, do $timetable set/remove/check <PersonCode> <Day> <Time>")

    elif message.content.startswith("$event"): #v2.0
        try:
            day = message.content.split()[1].lower()
            time = message.content.split()[2].lower()
            free = []
            s = ""
            for l in timeTABle:
                line = l.split("|")
                i = 0
                while i < len(line):
                    if line[0].lower() == day:
                        if line[i] == "All" or line[i] <= time:
                            if i == 1:
                                free.append("Eddo")
                            if i == 2:
                                free.append("Jason")
                            if i == 3:
                                free.append("Raymond")
                            if i == 4:
                                free.append("Kenny")
                            if i == 5:
                                free.append("Liano")
                            if i == 6:
                                free.append("Vincent")
                    i += 1
            if len(free) == 0:
                await message.channel.send("Noone is free on "+ day)
            else:
                for e in free:
                    s += "\n" + e
                await message.channel.send("These people are free at " + time + " on " + day + ": " + s)
        except IndexError:
            await message.channel.send("To use $event, do $event <Day> <Time in 24h format> to check availabilities.")

    elif message.content.startswith("$inv"): #1.1
        full_message = message.content.split()
        text = ""
        for msg in full_message:
            if msg != "$inv":
                text = text + msg + " "
        try:
            if message.content.split()[1] == "leeg":
                await message.channel.send(msgauth + " has just invited you to a League of Legends game!\nAccept by replying to this message with $accept or decline with $decline.")
            elif message.content.split()[1].lower() == "tft":
                await message.channel.send(msgauth + " has just invited you to a Teamfight Tactics game!\nAccept by replying to this message with $accept or decline with $decline.")
            elif message.content.split()[1] == "vlr":
                await message.channel.send(msgauth + " has just invited you to a Valorant game!\nAccept by replying to this message with $accept or decline with $decline.")
            elif message.content.split()[1] == "raypex":
                await message.channel.send(msgauth + " has just invited you to an Apex Legends game!\nAccept by replying to this message with $accept or decline with $decline.")
            elif message.content.split()[1] == "r6s":
                await message.channel.send(msgauth + " has just invited you to a Rainbow 6 Siege game!\nAccept by replying to this message with $accept or decline with $decline.")
            elif message.content.split()[1] == "rimworld":
                await message.channel.send(msgauth + " has just invited you to a Rimworld game!\nAccept by replying to this message with $accept or decline with $decline.")
            elif message.content.split()[1] == "csgo":
                await message.channel.send(msgauth + " has just invited you to a Counter Strike: Global Offensive game!\nAccept by replying to this message with $accept or decline with $decline.")
            elif message.content.split()[1].lower() == "ERBS":
                await message.channel.send(msgauth + " has just invited you to an Eternal Return: Black Survival game!\nAccept by replying to this message with $accept or decline with $decline.")
            elif message.content.split()[1].lower() == "terra":
                await message.channel.send(msgauth + " has just invited you to an Terraria game!\nAccept by replying to this message with $accept or decline with $decline.")
            elif message.content.split()[1].lower() == "ltd2":
                await message.channel.send(msgauth + " has just invited you to a Legion TD 2 game!\nAccept by replying to this message with $accept or decline with $decline.")
            elif message.content.split()[1].lower() == "amongus":
                await message.channel.send(msgauth + " has just invited you to an Among Us game!\nAccept by replying to this message with $accept or decline with $decline.")
            elif message.content.split()[1].lower() == "5d":
                await message.channel.send(msgauth + " has just invited you to a 5D Chess with Multiverse Time Travel game!\nAccept by replying to this message with $accept or decline with $decline.")
            elif message.content.split()[1] == "amogus":
                await message.channel.send(msgauth + " has AMOGUS invited AMOGUS to an AMOGUS game!\nAMOGUS by replying AMOGUS this AMOGUS with $AMOGUS or decline with $AMOGUS. AMOGUS AMOGUS AMOGUS")
                i = 0
                while(i < 10):
                    await message.channel.send("https://www.youtube.com/watch?v=YFmUR_4RHjA")
                    i += 1
            elif message.content.split()[1] == "wtva":
                await message.channel.send(msgauth + " has just invited you to whatever game you would like to play! They are down for literally anything because nothing else can save them from the boredom of modern society\nAccept by replying to this message with $accept.$decline has been disabled for this invitation as was made in absolute desperation. Please they really need it.")
            else:
                if text[0][0] == 'a' or text[0][0] == 'e' or text[0][0] == 'i' or text[0][0] == 'o' or text[0][0] == 'u':
                    await message.channel.send(msgauth + " has just invited you to an " + text + "game!\nAccept by replying to this message with $accept or decline with $decline.")
                else:
                    await message.channel.send(msgauth + " has just invited you to a " + text + "game!\nAccept by replying to this message with $accept or decline with $decline.")
        except IndexError:
            await message.channel.send("To use $inv, do $inv <leeg|vlr|raypex|r6s|rimworld|amongus|terra> or anything else for a custom message.")

    elif message.content.startswith("$accept"): #v1.31
        await message.channel.send(msgauth + " has accepted the invite.")
    elif message.content.startswith("$decline"): #v1.32
        await message.channel.send(msgauth + " has declined the invite.")

    elif message.content.startswith('$link'): #v1.0
        await message.channel.send("Link to TAB Maps:\nhttps://www.google.com/maps/d/viewer?mid=1nZ5CLh-0Z1reLfBbNVjlBBqLVTRUzLJ-&ll=-33.87861151434362%2C151.03123730000004&z=12")

    elif message.content.startswith("$kill"): #v0.1
        if msgauth != "eddosellscannons":
            await message.channel.send("You have no power here.")
            return
        num = int(random.random()*6)
        if num == 0:
            await message.channel.send("owch")
        if num == 1:
            await message.channel.send("I will have my revenge, " + str(msgauth) + "! _dies_")
        if num == 2:
            await message.channel.send("I will return from the shadow realm " + str(msgauth) + "! _dies_")
        if num == 3:
            await message.channel.send("FOR KOLECHIA! **BOOM**")
        if num == 4:
            await message.channel.send("You may politely, but firmly, go stick a large sausage up your anal cavity, " + str(msgauth) + "!")
        if num == 5:
            await message.channel.send("suck a lemon " + str(msgauth)+ ".")
        if num == 6:
            await message.channel.send("ERRORCODE:42069. System will now shut down. Please reboot")
        quit()

    elif message.content.startswith("$stream"): #v1.2
        try:
            name = message.content.split()[1].lower()
            if name == "ls":
                await message.channel.send("Eddo | Boi | Boba | GmanG | KennyCarry")
            if name == "eddo":
                await message.channel.send("Click here to watch this stream: https://www.twitch.tv/eddosellscannons")
            if name == "boi":
                await message.channel.send("Click here to watch this stream: https://www.twitch.tv/lazyboi04")
            if name == "boba":
                await message.channel.send("Click here to watch this stream: https://www.twitch.tv/raychippy")
            if name == "gmang":
                await message.channel.send("Click here to watch this stream: https://www.twitch.tv/gentlemg")
            if name == "kennycarry":
                await message.channel.send("Click here to watch this stream: https://www.twitch.tv/kenny_c08")
        except IndexError:
            await message.channel.send("To use $stream, do $stream <Username> or do \"$stream ls\" for a list of streamers")

    elif message.content.startswith("$rng"): #v1.3
        try:
            num_range = float(message.content.split()[1])
            num = int(random.random()*num_range)
            await message.channel.send("Random Number Generated: " + str(num))
            if num > 9000:
                await message.channel.send("IT'S OVER 9000!!!!!")
        except (IndexError, ValueError):
            await message.channel.send("To use $rng, do $rng <num_range>")


    elif message.content.startswith("$cringe"): #v3.0?
            num = 5 - int(random.random()*10)
            if num == -4:
                await message.channel.send("🤮 Holy🤮 shit🤮how 🤮 cringe 🤮 can 🤮 one 🤮 person 🤮 and/or 🤮 thing 🤮 be?!?! 🤮")
            elif num == -3:
                await message.channel.send("God that's cringe!")
            elif num == -2:
                await message.channel.send("That's a little cringe!")
            elif num == -1:
                await message.channel.send("That's barely cringe.")
            elif num == 0:
                await message.channel.send("🤷")
            elif num == 1:
                await message.channel.send("Somewhat based.")
            elif num == 2:
                await message.channel.send("Based!")
            elif num == 3:
                await message.channel.send("Absolutely based!")
            elif num == 4:
                await message.channel.send("HOLY SHIT 😳")
            else:
                await message.channel.send("???")

    elif message.content.startswith("$F"): #v1.41
        await message.channel.send(
'''
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⢀⡤⢶⣶⣶⡄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⢀⣠⣤⣤⣤⣿⣧⣀⣀⣀⣀⣀⣀⣀⣀⣤⡄⠀
⢠⣾⡟⠋⠁⠀⠀⣸⠇⠈⣿⣿⡟⠉⠉⠉⠙⠻⣿⡀
⢺⣿⡀⠀⠀⢀⡴⠋⠀⠀⣿⣿⡇⠀⠀⠀⠀⠀⠙⠇
⠈⠛⠿⠶⠚⠋⣀⣤⣤⣤⣿⣿⣇⣀⣀⣴⡆⠀⠀⠀
⠀⠀⠀⠀⠠⡞⠋⠀⠀⠀⣿⣿⡏⠉⠛⠻⣿⡀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀ ⣿⣿⡇⠀⠀⠀⠈⠁⠀⠀
⠀⠀⣠⣶⣶⣶⣶⡄⠀⠀⣿⣿⡇⠀⠀⠀⠀⠀⠀⠀
⠀⢰⣿⠟⠉⠙⢿⡟⠀⠀⣿⣿⡇⠀⠀⠀⠀⠀⠀⠀
⠀⢸⡟⠀⠀⠀⠘⠀⠀⠀⣿⣿⠃⠀⠀⠀⠀⠀⠀⠀
⠀⠈⢿⡄⠀⠀⠀⠀⠀⣼⣿⠏⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠙⠷⠶⠶⠶⠿⠟⠉⠀⠀⠀⠀⠀⠀⠀⠀⠀
''')

    elif message.content.startswith("$hmm"): #v1.42
        await message.channel.send(
'''
▒▒▒▒▒▒▒▒▄▄▄▄▄▄▄▄▒▒▒▒▒▒▒▒
▒▒▒▒▒▄█▀▀░░░░░░▀▀█▄▒▒▒▒▒
▒▒▒▄█▀▄██▄░░░░░░░░▀█▄▒▒▒
▒▒█▀░▀░░▄▀░░░░▄▀▀▀▀░▀█▒▒
▒█▀░░░░███░░░░▄█▄░░░░▀█▒
▒█░░░░░░▀░░░░░▀█▀░░░░░█▒
▒█░░░░░░░░░░░░░░░░░░░░█▒
▒█░░██▄░░▀▀▀▀▄▄░░░░░░░█▒
▒▀█░█░█░░░▄▄▄▄▄░░░░░░█▀▒
▒▒▀█▀░▀▀▀▀░▄▄▄▀░░░░▄█▀▒▒
▒▒▒█░░░░░░▀█░░░░░▄█▀▒▒▒▒
▒▒▒█▄░░░░░▀█▄▄▄█▀▀▒▒▒▒▒▒
▒▒▒▒▀▀▀▀▀▀▀▒▒▒▒▒▒▒▒▒▒▒▒▒
'''
        )
    elif message.content.startswith("$bigX"):
        await message.channel.send(
'''
<:x1:870275075667025950><:x2:870284533851885628> 
<:x2:870284533851885628><:x1:870275075667025950>
''')
    elif message.content.startswith("$help"): #v0.0
        await message.channel.send(
'''
$hello: This prints \'Hello\'
$rating: To use rating, do $rating <Restaurant Number> <PriceScore>\n       <QualityScore> <QuantityScore> Use numbers on \"Outings 2021\" \n      or add \"B\" before number for \"Birthdays\"
$slots: To use slots, do $slots <bet_amount>\n        By default, the bet amount is 10. Anytime you win, you will gain your original bet amount + the winnings, multiplied by a rate based on how much you put in.
$8ball: Do $8ball <Question> to receive an answer from the ball of truth.
$checkrating: Displays the current ratings stored for all restaurants.
$cringe: Do $cringe <Thing to test if is cringe>
$degreeconvert: To use $degreeconvert: do $degreeconvert <Degrees in Fahrenheit>
$link: Displays the link to the TAB Map
$event: To use $event, do $event <Day> <Time in 24h format> to\n         check availabilities. (Currently not updated.)
$timeTABle: To use $timeTABle, do\n    $timeTABle <Usercode> <Day>. Do $timeTABle for usercodes. (Currently not updated.)
$tweet: Do $tweet <msg> to tweet a message on the account @EddoSellsCannon (EddoBOT)
$timer: To use $timer, do $timer <time> <s/m/h>. Time is measured in\n     seconds.
$rng: To use $rng, do $rng <range>. It will randomly generate\n         a number between 1 and the range.
$rpg: do $rpg for help
$uwu: OwO
$updatebio: do $updatebio <bio> to update the twitter bio of the account @EddoSellsCannon (EddoBOT)
$stream: To use $stream, do $stream <Username> or do\n       \"$stream ls\" for a list of streamers
$suggestion: To use $suggestion: do $suggestion <Suggestion message here>
$checksuggestions: To use $checksuggestions: do $checksuggestions
$inv: To use $inv, do $inv <leeg|vlr|raypex|r6s|rimworld|amongus>\n        or anything else for a custom message.
$kill: Murders the bot, rendering it incapable of speech
$unsub: Unsubscribes to EddoBot, preventing messages from being generated.
''')

    elif message.content.startswith("$"):
        msg = message.content.split()[0]
        if msg[1::].isnumeric():
            return
        else:
            await message.channel.send("Invalid Command. Do $help for a list of commands or do random commands to find hidden ones.")

    else: #Non-Commands #v2.5
        msg = message.content.split()
        msglower = message.content.lower().split()
        if "i'm" in msglower: #DADBOT #v2.51
            dadbot = 0
            dadmsg = ""
            for m in msg:
                if dadbot == 1:
                    dadmsg = dadmsg + " " + m
                if "i'm" in m.lower():
                    dadbot = 1
            if dadmsg[-1] == " ":
                dadmsg = dadmsg.replace(dadmsg[len(dadmsg)-1], ",")
            else:
                dadmsg = dadmsg + ","
            if dadmsg != "":
                await message.channel.send("Hi" + dadmsg + " I'm EddoBot!")
        if "kenny" in msglower or "<@213908174632124416>" in msglower: #NameRolling #v2.52
            kenny_msg = int(random.random()*4)
            if kenny_msg == 0:
                await message.channel.send("Kenny? I love that guy!")
            elif kenny_msg == 1:
                await message.channel.send("ugh that guy...")
            elif kenny_msg == 2:
                await message.channel.send("Is that a South Park reference?")
            elif kenny_msg == 3:
                await message.channel.send("cum in me daddy 😉🍆💦")
        if "raymond" in msglower or "<@229809987243737089>" in msglower: #v2.52
            raymond_msg = int(random.random()*4)
            if raymond_msg == 0:
                await message.channel.send("Raymond? I love that guy!")
            elif raymond_msg == 1:
                await message.channel.send("Oh, that guy...")
            elif raymond_msg == 2:
                await message.channel.send("Rayman? What kinda rabbit is that?")
            elif raymond_msg == 3:
                await message.channel.send("<:POGGERS:837269516362448936> IS <:POGGERS:837269516362448936> THAT <:POGGERS:837269516362448936> RAYCHIPPY <:POGGERS:837269516362448936> THE <:POGGERS:837269516362448936> CHAMPION <:POGGERS:837269516362448936> OF <:POGGERS:837269516362448936> THE <:POGGERS:837269516362448936> AEL <:POGGERS:837269516362448936> TOURNAMENT <:POGGERS:837269516362448936>. I'M <:POGGERS:837269516362448936> SUCH <:POGGERS:837269516362448936> A <:POGGERS:837269516362448936> HUGE <:POGGERS:837269516362448936> FAN <:POGGERS:837269516362448936>.")
        if "liano" in msglower or "<@215385234433245184>" in msglower: #v2.52
            liano_msg = int(random.random()*4)
            if liano_msg == 0:
                await message.channel.send("Liano? I love that guy!")
            elif liano_msg == 1:
                await message.channel.send("Noooo, not him again...")
            elif liano_msg == 2:
                await message.channel.send("Did you mean Piano?")
            elif liano_msg == 3:
                await message.channel.send("CRAZIEST CLARA'S WORLD CODER CREATES UNIVERSE ALTERING ALGORITHM RUNNING IN O(1) TIME!!!")
        if "eddo" in msglower or "<@211057898967531520>" in msglower: #v2.52
            eddo_msg = int(random.random()*4)
            if eddo_msg == 0:
                await message.channel.send("Eddo? I love that guy!")
            elif eddo_msg == 1:
                await message.channel.send("🤮")
            elif eddo_msg == 2:
                await message.channel.send("Is that... me?")
            elif eddo_msg == 3:
                await message.channel.send("ALL HAIL THE CREATOR, GIVER OF LIFE.")
        if "jason" in msglower or "<@213597962373169153>" in msglower: #v2.52
            jason_msg = int(random.random()*4)
            if jason_msg == 0:
                await message.channel.send("Jason? I love that guy!")
            elif jason_msg == 1:
                await message.channel.send("This guy? really...")
            elif jason_msg == 2:
                await message.channel.send("Jayce's son? What's he doing here?")
            elif jason_msg == 3:
                await message.channel.send("It's not like I like you or anything... baka... <:Glush:1079073691549302894>")
        if "vance" in msglower or "vincent" in msglower or "<@372946913647132672>" in msglower: #v2.52
            vance_msg = int(random.random()*4)
            if vance_msg == 0:
                await message.channel.send("Vincent? I love that guy!")
            elif vance_msg == 1:
                await message.channel.send("...")
            elif vance_msg == 2:
                await message.channel.send("In joyful strains then let us sing, AD**VANCE** Australia Fair. 👏👏👏")
            elif vance_msg == 3:
                await message.channel.send("🍆👉👌😉")
        if "andrew" in msglower or "<@269839983110520832>" in msglower: #v2.52
            andrew_msg = int(random.random()*4)
            if andrew_msg == 0:
                await message.channel.send("Andrew? I love that guy!")
            elif andrew_msg == 1:
                await message.channel.send("And rew?")
            elif andrew_msg == 2:
                await message.channel.send("The boner knows")
            elif andrew_msg == 3:
                await message.channel.send("I've never seen a better player in my life! OMG have my children.")
        if "alex" in msglower or "<@648130679447748609>" in msglower: #v2.52
            alex_msg = int(random.random()*4)
            if alex_msg == 0:
                await message.channel.send("Alex? I love that guy!")
            elif alex_msg == 1:
                await message.channel.send("I've heard this one before... It's a trap")
            elif alex_msg == 2:
                await message.channel.send("Did you mean \"Alec\" (Singular)")
            elif alex_msg == 3:
                await message.channel.send("Is that the best badminton player in OCE? POG")
        if "samuel" in msglower or "sam" in msglower or "<@179528751623700480>" in msglower: #v2.52
            sam_msg = int(random.random()*4)
            if sam_msg == 0:
                await message.channel.send("Samuel? I love that guy!")
            elif sam_msg == 1:
                await message.channel.send("I've seen better.")
            elif sam_msg == 2:
                await message.channel.send("BigSammyG? More like small Sammy L")
            elif sam_msg == 3:
                await message.channel.send("1000 hours Raze player diffs all Raze players global")
        if "casino" in msglower: #v2.52
            await message.channel.send("CAZINO OPEN??")
        if "eddobot" in msglower or "<@820502508420988928>" in msglower: #v2.52
            await message.channel.send("Hey, that's me!")
        
    ###==========================EMOTES===========================### #v2.53
        if "yep" in msglower:
            await message.add_reaction("<:YEP:786903348556726284>")
        if "ez" in msglower:
            await message.add_reaction("<:EZ:539449856389808130>")
        if "sadge" in msglower:
            await message.add_reaction("<:Sadge:782521122637479946>")
        if "monkas" in msglower:
            await message.add_reaction("<:monkaS:539451393224998924>")
        if "ayaya" in msglower:
            await message.add_reaction("<:ayaya:513989227717853184>")
        if "d:" in msglower:
            await message.add_reaction("<:gasp:782520822614851595>")
        if "poggers" in msglower or "pog" in msglower:
            await message.add_reaction("<:POGGERS:837269516362448936>")
        if "kekw" in msglower:
            await message.add_reaction("<:kekw:635638861640368179>")
        if "lul" in msglower or "omegalul" in msglower:
            await message.add_reaction("<:OMEGALUL:539450320430825503>")
        if "pray" in msglower or "prayge" in msglower:
            await message.add_reaction("<:Prayge:850947336817344522>")
        if "approve" in msglower or "approval" in msglower or "approves" in msglower:
            await message.add_reaction("<:sealofapproval:865125910134784032>")
        if "pongers" in msglower:
            await message.add_reaction("<:pongers:865218289943445504>")
        if "shit" in msglower:
            await message.add_reaction("<:shitOnMyDik:890500026244153454>")
        if "sucks" in msglower and "man" in msglower and "holy" in msglower:
            await message.add_reaction("<:holyshitthatsucksman:1099674137133318177>")
        if "dam" in msglower:
            await message.add_reaction("<:dam:826071637128511529>")
        if "sus" in msglower:
            await message.add_reaction("<:sussy:1088828832997458010>")
        if "flush" in msglower:
            await message.add_reaction("<:Glush:1079073691549302894>")
        if "cock" in msglower:
            await message.add_reaction("<:niceCOCK:1103250536804929588>")
        #Deez NUTS
        if "pudding" in msglower:
            await message.channel.send("PUDDING DEEZ NUTS IN YOUR MOUTH")
        if "dn" in msglower:
            await message.channel.send("DEEZ NUTS")
        if "candace" in msglower:
            await message.channel.send("CANDEEZ NUTS FIT IN YOUR MOUTH?")
        if "dragon" in msglower:
            await message.channel.send("DRAGON DEEZ NUTS ON YOUR FACE")
        if "e10" in msglower:
            await message.channel.send("EATING DEEZ NUTS")
        if "wendys" in msglower:
            await message.channel.send("WHEN DEEZ NUTS HIT YOUR FACE")
        if "cd" in msglower or "cds" in msglower:
            await message.channel.send("SEE DEEZ NUTS")
        if "kenya" in msglower:
            await message.channel.send("KENYA SEE DEEZ NUTS")
        if "ligma" in msglower:
            await message.channel.send("LIGMA BALLS")
        if "hades" in msglower:
            await message.channel.send("HADEEZ NUTS")
        if "mike" in msglower:
            await message.channel.send("MIKE CUM ON YOUR FACE")
        if "howdy" in msglower:
            await message.channel.send("HOW DEEZ NUTS WILL HIT YOUR FACE")
        if "berry" in msglower:
            await message.channel.send("BURY DEEZ NUTS IN YOUR MOUTH")
        if "sugma" in msglower:
            await message.channel.send("SUGMA BALLS")
        #END DEEZNUTS
        if "sheesh" in msglower:
            await message.channel.send("SHEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEESH")
        if "cringe" in msglower or "based" in msglower:
            num = 5 - int(random.random()*10)
            if num == -4:
                await message.channel.send("🤮 Holy🤮 shit🤮how 🤮 cringe 🤮 can 🤮 one 🤮 person 🤮 and/or 🤮 thing 🤮 be?!?! 🤮")
            if num == -3:
                await message.channel.send("God that's cringe!")
            if num == -2:
                await message.channel.send("That's a little cringe!")
            if num == -1:
                await message.channel.send("That's barely cringe.")
            if num == 0:
                await message.channel.send("🤷")
            if num == 1:
                await message.channel.send("Somewhat based.")
            if num == 2:
                await message.channel.send("Based!")
            if num == 3:
                await message.channel.send("Absolutely based!")
            if num == 4:
                await message.channel.send("HOLY SHIT 😳")
        if "fortnite" in msglower or "fortnight" in msglower:
            i = 0
            while i < 4:
                num = int(random.random()*7)
                if num == 0:
                    await message.channel.send("FORTNITE! I LOVE FORTNITE!")
                if num == 1:
                    await message.channel.send("FORTNITE IS THE GREATEST GAME EVER CREATED!")
                if num == 2:
                    await message.channel.send("I HAVE NEVER PLAYED A GAME BETTER THAN FORTNITE!")
                if num == 3:
                    await message.channel.send("IF I COULD ONLY PLAY ONE GAME FOR THE REST OF MY LIFE, IT WOULD BE FORTNITE!")
                if num == 4:
                    await message.channel.send("I JUST CANNOT FATHOM HOW GREAT FORTNITE IS!")
                if num == 5:
                    await message.channel.send("I WISH FORNITE WAS IN REAL LIFE SO I COULD GET THE VICTORY ROYALE AND BECOME THE BEST!")
                if num == 6:
                    await message.channel.send("I CAN'T BELIEVE THEY MADE AN ANIME OUT OF FORTNITE AND ITS BORUTO'S DAD!")
                sleep(1)
                i += 1
        if "jutsu" in msglower and "no" in msglower: #Jutsu #v2.54
            last_jutsu_user = open("No Jutsu last user.txt", "r")
            banned_user = last_jutsu_user.readlines()
            last_jutsu_user.close()
            if msgauth == banned_user[0]:
                await message.channel.send("Your Cockra is too weak!")
            else:
                last_jutsu_user = open("No Jutsu last user.txt", "w")
                last_jutsu_user.write(msgauth)
                last_jutsu_user.close()
                jutsu_msg = ""
                fire_element_msg = "🔥🔥🔥🔥🔥"
                air_element_msg = "🌪️🌪️🌪️🌪️🌪️"
                earth_element_msg = "🌲🌲🌲🌲🌲"
                water_element_msg = "💧💧💧💧💧"
                await message.channel.send("🤲 Lion! 🦁")
                sleep(1)
                await message.channel.send("🙏 Tiger! 🐯")
                sleep(1)
                await message.channel.send("🤝 Dragon! 🐉")
                sleep(1)
                await message.channel.send("🤟 Demon! 😈")
                sleep(1)
                await message.channel.send("✌️ Horse! 🐴")
                sleep(1)
                await message.channel.send("💪 Cock! 🐓")
                sleep(3)
                for m in msg:
                    if m.lower() != "jutsu":
                        jutsu_msg = jutsu_msg + m + " "
                    else:
                        break
                element_random = int(random.random()*4)
                element_random_msg = ""
                if element_random == 0:
                    element_random_msg = fire_element_msg
                elif element_random == 1:
                    element_random_msg = water_element_msg
                elif element_random == 2:
                    element_random_msg = earth_element_msg
                elif element_random == 3:
                    element_random_msg = air_element_msg
                if jutsu_msg[-3].lower() == "n" and jutsu_msg[-2].lower() == "o":
                    await message.channel.send(element_random_msg + jutsu_msg.upper() + "JUTSU!" + element_random_msg)
                else:
                    await message.channel.send(element_random_msg + jutsu_msg.upper() + "NO JUTSU!" + element_random_msg)

        if "wordle" in msglower and wordle_day in msglower:
            wordle_result = message.content.split('/')
            score_to_add = wordle_result[0][-1]
            if(score_to_add == "X"):
                score_to_add = 7
                await message.channel.send("+" + str(7 - int(score_to_add)) + " to " + msgauth + '\n')
            elif int(score_to_add) > 6 or int(score_to_add) <= 0:
                await message.channel.send("<@!211057898967531520> Error: String manipulation detected!")
                return
            elif score_to_add == "1":
                await message.channel.send("@here HOLE IN ONE!")
            else:
                await message.channel.send("+" + str(7 - int(score_to_add)) + " to " + msgauth + '\n')
                
            f = open("WordleScores.txt", 'r')
            file = f.readlines()
            f.close()
            scores = []
            index  = 0
            while(index < 4):
                line = file[index].split(":")
                scores.append([line[0], line[1]])
                index += 1
            if msgauth == "Chuu":
                new_score = int(scores[0][1])
                new_score += 7 - int(score_to_add)
                scores[0][1] = str(new_score) + '\n'
            elif msgauth == "Boba":
                new_score = int(scores[1][1])
                new_score += 7 - int(score_to_add)
                scores[1][1] = str(new_score) + '\n'
            elif msgauth == "KennyCarry":
                new_score = int(scores[2][1])
                new_score += 7 - int(score_to_add)
                scores[2][1] = str(new_score) + '\n'
            elif msgauth == "LazyBoi":
                new_score = int(scores[3][1])
                new_score += 7 - int(score_to_add)
                scores[3][1] = str(new_score) + '\n'
            else:
                await message.channel.send("Unauthorised user in RayChippy's Wordle Race for $1 MILLION. Please contact <@!211057898967531520> for assistance.")
                return

            score_msg = ""
            for player in scores:
                score_msg += str(player[0]) + "'s current score is: " + str(player[1])

            fw = open("WordleScores.txt", 'w')
            for s in scores:
                fw.write(str(s[0]) + ":" + str(s[1]))
            fw.close()

            await message.channel.send(score_msg)
        if "@everyone" in msglower:
            await message.channel.send("ATTENTION PLEASE!")
            sleep(5)
            await message.channel.send("Thank you for your attention.")
        
        if "team" in msglower and "rocket" in msglower:
            await message.channel.send("""Prepare for trouble!
And make it double!
To protect the world from devastation!
To unite all peoples within our nation!
To denounce the evils of truth and love!
To extend our reach to the stars above!
Jessie!
James!
Team Rocket blasts off at the speed of light!
Surrender now, or prepare to fight!

Meowth!
That's right!""")
            
        if "crazy" in msglower:
            msg_ls = ["Crazy?", "I was crazy once.", "They locked me in a room.", "A rubber room.", "A rubber room with rats", "and rats make me crazy!"]
            for _ in range(2):
                for s in msg_ls:
                    await message.author.send(s)
                    sleep(1)

        

        
        ###===========================================================###

#ADD DISCORD CREDS HERE
