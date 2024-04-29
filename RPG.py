from time import sleep
import random
import re

XP_TO_LEVEL_UP = 10 #Level * Amount = XP needed level up
SP_GAINED_PER_LEVEL = 3
HP_GAINED_PER_LEVEL = 2
RANGED_CRIT_MULTIPLIER = 3
MELEE_CRIT_MULTIPLIER = 2
LUCK_CAP = 80 #Cap luck rolls to 80%
BASE_LUCK = 10 #Lowest amount of luck for dodging/critting
DUPE_ROLL_ODDS = 400 #Rolls out of this number to determine whether enemy drops the same item
MOB_CARRIES_ITEM_ODDS = 400 #Rolls out of this number to determine if enemy goes into battle with item (out of 1000)
ITEM_DROP_CHANCE = 80 #This - enemy level = chance of dropping any item (inverse)
SHOP_SIZE = 5 #How many items in a shop
REROLL_SHOP_COST = 5 #How much it costs to reroll the shop
HP_DISPLAY_LIMIT = 100
ITEM_BREAK_CHANCE = 500
FLOORS_LOST_ON_DEATH = 5
BOSS_CARRIES_ITEM = 800 #Out of 1000
ASCENSION_STAT_KEPT = 4 #Divide cur stat by this (floored)
ASCENSION_LEVEL = 100
ITEM_BONUS_LOST_ON_DEATH = 10

ATK_UPGRADE = 1
DEF_UPGRADE = 1
LCK_UPGRADE = 1
AGL_UPGRADE = 2

#[Name|img|maxhp|atk|df|lck|agl|sp|lvl|xp|gold|floor|equipped|offhand] 
# #Make sure DEF and AGL arent too high, otherwise it creates infinite battles
boss_list = [["Bunny of Death", "bunny", "40", "16", "30", "20", "20", "-1", "25", "0", "0", "0"], 
            ["Seal of Approval", "sealofapproval", "10", "10", "10", "10", "10","-1", "10", "0", "0", "0"],
            ["PONGERS!", "pongers", "25", "15", "15", "15", "15","-1", "15", "0", "0", "0"],
            ["HIM!", "him", "120", "40", "20", "60", "80","-1", "50", "0", "0", "0"],
            ["HER!", "her", "500", "50", "80", "50", "40", "-1", "130", "0", "0", "0"],
            ["Spongebob", "sponge", "5000", "20", "0", "0", "0", "-1", "200", "0", "0", "0"],
            ["Possessed Bocchi", "Bocchi", "347", "100", "106", "116", "151","39", "113", "658", "2911", "2"],
            ["KennyCarry","KennyCarry", "160", "30", "50", "30","20", "0","30", "4", "407", "10"]
            ]

mob_list = [["Slime", "slime", 5, 1, 0, 0, 0, -1, 1, 0, 0, 0],
            ["Goblin", "", 30, 10, 10, 10, 10, -1, 10, 0, 0, 0],
            ["Orc", "", 50, 20, 20, 20, 20, -1, 20, 0, 0, 0],
            ["Skeleton", "", 70, 30, 30, 30, 30, -1, 30, 0, 0, 0, "Bow", ""],
            ["Zombie", "", 90, 40, 40, 40, 40, -1, 40, 0, 0, 0],
            ["Vampire", "", 110, 50, 50, 50, 50, -1, 50, 0, 0, 0],
            ["Werewolf", "", 130, 60, 60, 60, 60, -1, 60, 0, 0, 0],
            ["Demon", "", 150, 70, 70, 70, 70, -1, 70, 0, 0, 0],
            ["Dragon", "", 180, 80, 80, 80, 80, -1, 80, 0, 0, 0],
            ["Death Knight", "", 210, 90, 90, 90, 90, -1, 90, 0, 0, 0, "Rapier+1", ""],
            ["Dark Lord", "", 300, 150, 150, 150, 150, -1, 100, 0, 0, 0, "Needlessly Large Rod", ""],
            ["Ancient Dragons", "", 350, 200, 200, 200, 200, -1, 110, 0, 0, 0],
            ["Demon Lord", "", 400, 220, 220, 220, 220, -1, 120, 0, 0, 0],
            ["Behemoth", "", 450, 130, 240, 240, 240, -1, 130, 0, 0, 0],
            ["Eldritch Abomination", "", 500, 260, 260, 260, 260, -1, 140, 0, 0, 0],
            ["Celestial Being", "", 550, 280, 280, 280, 280, -1, 150, 0, 0, 0],
            ["Titan", "", 600, 300, 300, 300, 300, -1, 160, 0, 0, 0],
            ["Necromancer", "", 650, 320, 320, 320, 320, -1, 170, 0, 0, 0],
            ["Archdevil", "", 700, 340, 340, 340, 340, -1, 180, 0, 0, 0],
            ["Lich", "", 750, 360, 360, 360, 360, -1, 190, 0, 0, 0],
            ["Great Old One", "", 800, 450, 450, 450, 450, -1, 200, 0, 0, 0, "Duplicator", ""],
            ["Outer God", "", 900, 480, 480, 480, 480, -1, 210, 0, 0, 0],
            ["Cosmic Entity", "", 1000, 510, 510, 510, 510, -1, 220, 0, 0, 0],
            ["Abstract Entity", "", 1100, 540, 540, 540, 540, -1, 230, 0, 0, 0],
            ["Creator God", "", 1200, 570, 570, 570, 570, -1, 240, 0, 0, 0],
            ["One-Above-All", "", 1300, 600, 600, 600, 600, -1, 250, 0, 0, 0],
            ["The Presence", "", 1400, 630, 630, 630, 630, -1, 260, 0, 0, 0],
            ["The Fulcrum", "", 1500, 660, 660, 660, 660, -1, 270, 0, 0, 0],
            ["The Source", "", 1600, 690, 690, 690, 690, -1, 280, 0, 0, 0],
            ["The Over-Monitor", "", 1700, 720, 720, 720, 720, -1, 290, 0, 0, 0],
            ["The Primal Monitor", "", 2000, 800, 800, 800, 800, -1, 300, 0, 0, 0],
            ["EddoBot", "uwuowo", 5000, 1500, 1500, 1500, 1500, -1, 500, 0, 0, 0, "Eddo's Balanced Item"]
            ]

