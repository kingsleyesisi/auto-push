#!/usr/bin/env python
# coding:utf-8
#   |                                                          |
# --+----------------------------------------------------------+--
#   |   Code by : kingsleyesisi                                |
#   |   Email   : kingsleyesisi@yahoo.com                      |
#   |   Github  : https://github.com/kingsleyesisi             |
# --+----------------------------------------------------------+--  
# --+----------------------------------------------------------+--
#   |                                                          |

#START{
# IMPORT
import requests
import os
import time
from base64 import b64encode
from hexor import *
from dotenv import load_dotenv


load_dotenv()
# Read configuration from environment variables
username = os.getenv('GITHUB_USERNAME') or os.getenv('USERNAME')
token    = os.getenv('GITHUB_TOKEN') or os.getenv('TOKEN')

if not username or not token:
    print("Error: Missing GITHUB_USERNAME or TOKEN in environment.")
    exit(1)

p1 = hexor(False, "hex")

# RESPONE AUTH
HEADERS = {"Authorization": "Basic " + b64encode(f"{username}:{token}".encode('utf-8')).decode('utf-8')}
res = requests.get("https://api.github.com/user", headers=HEADERS)
if res.status_code != 200:
    p1.c("Failure to Authenticate! Please check PersonalAccessToken and Username!", "#ff0000")
    exit(1)
else:
    p1.c("Authentication Succeeded!", "#22a701")

# SESSION HEADER
sesh = requests.session()
sesh.headers.update(HEADERS)

def following_new(new_users):
    new_list = new_users.copy()
    print("Starting to Follow Users...")
    for user in new_users:
        time.sleep(2)
        res = sesh.put(f"https://api.github.com/user/following/{user}")
        if res.status_code != 204:
            print("Rate-limited, please wait until it finish!")
            time.sleep(60)
        else:
            print(f"Start Following: {user}")
            new_list.remove(user)
    with open("new_users_list.txt", "w") as f:
        for user in new_list:
            f.write(user + "\n")

# Load users and follow
new_users = []
try:
    with open("new_users_list.txt") as file_in:
        new_users = [line.strip() for line in file_in]
    if new_users:
        following_new(new_users)
except FileNotFoundError:
    print("new_users_list.txt not found.")
