# Import Splinter and BeautifulSoup
from splinter import Browser
from bs4 import BeautifulSoup as soup
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import datetime as dt

def scrape_all():
    # Initiate headless driver for deployment
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=True)

    news_title, news_paragraph = mars_news(browser)

    # Run all scraping functions and store results in a dictionary
    data = {
        "news_title": news_title,
        "news_paragraph": news_paragraph,
        "featured_image": featured_image(browser),
        "facts": mars_facts(),
        "last_modified": dt.datetime.now(),
        "hemisphere_image_info": hemisphere_image(browser)
    }

    # Stop webdriver and return data
    browser.quit()
    return data

def mars_news(browser):

    # Visit the mars nasa news site
    url = 'https://data-class-mars.s3.amazonaws.com/Mars/index.html'
    browser.visit(url)

    # Optional delay for loading the page
    browser.is_element_present_by_css('div.list_text', wait_time=1)

    #Convert the browser html to a soup object
    html = browser.html
    news_soup = soup(html, 'html.parser')

    # Add try/except for error handling
    try:
        slide_elem = news_soup.select_one('div.list_text')
        # Use the parent element to find the first 'a' tag and save it as 'news_title'
        news_title = slide_elem.find('div', class_='content_title').get_text()
        # Use the parent element to find the paragraph text
        news_p = slide_elem.find('div', class_='article_teaser_body').get_text()

    except AttributeError:
        return None, None
    
    return news_title, news_p



def featured_image(browser):
    # Visit URL
    url = 'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/index.html'
    browser.visit(url)

    # Find and click the full image button
    full_image_elem = browser.find_by_tag('button')[1]
    full_image_elem.click()

    # Parse the resulting html with soup
    html = browser.html
    img_soup = soup(html, 'html.parser')

    # Add try/except for error handling
    try:
        # Find the relative image url
        img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')

    except AttributeError:
        return None

    # Use the base url to create an absolute url
    img_url = f'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/{img_url_rel}'

    return img_url

# ## Mars Facts

def mars_facts():
    # Add try/except for error handling
    try:
        # Use 'read_html' to scrape the facts table into a dataframe
        df = pd.read_html('https://data-class-mars-facts.s3.amazonaws.com/Mars_Facts/index.html')[0]

    except BaseException:
        return None

    # Assign columns and set index of dataframe
    df.columns=['Description', 'Mars', 'Earth']
    df.set_index('Description', inplace=True)

    # Convert dataframe into HTML format, add bootstrap
    return df.to_html(classes="table table-striped")

def hemisphere_image(browser):

    #Use browser to visit the URL 
    url = 'https://marshemispheres.com/'

    browser.visit(url)

    # Create a list to hold the images and titles.
    hemisphere_image_urls = []

    #Write code to retrieve the image urls and titles for each hemisphere.

    # Parse the html w/ soup
    html = browser.html
    home_page_soup = soup(html, 'html.parser')

    # Try / Except for errors
    try:

        # Number of pictures we need to scan
        count_of_pictures = len(home_page_soup.select("div.item"))

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
        
    except BaseException:
        return None


    # Return the list that holds the dict
    return hemisphere_image_urls


if __name__ == "__main__":
    # If running as script, print scraped data
    print(scrape_all())







