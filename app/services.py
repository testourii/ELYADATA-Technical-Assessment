import os
from facebook_scraper import get_posts,set_user_agent,get_page_info
from fastapi.responses import JSONResponse
import pymongo

client=pymongo.MongoClient(os.environ.get("MONGO_URI"))
mydb=client['mydb']
mycol=mydb["page"] 

class Scraper():
    def scrapdata(self,name):
        set_user_agent(
    "Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)")
        posts=[]
        page={}
        data=get_page_info(name)
        page["name"]=name
        page["likes"]=data["likes"]

        try:
            for post in get_posts(name, pages=1):
                posts.append(post)
            page["posts"]=posts
            mycol.update_one({"name":name}, {"$set": page}, upsert=True)
            return(page) 
        except Exception as e:
                return JSONResponse(status_code=404,content = {"message": "Page " +name+" not found"}) 


class Fetcher():
    def fetchdata(self,name):
        try:
            page=mycol.find_one({"name":name}, {'_id': 0})
            if page is None:
                return JSONResponse(status_code=404,content = {"message": 'Page does not exist in database, try to scrap it from facebook first'}) 
            return((page)) 
        except Exception as e:
            return('An exception occurred: {}'.format(e))

