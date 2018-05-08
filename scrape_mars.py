import time
import pandas as pd
import requests
import pymongo
from splinter import Browser
from bs4 import BeautifulSoup
from selenium import webdriver


def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    executable_path = {'executable_path': 'chromedriver'}
    browser = Browser('chrome', **executable_path, headless=False)


def scrape():
    browser = init_browser()
    # create surf_data dict that we can insert into mongo
    mars_data = {}
    hemisphere_image_urls = []
    # visit nasa
    news_url = 'https://mars.nasa.gov/news/'
    browser.visit(news_url)
    time.sleep(1)

    html = browser.html
    news_soup = BeautifulSoup(html, 'html.parser')
    results = news_soup.find_all('div', class_='grid_layout')
    news_title = result.find('div', class_='content_title').text
    news_p = result.find('div', class_='rollover_description_inner').text

    # add title and p to mars data with a key of news_title and news_p
    mars_data["news_title"] = news_title
    mars_data["news_p"] = news_p

    # visit jpl
    img_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(img_url)
    time.sleep(1)

    # get new html from jpl
    html = browser.html
    img_soup = BeautifulSoup(html, 'html.parser')
    image = soup.find('div', class_='carousel_items')
    image_url = image.article['style']
    # Formatting string
    url = image_url.split('/s')[-1].split('.')[0]
    # Define jpl.nasa as a VAR
    base_url = 'https://www.jpl.nasa.gov'
    # Build jpg URL
    featured_image_url = base_url + '/s' + url + '.jpg'
    mars_data["featured_image_url"] = featured_image_url

    # visit twitter
    twitter_url = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(twitter_url)
    time.sleep(1)
    html = browser.html
    weather_soup = BeautifulSoup(html, 'html.parser')
    weather = weather_soup.find('div', class_='js-tweet-text-container')
    mars_weather = weather.p.text
    # send data to database
    mars_data["mars_weather"] = mars_weather

    # visit space-facts
    facts_url = 'https://space-facts.com/mars/'
    facts = pd.read_html(facts_url)
    df = facts[0]
    df.columns = ['Mars Planet Profile', 'Value']
    mars_data["mars_facts"] = Table

    # visit astrogeology
    astrogeology_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    # Define a list stored four hemisphere
    hemisphere_list = []

    # Web Scraping
    executable_path = {'executable_path': 'chromedriver'}
    browser = Browser('chrome', **executable_path, headless=False)
    # Write a for-loop attempt to get all hemisphere url
    for i in range(4):
        images = browser.find_by_tag('h3')
        images[i].click()
        html = browser.html
        hem_soup = BeautifulSoup(html, 'html.parser')
        partial = hem_soup.find('img', class_='wide-image')['src']
        # Get the title for each hemisphere
        image_title = hem_soup.find('h2', class_='title').text
        img_url = 'https://astrogeology.usgs.gov' + partial
        dictionary = {"title": img_title, "img_url": img_url}
        # Append url and title to hemisphere_list
        hemisphere_list.append(dictionary)

        mars_data["mars_hemisphere"] = hemisphere_list

        browser.back()
