import requests
from bs4 import BeautifulSoup

def get_gaming_news():
    # Rock Paper Shotgun - reliable RSS feed
    url = "https://www.rockpapershotgun.com/feed"
    headers = {"User-Agent": "Mozilla/5.0"}
    
    print("🎮 Latest Gaming News\n")
    print("-" * 40)
    
    response = requests.get(url, headers=headers)
    print("Status:", response.status_code)
    
    soup = BeautifulSoup(response.content, "lxml-xml")
    articles = soup.find_all("item")
    print("Articles found:", len(articles))
    
    for i, article in enumerate(articles[:10]):
        title = article.title.text
        link = article.link.text
        print(f"{i+1}. {title}")
        print(f"   {link}\n")

get_gaming_news()