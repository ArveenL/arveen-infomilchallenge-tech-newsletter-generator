import feedparser

rss_url = "https://devblogs.microsoft.com/dotnet/feed/"
feed = feedparser.parse(rss_url)

print("Infomil Tech Newsletter Generator")

for article in feed.entries:
    print (article.title)
    print (article.link)
    print (article.published)
    print ("-" * 50)
    print()


