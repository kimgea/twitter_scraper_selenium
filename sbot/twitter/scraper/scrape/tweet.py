'''
Created on 28. nov. 2015

@author: kga
'''
import datetime

import timeline

import sbot.twitter.scraper.functions.db as dbfunctions
import sbot.twitter.scraper.functions.helper as helper



class GetTweets(timeline.GetTimlineBase):
    """    
        Get tweets class.
        
        args:
            max_items (int): max number of items/firends to be scraped
            new (bool): scrape from scratch or scrape untill existing item/friendship is found
    """
    def __init__(self,max_items=0, new=False):
        super(GetTweets,self).__init__(max_items=max_items, new=new)
        
    def make_url(self):
        return self.base_url + self.user + "/"
    
    def item_exist(self):
        """
            Check last item in current html list to se if it exist
        """
        element = self.browser.find_elements_by_class_name("Timeline-item")[-1]
        iid = element.find_element_by_class_name("Tweet").get_attribute('data-tweet-id')
        return dbfunctions.exist_tweet(iid)
    
    def store_data(self):
        dbfunctions.store_tweets(self.get_storage_data(), self.new)
        
        
    def scrape_items(self):
        """
            Scrape tweet information
        """
        items=[]
        for element in self.browser.find_elements_by_class_name("Timeline-item"):
            item={}
            item["screen_name"] = self.user            
            item["poster_display_name"] = element.find_element_by_class_name("UserNames-displayName").text
            item["poster_screen_name"] = element.find_element_by_class_name("UserNames-screenName").text.strip("@")
            item["text"] = element.find_element_by_class_name("TweetText").text#.encode('utf8').decode('utf8')
            item["text_html"] = element.find_element_by_class_name("TweetText").get_attribute('innerHTML')#.encode('utf8').decode('utf8')
            item["id"] = element.find_element_by_class_name("Tweet").get_attribute('data-tweet-id')
            
            
            try:
                item["inline_media"] = element.find_element_by_class_name("InlineMedia-content").text
                item["inline_media"] = True
            except:
                item["inline_media"] = False
            try:
                item["retweets"] = element.find_element_by_css_selector("button[jsaction='click:retweet']").find_element_by_class_name("TweetAction-count").text
                item["retweets"] = helper.prep_number(item["retweets"])
            except:
                item["retweets"] = 0
            try:
                item["favorites"] = element.find_element_by_css_selector("button[jsaction='click:heart']").find_element_by_class_name("TweetAction-count").text
                item["favorites"] = helper.prep_number(item["favorites"])
            except:
                item["favorites"] = 0
                
            
            item["posted_date"] = element.find_element_by_class_name("Tweet-timestamp").find_element_by_tag_name("time").get_attribute("datetime")
            item["posted_date"]=item["posted_date"].split("+")[0]
            item["posted_date"] = datetime.datetime.strptime(item["posted_date"], '%Y-%m-%dT%H:%M:%S')
            
            
            
            items.append(item)
        self.data = items



