'''
Created on 23. nov. 2015

@author: kga



DB structure

twitter_user(
    display_name, 
    screen_name, 
    user_id,     #Looks like it need api calls to get
    avatar,
    avatar_small, 
    protected, 
    followers_nr, 
    following_nr, 
    ....,
    updated,
    friendship_new - datetime,
    friendship_updated - datetime,
    degree - int/controlls friendship scrape,
    )

twitter_friendships(following_id, follower_id, ...)

'''
import logging
import datetime
from  sqlalchemy.sql.expression import func

import sbot.twitter.scraper.db.models as models
import sbot.twitter.scraper.config as twitter_config
import sbot.const as twitter_const

##################################
#
#    user info
#

# ______________ STORE _____________________________


def store_followers(data, new=False):
    """
        Store users following user
        
        PRE:User must exist from before
        
        @param data: User and its friendship links
        @param new: True|False - Delete all friendship links and scrape them all again or scrape only new ones  
    """
    logging.debug(u"store followers of: "+unicode(data.get("user","")))
    _store_friendships(data, True, new)

def store_followings(data, new=False):
    """
        Store user`s friends, who he/she is following
        
        PRE:User must exist from before
        
        @param data: User and its friendship links
        @param new: True|False - Delete all friendship links and scrape them all again or scrape only new ones  
    """
    logging.debug(u"store friends/following of: "+unicode(data.get("user","")))
    _store_friendships(data, False, new)

def _store_friendships(data, followers=True, new=False):
    """
        PRE:User must exist from before
        
        @param data: User and its friendship links
        @param followers: True|False - is friendship links in data followers of user or users user is following.
        @param new: True|False - Delete all friendship links and scrape them all again or scrape only new ones  
    """
    
    user = data["user"]    
    items = data["data"]
    
    session = models.load_session()
    
    #Update users friendship date scraped info
    muser = session.query(models.User).filter_by(screen_name=user).first()
    muser.friendships_last_updated = datetime.datetime.now()
    if not muser.friendships_last_update_full or new:
        muser.friendships_last_update_full = datetime.datetime.now()
    session.commit()
    
    #If new then DELETE all friendships for this user. All will be scraped again
    if new:
        if followers:
            session.query(models.Friendship).filter(models.Friendship.following_id == user).delete(synchronize_session=False)
        else:
            session.query(models.Friendship).filter(models.Friendship.follower_id == user).delete(synchronize_session=False)
        session.commit()
            
    
    #Get degree for this new user
    degree = session.query(models.User).filter_by(screen_name=user).first().degree + 1
    
    logging.debug(u"start storing friendships")
    for item in items:
        logging.debug(u"store friendship with: "+unicode(item["screen_name"]))
        friend = models.User(screen_name=item["screen_name"],display_name=item["display_name"],
                             protected = item["protected"], degree=degree)
        try:
            session.add(friend)
            session.commit()
        except:
            logging.debug("ROLLBACK on storing friend")
            session.rollback()
        
        if followers:            
            friendship = models.Friendship(following_id=user, follower_id=item["screen_name"], date_added=datetime.datetime.now())
        else:            
            friendship = models.Friendship(following_id=item["screen_name"], follower_id=user, date_added=datetime.datetime.now())
            
        try:
            session.add(friendship)
            session.commit()
        except:
            if new:
                session.rollback()
                logging.debug("ROLLBACK on storing friendship")
            else:
                #If this friendship exist, then the rest should exist too.
                logging.debug("Commiting friendship failed - friendship likely exist")
                break
        


