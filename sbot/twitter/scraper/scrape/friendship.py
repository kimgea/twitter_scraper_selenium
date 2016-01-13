'''
Created on 28. nov. 2015

@author: kga
'''

import logging
import timeline

import sbot.twitter.scraper.functions.db as dbfunctions


       
class GetFriends(timeline.GetTimlineBase):
    """    
        Get friendship base class.
        
        args:
            max_items (int): max number of items/firends to be scraped
            new (bool): scrape from scratch or scrape untill existing item/friendship is found
    """
    def __init__(self,max_items=0, new=False):
        super(GetFriends,self).__init__(max_items=max_items, new=new)
    
    def _item_exist_check(self,screen_name):
        """
            Overwrite 
            Connect to db to check if exist. DB call depend on following or follower
            
            args:
                screen_name (str): Twitter users screen_name. Screen name of friend/follower to be checked
        """
        raise NotImplementedError("Please Implement _item_exist_check method")
    
    def item_exist(self):
        """
            Check last item in current html list to se if it exist
        """
        element = self.browser.find_elements_by_class_name("Timeline-item")[-1]
        screen_name = element.find_element_by_class_name("UserNames-screenName").text.strip("@")
        if self._item_exist_check(screen_name):
            return True
        return False
    
    def scrape_items(self):
        """
            Scrape friendship information
        """
        logging.debug(u"start scrape data")
        items=[]
        for element in self.browser.find_elements_by_class_name("Timeline-item"):
            logging.debug(u"timeline item found")
            item={}
            item["display_name"] = element.find_element_by_class_name("UserNames-displayName").text.split("\n")[0]
            item["screen_name"] = element.find_element_by_class_name("UserNames-screenName").text.strip("@")
            item["avatar"] = element.find_element_by_class_name("UserAvatar").get_attribute("src")
            
            protected = 0
            for i in element.find_elements_by_class_name("u-hiddenVisually"):
                if "Protected account" in i.text.split("\n")[0]:
                    protected = 1
                    break
            item["protected"] = protected
            logging.debug(u"friend name: "+unicode(item["screen_name"]))
            logging.debug("timeline item scraped")
            items.append(item)
        self.data = items
                
                
                
class GetFollowers(GetFriends):
    """    
        Get followers class.
        
        args:
            max_items (int): max number of items/firends to be scraped
            new (bool): scrape from scratch or scrape untill existing item/friendship is found
    """
    def __init__(self,max_items=0, new=False):
        super(GetFollowers,self).__init__(max_items=max_items, new=new)
    
    def make_url(self):
        return self.base_url + self.user + "/"+"followers"
    
    def store_data(self):
        dbfunctions.store_followers(self.get_storage_data(), self.new)
        
    def _item_exist_check(self,screen_name):
        return dbfunctions.exist_friendship(self.user, screen_name)
    
        
        
class GetFollowing(GetFriends):
    """    
        Get following/friends class.
        
        args:
            max_items (int): max number of items/firends to be scraped
            new (bool): scrape from scratch or scrape untill existing item/friendship is found
    """
    def __init__(self,max_items=0, new=False):
        super(GetFollowing,self).__init__(max_items=max_items, new=new)
        
    def make_url(self):
        return self.base_url + self.user + "/"+"following"
            
    def store_data(self):
        dbfunctions.store_followings(self.get_storage_data(), self.new)    
    
    def _item_exist_check(self,screen_name):
        return dbfunctions.exist_friendship(screen_name, self.user)
 
 