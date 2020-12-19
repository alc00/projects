# Data Collection Process #

# Importing Libraries

## Import Directory Packages and set Initial Working Directory
import os
os.chdir("C:\\Users\\Allen\\Desktop\\Code\\Projects\\Property\\Python Data Collection")

## Import Date and Time
import datetime

## Import package to open and access web pages
import requests as req

## Import package to parse web pages
from bs4 import BeautifulSoup as BS

## Import Regular Expressions
import re

## Import Delay
import time

## Import Package to Access SQLite
import sqlite3

## Import Custom Functions
from web_scraping_99_co import *
from web_scraping_99_co_list_of_listings import *


# Setting up connection to SQLite Database
db_conn = sqlite3.connect("C:\\Users\\Allen\\Desktop\\Code\\Projects\\Property\\SQLite\\project_property.db", timeout=5)

# Preparing Web Scraping Initial Details
## Adding Browser Headers
firefox_headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:83.0) Gecko/20100101 Firefox/83.0"}

## Adding the initial URL of the site
initial_url = "https://www.99.co/singapore/sale"
### URL List
#### Rental Whole Units/Property: https://www.99.co/singapore/rent
#### Rental Rooms: https://www.99.co/singapore/rent?rental_type=room
#### Sale Listings: https://www.99.co/singapore/sale



# Collecting Listing Links
## Getting the links in python list object
listing_links_cleaned = list()
listing_links_cleaned = all_99_co_gather_listing_links(initial_url, firefox_headers)

## Confirmation of Collection of Links
print("Gathered a total of " + str(len(listing_links_cleaned)) + " Listing Links")

## Addings Links to Database
db_cur = db_conn.cursor()
for link in listing_links_cleaned:
    db_cur.execute(
        '''
        INSERT OR IGNORE 
        INTO DM_99_CO_LISTING_LINKS_T (LINK)
        VALUES( ? )
        ''', 
        ( link, )
        )
    
db_cur.close()
db_conn.commit()


# Gathering Listings Data
## Getting link
### Get links from database
db_cur = db_conn.cursor()
db_cur.execute(
    '''
        SELECT
        DISTINCT
        LINK
        FROM DM_99_CO_LISTING_LINKS_T
        
        EXCEPT
        
        SELECT
        DISTINCT
        LINK
        FROM DM_99_CO_LISTINGS_LINKS_USED_T
    '''
    )

listing_links_gathering_p1 = db_cur.fetchall()

db_cur.close()

listing_links_gathering = list()

for link in listing_links_gathering_p1:
    listing_links_gathering.append(link[0])

print("Unused Links Gathered: " + str(len(listing_links_gathering)))

# Getting Data from Webpage
list_insert_cnt_num = 0
list_insert_fail_cnt_num = 0
db_cur = db_conn.cursor()


