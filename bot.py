#!/usr/bin/env python3
import discord
import random
import random_npcs
from secret import discord_token, guilds
import interactions
from os import name, system, getenv
from math import floor
from weapons import weapons
from descriptions import weaponDescriptions
from datetime import datetime, timedelta
from time import sleep
from bs4 import BeautifulSoup

bot = interactions.Client(token=discord_token)

@bot.event
async def on_ready():
    print('Ready!')

def clear():
    if name == 'nt':
        system('cls')
    else:
        system('clear')

# Functions
def getWeapon():
    '''Return a random weapon from the list of weapons.'''
    roll = random.randint(0, len(weapons))
    return weapons[roll]

def getFlatDamage():
    '''Returns a flat damage between 1 and 30.
      3%: 26-30
      6%: 21-25
      6%: 16-20
     40%: 11-15
     40%: 6-10
      5%: 0-5'''
    rollTier = random.randint(0, 10000)
    if rollTier < 300:
        return random.randint(26, 30)
    elif rollTier < 900:
        return random.randint(21, 25)
    elif rollTier < 1500:
        return random.randint(16, 20)
    elif rollTier < 5500:
        return random.randint(11, 15)
    elif rollTier < 9500:
        return random.randint(6, 10)
    else:
        return random.randint(0, 5)

def getRollDamage():
    '''Returns a roll damage between 1 and 10.
     5% - 9-10
     5% - 6-8
    50% - 3-5
    40% - 0-2'''
    rollTier = random.randint(0, 10000)
    if rollTier < 500:
        return random.randint(9, 10)
    elif rollTier < 1000:
        return random.randint(6, 8)
    elif rollTier < 6000:
        return random.randint(3, 5)
    else:
        return random.randint(0, 2)

def getSkill():
    '''Returns a skill from the list of Power, Brawn, Accuracy, or Hand-to-hand.'''
    skills = [
            'Power',
            'Brawn',
            'Accuracy',
            'Hand-to-hand'
            ]
    return random.choice(skills)

def getDamageClass():
    '''Return a random damage class from the list of Energy, Physical, or Quantum.'''
    classes = [
            'Energy',
            'Physical',
            'Quantum'
            ]
    return random.choice(classes)

def getDamageType():
    '''Return a random damage type from the list of Piercing, Slashing, Concussive, or Impact.'''
    types = [
            'Piercing',
            'Slashing',
            'Concussive',
            'Impact'
            ]
    return random.choice(types)

def getSecondaryDamage():
    '''Return a random secondary damage number if one is called.'''
    return random.randint(1, 4)

def getRange():
    '''Return a random range from 1 to 10.'''
    listOfRanges = [5, 5, 10, 10, 15, 15, 20, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80, 85, 90, 95, 100, 105]
    weaponRange = random.choice(listOfRanges)
    if weaponRange == 105:
        return '∞'
    else:
        return str(weaponRange) + 'ft'

def getSkillBonus():
    '''Returns a skill bonus between 1 and 6.'''
    return random.randint(1, 6)

def rollWeapon():
    newWeapon = {
            'Weapon': getWeapon(),
            'Flat Damage': getFlatDamage(),
            'Roll Damage': getRollDamage(),
            'Skill': getSkill(),
            'Damage Class': getDamageClass(),
            'Damage Type': getDamageType(),
            }
    while newWeapon['Flat Damage'] == 0 and newWeapon['Roll Damage'] == 0:
        newWeapon['Flat Damage'] = getFlatDamage()
        newWeapon['Roll Damage'] = getRollDamage()


    # 10% chance of corrosive
    corrosive = random.randint(1, 10)
    if corrosive == 1:
        newWeapon['Secondary Damage'] = 'Corrosive'
        newWeapon['Corrosive Damage'] = random.randint(1, 4)
    newWeapon['Range'] = getRange()
    newWeapon['Skill Bonus'] = getSkillBonus()

    return newWeapon

def generateNPC(race=None, gender=None):
#   if race:
#       if gender:
            # TODO: Randomize the rest of the specific race and gender.
        # TODO: Randomize the gender and rest of the character.
#   else:
        # TODO: Randomize the rest of the character.
    return random.choice(list(random_npcs.races))

@bot.command(
        name='chaosgauntlet',
        description='Reach through and pull a weapon from a dimension of chaos.',
        scope=guilds,
        )
