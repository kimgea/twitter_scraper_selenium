'''
Created on 23. nov. 2015

@author: kga
'''
import logging
from selenium import webdriver


class ScrapeBaseSelenium(object):
    """
        Base class for scraping 
    """
    def __init__(self):
        """
            @param data: A dict or a list of dicts 
        """
        self.browser = None
        self.base_url="http://mobile.twitter.com/"
        self.data = None
        self.user=None
        
    def get_storage_data(self):
        return dict(user=self.user, data=self.data)
    
    def scrape_data(self):
        raise NotImplementedError("Please Implement scrape_data method")
    
    def store_data(self):
        raise NotImplementedError("Please Implement store_data method")
    
    def make_url(self):
        raise NotImplementedError("Please Implement make_url method")
    
    def run(self, user):
        logging.debug(u"username: "+unicode(user))
        self.user=user
        
        logging.debug(u"Set up selenium")
        self.setup_selenium()
        logging.debug(u"Scrape data")
        self.scrape_data()
        logging.debug(u"store data")
        self.store_data()
        logging.debug(u"tear down selenium")
        self.tear_down_selenium()
        
    def setup_selenium(self):
        logging.debug(u"Open browser")
        #self.browser = webdriver.Firefox()
        self.browser = webdriver.Chrome()
        logging.debug(u"Browser is open")
        logging.debug(u"url: "+unicode(self.make_url()))
        self.browser.get(self.make_url())
        logging.debug(u"Page is accessed")
        
    def tear_down_selenium(self):
        self.browser.quit()
        