for link in listing_links_gathering:
    try: # Attempt to Retrieve Web Page Data
        ## Access Web Page
        time.sleep(5)
        
        url_current = link
        
        url_req = req.get(url_current, headers = firefox_headers)
        
        url_req.close()
        
        url_content = BS(url_req.content.decode(),"html.parser")
        
        ## Determine Sale or Rental Listing
        if re.search("^https://www.99.co/singapore/sale/", link):
            listing_type = "Sale"
        elif re.search("^https://www.99.co/singapore/rent/", link) or re.search("^https://www.99.co/singapore/rooms/", link):
            listing_type = "Rental"
        
        
        ## Checking Webpage Layout - Based on Identification of Class
        layout_identifier = len(
                                url_content.find_all("div", {"class":"TBTkb _36xav kjJF5"})
                                )
        
        if layout_identifier != 0:
            layout_tag = 1 #Layout of Must See Pages
        else:
            layout_tag = 2 #Layout of Other Listing Pages
        
        ## Gather the Data based on the functions from a different file
        results = dict()
        if layout_tag == 1 and listing_type == "Rental":
            results = rental_99_co_layout_1_webpage_collection_f(url_content)
        elif layout_tag == 2 and listing_type == "Rental":
            results = rental_99_co_layout_2_webpage_collection_f(url_content)
        elif layout_tag == 1 and listing_type == "Sale":
            results = sale_99_co_layout_1_webpage_collection_f(url_content)
        elif layout_tag == 2 and listing_type == "Sale":
            results = sale_99_co_layout_2_webpage_collection_f(url_content)
        
        ## Insert into Database
        ### Insert into Property - Developer / Building Info Table
        db_cur.execute(
            '''
            INSERT OR IGNORE INTO DM_99_CO_LISTING_PROPERTY_T 
            (NAME, TYPE, UNIT_TYPES, UNIT_CNT, BUILD_YEAR, GOV_LEASE, DEVELOPER_NAME, NEIGHBOURHOOD)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''',
            (results["property_name"], results["property_type"], results["property_unit_types"],
             results["property_unit_cnt"], results["property_build_year"], results["property_gov_lease"],
             results["property_developer"], results["property_neigbourhood"])
            )
        
        ### Insert into Listing Additional Info Table
        #### Get Property ID
        db_cur.execute(
            'SELECT PROPERTY_ID FROM DM_99_CO_LISTING_PROPERTY_T WHERE NAME = ?', 
            (results["property_name"],)
            )
        
        property_id = db_cur.fetchone()
        
        #### Add Additional Info
        db_cur.execute(
            '''
            INSERT OR IGNORE INTO DM_99_CO_LISTING_ADD_INFO_T 
            (LEASE_START, LEASE_TYPE, LEASE_FACING, LEASE_FURNITURE, RULE_PETS, 
             RULE_COOKING, RULE_GUESTS, LEASE_STAY_IN_OWNER, RULE_SMOKING, PROPERTY_ID)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''',
            (results["lease_start"], results["lease_type"], results["property_facing"],
             results["property_furniture"], results["rule_pets"], results["rule_cooking"],
             results["rule_guests"], results["lease_stay_in_owner"], results["rule_smoking"],
             property_id[0])
            )
        
        ### Insert into Amenities Table
        
        #### Get Listing ID
        db_cur.execute(
            'SELECT IFNULL(MAX(LISTING_ID),0) FROM DM_99_CO_LISTING_ADD_INFO_T'
            )
        
        listing_id = db_cur.fetchone()
        
        
        #### Insert Amenities Data
        for amenity_item in range(len(results["amenities"])):
            db_cur.execute(
                '''
                INSERT OR IGNORE INTO DM_99_CO_LISTING_AMENITIES_T
                (LISTING_ID, NAME_AMENITY)
                VALUES (?, ?)
                ''',
                (listing_id[0], results["amenities"][amenity_item])
                )
        
        ### Insert into Primary Listing Table
        db_cur.execute(
            '''
            INSERT OR IGNORE INTO DM_99_CO_LISTING_SUMMARY_T
            (DTIME_INSERTED, LISTING_TYPE, RENTAL_TYPE, LISTING_NAME, VALUE, VALUE_PSF,
             CNT_BEDS, CNT_BATHS, SIZE_SQFT, LATITUDE, LONGITUDE, LISTING_LINK)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''',
            (datetime.datetime.now().strftime("%Y/%m/%d %H:%M:%S"), listing_type,
             results["rental_type"], results["listing_name"], results["value"], 
             results["value_psf"], results["cnt_beds"], results["cnt_baths"], 
             results["property_size"], results["latitude"], results["longitude"], 
             url_current)
            )
        
        ### Insert Link into Used Links
        db_cur.execute(
            '''
            INSERT OR IGNORE INTO DM_99_CO_LISTINGS_LINKS_USED_T (LINK)
            VALUES (?)
            ''',
            (url_current, )
            )
        
        ### Commit Changes
        db_conn.commit()
        ## Indicate Progress
        list_insert_cnt_num = list_insert_cnt_num + 1
        print("Listing Inserted: " + str(list_insert_cnt_num))
        
    except: # If fail note now the number of failures then skip the link for now
        list_insert_fail_cnt_num = list_insert_fail_cnt_num + 1
        print("Listing Insert Failed: " + str(list_insert_fail_cnt_num))

## Closing Cursor
db_cur.close()

# Summary Results
print("Listings Inserted: " + str(list_insert_cnt_num))
print("Listings Insert Failures: " + str(list_insert_fail_cnt_num))
print("Total Attempted Retrievals: " + str(list_insert_cnt_num + list_insert_fail_cnt_num))


