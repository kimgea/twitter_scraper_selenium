'''
Created on 26. nov. 2015

@author: kga
'''

import sbot.twitter.scraper.functions.db as db_functions


def add_user(user, degree=1):
    """
        Add user to be scraped
        IF user exist, then update it with given degree
        
        @param user:  twitter user screen name
        @param degree: indicates how important user is 
    """
    db_functions.add_new_user(user, degree)