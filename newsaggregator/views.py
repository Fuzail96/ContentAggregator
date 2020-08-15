from django.shortcuts import render, redirect
import requests
from bs4 import BeautifulSoup
from newsaggregator.models import Article


def scrape(request):
    session = requests.session()
    session.headers = {'User-Agent':'Googlebot/2.1 (+http://www.google.com/bot.html)'}
    url1 = "https://www.forbes.com/real-estate/#75f106bd730e"
    url2 = "https://realtytimes.com/"
    u= [url1, url2]

    for url in u:
        if url==url1:
            content = session.get(url, verify = False).content
            soup = BeautifulSoup(content, "html.parser")


            for article in soup.find_all('article', {
                "class": "stream-item et-promoblock-removeable-item et-promoblock-star-item"}):
                main = article.find_all('a')[0]
                title = main.text.strip()
                link = main['href']
                new_article = Article()
                new_article.source = "Forbes"
                new_article.title = title
                new_article.url = link
                new_article.save()

        elif url==url2:
            content = session.get(url, verify=False).content
            soup = BeautifulSoup(content, "html.parser")

            for h3 in soup.find_all('h3', {"class":"sppb-article-title"}):
                main=h3.find_all('a')[0]
                title=main.text.strip()
                link=main['href']
                new_article = Article()
                new_article.source = "RealtyTimes"
                new_article.title = title
                new_article.url = link
                new_article.save()

    return redirect("/")


def news_list(request):
    articles1 = Article.objects.filter(source = "Forbes")[::-1]
    articles2 = Article.objects.filter(source = "RealtyTimes")[::-1]
    context = {
        'object_list': articles1,
        'objects': articles2
    }
    return render(request, "home.html", context)











