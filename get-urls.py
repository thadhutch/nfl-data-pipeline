import requests
from bs4 import BeautifulSoup
import time

# Base URL structure
base_url = "https://www.pro-football-reference.com/years/{}/week_{}.htm"

# Years and weeks to loop through
start_year = 2015
end_year = 2023
max_week = 18

# Function to extract boxscores from a specific URL
def get_boxscores(year, week):
    url = base_url.format(year, week)
    response = requests.get(url)
    
    # Check if the page was successfully fetched
    if response.status_code != 200:
        print(f"Failed to fetch {url}")
        return []
    
    soup = BeautifulSoup(response.text, 'html.parser')
    boxscores = []
    
    # Find all td elements with class 'right gamelink'
    for gamelink in soup.find_all('td', class_='right gamelink'):
        a_tag = gamelink.find('a')
        if a_tag and 'href' in a_tag.attrs:
            boxscore_url = "https://www.pro-football-reference.com" + a_tag['href']
            boxscores.append(boxscore_url)
    
    return boxscores

# Main loop to gather boxscores
all_boxscores = []

for year in range(start_year, end_year + 1):
    # Determine the range of weeks to scrape based on the year
    max_weeks = max_week if year == end_year else 17  # Typically 17 weeks per year
    for week in range(1, max_weeks + 1):
        print(f"Scraping year {year}, week {week}...")
        boxscores = get_boxscores(year, week)
        print(f"Found {len(boxscores)} boxscores.")
        print(boxscores)
        all_boxscores.extend(boxscores)
        time.sleep(1)  # Add a small delay to avoid overwhelming the server

# Output the gathered boxscores
for boxscore in all_boxscores:
    print(boxscore)

# Optionally save the results to a file
with open('boxscores_urls.txt', 'w') as f:
    for boxscore in all_boxscores:
        f.write(boxscore + '\n')

print(f"Scraped {len(all_boxscores)} boxscores.")
