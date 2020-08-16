import requests
from bs4 import BeautifulSoup
from django.shortcuts import render, redirect

from newsaggregator.models import Article


def scrape(request):
    a1 = Article.objects.all()
    a1.delete()
    session = requests.session()
    session.headers = {'User-Agent': 'Googlebot/2.1 (+http://www.google.com/bot.html)'}
    url1 = "https://www.zillow.com/blog/"

    content1 = session.get(url1, verify=False).content
    soup = BeautifulSoup(content1, "html.parser")

    for article in soup.find_all('article', {"class": "post story"}):
        main1 = article.find_all('div', {"class": "col-sm-8"})[0]
        main2 = main1.find_all('h5', {"class": "post-title"})[0]
        main = main2.find_all('a')[0]
        title = main.text.strip()
        link = main["href"]
        new_article = Article()
        new_article.source = "Zillow"
        new_article.title = title
        new_article.url = link
        new_article.save()


    url2 = "https://realtytimes.com/"
    content2 = session.get(url2, verify=False).content
    soup2 = BeautifulSoup(content2, "html.parser")

    for h3 in soup2.find_all('h3', {"class": "sppb-article-title"}):
        main = h3.find_all('a')[0]
        title = main.text.strip()
        link = "https://realtytimes.com" + main["href"]
        new_article = Article()
        new_article.source = "RealtyTimes"
        new_article.title = title
        new_article.url = link
        new_article.save()

    return redirect("/")


def news_list(request):
    articles1 = Article.objects.filter(source="Zillow")[::-1]
    articles2 = Article.objects.filter(source="RealtyTimes")[::-1]
    context = {
        'object1': articles1,
        'object2': articles2
    }
    return render(request, "home.html", context)
