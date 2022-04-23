from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi
from app.services import Scraper,Fetcher

app=FastAPI()
page=Scraper()
dbPage=Fetcher()
@app.get("/")
async def check_server():
    return  {"msg": "Server running"}

# scrap data by page name
@app.get("/{pageName}",tags=["pages"])
async def get_page_posts_by_page_name(pageName):
    return page.scrapdata(pageName)

# fetch data by page name from database
@app.get("/db/{pageName}",tags=["pagesDB"])
async def get_page_posts_by_page_name_from_DataBase(pageName):
    return dbPage.fetchdata(pageName)


# customize OAS metadata
def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="Facebook scrapper",
        version="0.0.1",
        description="This task is realized within the context of the job application to Full stack developer positon at ELYADATA",
        routes=app.routes,
    )
    app.openapi_schema = openapi_schema
    return app.openapi_schema

tags_metadata = [
    {
        "name": "pages",
        "description": "get page informations (name, followers, posts...) by page name and store data in MongoDB",
    },
    {
        "name": "pagesDB",
        "description": "Since scrapping data from facebook pages take some seconds, this api fetch last stored data from database instantly",
       
    },
]


app.openapi = custom_openapi