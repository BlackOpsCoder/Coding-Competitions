#!/bin/python3

import math
import os
import random
import re
import sys


#
# Complete the 'verifyPlate' function below.
#
# The function is expected to return a STRING.
# The function accepts STRING plate as parameter.
#

def verifyPlate(plate):
    letters_count = 0
    digits_count = 0
    dashes_count = 0
    spaces_count = 0
    plate_format_list = []
    # Invalid plate if length not between 2 and 8
    if len(plate) > 8 or len(plate) < 2:
        return "IV"
        
    plate = list(plate)
    
    for char in plate:
        if char == " ":
            spaces_count += 1
            plate_format_list.append(" ")
        elif char == "-":
            dashes_count += 1
            plate_format_list.append("d")
        elif char.isalpha():
            letters_count += 1
            plate_format_list.append("a")
        elif char.isdigit():
            digits_count += 1
            plate_format_list.append("n") 
        else:
            # Invalid plate if character other than letter, number, dash, and space
            return "IV"
    # Plate is invalid if there are more than one dashes/spaces   
    if dashes_count + spaces_count > 1:
        return "IV"
      
    if plate_format_list == ['n', 'n', 'n', 'n', 'n', 'n', 'n']:
        return "G7A"
    elif plate_format_list == ['n', 'n', 'n', 'n', 'n', 'n']:
        return "G6A"
    elif plate_format_list[:4] == ['a', 'a', 'a', 'd'] and sorted(plate_format_list[4:]) == ['a', 'n', 'n', 'n']:
        return "G7B"
    elif plate_format_list == ['a', 'a', 'd', 'n', 'n', 'n', 'n', 'n']:
        return "G7E" 
    elif plate_format_list[:4] == ['a', 'a', 'a', 'd'] and sorted(plate_format_list[4:]) == ['a', 'n', 'n']:
        return "G6B"
    elif plate_format_list == ['n', 'n', 'n', 'd', 'a', 'a', 'a']:
        return "G6D"       
    elif plate_format_list == ['a', 'a', 'a', 'd', 'n', 'n', 'n']:
        return "G6C"
    elif plate_format_list == ['a', 'a', 'a', 'n', 'n', 'n', 'n']:
        return "G7D"
    elif plate_format_list == ['n', 'n', 'n', 'n', 'a', 'a', 'a']:
        return "G7C"
    # G7F check should always be after the G7C and G7D checks
    elif digits_count == 4 and letters_count == 3 and dashes_count == 0 and spaces_count == 0:
        return "G7F"
    elif (plate_format_list[:2] == ['a', 'a']) and ((digits_count + letters_count) <= 7):
        return "V"
    else:
        return "IV"
       
              
    
        

if __name__ == '__main__':
    fptr = open(os.environ['OUTPUT_PATH'], 'w')

    plate = input()

    result = verifyPlate(plate)

    fptr.write(result + '\n')

    fptr.close()