def set_img(img_name):
    if img_name == "Eddo":
        return """
[:)]
-|-
/\\"""
    elif img_name == "Bocchi":
        return """
<a:bocchiPossessed:1088659149488922695>"""
    elif img_name == "KennyCarry":
        return "<a:kill:1082935360918667284>"
    elif img_name == "bunny":
        return """
 (\\\_/)
(='-'=)
(")\_(")"""
    elif img_name == "him":
        return """
[>:(]
 -|-
 /\ """
    elif img_name == "her":
        return """
/[>:(]\\
 -oo-
  /\ """
    elif img_name == "slime":
            return "('-')"
    elif img_name == "sealofapproval":
        return "<:sealofapproval:865125910134784032>"
    elif img_name == "pongers":
        return "<:pongers:865218289943445504>"
    elif img_name == "sponge":
        return "🧽"
    elif img_name == "uwuowo":
        return "<a:UwUOwO:782575562203988019>"
    
    else:
        return ""

###TODO until this becomes too difficult or tedious.
###Now currently on Hiatus.

###Adventure Update:
#[DONE]Tower idle progression. Endlessly grind of weaker units. Bosses reserved for dungeon. Enemies scale with floor level but very minor. (Temp: bosses appear in dungeon randomly while dungeon not created)
#[DONE]Death = Lose items. Items are quick progression. Level are slow progression. Reset floors though
#[DONE]Add Floors as a player/mobject stat. Battle should be grindable, but need to beat boss to progress. Higher floor = better loot
#[DONE]Possibly a shop or gacha based item rolling system. Some way to upgrade the player. Thinking TFT shop of 3-5 options, then reroll cost money. 
#[DONE]Add GOLD as a player/mobject stat
#[DONE]item drops scale with enemy XP. Enemies sometimes randomly carry items to take (if None in equipped)
#[DONE]Scrap the idea of rare drops. Now, you need multiple to upgrade. Also do replacement for offhand without discarding

###Dungeon Update
#[DONE]Add dungeon with randomly generated storyline. Able to find lots of loot and gold quickly, provided they make some choices. Luck influences what they find. Also possible death and no quitting
#[DONE]Quitting will be considered "escaping" which just saves loot. Death is common, but loot is high. (High Risk high reward). Timeout or escaping = quitting
#[DONE]Uses React UI to determine choices, and standard battling system.
#ChatGPT can generate simple storylines to use. Text file can be organised by split "|" and option = index. Make events with some other annotation.
#[DONE]Exit symbol = 🏳️. Auto exit after timeout.
#Charisma can actually be useful when encountering enemies in situations. CHR = better odds to getting out of situations. 
#Charisma also gives discount in shop after rerolling.
#[DONE]Possibly, SPECIAL items no longer drop from regular mobs. They are significantly stronger and only obtained through Dungeon. therefore, their upgraded forms should be formidable and have much stronger effects
#[DONE]Each choice/event needs a identifier such as [STORY]Something happens. Easier to jump through each line. Lines will also have some randomness so it can technically go on forever.
#[DONE]another identifier could also be [RANDOM] which will give out a random story.
#[DONE]another identifier could also be [BATTLE:<index/name>] to determine what it will battle. Progression will only occur after defeating enemy.
#[DONE]another identifier could also be [LOOT:<item_name>] to give an item. Usually followed by a [BATTLE] tag.
#[CANCELLED]use ~ to split each line for a before and after text.
#each line probably needs an index 0:[STORY]somethign something |[RANDOM]open door|[RANDOM]go down ladder. (This puts you somewhere else in the storyline everytime +replayability)
#   THEN 3:[BATTLE:slime1]You encounter slime1~(text after winning)you beat slime1. you see the ladder again or door|[4]ladder|[5]door
#   THEN 4:[LOOT:Magic Armor]You found a Magic Armor. It glows in the dark etc.|[RANDOM]Glowing door~You place your hand on the glowing doorknob. It fills you with excitement. You open the door|[2]Hole in ground~you jump down
#   THEN 5:[STORY]You find an empty room|[6]Follow trail~you follow the trail|[6]open door~you open door
#   THEN 6:[BATTLE:Bocchi]You find OP Bocchi. Death is likely~Pog what a win|[4]Loot the treasure room~You go treasure room|[RANDOM]Respectfully leave the tomb~You respectfully leave the tomb and head down the hallway

### Magic update
#Magic applies status effects
#Status effect represented by an emoji. Simply idea is fire = -def ice = -agl electric = stun/lose turn.
#Scrap idea that magic simply ignores enemy 1/2 def and prevents self from dodging.

### Visual Update
# Add health bar and possibly custom emotes for certain things.
# Add attack 'animation' based on ranged, melee, magic etc.
# Add dodge animation to move profile picture to left and right. Possibly add speedL and speedR
# Add randomised event log text when attacking and dodging. 
# Change more things in to React UI like swapping items