def store_tweets(data, new=False):
    """
        Store user`s tweets
        
        PRE:User must exist from before
        
        @param data: User and its friendship links
        @param new: True|False - Delete all friendship links and scrape them all again or scrape only new ones  
    """
    user = data["user"]    
    items = data["data"]
    
    session = models.load_session()
    
    #Update users friendship date scraped info
    muser = session.query(models.User).filter_by(screen_name=user).first()
    muser.tweets_last_updated = datetime.datetime.now()
    if not muser.tweets_last_update_full or new:
        muser.tweets_last_update_full = datetime.datetime.now()
    session.commit()
    
    
    
    for item in items:       
        tweet = models.Tweets(screen_name=user, poster_screen_name=item["poster_screen_name"],
                                  poster_display_name=item["poster_display_name"], text=item["text"],
                                  text_html=item["text_html"], id=item["id"], posted_date=item["posted_date"],
                                  retweets=item["retweets"], favorites=item["favorites"], inline_media=item["inline_media"])
        try:
            session.add(tweet)
            session.commit()
        except:
            if new:
                session.rollback()
            else:
                break
    

def _user_prep(data):
    data = data["data"]
    
    updated = datetime.datetime.now()
    
    ctx={}
    #Add scraped data
    for name in ["screen_name","display_name","avatar","bio","website","details_html","followers_nr","following_nr","last_active"]:
        if name not in data:
            continue
        ctx[name] = data[name]
    
    #Add extra data
    ctx["last_updated"]=updated
    return ctx

def update_user(data):
    
    ctx = _user_prep(data)    
    
    session = models.load_session()
    
    session.query(models.User).filter_by(screen_name=data["user"]).update(ctx)
    
    session.commit()
    

# ________________ EXIST cheks_____________________________
def exist_friendship(following, follower):
    session = models.load_session()
    if session.query(models.Friendship).filter_by(follower_id=follower, following_id=following).first() != None:
        return True
    return False


def exist_user(user):
    session = models.load_session()
    if session.query(models.User).filter_by(screen_name=user).first() != None:
        return True
    return False

def exist_tweet(tweet_id):
    session = models.load_session()
    if session.query(models.Tweets).filter_by(id=tweet_id).first() != None:
        return True
    return False

# ________________ GET _____________________________
def get_user_degree(user):
    """
        Get users degree of importance.
    """
    session = models.load_session()
    user = session.query(models.User).filter_by(screen_name=user).first()
    if user:
        return user.degree
    return None

"""def _pick_user_friendship():
    session = models.load_session()
    #1. If main user never scraped
    users = session.query(models.User).filter(models.User.degree <= twitter_config.DEGREE_FULL_SCRAPE,
                                              models.User.friendships_last_updated == None, models.User.main == True)
    if users.first():
        return users
    #2. If main user to old since update
    tresh = datetime.datetime.now() - datetime.timedelta(days=twitter_config.USER_MAIN_FRIENDSHIP_UPDATED_DELTA_DAYS)
    users = session.query(models.User).filter(models.User.degree <= twitter_config.DEGREE_FULL_SCRAPE,
                                              models.User.last_updated < tresh, models.User.main == True)
    if users.first():
        return users
    #3. if user never scraped
    users = session.query(models.User).filter(models.User.degree <= twitter_config.DEGREE_FULL_SCRAPE,
                                              models.User.last_updated == None, models.User.main == False)
    if users.first():
        return users
    #4. If user to old since update
    tresh = datetime.datetime.now() - datetime.timedelta(weeks=twitter_config.USER_FRIENDSHIP_UPDATED_DELTA_WEEKS)
    users = session.query(models.User).filter(models.User.degree <= twitter_config.DEGREE_FULL_SCRAPE,
                                              models.User.friendships_last_updated < tresh, models.User.main == False)
    return users

def _pick_user():
    session = models.load_session()
    #1. If main user never scraped
    users = session.query(models.User).filter(models.User.last_updated == None, models.User.main == True)
    if users.first():
        return users
    #2. If main user to old
    tresh = datetime.datetime.now() - datetime.timedelta(days=twitter_config.USER_MAIN_UPDATED_DELTA_DAYS)
    users = session.query(models.User).filter(models.User.last_updated < tresh, models.User.main == True)
    if users.first():
        return users
    #3. if user never scraped
    users = session.query(models.User).filter(models.User.last_updated == None, models.User.main == False)
    if users.first():
        return users
    #4. If user to old
    tresh = datetime.datetime.now() - datetime.timedelta(weeks=twitter_config.USER_UPDATED_DELTA_WEEKS)
    users = session.query(models.User).filter(models.User.last_updated < tresh, models.User.main == False)
    return users

def _pick_tweet():
    return None"""