async def chaosgauntlet(ctx: interactions.CommandContext):
    weapon = rollWeapon()

    # Weapon specific modifications
    if weapon['Weapon'] == 'Chaos Blade':
        weapon['Range'] = '10ft'
        weapon['Flat Damage'] = '10'
        weapon['Roll Damage'] = '5D8'
        weapon['Skill'] = 'Brawn'
        weapon['Skill Bonus'] = 4
        weapon['Damage Class'] = 'Chaos'
        weapon['Damage Type'] = 'Chaos'
    elif weapon['Weapon'] == 'Chaos Cannon':
        weapon['Range'] = '100ft'
        weapon['Flat Damage'] = '5'
        weapon['Roll Damage'] = '3D10'
        weapon['Skill'] = 'Pow'
        weapon['Skill Bonus'] = 6
        weapon['Damage Class'] = 'Chaos'
        weapon['Damage Type'] = 'Chaos'
        weapon['Description'] = 'Crackling with harsh crimson energy, this rifle hums with chaos itself. Once pulled, keep this weapon until the end of combat, instead of it vanishing after the first use.'
    elif weapon['Weapon'] in ['Blade of Ice', 'Frozen Baseball']:
        weapon['Damage Type'] = 'Cold'
    elif weapon['Weapon'] in ['Blade of Fire', 'Flaming Baseball']:
        weapon['Damage Type'] = 'Fire'
    elif weapon['Weapon'] == 'Eroshevaal\'s Ether Bow':
        weapon['Damage Type'] = 'Almighty'
    elif weapon['Weapon'] == 'Blade of Ice and Fire':
        if random.randint(1,2) == 1:
            weapon['Damage Type'] = 'Fire'
        else:
            weapon['Damage Type'] = 'Cold'
    elif weapon['Weapon'] == 'Alligator Snapping Turtle':
        weapon['Damage Type'] = 'Snapping'
    elif weapon['Weapon'] == 'Lego':
        weapon['Flat Damage'] = 0
        weapon['Roll Damage'] = '6D4'
        weapon['Damage Type'] = 'Piercing'

    if weaponDescriptions[weapon['Weapon']]:
        weapon['Description'] = weaponDescriptions[weapon['Weapon']]
    weaponText = interactions.Embed(
        title="Chaos Gauntlet",
        url='https://nexustabletop.com',
        description='A chaotic weapon is pulled.',
        color=interactions.Color.blurple()
        )

    weaponText.add_field(name='Weapon', value=weapon['Weapon'], inline=True)
    weaponText.add_field(name='\u200b', value='\u200b', inline=True)
    weaponText.add_field(name='Range', value=weapon['Range'], inline=True)
    weaponText.add_field(name='Flat Damage', value=weapon['Flat Damage'], inline=True)
    weaponText.add_field(name='\u200b', value='\u200b', inline=True)
    weaponText.add_field(name='Roll Damage', value=weapon['Roll Damage'], inline=True)
    weaponText.add_field(name='Skill', value=weapon['Skill'], inline=True)
    weaponText.add_field(name='\u200b', value='\u200b', inline=True)
    weaponText.add_field(name='Skill Bonus', value=weapon['Skill Bonus'], inline=True)
    weaponText.add_field(name='Damage Class', value=weapon['Damage Class'], inline=True)
    weaponText.add_field(name='\u200b', value='\u200b', inline=True)
    weaponText.add_field(name='Damage Type', value=weapon['Damage Type'], inline=True)
    if 'Secondary Damage' in weapon:
        weaponText.add_field(name='Secondary Damage', value=weapon['Secondary Damage'], inline=True)
        weaponText.add_field(name='\u200b', value='\u200b', inline=True)
        weaponText.add_field(name='Corrosive Damage', value=weapon['Corrosive Damage'], inline=True)
    if 'Description' in weapon:
        weaponText.add_field(name='Description', value=weapon['Description'], inline=True)
    await ctx.send(embeds=weaponText)