class mob():
    def __init__(self, name, img, hp, atk, df, lck, agl, sp, lvl, xp, gold, floor, equipped, offhand):
        self.name = name
        self.img = img
        self.maxhp = int(hp)
        self.hp = int(hp)
        self.statk = int(atk) #Stands for Standard ATK. Set amount
        self.atk = int(atk) #Changable during battle
        self.stdf = int(df)
        self.df = int(df)
        self.stlck = int(lck)
        self.lck = int(lck)
        self.stagl = int(agl)
        self.agl = int(agl)
        self.sp = int(sp)
        self.lvl = int(lvl)
        self.xp = int(xp)
        self.gold = int(gold)
        self.floor = int(floor)
        self.equipped = initialise_item(equipped)
        self.offhand = initialise_item(offhand)

        self.gain_item_stats()
    
    def takeDamage(self, dmg): #Check for other things later
        self.hp -= dmg

    def checkLevelUp(self):
        if self.xp >= self.lvl * XP_TO_LEVEL_UP:
            self.xp -= self.lvl * XP_TO_LEVEL_UP
            self.lvl += 1
            self.sp += SP_GAINED_PER_LEVEL
            self.maxhp += HP_GAINED_PER_LEVEL
            return True
        return False
        
    def roll_crt(self, enemySTAT): #out of 100%
        cur_lck = self.lck + BASE_LUCK - enemySTAT
        if cur_lck >= LUCK_CAP: 
            cur_lck = LUCK_CAP
        if cur_lck <= 0:
            cur_lck = BASE_LUCK
        random_roll = int(random.random()*100)
        if random_roll >= 0 and random_roll <= cur_lck:
            return True
        return False
    
    def roll_dgd(self, enemySTAT): #out of 100%
        cur_agl = int(self.agl/2 + BASE_LUCK - enemySTAT)
        if cur_agl >= LUCK_CAP: 
            cur_agl = LUCK_CAP
        if cur_agl <= 0:
            cur_agl = BASE_LUCK
        random_roll = int(random.random()*100)
        if random_roll >= 0 and random_roll <= cur_agl:
            return True
        return False
    
    def spend_SP(self, stat):
        stat_to_upgrade = stat.lower()
        if stat_to_upgrade == "atk":
            self.statk += ATK_UPGRADE
        elif stat_to_upgrade == "def":
            self.stdf += DEF_UPGRADE
        elif stat_to_upgrade == "lck":
            self.stlck += LCK_UPGRADE
        elif stat_to_upgrade == "agl":
            self.stagl += AGL_UPGRADE
        else:
            return False
        self.sp -= 1
        return True
    
    def gain_item_stats(self):
        if self.equipped.name == "None":
            self.hp = self.maxhp
            self.atk = self.statk
            self.df = self.stdf
            self.lck = self.stlck
            self.agl = self.stagl
            return
        stats = self.equipped.stat.split(",")
        if stats == [""]:
            return
        for s in stats:
            pn = 1
            set_type = -1
            if s[0] == "+":
                pn = 1
                set_type = 0
            elif s[0] == "-":
                pn = -1
                set_type = 0
            elif s[0] == "=":
                pn = 1
                set_type = 1
            elif s[0] == "x":
                pn = 1
                set_type = 2
            elif s[0] == "/":
                pn = 1
                set_type = 3
            
            if set_type == 0: #Additive
                if s[-1] == "a":
                    self.atk += pn * int(float(s[1:-1]))
                elif s[-1] == "d":
                    self.df += pn * int(float(s[1:-1]))
                elif s[-1] == "l":
                    self.lck += pn * int(float(s[1:-1]))
                elif s[-1] == "g":
                    self.agl += pn * int(float(s[1:-1]))
                elif s[-1] == "h":
                    self.hp += pn * int(float(s[1:-1]))
            elif set_type == 1: #Set num to exact
                if s[-1] == "a":
                    self.atk = pn * int(float(s[1:-1]))
                elif s[-1] == "d":
                    self.df = pn * int(float(s[1:-1]))
                elif s[-1] == "l":
                    self.lck = pn * int(float(s[1:-1]))
                elif s[-1] == "g":
                    self.agl = pn * int(float(s[1:-1]))
                elif s[-1] == "h":
                    self.hp = pn * int(float(s[1:-1]))
            elif set_type == 2: #Multiplicative
                if s[-1] == "a":
                    self.atk *= 1 + float(s[1:-1])
                elif s[-1] == "d":
                    self.df *= 1 + float(s[1:-1])
                elif s[-1] == "l":
                    self.lck *= 1 + float(s[1:-1])
                elif s[-1] == "g":
                    self.agl *= 1 + float(s[1:-1])
                elif s[-1] == "h":
                    self.hp *= 1 + float(s[1:-1])
            elif set_type == 3: #Divisibly
                if s[-1] == "a":
                    self.atk //= 1 + float(s[1:-1])
                elif s[-1] == "d":
                    self.df //= 1 + float(s[1:-1])
                elif s[-1] == "l":
                    self.lck //= 1 + float(s[1:-1])
                elif s[-1] == "g":
                    self.agl //= 1 + float(s[1:-1])
                elif s[-1] == "h":
                    self.hp //= 1 + float(s[1:-1])
            self.atk = int(self.atk)
            self.df = int(self.df)
            self.lck = int(self.lck)
            self.agl = int(self.agl)
            self.hp = int(self.hp)

    def swap_item(self):
        self.equipped, self.offhand = self.offhand, self.equipped
        self.reset_stats()
        self.gain_item_stats()

    def reset_stats(self): #Reset back to standard (no item modifiers)
        self.hp = self.maxhp
        self.atk = self.statk
        self.df = self.stdf
        self.lck = self.stlck
        self.agl = self.stagl

    def discard_item(self, hand):
        item_discarded = ""
        if hand == "equipped":
            item_discarded = self.equipped.name
            self.equipped = EMPTY_ITEM
        else:
            item_discarded = self.offhand.name
            self.offhand = EMPTY_ITEM
        return item_discarded
    
    def get_item_without_bonus_name(self):
        if "+" in self.equipped.name:
            return str(self.equipped.name.split("+")[0])
        else:
            return self.equipped.name
        
    def upgrade_equipped(self):
        if "+" in self.equipped.name:
            item_bonus = self.equipped.name.split("+")
            self.equipped.name = item_bonus[0] + "+" +str(int(item_bonus[1]) + 1)
        else:
            self.equipped.name += "+1"

    def check_if_item_exists(self, item_name):
        equipped_item = self.get_item_without_bonus_name()
        if item_name == equipped_item:
            return True
        return False

#[name|description|stat|type]
class item():
    def __init__(self, name, description, stat, item_type):
        self.name = name
        self.description = description
        self.stat = stat #What stat is changed. will use +00a format
        self.item_type = item_type

        if "+" in self.name:
            self.apply_bonus_stat()
    
    def apply_bonus_stat(self):
        item_bonus = int(self.name.split("+")[1]) + 1
        stat_list = self.stat.split(",")
        new_stat_string = ""
        for s in stat_list:
            stat_num = round(float(s[1:-1]) * item_bonus, 2)
            new_stat_string += s[0] + str(stat_num) + s[-1] + ","
        new_stat_string = new_stat_string[:-1]
        self.stat = new_stat_string

EMPTY_ITEM = item("None", "", "", False)

class story_node:
    def __init__(self, marker, event_text, ch1_text, ch2_text):
        self.marker = marker
        self.event_text = event_text
        self.ch1_text = ch1_text
        self.ch2_text = ch2_text
        self.left = None
        self.right = None

