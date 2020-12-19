### Import package to open and access web pages
import requests as req

### Import package to parse web pages
from bs4 import BeautifulSoup as BS

### Import Regular Expressions
import re

### Import Delay
import time

### Create 1 Line Try/Except for the equivalent of if error / null then
def iferror(task, default):
    try:
        return task()
    except:
        return default

def all_99_co_gather_listing_links(initial_url, firefox_headers):
    
    # Access Initial Page
    url_req = req.get(initial_url, headers = firefox_headers)
    
    url_req.close()
    
    url_content = BS(url_req.content.decode(),"html.parser")
    
    # Get Total Number of Pages for Rental
    cnt_pages_raw = url_content.find_all("a", {"role": "button"}, href=True)
    
    ## Got the max number of pages based on webpage layout
    cnt_pages = int(cnt_pages_raw[len(cnt_pages_raw)-2].text)
    
    # Get Listing Links
    listing_links_raw = url_content.find_all("a", {"class": "_17qrb WgBDo"}, href=True)
    listing_links = re.findall(r'href=\"(.+?)\?enquiry_position',str(listing_links_raw))
    
    # Get Link for Next Page
    
    ## Check if Rent is Room or Entire Unit/Property
    if initial_url == "https://www.99.co/singapore/rent?rental_type=room":
        room_rent_tag = 1
    else:
        room_rent_tag = 0
        
    listings_next_page_raw = url_content.find_all("a", {"role": "button", "rel":"next"})
    listings_next_page = re.findall(r'href=\"(.+?)\"',str(listings_next_page_raw))[0]
    
    ## If Rental is Room then add required parameter
    if room_rent_tag == 0:
        listings_next_page = "https://www.99.co" + listings_next_page
    elif room_rent_tag == 1:
        listings_next_page = "https://www.99.co" + listings_next_page + "&rental_type=room"
    
    
    print("Page 1 Done")
    
    
    
    # Get Number of Pages to Scrape
    retry_pages = 0
    
    while retry_pages < 3:
        cnt_pages_input = input(r'Number of Pages to Extract (input "All" for all pages): ')
        try:
            cnt_pages_input = int(cnt_pages_input)
            if cnt_pages_input > 0:
                if cnt_pages_input >= cnt_pages:
                    cnt_pages_input = cnt_pages # if the requested pages is greater or equal to total pages, then put total pages instead
                    break
                else:
                    break
            else:
                retry_pages = retry_pages + 1
            
            print("Error - Number of Retries Left: " + str(3-retry_pages))

        except:            
            if cnt_pages_input == "All":
                cnt_pages_input = cnt_pages 
                break
            else:
                retry_pages = retry_pages + 1
            
            print("Error - Number of Retries Left: " + str(3-retry_pages))
            
    if retry_pages == 3:
        cnt_pages_input = 1
        
    print("Pages to be Gathered: " + str(cnt_pages_input))
    
    
    
    # Get Listings from Next Page
    for page_num in range(cnt_pages_input-1): # -1, as first page links have been gathered already
        # Wait for 5 Seconds
        time.sleep(5)
        
        # Access Next Page
        url_req = req.get(listings_next_page, headers = firefox_headers)
        
        url_req.close()
        
        url_content = BS(url_req.content.decode(),"html.parser")
    
        # Get Listing Links
        listing_links_raw = url_content.find_all("a", {"class": "_17qrb WgBDo"}, href=True)
        listing_links = listing_links + re.findall(r'href=\"(.+?)\?enquiry_position',str(listing_links_raw))
        
        # Get Link for Next Page
        listings_next_page_raw = url_content.find_all("a", {"role": "button", "rel":"next"})
        listings_next_page = re.findall(r'href=\"(.+?)\"',str(listings_next_page_raw))[0]
        
        ## If Rental is Room then add required parameter
        if room_rent_tag == 0:
            listings_next_page = "https://www.99.co" + listings_next_page
        elif room_rent_tag == 1:
            listings_next_page = "https://www.99.co" + listings_next_page + "&rental_type=room"
        
        print("Page " + str(2 + page_num) + " Done")
        
    # Clean the links
    listing_links_cleaned = list()
    for link_num in range(len(listing_links)):
        listing_link_complete = ("https://www.99.co" + listing_links[link_num])
        listing_links_cleaned.append(listing_link_complete)
    return listing_links_cleaned
