'''
Created on 20. nov. 2015

@author: kga


TODO: finish delete items
TODO: remove temporary break in scroll so it scrolls all the way down
'''
import logging

from selenium.webdriver.support.ui import WebDriverWait
#from pymongo import MongoClient


from base import ScrapeBaseSelenium



class GetTimlineBase(ScrapeBaseSelenium):
    """    
        Get timeline base class.
        
        args:
            max_items (int): max number of items/firends to be scraped
            new (bool): scrape from scratch or scrape untill existing item/friendship is found
    """
    def __init__(self, max_items=0, new=False):
        super(GetTimlineBase,self).__init__()
        self.max_items=max_items
        self.new=new
    
    def item_exist(self):
        """
            Overwrite this method
            Check if item is added earlier. Used in scroll page
        """
        raise NotImplementedError("Please Implement item_exist method")
    
    def scrape_items(self):
        """
            Overwrite this method
            Scrapeing of data is moved to this function in timeline classes
        """
        raise NotImplementedError("Please Implement scrape_items method")
    
    def scroll_page(self):
        """
            Scrols current page down.
                all the way 
                or until existing item is found 
                or until max items are scrolled over
                or stops if site timesout
        """
        logging.debug(u"start scrolling page")
        while True:
        
            if not self.new:
                if self.item_exist():
                    logging.debug(u"STOP scrolling page - item exist")
                    break
            
            elemsCount = self.browser.execute_script("return document.querySelectorAll('.Timeline-item').length")
            
            if elemsCount > self.max_items and self.max_items > 0:
                logging.debug(u"STOP scrolling page - max items found")
                break
            #Scroll
            self.browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            
            def is_new_items_loaded(browser):
                #Test to check if new items has been loaded after scroll
                nelemsCount = browser.execute_script("return document.querySelectorAll('.Timeline-item').length")
                return nelemsCount > elemsCount
            try:
                WebDriverWait(self.browser, 20).until(is_new_items_loaded)
            except:
                logging.debug(u"STOP scrolling page - timeout")
                break
            
    def scrape_data(self):
        self.scroll_page()
        self.scrape_items()
            
            
            
        
 
            

        