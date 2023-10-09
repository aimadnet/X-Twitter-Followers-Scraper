import csv
import requests
from colorama import Fore, Style, init

TWTTRAPI_KEY = "XXXXXXXXXXXX" # get api key from https://twttrapi.com

field_names = ["id_str", "screen_name", "name", "followers_count", "friends_count"]

init(autoreset=True)
key_color = Fore.YELLOW + Style.BRIGHT
value_color = Fore.WHITE + Style.BRIGHT


print(f"""{Fore.CYAN + Style.BRIGHT}
			
   _  __    ______      ____                                _____                                
  | |/ /   / ____/___  / / /___ _      _____  __________   / ___/______________ _____  ___  _____
  |   /   / /_  / __ \/ / / __ \ | /| / / _ \/ ___/ ___/   \__ \/ ___/ ___/ __ `/ __ \/ _ \/ ___/
 /   |   / __/ / /_/ / / / /_/ / |/ |/ /  __/ /  (__  )   ___/ / /__/ /  / /_/ / /_/ /  __/ /    
/_/|_|  /_/    \____/_/_/\____/|__/|__/\___/_/  /____/   /____/\___/_/   \__,_/ .___/\___/_/     
                                                                             /_/                 

{Fore.WHITE + Style.BRIGHT}Scrape followers of any X/Twitter account	
{Fore.RED + Style.BRIGHT}by @aimadnet
			
""")

username = input("Enter username: ").strip()
max_followers = int(input("Enter max followers to scrape: "))

users = []

def get_followers(username, cursor=None):
	try:
		url = "https://twttrapi.p.rapidapi.com/user-followers"
		querystring = {"username":username}
		if cursor:
			querystring["cursor"] = cursor
		headers = {
			"X-RapidAPI-Key": TWTTRAPI_KEY,
			"X-RapidAPI-Host": "twttrapi.p.rapidapi.com",
		}
		response = requests.get(url, headers=headers, params=querystring)
		response = response.json()

		cursor = None
		for instruction in response["data"]["user"]["timeline_response"]["timeline"]["instructions"]:
			if instruction["__typename"] == "TimelineAddEntries":
				entries = instruction["entries"]
				for entry in entries:
					if len(users) >= max_followers:
						return False
					
					if entry["content"]["__typename"] == "TimelineTimelineItem":
						userInfo = entry["content"]["content"]["userResult"]["result"]["legacy"]
						screen_name = userInfo["screen_name"]
						user_id = userInfo["id_str"]
						print(f"{key_color}{user_id}: {value_color}{screen_name}")
						users.append({key: userInfo[key] for key in field_names})
														
					if entry["content"]["__typename"] == "TimelineTimelineCursor" and entry["content"]["cursorType"] == "Bottom":
						cursor = entry["content"]["value"]

		if cursor and "0|" not in cursor:
			get_followers(username, cursor)
			
	except:
		raise Exception("Can't scrape user followers.")

print(f"Scraping followers of {username}...")

get_followers(username)

print(f"Scraped {len(users)} followers")

csv_file = f"{username}-followers.csv"

with open(csv_file, mode='w', newline='') as file:
	writer = csv.DictWriter(file, fieldnames=field_names)
	writer.writeheader()
	for user in users:
		writer.writerow(user)

print(f"Data saved to {csv_file}")