def get_user(screen_name):
    session = models.load_session()
    return session.query(models.User).filter(models.User.screen_name==screen_name).first()
    
    
def _get_random_user(last_updated=None, user_main_delta=None, user_full_delta=None, user_delta=None):
    session = models.load_session()
    model = models.User
    
    if not last_updated or not user_main_delta:
        return        
    #1. If main user never scraped
    users = session.query(model).filter(getattr(model, last_updated) == None, model.main == True)
    if users.first():
        return users
    
    #2. If main user to long since scraped
    tresh = datetime.datetime.now() - datetime.timedelta(days=user_main_delta)
    users = session.query(model).filter(getattr(model, last_updated) < tresh, model.main == True)
    if users.first():
        return users
    
    
    if not user_full_delta:
        return
    #3. If user with degree priority high enough to be fully scraped never was scraped
    users = session.query(model).filter(model.degree <= twitter_config.DEGREE_FULL_SCRAPE,
                                        getattr(model, last_updated) == None)
    if users.first():
        return users
    
    #4. If user with degree priority high enough to be fully scraped is to long since updated
    tresh = datetime.datetime.now() - datetime.timedelta(days=user_full_delta)
    users = session.query(model).filter(model.degree <= twitter_config.DEGREE_FULL_SCRAPE,
                                        getattr(model, last_updated) < tresh)
    if users.first():
        return users
        
    if not user_delta:
        return
    #5. if user never scraped
    users = session.query(model).filter(getattr(model, last_updated) == None)
    if users.first():
        return users
    
    #6. If user to old since update
    tresh = datetime.datetime.now() - datetime.timedelta(days=user_delta)
    users = session.query(model).filter(getattr(model, last_updated) < tresh)
    return users


def get_random_user(method):
    """
        Pick random user from db
    """
    users=None
    if method == "friendship":
        users = _get_random_user("friendships_last_updated", user_main_delta=twitter_config.FRIENDSHIP_USER_MAIN_DELTA, 
                      user_full_delta=twitter_config.FRIENDSHIP_USER_FULL_DELTA)
    elif method == "user":
        users = _get_random_user("last_updated", user_main_delta=twitter_config.USER_MAIN_DELTA, 
                      user_full_delta=twitter_config.USER_FULL_DELTA, user_delta=twitter_config.USER_DELTA)
    elif method == "tweet":
        users = _get_random_user("tweets_last_updated", user_main_delta=twitter_config.TWEET_USER_MAIN_DELTA, 
                      user_full_delta=twitter_config.TWEET_USER_FULL_DELTA)
    
    if not users:
        return None
    if not users.first():
        return None
    
    #This should shuffle the list retrieved for different type of db. Not tested on all
    #Might also become to slow when db gets large, not tested.
    if twitter_config.DATABASE == twitter_const.MYSQL:
        users = users.order_by(func.rand())
    elif twitter_config.DATABASE == twitter_const.POSTGRESSQL or twitter_config.DATABASE == twitter_const.SQLITE:
        users = users.order_by(func.random())
    elif twitter_config.DATABASE == twitter_const.ORACLE:
        users = users.order_by('dbms_random.value')
        
    return users.first()

# ________________ ADD/NEW _____________________________
def add_new_user(user, degree=1, main=False):
    """
        IF user exist, then update it with given degree and main
    """
    session = models.load_session()
    friend = models.User(screen_name=user, degree=degree, main=main)
    try:
        session.add(friend)
        session.commit()
    except:
        session.rollback()
        session.query(models.User).filter_by(screen_name=user).update({"degree":degree, "main":main})
        session.commit()
        
#add_new_user("FictionalUni", degree=1)

