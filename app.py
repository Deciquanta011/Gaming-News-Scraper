from flask import Flask, request
from bs4 import BeautifulSoup
import requests
from datetime import datetime

app = Flask(__name__)

SOURCES = {
    "Rock Paper Shotgun": "https://www.rockpapershotgun.com/feed",
    "Eurogamer": "https://www.eurogamer.net/?format=rss",
    "PC Gamer": "https://www.pcgamer.com/rss/",
}

def get_news():
    headers = {"User-Agent": "Mozilla/5.0"}
    all_articles = []

    for source, url in SOURCES.items():
        try:
            response = requests.get(url, headers=headers, timeout=5)
            soup = BeautifulSoup(response.content, "lxml-xml")
            articles = soup.find_all("item")
            for article in articles[:8]:
                title = article.title.text if article.title else ""
                link = article.link.text if article.link else ""
                date = article.pubDate.text[:16] if article.pubDate else ""
                if title and link:
                    all_articles.append({
                        "title": title,
                        "link": link,
                        "date": date,
                        "source": source
                    })
        except:
            pass

    return all_articles

@app.route("/")
def home():
    query = request.args.get("q", "").lower()
    articles = get_news()

    if query:
        articles = [a for a in articles if query in a["title"].lower()]

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
            .time {{ color: #555; margin-bottom: 20px; }}
            .search-bar {{ display: flex; gap: 10px; margin-bottom: 30px; }}
            .search-bar input {{ flex: 1; padding: 12px; border-radius: 8px; border: none; background: #1a1a1a; color: white; font-size: 16px; }}
            .search-bar button {{ padding: 12px 24px; background: #00aaff; color: white; border: none; border-radius: 8px; cursor: pointer; font-size: 16px; }}
            .search-bar button:hover {{ background: #0088cc; }}
            .card {{ background: #1a1a1a; border-radius: 10px; padding: 20px; margin-bottom: 20px; }}
            .card h2 {{ font-size: 17px; margin-bottom: 8px; }}
            .card a {{ color: #00aaff; text-decoration: none; font-size: 14px; }}
            .card a:hover {{ text-decoration: underline; }}
            .meta {{ color: #555; font-size: 13px; margin-bottom: 8px; }}
            .source {{ background: #00aaff22; color: #00aaff; padding: 3px 8px; border-radius: 4px; font-size: 12px; margin-right: 8px; }}
            .no-results {{ color: #555; text-align: center; padding: 40px; }}
        </style>
    </head>
    <body>
        <h1>🎮 Gaming News</h1>
        <p class="time">Last updated: {time}</p>

        <div class="search-bar">
            <form method="get" style="display:flex; gap:10px; width:100%">
                <input type="text" name="q" placeholder="Search news..." value="{query}">
                <button type="submit">Search</button>
            </form>
        </div>
    """

    if not articles:
        html += '<p class="no-results">No articles found for your search.</p>'
    else:
        for article in articles:
            html += f"""
            <div class="card">
                <h2>{article['title']}</h2>
                <p class="meta">
                    <span class="source">{article['source']}</span>
                    📅 {article['date']}
                </p>
                <a href="{article['link']}" target="_blank">Read more →</a>
            </div>
            """

    html += f"""
        <p class="time" style="text-align:center; margin-top:20px;">
            Showing {len(articles)} articles from {len(SOURCES)} sources
        </p>
    </body></html>
    """

    return html

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)