def get_all_story():
    f = open(".\RPGdungeon.txt", 'r')
    story_node_list = []
    while(1):
        readline = f.readline()
        if readline == "":
            break
        line = readline.rstrip().split("|")
        event = line[0]
        choice1 = line[1]
        choice2 = line[2]
        regex = re.search(r"\[([A-Za-z0-9\': ?.*$!]+)\]", event)
        marker = ""
        if regex:
            marker = regex.group(1)
        story_node_list.append(story_node(marker, event[len(marker)+2:], choice1, choice2))
    index = 0
    for sn in story_node_list:
        regex_ch1 = re.search(r"\[([A-Za-z0-9\': ?.*$!]+)\]", sn.ch1_text)
        choice1_result = ""
        if regex_ch1:
            choice1_result = regex_ch1.group(1)
        if(choice1_result.isalpha()):
            random_index = int(random.random()*len(story_node_list))
            while(random_index == index):
                random_index = int(random.random()*len(story_node_list))
            sn.left = story_node_list[random_index]
        else:
            sn.left = story_node_list[int(choice1_result) - 1]
        
        regex_ch2 = re.search(r"\[([A-Za-z0-9\': ?.*$!]+)\]", sn.ch2_text)
        choice2_result = ""
        if regex_ch2:
            choice2_result = regex_ch2.group(1)
        if(choice2_result.isalpha()):
            random_index = int(random.random()*len(story_node_list))
            while(random_index == index):
                random_index = int(random.random()*len(story_node_list))
            sn.right = story_node_list[random_index]
        else:
            sn.right = story_node_list[int(choice2_result) - 1]
        index += 1
    f.close()
    return story_node_list
        
def handle_choice(story, choice):
    if choice == 0:
        return story.left
    if choice == 1:
        return story.right
    
def handle_story(msgauth, story):
    if "BATTLE" in story.marker:
        opponent = str(story.marker.split(":")[1])
        index = 0
        mobject = None
        for m in boss_list:
            if m[0] == opponent:
                mobject = getBoss(msgauth, index)
            index += 1
        return ["battle", mobject]
    if "LOOT" in story.marker:
        item_found = story.marker.split(":")[1]
        if item_found == "RANDOM":
            item_found = get_all_item()[int(random.random() * len(get_all_item()))].name
        elif item_found == "SPECIAL":
            item_found = get_all_item()[int(random.random() * len(get_all_item()))]
            while(int(item_found.item_type) != 3):
                item_found = get_all_item()[int(random.random() * len(get_all_item()))]
            item_found = item_found.name
        return ["loot", item_found]
    if "STORY" in story.marker:
        return ["story", ""]

def display_story(story):
    story_display = story.event_text + "\n"
    regex_ch1 = re.search(r"\[([A-Za-z0-9\': ?.*$!]+)\]", story.ch1_text)
    choice1_result = ""
    if regex_ch1:
        choice1_result = regex_ch1.group(1)
    splice_len = len(choice1_result) + 2
    story_display += "Choice 1: " + story.ch1_text[splice_len:] + "\n"

    regex_ch2 = re.search(r"\[([A-Za-z0-9\': ?.*$!]+)\]", story.ch2_text)
    choice2_result = ""
    if regex_ch2:
        choice2_result = regex_ch2.group(1)
    splice_len = len(choice2_result) + 2
    story_display += "Choice 2: " + story.ch2_text[splice_len:] + "\n"

    return story_display

def initialise_item(item_name):
    f = open(".\RPGitem.txt", 'r')
    item_name = item_name.rstrip("\n")
    while(1):
        readline = f.readline()
        if readline == "":
            break
        line = readline.rstrip().split("|")
        name_only = item_name
        if "+" in item_name:
            name_only = str(item_name.split("+")[0])
        if line[0] == name_only:
            name = item_name
            desc = line[1]
            stat = line[2]
            item_type = line[3]
            f.close()
            return item(name, desc, stat, item_type)
    f.close()
    return EMPTY_ITEM

def get_all_item():
    f = open(".\RPGitem.txt", 'r')
    item_list = []
    while(1):
        readline = f.readline()
        if readline == "":
            break
        line = readline.split("|")
        name = line[0]
        desc = line[1]
        stat = line[2]
        item_type = line[3]
        item_list.append(item(name, desc, stat, item_type))
    return item_list

def show_shop_formatted(msgauth):
    shop_list = show_shop()
    player = set_player(msgauth)
    gold_remaining = player.gold
    item_equipped = player.equipped.name
    offhand_item = player.offhand.name
    shop_string = f"Gold Remaining: {gold_remaining}\nItem currently equipped: {item_equipped}\nItem in offhand: {offhand_item}\n\n"
    for s in shop_list:
        if s[0] == player.get_item_without_bonus_name() and s[0] != "None":
            shop_string += f"**Item Name: {s[0]} x10 | Cost: {s[1]}** "
        else:
            shop_string += f"Item Name: {s[0]} x10 | Cost: {s[1]}"
    return shop_string

def show_shop():
    f = open(".\RPGshop.txt", 'r')
    shop_content = []
    while(1):
        readline = f.readline()
        if readline == "":
            break
        shop_line = readline.split("|")
        shop_content.append(shop_line)
    f.close()
    return shop_content

def buy_shop(msgauth, option):
    player = set_player(msgauth)
    shop_content = show_shop()
    shop_item_name = shop_content[option][0]
    shop_cost = int(shop_content[option][1])

    if player.gold < shop_cost:
        return False
    
    shop_item = initialise_item(shop_item_name)
    if shop_item == EMPTY_ITEM:
        return False
    item_granted = False
    for _ in range(10):
        if player.check_if_item_exists(shop_item.name):
            player.upgrade_equipped()
        else:
            if item_granted == False:
                item_granted = True
                if player.equipped != EMPTY_ITEM:
                    shop_item.name = shop_item.name + "+9"
                    player.offhand = shop_item
                else:
                    shop_item.name = shop_item.name + "+9"
                    player.equipped = shop_item
    player.gold -= shop_cost

    update_players(player)
    update_shop(option)
    return True
    
def update_shop(item_bought_index): #Only after purchase of a single item
    shop_list = show_shop()
    fw = open(".\RPGshop.txt", 'w')
    index = 0
    for s in shop_list:
        name = s[0]
        cost = str(s[1])
        line = ""
        if item_bought_index == index:
            line = "None|0\n"
        else:
            line = f"{name}|{cost}"
        index += 1
        fw.write(line)
    fw.close()
    
def reroll_shop(msgauth):
    player = set_player(msgauth)
    if player.gold < REROLL_SHOP_COST:
        return False
    new_item_list = []
    cur_cost = 50
    for _ in range(SHOP_SIZE):
        cur_cost += int(random.random() * 50)
        item_rolled_index = int(random.random()*len(get_all_item()))
        item_rolled = get_all_item()[item_rolled_index]
        if int(item_rolled.item_type) == 3:
            item_rolled = get_all_item()[0] #Default to first item if SPECIAL item is rolled
        new_item_list.append(item_rolled.name + f"|{cur_cost}")
    fw = open(".\RPGshop.txt", "w")
    for s in new_item_list:
        fw.write(s + "\n")
    player.gold -= REROLL_SHOP_COST
    update_players(player)
    fw.close()
    return True

