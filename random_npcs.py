#!/usr/bin/env python3
from os import name, system

def clear():
    if name == 'nt':
        system('cls')
    else:
        system('clear')

# 'Halfbreed': [0, 1, 2, 3], # 25% chance of being a halfbreed (if 

races = {
        'Arachni': {
            'Halfbreeds': None,
            'Origin': 'Andromeda',
            'Eye Color': ['Purple', 'Blue', 'Green', 'Grey', 'Tan', 'Black', 'White', 'Bronze'],
            'Skin Tone': ['Alabaster White', 'Ghost White', 'Shadow Black', 'Grey', 'Pale White', 'Fair', 'Medium Brown', 'Light Brown', 'Olive', 'Dark Brown', 'Black'],
            'Sub Species': ['Steel Weaver', 'Silk Weaver', 'Mind Weaver', 'Life Weaver'],    # Always one.
            'Species Features': ['Wolf Spider', 'Widow Spider', ],      # Always
            'Age': [0, 1100], # Average age is 1000, max is average + 10%
            'Gender': ['Male', 'Female'],
            'Height': [0, 81],
#           'Hair Style': ,
            },
        'Bedozite': {
#           'Halfbreeds': , # Can be halfbred with anything.
            'Origin': 'Milkyway',
            'Eye Color': ['Grey', 'Blue', 'Silver', 'Gold'],
            'Skin Tone': ['Grey', 'Ghost White', 'Dark Grey'],
            'Special Features': None,
            'Age': [0, 120],
            'Gender': ['Omni', 'Male', 'Female'],
            'Height': [0, 83],
#           'Hair Style': ,
            },
        'Corein': {
            'Halfbreeds': ['Humanoid'],
            'Origin': 'Milkyway',
            'Eye Color': ['Shock Blue', 'Glowing Gold', 'Shimmering Silver', 'Brilliant Bronze'],
#           'Skin Tone': [],
            'Special Features': 'Energy Colors - Matching Eyes',
            'Age': [0, 1300],
            'Gender': ['Male', 'Female'],
            'Height': [0, 84],
#           'Hair Style': ,
            },
        'Cryolite': {

            },
        'Dek': {

            },
        'Deltan': {

            },
        'Deovian': {

            },
        'Dey-Dren': {

            },
        'Draen': {

            },
        'Drah-Ken': {

            },
        'Drake': {

            },
        'Galigochun': {

            },
        'Genoan': {

            },
        'Haja': {

            },
        'Human': {

            },
        'K-9-5': {

            },
        'KiilKisaali': {

            },
        'Kyzen': {

            },
        'Leshei': {

            },
        'Locust': {

            },
        'Lorek': {

            },
        'Lova': {

            },
        'Magrunn': {

            },
        'Marquen': {

            },
        'Minorian': {

            },
        'Nehzae': {

            },
        'Nempetaket': {

            },
        'Omegan': {

            },
        'Prakkum': {

            },
        'Protian': {

            },
        'Quadrec': {

            },
        'Radrian': {

            },
        'Scenth': {

            },
        'ShenJen': {

            },
        'Soleran': {

            },
        'Tabbron': {

            },
        'Turi': {

            },
        'Unavali': {

            },
        'Ureon': {

            },
        'Varufahr': {

            },
        'Venturi': {

            },
        'Vuultaro': {

            },
        'Xalos': {

            },
        'Xavlian': {

            },
        'Zakon': {

            },
        'Zelion': {

            },
        'Zelokar': {

            },
}
