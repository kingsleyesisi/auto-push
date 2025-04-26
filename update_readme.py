#!/usr/bin/env python
# coding:utf-8

import os
import sys
import requests
from datetime import datetime
import json
from hexor import hexor
from dotenv import load_dotenv


load_dotenv()
# Read configuration from environment variables
USERNAME = os.getenv('GITHUB_USERNAME') or os.getenv('USERNAME')
TOKEN    = os.getenv('GITHUB_TOKEN') or os.getenv('TOKEN')

print(f'USERNAME: {USERNAME}')
print(f'TOKEN: {TOKEN}')

if not USERNAME or not TOKEN:
    print("Error: Please set GITHUB_USERNAME and GITHUB_TOKEN environment variables.")
    sys.exit(1)

p1 = hexor(False, "hex")

# Set up headers for GitHub API requests
HEADERS = {
    "Authorization": f"token {TOKEN}",
    "Accept":        "application/vnd.github.v3+json",
    "User-Agent":    "github-followers-bot"
}

def check_auth():
    response = requests.get("https://api.github.com/user", headers=HEADERS)
    if response.status_code != 200:
        message = response.json().get('message', '')
        p1.c(f"Auth failed ({response.status_code}): {message}", "#ff0000")
        sys.exit(1)
    else:
        p1.c("Authentication Succeeded!", "#22a701")

check_auth()

# Start a session
session = requests.Session()
session.headers.update(HEADERS)

def fetch_followers(user, per_page=100):
    page = 1
    followers = []
    while True:
        response = session.get(
            f"https://api.github.com/users/{user}/followers",
            params={"per_page": per_page, "page": page}
        )
        if response.status_code != 200:
            p1.c(f"Error fetching page {page}: {response.status_code}", "#ff0000")
            break
        batch = response.json()
        if not batch:
            break
        for u in batch:
            followers.append((u["login"], u["avatar_url"]))
        page += 1
    print(f"Total Followers Collected: {len(followers)}")
    return followers

followers_info = fetch_followers(USERNAME)

# Write README.md
now = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
with open("README.md", "w", encoding="utf-8") as f:
    f.write(f"""# Auto Push - make it all Green \n\n""")
    f.write("""# The Auto Push repository is designed to automate the process of updating a file content, following and unfollowing user in your github and pushing the changes directly to a GitHub repository. " \
        This project is written entirely in Python and leverages GitHub's API and Git commands to perform these operations. The repository is a great tool for developers, data analysts, or system administrators and for those who want's to keep a sterdy streaks and all green on their github contribution graph.\n\n""")
    f.write("<h1>My Followers:</h1><br>\n")
    for username, avatar in followers_info:
        f.write(
            f'<a href="https://github.com/{username}">'
            f'<img src="{avatar}" alt="{username}" style="height:50px;width:50px;"/></a>\n'
        )
    f.write(f"<br><h4>Last update: {now} (UTC)</h4><br>\n")

# Write JSON dataset
with open("Dataset.json", "w", encoding="utf-8") as f:
    json.dump(followers_info, f, indent=2)

print("Done. Check README.md and Dataset.json.")