def swap_items(auth):
    player = set_player(auth)
    player.swap_item()
    update_players(player)
    return player.equipped.name

def discard_item(auth):
    player = set_player(auth)
    item_discarded = player.discard_item("equipped")
    update_players(player)
    return item_discarded

def get_info(mob_index): #Make sure to check isnumeric before calling. Invalid name will create new account
    if mob_index.isnumeric():
        return create_display(getMob(int(mob_index)))
    else:
        player = set_player(mob_index) #Will be username instead
        return create_display(player)

def get_item_type_str(item):
    if int(item.item_type) == 0:
        return "Melee"
    elif int(item.item_type) == 1:
        return "Ranged"
    elif int(item.item_type) == 2:
        return "Magic"
    elif int(item.item_type) == 3:
        return "SPECIAL"

def get_item_info(auth):
    player = set_player(auth)
    equipped = player.equipped
    offhand = player.offhand
    equipped_type = get_item_type_str(equipped)
    offhand_type = get_item_type_str(offhand)
    equipped_stat_string = "\n"
    if equipped != EMPTY_ITEM:
        equipped_stat_list = equipped.stat.split(",")
        for e in equipped_stat_list:
            if e[0] == "+":
                equipped_stat_string += "+ " + str(e[1:-1])
            elif e[0] == "-":
                equipped_stat_string += "\- " + str(e[1:-1])
            elif e[0] == "x":
                equipped_stat_string += "x " + str(1 + float(e[1:-1]))
            elif e[0] == "/":
                equipped_stat_string += "/ " + str(1 + float(e[1:-1]))
            elif e[0] == "=":
                equipped_stat_string += "Set to " + str(e[1:-1])

            if e[-1] == "a":
                equipped_stat_string += " ATK\n"
            elif e[-1] == "d":
                equipped_stat_string += " DEF\n"
            elif e[-1] == "l":
                equipped_stat_string += " LCK\n"
            elif e[-1] == "g":
                equipped_stat_string += " AGL\n"
            elif e[-1] == "h":
                equipped_stat_string += " HP\n"

    offhand_stat_string = "\n"
    if offhand != EMPTY_ITEM:
        offhand_stat_list = offhand.stat.split(",")
        for e in offhand_stat_list:
            if e[0] == "+":
                offhand_stat_string += "+ " + str(e[1:-1])
            elif e[0] == "-":
                offhand_stat_string += "\- " + str(e[1:-1])
            elif e[0] == "x":
                offhand_stat_string += "x " + str(1 + float(e[1:-1]))
            elif e[0] == "/":
                offhand_stat_string += "÷ " + str(1 + float(e[1:-1]))
            elif e[0] == "=":
                offhand_stat_string += "Set to " + str(e[1:-1])

            if e[-1] == "a":
                offhand_stat_string += " ATK\n"
            elif e[-1] == "d":
                offhand_stat_string += " DEF\n"
            elif e[-1] == "l":
                offhand_stat_string += " LCK\n"
            elif e[-1] == "g":
                offhand_stat_string += " AGL\n"
            elif e[-1] == "h":
                offhand_stat_string += " HP\n"
    
    return f"Equipped: {equipped.name}\n{equipped.description}\nStat changes: {equipped_stat_string}\nType: {equipped_type}\n\nOffhand: {offhand.name}\n{offhand.description}\nStat changes: {offhand_stat_string}\nType: {offhand_type}"

def sp_spend(auth, stat):
    player = set_player(auth)
    upgrade_successful = False
    if player.sp > 0:
        upgrade_successful = player.spend_SP(stat)
        if upgrade_successful:
            update_players(player)
    return upgrade_successful

def set_player(msgauth):
    f = open(".\RPGinfo.txt", 'r')
    while(1):
        readline = f.readline()
        if readline == "":
            break
        line = readline.split("|")
        if line[0] == msgauth:
            name = line[0]
            img = line[1]
            hp = line[2]
            atk = line[3]
            df = line[4]
            lck = line[5]
            agl = line[6]
            sp = line[7]
            lvl = line[8]
            xp = line[9]
            gold = line[10]
            floor = line[11]
            equipped = line[12]
            offhand = line[13]
            return mob(name, img, hp, atk, df, lck, agl, sp, lvl, xp, gold, floor, equipped, offhand)
    f.close()

    #Character Create [Name|img|maxhp|atk|df|lck|sp|lvl|xp]
    name = msgauth
    img = msgauth
    hp = 10
    atk = 10
    df = 10
    lck = 0
    agl = 0
    sp = 3
    lvl = 1
    xp = 0
    gold = 5
    floor = 1
    equipped = ""
    offhand = ""
    line_to_write = f"{msgauth}|{msgauth}|{hp}|{atk}|{df}|{lck}|{agl}|{sp}|{lvl}|{xp}|{gold}|{floor}||\n"

    fw = open(".\RPGinfo.txt", 'a')
    fw.write(line_to_write)
    fw.close()
    return mob(name, img, hp, atk, df, lck, agl, sp, lvl, xp, gold, floor, equipped, offhand)

def ascend_player(msgauth): #TODO find a reward for ascension 
    player = set_player(msgauth)
    if player.lvl < ASCENSION_LEVEL:
        return False
    player.maxhp = 10
    player.statk //= ASCENSION_STAT_KEPT
    player.stdf //= ASCENSION_STAT_KEPT
    player.stlck //= ASCENSION_STAT_KEPT
    player.stagl //= ASCENSION_STAT_KEPT
    player.sp += player.lvl
    player.lvl = 1
    player.xp = 0
    player.gold = 0
    player.floor = 1
    player.equipped = EMPTY_ITEM
    player.offhand = EMPTY_ITEM
    update_players(player)
    return True

def update_players(player):
    f = open(".\RPGinfo.txt", "r")
    player_details = []
    while(1):
        readline = f.readline()
        if readline == "": #EOF
            break
        line = readline.rstrip().split("|")
        if player.name == line[0]:
            name = player.name
            img = player.img
            maxhp = player.maxhp
            atk = player.statk
            df = player.stdf
            lck = player.stlck
            agl = player.stagl
            sp = player.sp
            lvl = player.lvl
            xp = player.xp
            gold = player.gold
            floor = player.floor
            equipped = player.equipped.name
            offhand = player.offhand.name
            line = [name, img, maxhp, atk, df, lck, agl, sp, lvl, xp, gold, floor, equipped, offhand]
        player_details.append(line)
    f.close()

    fw = open(".\RPGinfo.txt", "w")
    for p in player_details:
        line_to_write = ""
        for x in p:
            line_to_write += str(x) + "|"
        line_to_write = line_to_write[:-1]
        fw.write(line_to_write + "\n")
    fw.close()

