import requests
from bs4 import BeautifulSoup
import time

# GitHub API details (Use a new secure token!)
GITHUB_TOKEN = "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"  
REPO_OWNER = "jeyanthangj2004"
REPO_NAME = "cricket"
DISCUSSION_ID = 2

# Cricbuzz URL for live scores
CRICBUZZ_URL = "https://www.cricbuzz.com/cricket-match/live-scores"

# Function to get the latest comment from GitHub discussion
def get_latest_comment():
    url = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/discussions/{DISCUSSION_ID}/comments"
    headers = {
        "Authorization": f"Bearer {GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3+json"
    }
    
    response = requests.get(url, headers=headers).json()
    
    if response and isinstance(response, list):
        return response[-1]["body"].strip().lower()  # Get last comment
    return ""

# Function to fetch live matches from Cricbuzz
def get_live_matches():
    response = requests.get(CRICBUZZ_URL)
    soup = BeautifulSoup(response.text, "html.parser")

    matches = []
    for match in soup.select(".cb-col.cb-col-100.cb-ltst-wgt-hdr"):
        title = match.select_one(".cb-col.cb-col-100.cb-mtch-tm").text.strip()
        link = "https://www.cricbuzz.com" + match.find("a")["href"]
        matches.append((title, link))

    return matches

# Function to fetch match details
def get_match_details(match_url):
    response = requests.get(match_url)
    soup = BeautifulSoup(response.text, "html.parser")

    # Get team scores
    score = soup.select_one(".cb-col.cb-col-100.cb-min-tm-scr").text.strip()

    # Get ball-by-ball commentary
    commentary = soup.select(".cb-col.cb-col-100.cb-com-ln")
    ball_by_ball = "\n".join([c.text.strip() for c in commentary[:5]])  # Last 5 balls

    return score, ball_by_ball

# Function to post comments to GitHub discussion
def post_to_github(comment_text):
    url = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/discussions/{DISCUSSION_ID}/comments"
    headers = {
        "Authorization": f"Bearer {GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3+json"
    }
    data = {"body": comment_text}
    requests.post(url, headers=headers, json=data)

# Main function to check discussion and fetch scores
def main():
    running = False

    while True:
        command = get_latest_comment()

        if command == "live" and not running:
            running = True
            post_to_github("Fetching live matches...")
            matches = get_live_matches()

            if matches:
                match_text = "\n".join([f"{i+1}. {m[0]}" for i, m in enumerate(matches)])
                post_to_github(f"Live Matches:\n{match_text}\nReply with the match number to get details.")

        elif command.isdigit() and running:
            match_index = int(command) - 1
            matches = get_live_matches()
            if 0 <= match_index < len(matches):
                match_url = matches[match_index][1]
                score, commentary = get_match_details(match_url)
                post_to_github(f"**{matches[match_index][0]}**\n{score}\n\nBall-by-ball:\n{commentary}")
            else:
                post_to_github("Invalid match number. Try again.")

        elif command == "stop" and running:
            running = False
            post_to_github("Stopped live updates.")

        time.sleep(10)  # Check GitHub discussion every 10 seconds

# Run the script
if __name__ == "__main__":
    main()
