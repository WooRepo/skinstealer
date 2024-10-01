import os
import requests
import json
import base64
import time
import subprocess
import random
from tqdm import tqdm

# Function to generate random Minecraft usernames
def generate_usernames(n):
    prefixes = ["Epic", "Super", "Cool", "Crazy", "Mega", "Dark"]
    suffixes = ["123", "456", "789", "X", "Y", "Z"]
    return [f"{random.choice(prefixes)}{random.choice(suffixes)}{random.randint(1, 100)}" for _ in range(n)]

# Function to download skin
def download_skin(username):
    url = f"https://api.mojang.com/users/profiles/minecraft/{username}"
    response = requests.get(url)

    if response.status_code == 200:
        uuid = response.json().get('id')
        skin_url = f"https://sessionserver.mojang.com/session/minecraft/profile/{uuid}?unsigned=false"
        skin_response = requests.get(skin_url)

        if skin_response.status_code == 200:
            skin_data = skin_response.json()
            skin_value = skin_data['properties'][0]['value']
            skin_texture = json.loads(base64.b64decode(skin_value))
            skin_image_url = skin_texture['textures']['SKIN']['url']
            image_response = requests.get(skin_image_url)

            # Save the skin
            skin_file = f"{username}.png"
            with open(skin_file, 'wb') as f:
                f.write(image_response.content)
            print(f"Downloaded skin for {username} as {skin_file}")
            return skin_file
    return None

# Function to push changes to Git
def push_changes():
    subprocess.run(["git", "add", "."])
    subprocess.run(["git", "commit", "-m", "Update skins"])
    subprocess.run(["git", "push"])

# Number of usernames to generate
num_usernames = 10  # Adjust as needed
usernames = generate_usernames(num_usernames)

# Infinite loop to check skins
while True:
    for username in tqdm(usernames, desc="Downloading skins", unit="skin"):
        if download_skin(username):
            push_changes()  # Push after downloading each skin
    time.sleep(3600)  # Wait an hour before the next check
