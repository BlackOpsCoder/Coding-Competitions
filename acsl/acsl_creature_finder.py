import math
import os
import random
import re
import sys




#
# Complete the 'findCreature' function below.
#
# The function is expected to return a STRING.
# The function accepts following parameters:
#  1. STRING guess
#  2. STRING distance
#
def add_coordinate(x_coordinate, y_coordinate, coordinates, num_to_hex):
    coordinates.append((num_to_hex(x_coordinate), num_to_hex(y_coordinate)))
       
       
   
def hex_to_num(hex_char):
    return int(hex_char, 16)
           
                       
def num_to_hex(num):
    return "0123456789ABCDEF"[num]
def findCreature(guess, distance):
    # Write your code here
    coordinates = []
    guess = list(guess)
    guess = list(map(hex_to_num, guess))
    guess = list(map(int, guess))
    distance = int(distance, 16)
    distance_list = []
       
   
    for i in range(distance + 1):
        distance_list.append((i, distance - i))
   
    for a in range(len(distance_list)):
        x_coordinate = distance_list[a][0] + guess[0]
        y_coordinate = distance_list[a][1] + guess[1]
        if 0 <= x_coordinate <= 15 and 0 <= y_coordinate <= 15:
            add_coordinate(x_coordinate, y_coordinate, coordinates, num_to_hex)


           
    for b in range(len(distance_list)):            
        x_coordinate = guess[0] - distance_list[b][0]
        y_coordinate = guess[1] - distance_list[b][1]
        if 0 <= x_coordinate <= 15 and 0 <= y_coordinate <= 15:
            add_coordinate(x_coordinate, y_coordinate, coordinates, num_to_hex)


           
    for c in range(len(distance_list)):
        x_coordinate = distance_list[c][0] + guess[0]
        y_coordinate = guess[1] - distance_list[c][1]
        if 0 <= x_coordinate <= 15 and 0 <= y_coordinate <= 15:
            add_coordinate(x_coordinate, y_coordinate, coordinates, num_to_hex)
     
    for d in range(len(distance_list)):
        x_coordinate = guess[0] - distance_list[d][0]
        y_coordinate = distance_list[d][1] + guess[1]
        if 0 <= x_coordinate <= 15 and 0 <= y_coordinate <= 15:
            add_coordinate(x_coordinate, y_coordinate, coordinates, num_to_hex)


   
    coordinates = list(set(coordinates))  
    smallest = min(coordinates)            
    largest = max(coordinates)            
    return f"{smallest[0]}{smallest[1]} {largest[0]}{largest[1]}"