@bot.command(
        name='roll',
        description='Rolls user-specified number of user-specified-sided dice.',
        scope=guilds,
        options=[
            interactions.Option(
                name='dice',
                description='Number of dice to roll.',
                required=True,
                type=interactions.OptionType.INTEGER,
                ),
            interactions.Option(
                name='sides',
                description='Number of sides each die has.',
                required=True,
                type=interactions.OptionType.INTEGER,
                ),
            interactions.Option(
                name='weakness',
                description='Decreases probability of wins.',
                required=False,
                type=interactions.OptionType.BOOLEAN,
                ),
            interactions.Option(
                name='weakness_factor',
                description='The level of Weakness to be applied.',
                required=False,
                type=interactions.OptionType.INTEGER,
                choices=[
                    interactions.Choice(
                        name='1',
                        value=1
                        ),
                    interactions.Choice(
                        name='2',
                        value=2
                        )
                    ]
                ),
            interactions.Option(
                name='strength',
                description='Increases probability of wins.',
                required=False,
                type=interactions.OptionType.BOOLEAN,
                ),
            interactions.Option(
                name='strength_factor',
                description='The level of Strength to be applied.',
                required=False,
                type=interactions.OptionType.INTEGER,
                choices=[
                    interactions.Choice(
                        name='1',
                        value=1
                        ),
                    interactions.Choice(
                        name='2',
                        value=2
                        )
                    ]
                )
            ]
        )
async def _roll(ctx: interactions.CommandContext, dice, sides, strength = None, strength_factor = None, weakness = None, weakness_factor = None):
    rollText = interactions.Embed(
        title="Roll Dice",
        url='https://nexustabletop.com',
        description='Rolls a user-specified number of user-specified-sided dice. Can include a Strength factor.',
        color=interactions.Color.blurple()
            )
    rolls = []
    rollText.add_field(name="Number of Dice", value=dice, inline=True)
    rollText.add_field(name="Number of Sides per Dice", value=sides, inline=True)
    rollText.add_field(name='\u200b', value='\u200b', inline=True)
    for i in range(dice):
        rolls.append(random.randint(1, sides))
    if sides == 6:
        wins = 0
        if strength and strength_factor:
            if strength_factor == 2:
                for val in rolls:
                    if val == 2 or val == 3 or val == 4 or val == 5 or val == 6:
                        wins += 1
            elif strength_factor == 1:
                for val in rolls:
                    if val == 3 or val == 4 or val == 5 or val == 6:
                        wins += 1
        elif weakness and weakness_factor:
            if weakness_factor == 2:
                for val in rolls:
                    if val == 6:
                        wins += 1
            elif weakness_factor == 1:
                for val in rolls:
                    if val == 5 or val == 6:
                        wins += 1
        else:
            for val in rolls:
                if val == 4 or val == 5 or val == 6:
                    wins += 1
        if wins == dice and dice >= 5:
            wins = floor(wins * 1.5)
            rollText.add_field(name='Critical wins!', value=wins, inline=True)
        else:
            rollText.add_field(name='Total Wins', value=wins, inline=True)
    rollText.add_field(name='Rolls', value=str(rolls), inline=True)
    rollText.add_field(name='\u200b', value='\u200b', inline=True)
    await ctx.send(embeds=rollText)

@bot.command(
        name='skill',
        description='Rolls a user-specified number of six-sided dice and a twenty-sided die. Optional Strength factor.',
        scope=guilds,
        options=[
            interactions.Option(
                name='dice',
                description='Number of dice to roll.',
                required=True,
                type=interactions.OptionType.INTEGER,
                ),
            interactions.Option(
                name='strength',
                description='Increases probability of wins.',
                required=False,
                type=interactions.OptionType.BOOLEAN,
                ),
            interactions.Option(
                name='strength_factor',
                description='The level of Strength to be applied.',
                required=False,
                type=interactions.OptionType.INTEGER,
                choices=[
                    interactions.Choice(
                        name='1',
                        value=1
                        ),
                    interactions.Choice(
                        name='2',
                        value=2
                        )
                    ]
                )
            ]
        )
