import time
import requests
import pymongo
import pandas as pd
from splinter import Browser
from bs4 import BeautifulSoup
from selenium import webdriver


def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    executable_path = {"executable_path": "chromedriver"}
    return Browser("chrome", **executable_path, headless=False)


def scrape():
    browser = init_browser()
    # create mars_data dict that we can insert into mongo
    mars_data = {}
    hemisphere_image_urls = []

    ##### visit mars.nasa.gov/news/ #####
    news_url = 'https://mars.nasa.gov/news/'
    browser.visit(news_url)
    time.sleep(1)

    html = browser.html
    # create a soup object from the html
    news_soup = BeautifulSoup(html, 'html.parser')
    result = news_soup.find('div', class_='content_title')
    news_title = result.next_element.get_text()
    result1 = news_soup.find('div', class_='article_teaser_body')
    news_p = result1.get_text()
    # transfer data into mars_data db
    mars_data["news_title"] = news_title
    mars_data["news_p"] = news_p

    # visit jpl to get spaceimages
    image_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(image_url)
    time.sleep(1)
    # grab our new html from jpl
    html = browser.html
    # create soup object from html
    image_soup = BeautifulSoup(html, "html.parser")
    image = image_soup.find('div', class_='carousel_items')

    image_url = image.article['style']

    url = image_url.split('/s')[-1].split('.')[0]

    featured_image_url = 'https://www.jpl.nasa.gov' + '/s' + url + '.jpg'
    # transfer data into mars_data db
    mars_data["featured_image_url"] = featured_image_url

    ##### visit https://twitter.com #####
    weather_url = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(weather_url)
    time.sleep(1)
    html = browser.html
    # create soup object from html
    weather_soup = BeautifulSoup(html, 'html.parser')
    weather = weather_soup.find('div', class_='js-tweet-text-container')

    mars_weather = weather.p.text
    # transfer data into mars_data db
    mars_data["mars_weather"] = mars_weather

    ##### visit space-facts.com/mars/ #####
    facts_url = 'http://space-facts.com/mars/'
    tables = pd.read_html(facts_url)
    tables
    df = tables[0]
    df.columns = ['Mars_planet_profile', 'Value']
    df
    mars_facts = df.to_dict('records')
    Table = []
    for i in range(0, len(mars_facts)):
        temp = list(mars_facts[i].values())
        Table.append(temp)
    mars_data["mars_facts"] = Table

    ##### visit astrogeology.usgs.gov #####
    hemisphere_urls = ['https://astrogeology.usgs.gov/search/map/Mars/Viking/cerberus_enhanced',
                       'https://astrogeology.usgs.gov/search/map/Mars/Viking/schiaparelli_enhanced',
                       'https://astrogeology.usgs.gov/search/map/Mars/Viking/syrtis_major_enhanced',
                       'https://astrogeology.usgs.gov/search/map/Mars/Viking/valles_marineris_enhanced']
    for url in hemisphere_urls:
        browser.visit(url)
        time.sleep(1)
        html = browser.html
        # create soup object from html
        hemisphere_soup = BeautifulSoup(html, 'html.parser')

        dictionary = {}
        hemipshere_title = hemisphere_soup.find('div', class_='content')
        dictionary["title"] = hemipshere_title.h2.text.lstrip()

        hemipshere_download = hemisphere_soup.find('div', class_='downloads')
        image = hemipshere_download.find('li')
        dictionary["image_url"] = image.find('a')['href']

        hemisphere_image_urls.append(dictionary)
    hemisphere_image_urls = list(hemisphere_image_urls)
    # transfer data into mars_data db
    mars_data["mars_hemisphere"] = hemisphere_image_urls

    # return mars_data
    return mars_data
