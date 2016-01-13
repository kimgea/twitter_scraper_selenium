'''
Created on 23. nov. 2015

@author: kga
'''
from datetime import datetime

from base import ScrapeBaseSelenium

import sbot.twitter.scraper.functions.db as dbfunctions
import sbot.twitter.scraper.functions.helper as helper




class GetUser(ScrapeBaseSelenium):
    """    
        Get user class.
    """
    def __init__(self):
        super(GetUser,self).__init__()
        
    def make_url(self):
        return self.base_url + self.user + "/"
    
    def store_data(self):
        dbfunctions.update_user(self.get_storage_data())
        
    def scrape_data(self):
        """
            Scrape user data
        """
        item = {}
        item["display_name"] = self.browser.find_element_by_class_name("UserProfileHeader-displayName").text.split("\n")[0]
        item["screen_name"] = self.browser.find_element_by_class_name("UserProfileHeader-screenName").text.strip("@")
        item["avatar"] = self.browser.find_element_by_class_name("UserAvatar").get_attribute("src")
        
        try:
            item["bio"] = self.browser.find_element_by_class_name("UserProfileHeader-bio").text.replace("\n"," ")
        except:
            item["bio"] = None
        try:
            item["website"] = self.browser.find_element_by_class_name("UserProfileHeader-url").get_attribute("href")
        except:
            item["website"] = None
        try:
            item["details_html"] = self.browser.find_element_by_class_name("UserProfileHeader-details").get_attribute('innerHTML')
        except:
            item["details_html"] = None
            
        item["followers_nr"] = self.browser.find_element_by_class_name("UserProfileHeader-stat--followers").find_element_by_class_name("UserProfileHeader-statCount").text
        item["followers_nr"] = int(helper.prep_number(item["followers_nr"]))
        
        item["following_nr"] = self.browser.find_element_by_class_name("UserProfileHeader-stat--following").find_element_by_class_name("UserProfileHeader-statCount").text
        item["following_nr"] = int(helper.prep_number(item["following_nr"]))
        
        
        try:
            item["last_active"] = self.browser.find_elements_by_class_name("Tweet-timestamp")[0].find_element_by_tag_name("time").get_attribute("datetime")
            item["last_active"]=item["last_active"].split("+")[0]
            item["last_active"] = datetime.strptime(item["last_active"], '%Y-%m-%dT%H.%M.%S')
        except:
            item["last_active"] = None
        
        self.data = item
        
