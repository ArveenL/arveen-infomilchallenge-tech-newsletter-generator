import feedparser

rss_url = "https://devblogs.microsoft.com/dotnet/feed/"
feed = feedparser.parse(rss_url)


print("--> Infomil Tech Newsletter Generator <--")
print()

articles = []

for article in feed.entries:
    article_data = {}
    article_data["title"] = article.title
    article_data["link"] = article.link
    article_data["published"] = article.published
    articles.append(article_data)

    print (article.title)
    print (article.link)
    print (article.published)
    print ("-" * 50)
    print()

print(articles)

