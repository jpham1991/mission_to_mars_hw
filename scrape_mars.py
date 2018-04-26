from bs4 import BeautifulSoup
import requests
import pymongo
from splinter import Browser
import tweepy
import time
import pandas as pd

def Scrape():

    print("Scraping")
    print("----------------------------------")

    mars_dict = {}

    url = "https://mars.nasa.gov/news/"

    html = requests.get(url)

    soup = BeautifulSoup(html.text, 'html.parser')

    news_title = soup.find('div', 'content_title', 'a').text
    news_p = soup.find('div', 'rollover_description_inner').text

    mars_dict["news_title"] = news_title
    mars_dict["news_p"] = news_p

    print("NEWS TITLE & DESCRIPTION")


    url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"

    executable_path = {'executable_path':'/usr/local/bin/chromedriver'}
    browser = Browser('chrome', **executable_path, headless=False)
    browser.visit(url)

    time.sleep(5)
    browser.click_link_by_partial_text('FULL IMAGE')
    time.sleep(5)
    browser.click_link_by_partial_text('more info')
    time.sleep(5)

    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    results = soup.find('article')
    extension = results.find('figure', 'lede').a['href']
    link = "https://www.jpl.nasa.gov"
    featured_image_url = link + extension

    mars_dict["featured_image_url"] = featured_image_url

    print("---Feature Image Acquired---")


    consumer_key = "BSWLJ9T5f2QBZD1z5TX0raxNP"
    consumer_secret = "CBNQZpaP6Ob2wTIzhlFt2U4hVwwBfg3ocn7toRDYc8zJSmxTRK"
    access_token = "955906672878346240-D711g4Lz9ghDymXjY5DQtUSqZaDW3as"
    access_token_secret = "N2GpvVdzWbtU0rCc5aTyVIaxnGn15Xtle9e27EJrnU86g"



    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth, parser=tweepy.parsers.JSONParser())

    target_user = "@MarsWxReport"

    tweet = api.user_timeline(target_user, count=1)[0]

    mars_weather = tweet['text']

    mars_dict["mars_weather"] = mars_weather

    print("---Weather Acquired---")


    url = "https://space-facts.com/mars/"

    html = requests.get(url)

    soup = BeautifulSoup(html.text, 'html.parser')

    mars_profile = {}

    results = soup.find('tbody').find_all('tr')

    for result in results:
        key = result.find('td', 'column-1').text.split(":")[0]
        value = result.find('td', 'column-2').text
        
        mars_profile[key] = value
        
    profile_df = pd.DataFrame([mars_profile]).T.rename(columns = {0: "Value"})
    profile_df.index.rename("Description", inplace=True)

    profile_html = "".join(profile_df.to_html().split("\n"))

    mars_dict["profile_html"] = profile_html

    print("FACTS ACQUIRED")



    url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"


    hemisphere_image_urls = []


    executable_path = {'executable_path':'/usr/local/bin/chromedriver'}
    browser = Browser('chrome', **executable_path, headless=False)
    browser.visit(url)

    time.sleep(5)
    browser.click_link_by_partial_text('Valles Marineris Hemisphere Enhanced')
    time.sleep(5)

    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    valles_link = soup.find('div', 'downloads').a['href']

    valles_marineris = {
        "title": "Valles Marineris Hemisphere",
        "img_url": valles_link
    }

    hemisphere_image_urls.append(valles_marineris)


    executable_path = {'executable_path':'/usr/local/bin/chromedriver'}
    browser = Browser('chrome', **executable_path, headless=False)
    browser.visit(url)

    time.sleep(5)
    browser.click_link_by_partial_text('Cerberus Hemisphere Enhanced')
    time.sleep(5)

    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    cerberus_link = soup.find('div', 'downloads').a['href']

    cerberus = {
        "title": "Cerberus Hemisphere",
        "img_url": cerberus_link
    }

    hemisphere_image_urls.append(cerberus)



    executable_path = {'executable_path':'/usr/local/bin/chromedriver'}
    browser = Browser('chrome', **executable_path, headless=False)
    browser.visit(url)

    time.sleep(5)
    browser.click_link_by_partial_text('Schiaparelli Hemisphere Enhanced')
    time.sleep(5)

    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    schiaparelli_link = soup.find('div', 'downloads').a['href']

    schiaparelli = {
        "title": "Schiaparelli Hemisphere",
        "img_url": schiaparelli_link
    }

    hemisphere_image_urls.append(schiaparelli)



    executable_path = {'executable_path':'/usr/local/bin/chromedriver'}
    browser = Browser('chrome', **executable_path, headless=False)
    browser.visit(url)


    time.sleep(5)
    browser.click_link_by_partial_text('Syrtis Major Hemisphere Enhanced')
    time.sleep(5)


    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')


    syrtis_link = soup.find('div', 'downloads').a['href']


    syrtis_major = {
        "title": "Syrtis Major Hemisphere",
        "img_url": syrtis_link
    }


    hemisphere_image_urls.append(syrtis_major)


    mars_dict["hemisphere_image_urls"] = hemisphere_image_urls

    print("Images Acquired")

    print("----------------------------------")
    print("Scraping is finished!")

    return mars_dict