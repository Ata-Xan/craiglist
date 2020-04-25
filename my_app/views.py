from urllib.parse import quote_plus

from django.shortcuts import render
from bs4 import BeautifulSoup
import requests
from .import models
import json
#from requests.compat import quote_plus

BASE_URL = "https://losangeles.craigslist.org/search/?query={}"

# Create your views here.
def home(request):
    return render(request, 'base.html')

def new_search(request):
    search = request.POST.get('search')
    models.Search.objects.create(search=search)
    print(BASE_URL.format(quote_plus(search)))
    response = requests.get(BASE_URL.format(search))
    # print(response.text)
    soup = BeautifulSoup(response.text, features="html.parser")
    post_title = soup.find_all('li',{'class':'result-row'})

    data = dict()

    print(len(post_title))

    i=0
    for element in post_title:
        ele = dict()
        ele['title']= element.find(class_="result-title").text
        ele['url']= element.find('a').get('href')

        if element.find('a').get('data-ids'):
            tempImages = f",{element.find('a').get('data-ids')}"
            ele['images'] = tempImages.split(",1:")
            ele['images'].remove(ele['images'][0])
            ele['images'] = ["https://images.craigslist.org/{}_300x300.jpg".format(x) for x in ele['images'] ]
        else:
            ele['images'] = "https://craigslist.org/images/peace.jpg"

        ele['price'] = element.find(class_='result-price').text if element.find(class_='result-price') is not None else "N/A"
        data.update({f'element{i}':ele})
        i+=1


    # for i,v in data.items():
    #     print(i)
    #     for x in v['images']:
    #         print(f"https://images.craigslist.org/{x}_300x300.jpg")

    stuff_for_frontend ={
        'search':search,
        'final_results':data,
    }
    return render(request, 'my_app/new_search.html', stuff_for_frontend)
