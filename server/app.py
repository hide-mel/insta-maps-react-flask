from flask import Flask, jsonify, request, send_file
import instaloader
import os, json
import pandas as pd
import numpy as np
from time import sleep
from flask_cors import CORS

from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from explicit import waiter, XPATH
from bs4 import BeautifulSoup

from random import randint


app = Flask(__name__)
CORS(app)

def readJson(path_to_json):
    json_files = [pos_json for pos_json in os.listdir(path_to_json) if pos_json.endswith('.json')]
    #app.logger.info(json_files)
    jsons_data = pd.DataFrame(columns=['id', 'slug', 'display_url', 'file_name'])
    app.logger.info(len(json_files))
    for index, js in enumerate(json_files):
        try:
            with open(os.path.join(path_to_json, js)) as json_file:
                json_text = json.load(json_file)
                app.logger.info(index)
                app.logger.info(js)
                #prevent key errors
                
                id = json_text['node']['location']['id']
                slug = json_text['node']['location']['slug']
                display_url = json_text['node']['display_url']
                file_name = os.path.join(path_to_json, js)
                jsons_data.loc[index] = [id, slug, display_url, file_name]
        except:
                app.logger.info('error during iteration')
            

    app.logger.info(len(jsons_data))

    #drop duplicated location id
    jsons_data = jsons_data.drop_duplicates(subset=['id']) 

    app.logger.info(len(jsons_data))

    #add latitude and longitude columns
    jsons_data["lat"] = np.nan
    jsons_data["lng"] = np.nan

    
    return jsons_data


def selenium_open(username, passwd):

    getdriver = ("https://www.instagram.com/accounts/login/")
    options = Options()
    #options.add_argument("--headless")
    driver = webdriver.Firefox(options=options)
    driver.implicitly_wait(5)
    driver.get(getdriver)
    sleep(5)

    driver.find_element("xpath", "//input[@name='username']").send_keys(username)
    driver.find_element("xpath", "//input[@name='password']").send_keys(passwd)

    waiter.find_element(driver, "//div/button[@type='submit']", by=XPATH).click()

    sleep(5)

    return driver


def scraper_location(driver, location_name, location_id, count=0):
    if count > 3:
            return None
    
    query = 'https://www.instagram.com/web/search/topsearch/?context=blended&query=' + location_name

    try:
        location_json = selenium_requests(driver, query)
        #app.logger.info(location_json)
        for x in location_json['places']:
            if x['place']['location']['pk'] == location_id:
                app.logger.info(location_id)
                return x['place']['location']
    except: 
        sleep(randint(3*100,8*100)/100)
        count = count + 1
        scraper_location(driver, location_name, location_id, count)


def selenium_requests(driver, url):
    driver.get(url)
    soup = BeautifulSoup(driver.page_source, 'lxml')
    return json.loads(soup.find("body").text)


#@app.route('/api/download_data/', methods=['POST'])
def download_data(target):
    try:
        #req_json = request.get_json()
        #app.logger.info(req_json)

        #if not req_json["username"] or not req_json["passwd"] or not req_json["target"]:
        #    return {}

        #create instaloader instance
        L = instaloader.Instaloader(save_metadata = True,download_geotags = True,compress_json = False,download_pictures = True,download_videos = True,download_video_thumbnails = True)

        #L.context.session_id = None  # Force new session
        #L.login(req_json["username"], req_json["passwd"]) 
        
        #profile = instaloader.Profile.from_username(L.context, req_json["target"])
        profile = instaloader.Profile.from_username(L.context, target)
        L.download_profiles([profile],profile_pic=False) #fast_update=True

        return req_json
    except:
        return {}




@app.route('/api/get_geo/', methods=['POST'])
def get_geo():
    try:   
        req_json = request.get_json()
        app.logger.info(req_json)

        if not req_json["username"] or not req_json["passwd"] or not req_json["target"]:
            return {}
        

        #to download data
        download_data(req_json["target"])
        
        

        jsons_data = readJson(req_json["target"])
        
        driver = selenium_open(req_json["username"], req_json["passwd"])

        for i, row in jsons_data.iterrows():
            if np.isnan(row["lat"]) or np.isnan(row["lng"]):
                location = scraper_location(driver,row["slug"],row["id"])
                app.logger.info(location)
                if not (location is None):
                    jsons_data.loc[jsons_data['id'] == row["id"], 'lat'] = location['lat']
                    jsons_data.loc[jsons_data['id'] == row["id"], 'lng'] = location['lng']

                    #jsons_data.at[i,'lat'] = location['lat']
                    #jsons_data.at[i,'lng'] = location['lng']
                sleep(randint(3*100,8*100)/100)
        
        driver.close() 

        #double check if there is no null
        jsons_data.dropna(subset=['lat','lng'], inplace=True)

        #app.logger.info(jsons_data)

        with open(req_json["target"]+'/data.json', 'w+') as f:
            f.write(jsons_data.reset_index(drop=True).to_json(orient='records'))

        return {}
    except:
        return {}  


@app.route('/api/get_data/', methods=['POST'])
def get_data():
    try:    
        req_json = request.get_json()
        app.logger.info(req_json)

        if not req_json["target"]:
            return {}
        
        with open(req_json["target"]+'/data.json', 'r') as f:
            return json.load(f)

    except:
        return {}

@app.route('/api/get_media/', methods=['GET'])
def get_media():
    #try:    
        picDir = request.args.get('pic')

        if not picDir:
            return send_file('error.png', mimetype='image/png')
        
        app.logger.info(picDir)
        #support only png and jpg for now  
        file_types = ['png','jpg'] #,'mp4'
        
        for x in file_types:
            print(picDir[:-4]+x)
            if os.path.isfile(picDir[:-4]+x):
                if x == 'png':
                    return send_file(picDir[:-4]+x, mimetype='image/png')
                if x == 'jpg':
                    return send_file(picDir[:-4]+x, mimetype='image/jpg')

        return send_file('error.png', mimetype='image/png')

if __name__ == '__main__':
    app.run(debug=True, port=8001)