async def _skill(ctx: interactions.CommandContext, dice, strength = None, strength_factor = None):
    rollText = interactions.Embed(
        title="Use Skill",
        url='https://nexustabletop.com',
        description='Rolls a user-specified number of user-specified-sided dice. Can include a Strength factor.',
        color=interactions.Color.blurple()
            )
    rolls = []
    d20Roll = random.randint(1, 20)
    for i in range(dice):
        rolls.append(random.randint(1, 6))
    if d20Roll == 20:
        rollText.add_field(name="D20 Roll", value=str(d20Roll) + " | **Nat 20**", inline=True)
    elif d20Roll == 1:
        rollText.add_field(name="D20 Roll", value=str(d20Roll) + " | *Oof...*", inline=True)
    else:
        rollText.add_field(name='D20 Roll', value=d20Roll, inline=True)
    rollText.add_field(name='D6 Rolls', value=str(rolls), inline=True)
    rollText.add_field(name='\u200b', value='\u200b', inline=True)
    wins = 0
    if strength:
        if strength_factor:
            if strength_factor == 2:
                for roll in rolls:
                    if roll == 2 or roll == 3 or roll == 4 or roll == 5 or roll == 6:
                        wins += 1
            else:
                for roll in rolls:
                    if roll == 3 or roll == 4 or roll == 5 or roll == 6:
                        wins += 1
        else:
            for roll in rolls:
                if roll == 3 or roll == 4 or roll == 5 or roll == 6:
                    wins += 1
    else:
        for roll in rolls:
            if roll == 4 or roll == 5 or roll == 6:
                wins += 1
    if wins == dice and dice >= 5:
        wins = floor(wins * 1.5)
        rollText.add_field(name='Wins', value=str(wins) + ' | **Critical!**', inline=True)
    else:
        rollText.add_field(name='Wins', value=wins, inline=True)
    rollText.add_field(name='Total', value=d20Roll + wins, inline=True)
    rollText.add_field(name='\u200b', value='\u200b', inline=True)
    await ctx.send(embeds=rollText)

@bot.command(
        name='damage',
        description='Calculates total damage of rolls plus flat damage if there is any.',
        scope=guilds,
        options=[
            interactions.Option(
                name='flat_damage',
                description='Additional Flat Damage to add.',
                required=False,
                type=interactions.OptionType.INTEGER,
                ),
            interactions.Option(
                name='dice',
                description='Number of six-sided dice to roll when calculating total damage.',
                required=False,
                type=interactions.OptionType.INTEGER,
                )
            ]
        )
async def _damage(ctx: interactions.CommandContext, flat_damage = None, dice = None):
    damage=interactions.Embed(
        title="Damage Calculator",
        url='https://nexustabletop.com',
        description='Calculates the total damage of all 6-sided rolls plus flat damage.',
        color=interactions.Color.blurple()
    )
    totalDamage = 0
    if flat_damage or dice:
        if flat_damage:
            totalDamage += flat_damage
        if dice:
            rolls = []
            for i in range(dice):
                ranRoll = random.randint(1, 6)
                rolls.append(ranRoll)
                totalDamage += ranRoll
        damage.add_field(name='Total Damage', value=totalDamage, inline=False)
        if dice:
            damage.add_field(name='D6 rolls', value=str(rolls), inline=False)
        await ctx.send(embeds=damage)
    else:
        damage.add_field(name='Syntax Error', value='Must include flat damage and/or number of dice to roll.')
        await ctx.send(embeds=damage)

@bot.command(
        name='npc',
        description='Generates a random NPC.',
        scope=guilds,
        options=[
            interactions.Option(
                name="race",
                description="Specify Race",
                required=False,
                type=interactions.OptionType.STRING
            ),
            interactions.Option(
                name="gender",
                description="Specify Gender",
                required=False,
                type=interactions.OptionType.STRING,
                choices=[
                    interactions.Choice(
                        name="Male",
                        value="Male"
                    ),
                    interactions.Choice(
                        name="Female",
                        value="Female"
                    ),
                    interactions.Choice(
                        name="Omni",
                        value="Omni"
                    ),
                ]
            )
        ]
        )
async def _npc(ctx: interactions.CommandContext, race = None, gender = None):
    if race and gender:
        randomNPC = generateNPC(race, gender)
    elif race:
        randomNPC = generateNPC(race=race)
    elif gender:
        randomNPC = generateNPC(gender=gender)
    else:
        randomNPC = generateNPC()

    npc=interactions.Embed(
        title="Random NPC Generator",
        url='https://nexustabletop.com',
        description='Generates a random NPC. Can specify race, gender, and galaxy they\'re from',
        color=interactions.Color.blurple()
    )
    npc.add_field(name='Name', value='Billy Bob Thorton', inline=False)
    npc.add_field(name='Race', value=randomNPC, inline=False)
    await ctx.send(embeds=npc)

bot.start()
