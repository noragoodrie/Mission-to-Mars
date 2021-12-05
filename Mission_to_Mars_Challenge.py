#!/usr/bin/env python
# coding: utf-8

# In[49]:


# Import Splinter, BeautifulSoup, and Pandas
from splinter import Browser
from bs4 import BeautifulSoup as soup
import pandas as pd
from webdriver_manager.chrome import ChromeDriverManager


# In[50]:


# Set the executable path and initialize Splinter
executable_path = {'executable_path': ChromeDriverManager().install()}
browser = Browser('chrome', **executable_path, headless=False)


# ### Visit the NASA Mars News Site

# In[51]:


# Visit the mars nasa news site
url = 'https://redplanetscience.com/'
browser.visit(url)

# Optional delay for loading the page
browser.is_element_present_by_css('div.list_text', wait_time=1)


# In[52]:


# Convert the browser html to a soup object and then quit the browser
html = browser.html
news_soup = soup(html, 'html.parser')

slide_elem = news_soup.select_one('div.list_text')


# In[53]:


slide_elem.find('div', class_='content_title')


# In[54]:


# Use the parent element to find the first a tag and save it as `news_title`
news_title = slide_elem.find('div', class_='content_title').get_text()
news_title


# In[55]:


# Use the parent element to find the paragraph text
news_p = slide_elem.find('div', class_='article_teaser_body').get_text()
news_p


# ### JPL Space Images Featured Image

# In[56]:


# Visit URL
url = 'https://spaceimages-mars.com'
browser.visit(url)


# In[57]:


# Find and click the full image button
full_image_elem = browser.find_by_tag('button')[1]
full_image_elem.click()


# In[58]:


# Parse the resulting html with soup
html = browser.html
img_soup = soup(html, 'html.parser')
img_soup


# In[59]:


# find the relative image url
img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')
img_url_rel


# In[60]:


# Use the base url to create an absolute url
img_url = f'https://spaceimages-mars.com/{img_url_rel}'
img_url


# ### Mars Facts

# In[61]:


df = pd.read_html('https://galaxyfacts-mars.com')[0]
df.head()


# In[62]:


df.columns=['Description', 'Mars', 'Earth']
df.set_index('Description', inplace=True)
df


# In[63]:


df.to_html()


# # D1: Scrape High-Resolution Mars’ Hemisphere Images and Titles

# ### Hemispheres

# In[109]:


# 1. Use browser to visit the URL 
url = 'https://marshemispheres.com/'

browser.visit(url)

# 2. Create a list to hold the images and titles.
hemisphere_image_urls = []

# 3. Write code to retrieve the image urls and titles for each hemisphere.

# Number of pictures we need to scan
count_of_pictures = len(home_page_soup.select("div.item"))

# Parse the html w/ soup
html = browser.html
home_page_soup = soup(html, 'html.parser')

# Hemisphere loop to gain all photos
for i in range(count_of_pictures):
    
    # Empty dict *According to module this is a good way*
    hemispheres = {}

    # This opens the link being found to the photos we need
    link_image = home_page_soup.select("div.description a")[i].get('href')
    browser.visit(f'https://marshemispheres.com/{link_image}')

    # New HTML parse for our sample image
    html = browser.html
    sample_image_soup = soup(html, 'html.parser')
    
    # Sample image text & title
    img_title = sample_image_soup.select_one("h2.title").get_text()
    
    # Sample image url link
    img_url = sample_image_soup.select_one("div.downloads ul li a").get('href') 
    
    # Adding more info to our dict
    hemispheres = {
        'img_url': img_url,
        'title': img_title}
    
    # Append dict to hemisphere image urls list
    hemisphere_image_urls.append(hemispheres)
    
    # Return to main page once done looping through
    browser.back()
    

# 4. Print the list that holds the dictionary of each image url and title.
hemisphere_image_urls


# 5. Quit the browser
browser.quit()






