
# coding: utf-8

# In[1]:


# Dependencies
from splinter import Browser
from bs4 import BeautifulSoup
import requests
import pymongo
import pandas as pd


# In[2]:


# Initialize PyMongo to work with MongoDBs
conn = 'mongodb://localhost:27017'
client = pymongo.MongoClient(conn)


# In[3]:


# Define database and collection
db = client.nasa_db
collection = db.items


# In[4]:


# URL of page to be scraped
news_url = 'https://mars.nasa.gov/news/'

# Retrieve page with the requests module
response = requests.get(news_url)
# Create BeautifulSoup object; parse with 'lxml'
soup = BeautifulSoup(response.text, 'lxml')


# ### NASA Mars News

# In[5]:


# Examine the results, then determine element that contains sought info
results = soup.find_all('div', class_='grid_layout')

# Loop through returned results
for result in results:
    # Error handling
    try:
        # Identify and return title
        news_title = result.find('div', class_='content_title').text
        news_p = result.find('div', class_= 'rollover_description_inner').text

        # Run only if news title and news paragraph are available
        if (news_title and news_p):
            # Print results
            print('--------------------')
            print(news_title)
            print(news_p)

            # Dictionary to be inserted as a MongoDB document
            post = {
                'news_title': news_title,
                'news_p': news_p,
            }

            collection.insert_one(post)

    except:
        continue


# ### JPL Mars Space images - Featured Image

# In[6]:


# Dependencies
from splinter import Browser
from splinter.exceptions import ElementDoesNotExist


# In[7]:


# https://splinter.readthedocs.io/en/latest/drivers/chrome.html
get_ipython().system('which chromedriver')


# In[8]:


executable_path = {'executable_path': 'chromedriver'}
browser = Browser('chrome', **executable_path, headless=False)


# In[9]:


img_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
browser.visit(img_url)

html = browser.html
soup = BeautifulSoup(html, 'html.parser')


# In[10]:


image = soup.find('div', class_='carousel_items')
image_url = image.article['style']

# Formatting string
url = image_url.split('/s')[-1].split('.')[0]
# print (url)
# Define jpl.nasa as a VAR
base_url = 'https://www.jpl.nasa.gov'
# Build jpg URL
featured_image_url = base_url + '/s' + url + '.jpg'
# Print the result
print(featured_image_url)


# ### Mars Weather

# In[11]:


executable_path = {'executable_path': 'chromedriver'}
browser = Browser('chrome', **executable_path, headless=False)


# In[12]:


# Build url
url = 'https://twitter.com/marswxreport?lang=en'
browser.visit(url)

html = browser.html
soup = BeautifulSoup(html, 'html.parser')


# In[13]:


# 'js-tweet-text-container'
# Reference: https://stackoverflow.com/questions/48252610/web-scraper-isnt-filling-up-the-csv-file
weather = soup.find('div', class_='js-tweet-text-container')

mars_weather= weather.p.text
print(mars_weather)


# ### Mars Facts

# In[14]:


facts_url = 'https://space-facts.com/mars/'
facts = pd.read_html(facts_url)
facts


# In[15]:


# Get the type of facts
type(facts)


# In[17]:


# Convert data into DataFrame
df = facts[0]
df.columns = ['Mars Planet Profile', 'Value']
df


# In[18]:


# Generate HTML tables from DataFrames
html_table = df.to_html()
html_table


# In[19]:


# Strip unwanted newlines to clean up the table
html_table.replace('\n', '')
# Save the table to a file
df.to_html('table.html')


# ### Mars Hemisperes

# In[53]:


# Web Scraping
executable_path = {'executable_path': 'chromedriver'}
browser = Browser('chrome', **executable_path, headless=False)


# In[54]:


# Astrogeology url
astrogeology_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
browser.visit(astrogeology_url)


# In[56]:


# Define a list stored four hemisphere
hemisphere_list = []


# In[57]:


# Write a for-loop attempt to get all hemisphere url
for i in range (4):
    images = browser.find_by_tag('h3')
    images[i].click()
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    partial = soup.find('img', class_ = 'wide-image')['src']
    # Get the title for each hemisphere
    image_title = soup.find('h2', class_ = 'title').text
    image_url = 'https://astrogeology.usgs.gov'+ partial
    dictionary = {"title":img_title,"img_url":img_url}
    # Append url and title to hemisphere_list
    hemisphere_list.append(dictionary)
    browser.back()


# In[58]:


# Print the result
print(hemisphere_list)

