import requests
from bs4 import BeautifulSoup

# Cricbuzz live score URL
URL = "https://www.cricbuzz.com/cricket-match/live-scores"

def fetch_scores():
    response = requests.get(URL, headers={"User-Agent": "Mozilla/5.0"})
    
    if response.status_code != 200:
        return "Failed to fetch scores"
    
    soup = BeautifulSoup(response.text, "html.parser")
    
    # Find all match containers
    matches = soup.find_all("div", class_="cb-lv-scr-mtch-hdr")  # Match name
    scores = soup.find_all("div", class_="cb-lv-scrs-col")  # Score data
    
    if not matches or not scores:
        return "No live matches found!"

    live_matches = []
    for match, score in zip(matches, scores):
        match_name = match.get_text(strip=True)
        match_score = score.get_text(strip=True)
        live_matches.append((match_name, match_score))

    return live_matches

# Run and print all live matches
if __name__ == "__main__":
    scores = fetch_scores()
    
    if isinstance(scores, str):
        print(scores)
    else:
        print("\nLive Matches:")
        for i, (match, score) in enumerate(scores):
            print(f"{i+1}. {match} - {score}")

        # Select a match manually (optional)
        choice = int(input("\nEnter match number to track (or 0 to exit): ")) - 1
        if 0 <= choice < len(scores):
            print(f"\nTracking: {scores[choice][0]} - {scores[choice][1]}")
        else:
            print("Exited.")
