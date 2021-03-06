'''
Created on 27. nov. 2015

@author: kga
'''

import sbot.config as config



DATABASE = config.DATABASE

def get_database_string():
    return config.get_twitter_scraper_database_string()

DEGREE_FULL_SCRAPE = config.TWITTER_SCRAPER_CONTROLLER_DEGREE_FULL_SCRAPE


USER_DELTA = config.TWITTER_SCRAPER_CONTROLLER_USER_DELTA
USER_MAIN_DELTA = config.TWITTER_SCRAPER_CONTROLLER_USER_MAIN_DELTA 
USER_FULL_DELTA = config.TWITTER_SCRAPER_CONTROLLER_USER_FULL_DELTA


FRIENDSHIP_USER_MAIN_DELTA = config.TWITTER_SCRAPER_CONTROLLER_FRIENDSHIP_USER_MAIN_DELTA 
FRIENDSHIP_USER_FULL_DELTA = config.TWITTER_SCRAPER_CONTROLLER_FRIENDSHIP_USER_FULL_DELTA

FRIENDSHIP_USER_RESCRAPE_DELTA = config.TWITTER_SCRAPER_CONTROLLER_FRIENDSHIP_USER_RESCRAPE_DELTA


FRIENDSHIP_USER_MAX_SCRAPE = config.TWITTER_SCRAPER_CONTROLLER_FRIENDSHIP_USER_MAX_SCRAPE
FRIENDSHIP_USER_MAIN_MAX_SCRAPE = config.TWITTER_SCRAPER_CONTROLLER_FRIENDSHIP_USER_MAIN_MAX_SCRAPE


TWEET_USER_MAIN_DELTA = config.TWITTER_SCRAPER_CONTROLLER_TWEET_USER_MAIN_DELTA 
TWEET_USER_FULL_DELTA = config.TWITTER_SCRAPER_CONTROLLER_TWEET_USER_FULL_DELTA

TWEET_USER_RESCRAPE_DELTA = config.TWITTER_SCRAPER_CONTROLLER_TWEET_USER_RESCRAPE_DELTA

TWEET_USER_MAX_SCRAPE = config.TWITTER_SCRAPER_CONTROLLER_TWEET_USER_MAX_SCRAPE
TWEET_USER_MAIN_MAX_SCRAPE = config.TWITTER_SCRAPER_CONTROLLER_TWEET_USER_MAIN_MAX_SCRAPE