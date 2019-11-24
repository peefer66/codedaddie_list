import requests
from requests.compat import quote_plus
from django.shortcuts import render
from bs4 import BeautifulSoup

from .models import Search

BASE_CRAIGLIST_URL='https://manchester.craigslist.org/search/?query={}'
BASE_IMAGE_URL = 'https://images.craigslist.org/{}_300x300.jpg'


def home(request):
    return render(request, 'base.html')

def new_search(request):
    # get search text from the front end
    search = request.POST.get('search')
    # create a search object
    Search.objects.create(search=search)
    # create the search url
    final_url = BASE_CRAIGLIST_URL.format(quote_plus(search))
    # get the url
    response = requests.get(final_url)
    # get the raw html
    data = response.text
    # create a BS object called soup
    soup = BeautifulSoup(data,features='html.parser')
    # find all the instances of results-row
    post_listings = soup.find_all('li',{'class':'result-row'})

    
    # list of tuples
    final_post = []
    # loop through post_lisings and appen to final post
    for post in post_listings:
        post_title = post.find(class_='result-title').text
        post_url = post.find('a').get('href')
        
        if  not post.find(class_='result-price'):
            post_price = 'N/A'
        else:
            post_price = post.find(class_='result-price').text

        if not post.find(class_='result-image gallery'):
            post_image_url = 'https://craigslist.org/images/peace.jpg'
        else:
            post_image_id =post.find(class_='result-image gallery').get('data-ids').split(':')[1].split(',')[0]
            post_image_url = BASE_IMAGE_URL.format(post_image_id)
              
        final_post.append((post_title, post_url, post_price, post_image_url))
    
    
    context = {
        'search':search,
        'final_post':final_post,
        }
    
    return render(request, 'my_app/new_search.html', context)