def give_item(msgauth, item):
    player = set_player(msgauth)
    item_found = ""
    item_msg = ""
    for i in get_all_item():
        if item == i.name:
            item_found = i
    if player.equipped.name == "None":
        if item_found.name != "None":
            player.equipped = item_found
            item_msg += f"{player.name} has found a {player.equipped.name}!\nEquipped to main hand."
        update_players(player)
        return item_msg
    if item_found.name != "None":
        item_msg += f"{player.name} has found a {item_found.name}!\n"
        if player.get_item_without_bonus_name() == item_found.name:
            player.upgrade_equipped()
            item_msg += f"{item_found.name} combined with equipped item to create {player.equipped.name}!"
        else:
            player.offhand = item_found
            item_msg += "Equipped in offhand"
    update_players(player)
    return item_msg

def loot_roll(player, enemyMob):
    get_item_roll = int(random.random() * ITEM_DROP_CHANCE)
    if get_item_roll >= enemyMob.lvl:
        return EMPTY_ITEM
    item_list = get_all_item()
    item_index_rolled = int(random.random() * len(item_list)) 
    if int(player.equipped.item_type) != 3:
        dupe_roll = int(random.random() * DUPE_ROLL_ODDS)
        if dupe_roll <= (player.stlck + enemyMob.lvl):
            return initialise_item(player.get_item_without_bonus_name())
    if int(item_list[item_index_rolled].item_type) != 3:
        return item_list[item_index_rolled]
    else:
        return EMPTY_ITEM

def win_battle(player, enemyMob):
    player.xp += enemyMob.lvl
    player.floor += 1

    player.gold += (1 + int(random.random() * enemyMob.lvl/10))

    did_level_up = player.checkLevelUp()
    win_msg = f"{player.name} gained {enemyMob.lvl} xp\n"
    if did_level_up:
        win_msg += f"{player.name} has levelled up!\n"
    if player.equipped.name == "None":
        if enemyMob.equipped.name != "None":
            item_found = enemyMob.equipped
        else:
            item_found = loot_roll(player, enemyMob)
        if item_found.name != "None":
            player.equipped = item_found
            win_msg += f"{player.name} has found a {player.equipped.name}!\nEquipped to main hand."
        update_players(player)
        return win_msg
    item_found = loot_roll(player, enemyMob)
    if item_found.name != "None":
        win_msg += f"{player.name} has found a {item_found.name}!\n"
        if player.get_item_without_bonus_name() == item_found.name:
            player.upgrade_equipped()
            win_msg += f"{item_found.name} combined with equipped item to create {player.equipped.name}!"
        else:
            player.offhand = item_found
            win_msg += "Equipped in offhand"
    
    update_players(player)
    return win_msg

def lose_battle(player, enemyMob): #Lose weapon
    if "+" in player.equipped.name:
        item_bonus = int(player.equipped.name.split("+")[1])
        if item_bonus > ITEM_BONUS_LOST_ON_DEATH:
            item_bonus -= ITEM_BONUS_LOST_ON_DEATH
            if item_bonus <= 0:
                player.equipped.name = player.equipped.name.split("+")[0]
            else:
                player.equipped.name = player.equipped.name.split("+")[0] + "+" + str(item_bonus)
        else:
            player.discard_item("equipped")
    else:
        player.discard_item("equipped")
    player.discard_item("offhand")
    player.floor -= FLOORS_LOST_ON_DEATH
    if player.floor <= 1:
        player.floor = 1
    update_players(player)

def create_display(mobject): #[Name|img|maxhp|atk|df|lck|sp|lvl|xp|gold|floor|equipped|offhand]
    HpBar = f"{mobject.name} ["
    HpBarStacks = 1
    leftover_hp = mobject.hp
    created_display = ""
    if mobject.hp <= 0:
        mobject.hp = 0
    if mobject.hp >= HP_DISPLAY_LIMIT:
        HpBarStacks = mobject.hp // HP_DISPLAY_LIMIT
        leftover_hp = mobject.hp % HP_DISPLAY_LIMIT
        for _ in range(leftover_hp):
            HpBar += "="
        for _ in range(HP_DISPLAY_LIMIT - leftover_hp):
            HpBar += "  "
        HpBar += "]"
        if HpBarStacks > 0:
            created_display = set_img(mobject.img) + "\n" + HpBar + f" x{HpBarStacks}\n" + f"Level: {mobject.lvl} | ATK: {mobject.atk} | DEF: {mobject.df} | LCK: {mobject.lck} | AGL: {mobject.agl} | SP: {mobject.sp} | XP: {mobject.xp}\nEquipped: {mobject.equipped.name} | Offhand: {mobject.offhand.name}\nFloor: {mobject.floor}\n"
    elif mobject.maxhp < HP_DISPLAY_LIMIT:
        for _ in range(mobject.hp):
            HpBar += "="
        for _ in range(mobject.maxhp - mobject.hp):
            HpBar += "  "
        HpBar += "]\n"
        created_display = set_img(mobject.img) + "\n" + HpBar + f"Level: {mobject.lvl} | ATK: {mobject.atk} | DEF: {mobject.df} | LCK: {mobject.lck} | AGL: {mobject.agl} | SP: {mobject.sp} | XP: {mobject.xp}\nEquipped: {mobject.equipped.name} | Offhand: {mobject.offhand.name}\nFloor: {mobject.floor}\n"
    else:
        for _ in range(mobject.hp):
            HpBar += "="
        for _ in range(HP_DISPLAY_LIMIT - mobject.hp):
            HpBar += "  "
        HpBar += "]"
        created_display = set_img(mobject.img) + "\n" + HpBar + f"\nLevel: {mobject.lvl} | ATK: {mobject.atk} | DEF: {mobject.df} | LCK: {mobject.lck} | AGL: {mobject.agl} | SP: {mobject.sp} | XP: {mobject.xp}\nEquipped: {mobject.equipped.name} | Offhand: {mobject.offhand.name}\nFloor: {mobject.floor}\n"
    return created_display

def calc_stat_variance():
    return random.uniform(0.9, 1.5)

