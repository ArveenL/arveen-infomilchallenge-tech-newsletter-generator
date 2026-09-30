import feedparser
from bs4 import BeautifulSoup

rss_url = "https://devblogs.microsoft.com/dotnet/feed/"
feed = feedparser.parse(rss_url)


print("🕺🏽 Infomil Tech Newsletter Generator 🫈")
print()

articles = []

article_id = 1

for article in feed.entries:
    article_data = {}
    article_data["id"] = article_id
    article_data["source"] = "Microsoft .NET Blog"
    article_data["category"] = ".NET"
    article_data["relevance_score"] = 0
    article_data["title"] = article.title
    article_data["link"] = article.link
    article_data["published"] = article.published
    soup = BeautifulSoup(article.summary, "html.parser")
    article_data["summary"] = soup.get_text(" ", strip=True)
    articles.append(article_data)

    article_id += 1

    print (article.title)
    print (article.link)
    print (article.published)
    print ("-" * 50)
    print()




