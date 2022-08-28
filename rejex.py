# Source for rental date: https://www.census.gov/data/tables/time-series/dec/coh-grossrents.html
# In my search for some average state data I could use, I came across this txt file that I thought
# would be a great opportunity to practice rejex. I aplogize that it's from 2000!!

# This module reads through a txt file with censne rental data and creates a dictionary 
# with the median rent for each state in the year 2000

import re

with open ('grossrents-adj.txt') as f:
    data = f.readlines()

pattern = re.compile("([A-Za-z]+\.?\s?[a-z]*\s?[A-Za-z]*)\s*\$([\d]{3})")

states_info = {}

for state in data:
    match = pattern.match(state)
    if match:
        states_info[match.group(1).strip().lower()] = int(match.group(2))

def state_rent(x):
    if x.lower() in states_info.keys():
        return states_info[x]
    print("state not found. redirecting")
    return False