def getMob(mob_index):
    m = mob_list[mob_index%(len(mob_list))]
    hp = int(m[2]) * calc_stat_variance()
    atk = int(m[3]) * calc_stat_variance()
    df = int(m[4]) * calc_stat_variance()
    lck = int(m[5]) * calc_stat_variance()
    agl = int(m[6]) * calc_stat_variance()
    sp = int(m[7])
    lvl = int(m[8])
    xp = int(m[9])
    gold = int(int(m[8])/10)
    floor = int(m[8])

    equipped_name = ""
    try:
        equipped_name = m[12]
    except IndexError:
        carries_item = int(random.random() * 1000) 
        if carries_item <= MOB_CARRIES_ITEM_ODDS:
            equipped = get_all_item()[int(random.random()*len(get_all_item()))]
            equipped_name = equipped.name
            equipped_bonus = int(random.random()*lvl/2)
            if equipped_bonus != 0:
                equipped_name = equipped_name + "+" + str(equipped_bonus)
            if int(equipped.item_type) == 3:
                equipped_name = ""
    return mob(m[0], m[1], hp, atk, df, lck, agl, sp, lvl, xp, gold, floor, equipped_name, "")

def getBoss(msgauth, mob_index):
    player = set_player(msgauth)

    m = boss_list[mob_index%(len(mob_list))]
    hp = int(m[2]) * calc_stat_variance() + int(player.lvl/2) * calc_stat_variance()
    atk = int(m[3]) * calc_stat_variance() + int(player.lvl/2) * calc_stat_variance()
    df = int(m[4]) * calc_stat_variance() + int(player.lvl/2) * calc_stat_variance()
    lck = int(m[5]) * calc_stat_variance() + int(player.lvl/2) * calc_stat_variance()
    agl = int(m[6]) * calc_stat_variance() + int(player.lvl/2) * calc_stat_variance()
    sp = int(m[7])
    lvl = int(m[8])
    xp = int(m[9])
    gold = int(m[10])
    floor = int(m[11])

    equipped_name = ""
    try:
        equipped_name = m[12]
    except IndexError:
        carries_item = int(random.random() * 1000) 
        if carries_item <= BOSS_CARRIES_ITEM + player.lvl:
            equipped = get_all_item()[int(random.random()*len(get_all_item()))]
            equipped_name = equipped.name
            equipped_bonus = int(random.random()*lvl/2)
            if equipped_bonus != 0:
                equipped_name = equipped_name + "+" + str(equipped_bonus)
            if int(equipped.item_type) == 3:
                equipped_name = ""
    return mob(m[0], m[1], hp, atk, df, lck, agl, sp, lvl, xp, gold, floor, equipped_name, "")

def calc_damage_variance():
    return random.uniform(0.8, 1.2)

def make_animation_frame(mobject, hit_type, dir_dwn, amount, item_broken):
    animation_frame = ""
    if dir_dwn == True:
        if mobject.equipped.name == "None":
            animation_frame += "👊"
        elif int(mobject.equipped.item_type) == 3:
            animation_frame += "🌟"
        elif int(mobject.equipped.item_type) == 2:
            animation_frame += "🪄"
        elif int(mobject.equipped.item_type) == 1:
            animation_frame += "🏹"
        else:
            animation_frame += "🗡️"

        animation_frame += "\n\n"
    
        if hit_type == "hit":
            animation_frame += f"💥 -{amount}"
        elif hit_type == "dodge":
            animation_frame += "💨 _miss_"
        elif hit_type == "crit":
            animation_frame += f"💥🎯💥 -__**{amount}**__"

    else: #Player Animations
        if hit_type == "hit":
            animation_frame += f"💥 -{amount}"
        elif hit_type == "dodge":
            animation_frame += "💨 _miss_"
        elif hit_type == "crit":
            animation_frame += f"💥🎯💥 -__**{amount}**__"

        animation_frame += "\n\n"
        if item_broken == 3:
            animation_frame += "```🌟❌*broke*```"
        elif item_broken == 2:
            animation_frame += "``` 🪄 ❌*broke*```"#Magic wand emoji
        elif item_broken == 1:
            animation_frame += "```🏹❌*broke*```"
        elif item_broken == 0:
            animation_frame += "```🗡️❌*broke*```"
        elif mobject.equipped.name == "None":
            animation_frame += "👊"
        elif int(mobject.equipped.item_type) == 3:
            animation_frame += "🌟"
        elif int(mobject.equipped.item_type) == 2:
            animation_frame += "🪄" #Magic wand emoji
        elif int(mobject.equipped.item_type) == 1:
            animation_frame += "🏹"
        else:
            animation_frame += "🗡️"
    return animation_frame

