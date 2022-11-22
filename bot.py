#!/usr/bin/env python3
# Modules
import discord
import time
import platform
from discord import app_commands
from discord.ext import commands
from os import name, system, getenv
from math import floor
from bs4 import BeautifulSoup
from colorama import Back, Fore, Style
from typing import Literal
# Local file data
import random
import random_npcs
from secret import discord_token, guilds
from weapons import weapons
from descriptions import weaponDescriptions

class aclient(discord.Client):
    def __init__(self):
        super().__init__(intents=discord.Intents.default())
        self.synced = False

    async def on_ready(self):
        await self.wait_until_ready()
        if not self.synced:
            synced = await tree.sync()
            # For testing
            # synced = await tree.sync(guild = discord.Object(id = guilds[0]))
            self.synced = True
        prfx = (Back.BLACK + Fore.GREEN + time.strftime("%H:%M:%S UTC", time.gmtime())+ Back.RESET + Fore.WHITE + Style.BRIGHT)
        print(prfx + ' Logged in as ' + Fore.YELLOW + client.user.name)
        print(prfx + ' Bot ID ' + Fore.YELLOW + str(client.user.id))
        print(prfx + ' Discord Version ' + Fore.YELLOW + discord.__version__)
        print(prfx + ' Python Version ' + Fore.YELLOW + str(platform.python_version()))
        print(prfx + ' Slash CMDs Synced ' + Fore.YELLOW + str(len(synced)) + ' Commands')
        print('Synced Apps:')
        for app in synced:
            print('\t- ' + str(app))
        print('All ready!')


client = aclient()
tree = app_commands.CommandTree(client)

# Purely for testing changes
# @tree.command(
#         name = 'test',
#         description = 'Test',
#         guild = discord.Object(id = guilds[0])
#     )
# async def self(interaction: discord.Interaction, dice: int, sides: discord.Member=None):
#     await interaction.response.send_message(content = f'You rolled {dice} dice.')


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

@tree.command(
        name='chaosgauntlet',
        description='Reach through and pull a weapon from a dimension of chaos.',
        # guild = discord.Object(id = guilds[0])
    )
async def self(interaction: discord.Interaction):
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
    weaponText = discord.Embed(
        title="Chaos Gauntlet",
        url='https://nexustabletop.com',
        description='A chaotic weapon is pulled.',
        color=discord.Color.blurple()
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
    await interaction.response.send_message(embed=weaponText)

@tree.command(
        name='roll',
        description='Rolls user-specified number of user-specified-sided dice.',
        # guild = discord.Object(id = guilds[0])
    )
async def self(interaction: discord.Interaction, dice: int, sides: int, attribute:Literal['Strength', 'Weakness'] = None, attribute_factor: Literal[1, 2] = None):
    rollText = discord.Embed(
        title="Roll Dice",
        url='https://nexustabletop.com',
        description='Rolls a user-specified number of user-specified-sided dice. Can include a Strength factor.',
        color=discord.Color.blurple()
            )
    rolls = []
    rollText.add_field(name="Number of Dice", value=dice, inline=True)
    rollText.add_field(name="Number of Sides per Dice", value=sides, inline=True)
    rollText.add_field(name='\u200b', value='\u200b', inline=True)
    for i in range(dice):
        rolls.append(random.randint(1, sides))
    if sides == 6:
        wins = 0
        if attribute:
            rollText.add_field(name='Attribute', value=attribute.capitalize(), inline=True)
            if attribute_factor == 2:
                rollText.add_field(name='Modifier', value=2, inline=True)
                if attribute == 'Weakness':
                    for val in rolls:
                        if val == 6:
                            wins += 1
                else:
                    for val in rolls:
                        if 2 <= val <= 6:
                            wins += 1
            else:
                rollText.add_field(name='Modifier', value=1, inline=True)
                if attribute == 'Weakness':
                    for val in rolls:
                        if 5 <= val <= 6:
                            wins += 1
                else:
                    for val in rolls:
                        if 3 <= val <= 6:
                            wins += 1
            rollText.add_field(name='\u200b', value='\u200b', inline=True)
        else:
            for val in rolls:
                if 4 <= val <= 6:
                    wins += 1
        if wins == dice and dice >= 5:
            wins = floor(wins * 1.5)
            rollText.add_field(name='Critical wins!', value=wins, inline=True)
        else:
            rollText.add_field(name='Total Wins', value=wins, inline=True)
    rollText.add_field(name='Rolls', value=str(rolls), inline=True)
    rollText.add_field(name='\u200b', value='\u200b', inline=True)
    await interaction.response.send_message(embed=rollText)

@tree.command(
        name='skill',
        description='Rolls a user-specified number of six-sided dice and a twenty-sided die. Optional Strength factor.',
        # guild = discord.Object(id = guilds[0])
    )
async def self(interaction: discord.Interaction, dice: int, strength: bool = None, strength_factor: Literal[1, 2] = None):
    rollText = discord.Embed(
        title="Use Skill",
        url='https://nexustabletop.com',
        description='Rolls a user-specified number of user-specified-sided dice. Can include a Strength factor.',
        color=discord.Color.blurple()
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
    await interaction.response.send_message(embed=rollText)

@tree.command(
        name='damage',
        description='Calculates total damage of rolls plus flat damage if there is any.',
        # guild = discord.Object(id = guilds[0])
    )
async def self(interaction: discord.Interaction, flat_damage: int = None, dice: int = None):
    damage=discord.Embed(
        title="Damage Calculator",
        url='https://nexustabletop.com',
        description='Calculates the total damage of all 6-sided rolls plus flat damage.',
        color=discord.Color.blurple()
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
        await interaction.response.send_message(embed=damage)
    else:
        damage.add_field(name='Syntax Error', value='Must include flat damage and/or number of dice to roll.')
        await interaction.response.send_message(embed=damage)

@tree.command(
        name='npc',
        description='Generates a random NPC.',
        # guild = discord.Object(id = guilds[0])
    )
async def self(interaction: discord.Interaction, race: str = None, gender: Literal['Male', 'Female', 'Omni'] = None):
    if race and gender:
        randomNPC = generateNPC(race, gender)
    elif race:
        randomNPC = generateNPC(race=race)
    elif gender:
        randomNPC = generateNPC(gender=gender)
    else:
        randomNPC = generateNPC()

    npc=discord.Embed(
        title="Random NPC Generator",
        url='https://nexustabletop.com',
        description='Generates a random NPC. Can specify race, gender, and galaxy they\'re from',
        color=discord.Color.blurple()
    )
    npc.add_field(name='Name', value='Billy Bob Thorton', inline=False)
    npc.add_field(name='Race', value=randomNPC, inline=False)
    await interaction.response.send_message(embed=npc)

client.run(discord_token)
