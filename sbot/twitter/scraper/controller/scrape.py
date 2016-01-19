'''
Created on 23. nov. 2015

@author: kga
'''

import datetime
import logging

from sbot.twitter.scraper.scrape.user import GetUser
from sbot.twitter.scraper.scrape.friendship import GetFollowing
from sbot.twitter.scraper.scrape.friendship import GetFollowers
from sbot.twitter.scraper.scrape.tweet import GetTweets

import sbot.twitter.scraper.functions.db as db_functions
import sbot.twitter.scraper.config as twitter_config





##########################################
def scrape_one_user():
    """
        Scrape user info about one random user that is not scraped before, 
        or very long since last scraped
    """
    user = db_functions.get_random_user("user")
    if not user: return
    scrape_user(user)
    
def scrape_user(user):
    """
        Scrape user info. Do not scrape tmeline info like friends and tweets. 
        
        Note:
            User might have to exist in db to be scraped. CHECK
             
        args:
            user (optional): Twitter user screen_name must be property of object
    """
    temp = GetUser()
    temp.run(user.screen_name)
#__________________________________________

############################################    
def scrape_one_tweet():
    """
        Scrape tweets of one random user that is not scraped before, 
        or very long since last scraped
    """
    
    user = db_functions.get_random_user("tweet")
    if not user: return
    
    full=False
    if user.tweets_last_update_full:
        tresh = datetime.datetime.now() - datetime.timedelta(days=twitter_config.TWEET_USER_RESCRAPE_DELTA)
        if user.tweets_last_update_full < tresh:
            full=True
            
    scrape_tweet(user, full)
    
    
def scrape_tweet(user, full=False):
    """
        Scrape tweets. 
        
        Note:
            User might have to exist in db to be scraped. CHECK
             
        args:
            user (optional): Twitter user screen_name must be property of object
            full (bool): scrape all tweets or stop when scraped before. IF true deletes old tweets from db
    """
    if user.main:
        nr = twitter_config.TWEET_USER_MAIN_MAX_SCRAPE
    else:
        nr = twitter_config.TWEET_USER_MAX_SCRAPE
        
    temp = GetTweets(max_items=nr, new=full)
    temp.run(user.screen_name)
#______________________________________________
   
############################################    
def scrape_one_friendship():
    """
        Scrape all followers and following of one random user that is mot scraped before, 
        or very long since last scraped
    """
    logging.debug(u"Scrape one users friendships")
    user = db_functions.get_random_user("friendship")   
    if not user:
        logging.debug(u"user not found") 
        return
    
    #IF to long since rescraping all friendships, Delete friendships and scrape all from scratch
    full=False
    if user.friendships_last_update_full:
        tresh = datetime.datetime.now() - datetime.timedelta(days=twitter_config.FRIENDSHIP_USER_RESCRAPE_DELTA)
        if user.friendships_last_update_full < tresh:
            full=True
     
    scrape_friendship(user, full)
    
    
def scrape_friendship(user, full=False):
    """
        Scrape user friendships. Friends and followers. 
        
        Note:
            User might have to exist in db to be scraped. CHECK
             
        args:
            user (optional): Twitter user screen_name must be property of object
            full (bool): scrape all tweets or stop when scraped before. IF true deletes old tweets from db
    """
    logging.debug(u"Scrape friendship of user: "+unicode(user))
    if user.main:
        nr = twitter_config.FRIENDSHIP_USER_MAIN_MAX_SCRAPE
    else:
        nr = twitter_config.FRIENDSHIP_USER_MAX_SCRAPE
    
    temp = GetFollowing(max_items=nr, new=full)
    temp.run(user.screen_name)
    temp = GetFollowers(max_items=nr, new=full)
    temp.run(user.screen_name)
#______________________________________________


if __name__ == "__main__":
    db_functions.add_new_user("FictionalUni",1,True)
    #scrape_friendship(db_functions.get_user("FictionalUni"))
    #scrape_tweet(db_functions.get_user("FictionalUni"))
    scrape_one_user()
    scrape_one_tweet()
    scrape_one_friendship()
    