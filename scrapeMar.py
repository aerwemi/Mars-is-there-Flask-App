import time
from splinter import Browser
from bs4 import BeautifulSoup
import pandas as pd
from selenium import webdriver
import pandas as pd
import requests


def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    executable_path = {"executable_path": "chromedriver"}
    return Browser("chrome", **executable_path, headless=False)


def scrape():
    browser = init_browser()

    url = "https://mars.nasa.gov/news/"
    browser.visit(url)
    time.sleep(1)

    html = browser.html

    soup1 = BeautifulSoup(html, 'html.parser')
    latest_update=soup1.find('div', class_='list_text')

    news_targets=["list_date", "content_title", "article_teaser_body"]
    news_update={"list_date":"", "content_title":"", "article_teaser_body":""}

    # extracting latest news info to dict
    for i in news_targets:
        news_update[i] = latest_update.find('div', class_=i).text
    print('News Data Extracted')

    # Mars Space Images - Featured Image
    # URL of page to be scraped for images
    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'

    # Visit the URL
    browser.visit(url)
    time.sleep(2)

    # html from browser
    html = browser.html
    soup2 = BeautifulSoup(html, 'html.parser')

    featured=soup2.find('div', class_='image_and_description_container')

    lates_imges_update = featured.h3.text

    updates = news_update.copy()


    updates['featuredDate']=lates_imges_update
    print('featuredDate Extracted')
    ####

    latest_images=soup2.find_all('div', class_='image_and_description_container')
    #
    print('featured start')
    print('____')
    imgurl=[]
    imgs=[]
    for i in latest_images:
        try:
            if i.h3.text == lates_imges_update :
                #print(i.h3.text)
                img_loc="https://www.jpl.nasa.gov" + i.find('img', class_="thumb")['src']
                imgurl.append(img_loc)
                #browser_img.visit(img_loc)
                img_tit=latest_images[1].find('img', class_="thumb")['alt']
                imgs.append(img_tit)
        except:"AttributeError", 'NoneType'
    featuredImage=imgurl[0]
    updates['featuredImage']=featuredImage
    print('featured image Extracted')
    print(featuredImage)

    # Mars Weather
    print('Weather extracting started')

    # URL of page to be scraped
    url = 'https://twitter.com/marswxreport?lang=en'

    # Visit the URL
    browser.visit(url)
    time.sleep(1)

        # html from browser
    html = browser.html
    soup_Mars_weather= BeautifulSoup(html, 'html.parser')
    weathers=soup_Mars_weather.find_all('p', class_='TweetTextSize TweetTextSize--normal js-tweet-text tweet-text')

    marsWeathers=[]
    for i in range(len(weathers)):
        if 'pressure at' in weathers[i].text:
            marsWeathers.append(weathers[i].text)
    weather=marsWeathers[0]
    updates['weather']=weather

    #Mars Facts
    print('start of Facts')
    url="https://space-facts.com/mars/"
    marsFacts=pd.read_html(url)
    facts=marsFacts[0]
    facts.columns= ['fact', 'Number']
    facts=facts.set_index('fact')['Number'].to_dict()
    updates['facts']=facts
    print('end of Facts')

    # Mars 4 Images

    print('start the images of 4 sides')

    # URL of page to be scraped
    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'

    # Visit the URL
    browser.visit(url)
    time.sleep(5)

    # Scrape page into soup
    # html from browser
    html = browser.html
    images = BeautifulSoup(html, 'html.parser')

    imgs = images.find_all('img', class_='thumb')

    images=[]
    for i in range(0, len(imgs)):
        if imgs:
            a_tag = imgs[i].parent
            href = a_tag.get('href')
            url_ext = 'https://astrogeology.usgs.gov'
            img_urls = url_ext + href
            img_urls = img_urls.split()
        # print(img_urls)

        for img in img_urls:
            # print(img)
            sub_url = img
            dir_key=sub_url.split('/')[-1].split('_')[0]
            print(sub_url)
            dir_key
            executable_path = {'executable_path': 'chromedriver.exe'}
            browser = Browser('chrome', **executable_path, headless= False)
            browser.visit(sub_url)

            html = browser.html
            soup = BeautifulSoup(html, 'html.parser')

            image={}
            sub_imgs = soup.find_all('div', class_='downloads')
            for sub_img in sub_imgs:
                the_img = sub_img.find('a')['href']
                print(the_img)
                image[dir_key]=the_img
            images.append(image)
        response = requests.get(the_img, stream=True)

    updates['images']=images

    return updates
