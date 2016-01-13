'''
Created on 23. nov. 2015

@author: kga


'''

import const

DATABASE = const.MYSQL


#############################
#
#    Logging
#

import logging

LOGNAME = 'example.log'
#LOGNAME = False

if LOGNAME:
    logging.basicConfig(filename=LOGNAME,level=logging.DEBUG)
else:
    logging.basicConfig(level=logging.DEBUG)


###############################################################
###
###    TWITTER
###
##########################################################

######################
#
#    Scraper

#________ Controller __________
"""
    Every user with lover or equal degree than this is fully scraped
        - following, folloers, tweets
"""
TWITTER_SCRAPER_CONTROLLER_DEGREE_FULL_SCRAPE = 1


"""
    How often data is updated, in days
    user_main - is main user, controlled by users
    user_full - is users that are set to be fully scraped
    user - is the rest of the users
"""
TWITTER_SCRAPER_CONTROLLER_USER_DELTA = 150
TWITTER_SCRAPER_CONTROLLER_USER_MAIN_DELTA = 2
TWITTER_SCRAPER_CONTROLLER_USER_FULL_DELTA = 3

TWITTER_SCRAPER_CONTROLLER_FRIENDSHIP_USER_MAIN_DELTA = 1
TWITTER_SCRAPER_CONTROLLER_FRIENDSHIP_USER_FULL_DELTA = 10

TWITTER_SCRAPER_CONTROLLER_TWEET_USER_MAIN_DELTA = 1
TWITTER_SCRAPER_CONTROLLER_TWEET_USER_FULL_DELTA = 10


"""
    How often data is fully scraped, in days
"""
TWITTER_SCRAPER_CONTROLLER_FRIENDSHIP_USER_RESCRAPE_DELTA = 150
TWITTER_SCRAPER_CONTROLLER_TWEET_USER_RESCRAPE_DELTA = 90


"""
    How many items that are scraped
    NOTE: 
        this is curently not exact. It usualy scrapes and store more.
            It is used controll the page scroll behavior. It stops when 
            it has scrolled over max items.
"""
TWITTER_SCRAPER_CONTROLLER_FRIENDSHIP_USER_MAX_SCRAPE = 10
TWITTER_SCRAPER_CONTROLLER_FRIENDSHIP_USER_MAIN_MAX_SCRAPE = 10

TWITTER_SCRAPER_CONTROLLER_TWEET_USER_MAX_SCRAPE = 10
TWITTER_SCRAPER_CONTROLLER_TWEET_USER_MAIN_MAX_SCRAPE = 10



#_________ Database ___________

def get_twitter_scraper_database_string():
    return "mysql://root:@localhost/twitter_data?charset=utf8"






