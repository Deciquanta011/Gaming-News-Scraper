from flask import Flask
from bs4 import BeautifulSoup
import requests
from datetime import datetime

app = Flask(__name__)

def get_news():
    url = "https://www.rockpapershotgun.com/feed"
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, "lxml-xml")
    articles = soup.find_all("item")
    
    news = []
    for article in articles[:10]:
        news.append({
            "title": article.title.text,
            "link": article.link.text,
            "date": article.pubDate.text[:16] if article.pubDate else ""
        })
    return news

@app.route("/")
def home():
    articles = get_news()
    time = datetime.now().strftime("%d %B %Y, %I:%M %p")
    
    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Gaming News</title>
        <style>
            * {{ margin: 0; padding: 0; box-sizing: border-box; }}
            body {{ background: #0d0d0d; color: white; font-family: Arial; padding: 40px; }}
            h1 {{ color: #00aaff; font-size: 36px; margin-bottom: 10px; }}
            .time {{ color: #555; margin-bottom: 40px; }}
            .card {{ background: #1a1a1a; border-radius: 10px; padding: 20px; margin-bottom: 20px; }}
            .card h2 {{ font-size: 18px; margin-bottom: 10px; }}
            .card a {{ color: #00aaff; text-decoration: none; font-size: 14px; }}
            .card a:hover {{ text-decoration: underline; }}
            .date {{ color: #555; font-size: 13px; margin-bottom: 8px; }}
        </style>
    </head>
    <body>
        <h1>🎮 Gaming News</h1>
        <p class="time">Last updated: {time}</p>
    """
    
    for i, article in enumerate(articles):
        html += f"""
        <div class="card">
            <h2>{i+1}. {article['title']}</h2>
            <p class="date">📅 {article['date']}</p>
            <a href="{article['link']}" target="_blank">Read more →</a>
        </div>
        """
    
    html += "</body></html>"
    return html

if __name__ == "__main__":
    app.run(debug=True)
    