def battle(auth, enemyMob): #Tower Battle
    player = set_player(auth)
    isDungeon = True
    if(enemyMob == ""):
        isDungeon = False
        enemyMob = getMob(int(random.random()* 100))
        for _ in range(100):
            if enemyMob.lvl > player.floor:
                enemyMob = getMob(int(random.random()* 100))

    chat_log = []
    battle_frames = []
    
    battle_frames.append(create_display(enemyMob) + create_display(player))
    while(enemyMob.hp > 0 and player.hp > 0): #Battle loop
        player_chat_log_msg = ""
        enemy_chat_log_msg = ""

        player_animation_msg = ""
        enemy_animation_msg = ""

        #Item break check
        item_broken = -1
        if player.equipped.name != "None":
            item_break_roll = int(random.random() * ITEM_BREAK_CHANCE)
            if int(player.equipped.item_type) == 3: #Special weapon 2x less likely to break
                item_break_roll = int(random.random() * ITEM_BREAK_CHANCE * 2)
            if item_break_roll == 1:
                item_broken = int(player.equipped.item_type)
                player_chat_log_msg += f"```{player.equipped.name} broke!```"
                player.discard_item("equipped")
                player.gain_item_stats()
                
        enemy_damage_to_take = int((player.atk - enemyMob.df) * (calc_damage_variance()))
        player_damage_to_take = int((enemyMob.atk - player.df) * (calc_damage_variance()))

        if enemy_damage_to_take <= 0:
            enemy_damage_to_take = 1
        if player_damage_to_take <= 0:
            player_damage_to_take = 1

        #CRIT check
        player_did_crit = False
        enemy_did_crit = False
        if int(player.equipped.item_type) == 3: #Special
            enemy_damage_to_take += int(enemyMob.df/2) #Ignore half def
            if player.roll_crt(enemyMob.lck/2) == True:
                enemy_damage_to_take = enemy_damage_to_take * RANGED_CRIT_MULTIPLIER #Ranged Crit multiplier
                player_did_crit = True
        elif int(player.equipped.item_type) == 2: #Magic (ranged)
            enemy_damage_to_take += int(enemyMob.df/2)
            if player.roll_crt(enemyMob.lck/2) == True:
                enemy_damage_to_take = enemy_damage_to_take * RANGED_CRIT_MULTIPLIER
                player_did_crit = True
            
        elif int(player.equipped.item_type) == 1: #Ranged
            if player.roll_crt(enemyMob.lck/2) == True:
                enemy_damage_to_take = enemy_damage_to_take * RANGED_CRIT_MULTIPLIER
                player_did_crit = True
        else:
            if player.roll_crt(enemyMob.lck/2) == True: #Melee
                enemy_damage_to_take = enemy_damage_to_take * MELEE_CRIT_MULTIPLIER
                player_did_crit = True


        if int(enemyMob.equipped.item_type) == 3: #Special
            player_damage_to_take += int(enemyMob.df/2) #Ignore half def
            if player.roll_crt(enemyMob.lck/2) == True:
                player_damage_to_take = enemy_damage_to_take * RANGED_CRIT_MULTIPLIER #Ranged Crit multiplier
                player_did_crit = True
        if int(enemyMob.equipped.item_type) == 2: #Magic (ranged)
            player_damage_to_take += int(player.df/2)
            if enemyMob.roll_crt(player.lck/2) == True:
                player_damage_to_take = player_damage_to_take * RANGED_CRIT_MULTIPLIER
                enemy_did_crit = True
        elif int(enemyMob.equipped.item_type) == 1: #Ranged
            if enemyMob.roll_crt(player.lck/2) == True:
                player_damage_to_take = player_damage_to_take * RANGED_CRIT_MULTIPLIER
                enemy_did_crit = True
        else:
            if enemyMob.roll_crt(player.lck/2) == True: #Melee
                player_damage_to_take = player_damage_to_take * MELEE_CRIT_MULTIPLIER
                enemy_did_crit = True

        #DODGE CHECK
        player_did_dodge = False
        enemy_did_dodge = False
        if int(player.equipped.item_type) == 3: #Special
            if player.roll_dgd(enemyMob.agl/2) == True: #Dodge chance of a melee
                player_damage_to_take = 0
                player_did_dodge = True
        if int(player.equipped.item_type) == 2: #Magic
            pass
        elif int(player.equipped.item_type) == 1: #Ranged
            if player.roll_dgd(enemyMob.agl) == True:
                player_damage_to_take = 0
                player_did_dodge = True
        else:
            if player.roll_dgd(enemyMob.agl/2) == True: #Melee
                player_damage_to_take = 0
                player_did_dodge = True

        if int(enemyMob.equipped.item_type) == 3: #Special
            if enemyMob.roll_dgd(player.agl/2) == True: #Dodge chance of a melee
                enemy_damage_to_take = 0
                enemy_did_dodge = True
        elif int(enemyMob.equipped.item_type) == 2: #Magic
            pass
        elif int(enemyMob.equipped.item_type) == 1: #Ranged
            if enemyMob.roll_dgd(player.agl) == True:
                enemy_damage_to_take = 0
                enemy_did_dodge = True
        else:
            if enemyMob.roll_dgd(player.agl/2) == True: #Melee
                enemy_damage_to_take = 0
                enemy_did_dodge = True

        enemyMob.takeDamage(enemy_damage_to_take)
        if enemy_did_dodge:
            player_chat_log_msg += (f"{enemyMob.name} _dodged_ {player.name}'s attack")
            player_animation_msg = make_animation_frame(player, "dodge", False, enemy_damage_to_take, item_broken)
        elif player_did_crit:
            player_chat_log_msg += (f"{player.name} landed a __**CRITICAL strike!**__\n> {player.name} deals **{enemy_damage_to_take}** damage to {enemyMob.name}")
            player_animation_msg = make_animation_frame(player, "crit", False, enemy_damage_to_take, item_broken)
        else:
            player_chat_log_msg += (f"{player.name} deals {enemy_damage_to_take} damage to {enemyMob.name}")
            player_animation_msg = make_animation_frame(player, "hit", False, enemy_damage_to_take, item_broken)

        chat_log.append(player_chat_log_msg)

        if enemyMob.hp <= 0:
            battle_frames.append(create_display(enemyMob) + player_animation_msg + create_display(player))
            break

        battle_frames.append(create_display(enemyMob) + player_animation_msg + create_display(player))

        player.takeDamage(player_damage_to_take)
        if player_did_dodge:
            enemy_chat_log_msg += (f"{player.name} _dodged_ {enemyMob.name}'s attack")
            enemy_animation_msg = make_animation_frame(enemyMob, "dodge", True, player_damage_to_take, False)
        elif enemy_did_crit:
            enemy_chat_log_msg += (f"{enemyMob.name} landed a __**CRITICAL strike!**__\n> {enemyMob.name} deals **{player_damage_to_take}** damage to {player.name}")
            enemy_animation_msg = make_animation_frame(enemyMob, "crit", True, player_damage_to_take, False)
        else:
            enemy_chat_log_msg += (f"{enemyMob.name} deals {player_damage_to_take} damage to {player.name}")
            enemy_animation_msg = make_animation_frame(enemyMob, "hit", True, player_damage_to_take, False)

        battle_frames.append(create_display(enemyMob) + enemy_animation_msg + create_display(player))
        chat_log.append(enemy_chat_log_msg)

    if player.hp > 0:
        win_changes = win_battle(player, enemyMob)
        win_msg = f"{enemyMob.name} has died. You WON!\n" + win_changes
        chat_log.append(win_msg)
        if isDungeon:
            player.floor -= 1
        
    else:
        chat_log.append(f"{player.name} has died. Your body has been looted and some items have been lost D:\n")
        if isDungeon:
            player.discard_item("offhand")
            player.discard_item("equipped")
            update_players(player)
        else:
            lose_battle(player, enemyMob)
    battle_frames[-1] += f"\n{chat_log[-1]}"
    return battle_frames



def main(): #Testing purposes only
    msgauth = "testerWester"
    full_story = get_all_story()
    print(display_story(full_story[0]))
    new_story = handle_story(full_story[0], 1)
    print(display_story(new_story))
    return

if __name__ == "__main__":
    main()