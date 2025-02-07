from newspaper import Article

url = "https://www.bbc.com/news/articles/c1m5x1j3p2yo"

my_article = Article(url, language="en")

my_article.download()

my_article.parse()

print("Title:", my_article.title)

print('Authors:', my_article.authors)

print("Publishing date: ",my_article.publish_date)

print("Article text: ", my_article.text)