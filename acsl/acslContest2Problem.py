import math
import os
import random
import re
import sys

def verifyPlate(plate):
    # Write your code here
    letters = 0
    digits = 0
    dashes = 0
    spaces = 0
    character_list = []
    if len(plate) > 8:
        return "IV"
    plate = list(plate)
    for char in plate:
        if char == " ":
            spaces += 1
            character_list.append(" ")
        elif char == "-":
            dashes += 1
            character_list.append("d")
        elif char.isalpha():
            letters += 1
            character_list.append("a")
        elif char.isalpha() == False:
            digits += 1
            character_list.append("n") 
        else:
            return "IV"
            
    if character_list == ['n', 'n', 'n', 'n', 'n', 'n', 'n']:
        return "G7A"
    elif character_list == ['n', 'n', 'n', 'n', 'n', 'n']:
        return "G6A"
    elif character_list == ['a', 'a', 'a', 'd', 'n', 'n', 'n', 'a'] or character_list == ['a', 'a', 'a', 'd', 'a', 'n', 'n', 'n'] or character_list == ['a', 'a', 'a', 'd', 'n', 'a', 'n', 'n'] or character_list == ['a', 'a', 'a', 'd', 'n', 'n', 'a', 'n']:
        return "G7B"
    elif character_list == ['a', 'a', 'd', 'n', 'n', 'n', 'n', 'n']:
        return "G7E" 
    elif character_list == ['a', 'a', 'a', 'd', 'n', 'n', 'a'] or character_list == ['a', 'a', 'a', 'd', 'a', 'n', 'n'] or character_list == ['a', 'a', 'a', 'd', 'n', 'a', 'n']:
        return "G6B"
    elif character_list == ['n', 'n', 'n', 'd', 'a', 'a', 'a']:
        return "G6D"       
    elif character_list == ['a', 'a', 'a', 'd', 'n', 'n', 'n']:
        return "G6C"
    elif character_list == ['a', 'a', 'a', 'n', 'n', 'n', 'n']:
        return "G7D"
    elif character_list == ['n', 'n', 'n', 'n', 'a', 'a', 'a']:
        return "G7C"
    elif digits == 4 and letters == 3 and dashes == 0 and spaces == 0:
        return "G7F"
    elif (character_list[:2] == ['a', 'a']) and ((digits + letters) <= 7) and (dashes + spaces <= 1):
        return "V"
    else:
        return "IV"