### Import package to parse web pages
from bs4 import BeautifulSoup as BS

### Import Regular Expressions
import re


def rental_99_co_layout_1_webpage_collection_f(url_content):
    # Get Information under Class "_1zGm8 _1vzK2" only, which contains the listing name
    title_content = url_content.find_all("h1", {"class":"_1zGm8 _1vzK2"})
    listing_name = title_content[0].text
    
    # Get Information under Class "_1oSRo" only, which contains pricing and descriptive data
    main_content = url_content.find_all("div", {"class":"_1oSRo"})
    
    
    ## Get Rental Price per Month
    ### Split Rental per Month and Rental per Square Foot: Get Rental per Month Only
    rental_p = re.split("/", main_content[0].text)[0]
    ### Remove Currency
    rental_p = re.findall("S\\$(.+)", rental_p)[0]
    ### Remove thousands separator / commas
    rental_p = re.sub(",", "", rental_p)
    
    
    
    ## Get Rental Price per Square Foot
    ### Split Rental per Month and Rental per Square Foot: Get Rental per Square Foot Only
    rental_psf = re.split("/", main_content[0].text)[1]
    ### Remove any characters except for the amount
    rental_psf = re.findall("moS\\$(.+) psf", rental_psf)[0]
    rental_psf = re.sub(",", "", rental_psf)
    
    
    
    ## Get Number of Bed Spaces
    ### Get Initial Data
    num_beds = main_content[1].text
    ### Get Value Only
    if re.search("Studio", num_beds):
        num_beds = 1
    else:
        num_beds = re.sub("[A-z ]","", num_beds)
    
    
    ## Get Number of Bathrooms
    ### Get Initial Data
    num_baths = main_content[2].text
    ### Get Value Only
    num_baths = re.sub("[A-z ]","", num_baths)
    
    
    ## Get Rental Size
    ### Get Initial Data
    rental_size = main_content[3].text
    ### Get Value Only
    rental_size = re.findall("([0-9]+)", re.sub(",","",rental_size))[0]
    
    
    # Get Information under Class "_2NgLW" only, which contains the listing text description
    body_content = url_content.find_all("div", {"class":"_2NgLW"})
    listing_body = body_content[0].text
    
    # Get Information under Class "dm2g6" only, which contains additional leasing info about room and property
    add_info_content_attribute = url_content.find_all("td", {"class":"_3NChA"})
    add_info_content_value = url_content.find_all("td", {"class":"dm2g6"})
    add_info_content_data = dict()
    for attribute_num in range(len(add_info_content_attribute)):
        add_info_content_data[add_info_content_attribute[attribute_num].text] = add_info_content_value[attribute_num].text
    

    lease_start = add_info_content_data.get("Availability", "N/A")
    lease_type = add_info_content_data.get("Lease", "N/A")
    room_facing = add_info_content_data.get("Facing", "N/A")
    room_furnishing = add_info_content_data.get("Furnishing", "N/A")
    
    property_type = add_info_content_data.get("Property type", "N/A")
    property_name = add_info_content_data.get("Name", "N/A")
    property_unit_types = add_info_content_data.get("Unit types", "N/A")
    property_unit_cnt = add_info_content_data.get("Total units", "N/A")
    property_build_year = add_info_content_data.get("Built year", "N/A")
    
    # for property_gov_lease, as there may be numeric and non-numeric values
    if add_info_content_data.get("Tenure", "N/A") == "Freehold":
        property_gov_lease = "Freehold"
    elif add_info_content_data.get("Tenure", "N/A") == "N/A":
        property_gov_lease = "N/A"
    else:
        property_gov_lease = re.sub("[A-z ]", "", add_info_content_data.get("Tenure", "N/A"))
        
    property_developer = add_info_content_data.get("Developer", "N/A")
    property_neigbourhood = add_info_content_data.get("Neighbourhood", "N/A")
    
    rule_pets = add_info_content_data.get("Pets", "N/A")
    rule_cooking = add_info_content_data.get("Cooking", "N/A")
    rule_guests = add_info_content_data.get("Overnight Guest", "N/A")
    lease_stay_in_owner = add_info_content_data.get("Stay In Owner", "N/A")
    rule_smoking = add_info_content_data.get("Smoking", "N/A")
    
    # Get Coordinates Data based on layout of webpage
    ## Find 1st instance of "Coordinates"
    coordinates_content_html_2 = re.findall("coordinates.+?}", url_content.prettify())[0]
    ## Isolate Coordinates
    coordinates_lat = re.findall(r'"lat":(.+)?,', coordinates_content_html_2)[0]
    coordinates_lng = re.findall(r'"lng":(.+)?}', coordinates_content_html_2)[0]
    
    #Get Amenities Data
    amenities = list()
    amenities_content = url_content.find_all("p", {"class":"_2sIc2 AIgs2 _2rhE-"})
    for item_num in range(len(amenities_content)):
        amenities.append(amenities_content[item_num].text)
    
    # Return All Data
    results = dict()
    results["listing_name"] = listing_name
    results["value"] = rental_p
    results["value_psf"] = rental_psf
    results["cnt_beds"] = num_beds
    results["cnt_baths"] = num_baths
    results["property_size"] = rental_size
    results["latitude"] = coordinates_lat
    results["longitude"] = coordinates_lng
    results["coordinates"] = (coordinates_lat + ", " + coordinates_lng)
    results["lease_start"] = lease_start
    results["lease_type"] = lease_type
    results["property_facing"] = room_facing
    results["property_furniture"] = room_furnishing
    results["property_type"] = property_type
    results["property_name"] = property_name
    results["property_unit_types"] = property_unit_types
    results["property_unit_cnt"] = property_unit_cnt
    results["property_build_year"] = property_build_year
    results["property_gov_lease"] = property_gov_lease
    results["property_developer"] = property_developer
    results["property_neigbourhood"] = property_neigbourhood
    
    results["rental_type"] = "Entire Unit/Property"
    results["rule_pets"] = rule_pets
    results["rule_cooking"] = rule_cooking
    results["rule_guests"] = rule_guests
    results["lease_stay_in_owner"] = lease_stay_in_owner
    results["rule_smoking"] = rule_smoking
    
    results["amenities"] = amenities
    
    return results
    


def rental_99_co_layout_2_webpage_collection_f(url_content):
    # Get Information under Class "_1zGm8 _1vzK2" only, which contains the listing name
    title_content = url_content.find_all("h1", {"class":"Z0npN"})
    listing_name = title_content[0].text
    
        
    ## Get Rental Price per Month
    ### Get Information under Class "_2uceZ QjSiC" only, which contains the required data
    rpm_content = url_content.find_all("div", {"class":"_2uceZ QjSiC"})
    ### Split Rental per Month and Rental per Square Foot: Get Rental per Month Only
    rental_p = re.split("/", rpm_content[0].text)[0]
    ### Remove Currency
    rental_p = re.findall("S\\$(.+)", rental_p)[0]
    ### Remove thousands separator / commas
    rental_p = re.sub(",", "", rental_p)
    
    
    
    ## Get Rental Price per Square Foot
    ### Get Information under Class "_1W0zC" only, which contains the required data
    summary_content = url_content.find_all("div", {"class":"_1W0zC"})
    
    ### Allow for Dymanic Selection as Data Availability is inconsistent
    ## Create Varialbes
    rental_psf = "N/A"
    num_beds = "N/A"
    num_baths = "N/A"
    rental_size = "N/A"
    room_type = "Entire Unit/Property"
    
    for summary_content_item in summary_content:
        
        ## Get Rental per Square Foot 
        if re.search("psf", summary_content_item.text):
            rental_psf = summary_content_item.text
            ### Remove any characters except for the amount
            rental_psf = re.findall("S\\$(.+) psf", rental_psf)[0]
            rental_psf = re.sub(",", "", rental_psf)
            
        ## Get Number of Bed Spaces
        elif re.search("Bed", summary_content_item.text) or re.search("Studio", summary_content_item.text):
            ### Get Initial Data
            num_beds = summary_content_item.text
            ### Get Value Only
            if re.search("Studio", num_beds):
                num_beds = 1
            else:
                num_beds = re.sub("[A-z ]","", num_beds)
                
        ## Get Number of Bathrooms
        elif re.search("Bath", summary_content_item.text):
            ### Get Initial Data
            num_baths = summary_content_item.text
            ### Get Value Only
            num_baths = re.sub("[A-z ]","", num_baths)

        ## Get Room Type (for Room Rentals)
        elif re.search("Room", summary_content_item.text):
            ### Get Value
            room_type = summary_content_item.text
        
        ## Get Rental Size
        elif re.search("sqft", summary_content_item.text):
            ### Get Initial Data
            rental_size = summary_content_item.text
            ### Get Value Only
            if room_type == "Entire Unit/Property":
                rental_size = re.findall("([0-9]+)", re.sub(",","",summary_content[1].text))[0][0]
            else:
                rental_size = re.findall("([0-9]+)", re.sub(",","",summary_content[1].text))[0]
                

    
    # Get Information under Class "lEhtw" only, which contains the listing text description
    body_content = url_content.find_all("pre", {"class":"lEhtw"})
    listing_body = body_content[0].text
    
    # Get Information under Class "_28kbc" and "_16cFj", which contains additional leasing info about room and property
    add_info_content = url_content.find_all("div", {"class":"_28kbc"})
    
    # As the class names for the property data attribute sometimes changes, we will account for 2 scenarios
    
    ## Scenario A
    add_info_content_prop_scenario = "A"
    add_info_content_prop = url_content.find_all("div", {"class":"_16cFj"})
    
    ## If Scenario A is Empty: Check Scenario B
    if len(add_info_content_prop) == 0:
        add_info_content_prop = url_content.find_all("p", {"class":"JPolj"})
        add_info_content_prop_scenario = "B"
        
    
    
    ## As the information content is dynamic, we will be collecting the attributes available
    add_info_content_data = dict()
    for attribute_num in range(len(add_info_content)):
        add_info_v = add_info_content[attribute_num]
        add_info_content_data[add_info_v.contents[0].text] = add_info_v.contents[1].text
    

    add_info_content_data_prop = dict()
    ## If Property/Developer data is not available (e.g. landed house), then skip
    if len(add_info_content_prop) == 0:
        pass
    
    ### Scenario A
    #### Note that the length was deducted by 1, since the last attribute is merely a disclaimer
    elif add_info_content_prop_scenario == "A":
        for attribute_num in range(len(add_info_content_prop[0].contents)-1): 
            add_info_v2 = add_info_content_prop[0].contents[attribute_num].text
            add_info_v2_split = re.split(": ", add_info_v2)
            add_info_content_data_prop[add_info_v2_split[0]] = add_info_v2_split[1]
    #### Scenario B
    elif add_info_content_prop_scenario == "B":
        for attribute_num in range(len(add_info_content_prop)): 
            add_info_v2 = add_info_content_prop[attribute_num].text
            add_info_v2_split = re.split(": ", add_info_v2)
            ##### If Property Data, the data should contain ":", if not ignore
            if len(add_info_v2_split) > 1:
                add_info_content_data_prop[add_info_v2_split[0]] = add_info_v2_split[1]
            else:
                pass
    
        
    ## Add information if available
    lease_start = add_info_content_data.get("Availability", "N/A")
    lease_type = add_info_content_data.get("Lease", "N/A")
    room_facing = add_info_content_data.get("Facing", "N/A")
    room_furnishing = add_info_content_data.get("Furnishing", "N/A")
    
    property_type = add_info_content_data.get("Property type", "N/A")
    property_name = add_info_content_data_prop.get("Name", "N/A")
    property_unit_types = add_info_content_data_prop.get("Unit types", "N/A")
    property_unit_cnt = add_info_content_data_prop.get("Total units", "N/A")
    property_build_year = add_info_content_data_prop.get("Built year", "N/A")
    
    # for property_gov_lease, as there may be numeric and non-numeric values
    if add_info_content_data_prop.get("Tenure", "N/A") == "Freehold":
        property_gov_lease = "Freehold"
    elif add_info_content_data_prop.get("Tenure", "N/A") == "N/A":
        property_gov_lease = "N/A"
    else:
        property_gov_lease = re.sub("[A-z ]", "", add_info_content_data_prop.get("Tenure", "N/A"))

    property_developer = add_info_content_data_prop.get("Developer", "N/A")
    property_neigbourhood = add_info_content_data_prop.get("Neighbourhood", "N/A")
    
    rule_pets = add_info_content_data.get("Pets", "N/A")
    rule_cooking = add_info_content_data.get("Cooking", "N/A")
    rule_guests = add_info_content_data.get("Overnight Guest", "N/A")
    lease_stay_in_owner = add_info_content_data.get("Stay In Owner", "N/A")
    rule_smoking = add_info_content_data.get("Smoking", "N/A")
    
    # Get Coordinates Data based on layout of webpage
    ## Find 1st instance of "Coordinates"
    coordinates_content_html_2 = re.findall("coordinates.+?}", url_content.prettify())[0]
    ## Isolate Coordinates
    coordinates_lat = re.findall(r'"lat":(.+)?,', coordinates_content_html_2)[0]
    coordinates_lng = re.findall(r'"lng":(.+)?}', coordinates_content_html_2)[0]
    
    #Get Amenities Data
    amenities = list()
    amenities_content = url_content.find_all("p", {"class":"JPolj _26v8n"})
    for item_num in range(len(amenities_content)):
        amenities.append(amenities_content[item_num].text)
    
    # Return All Data
    results = dict()
    results["listing_name"] = listing_name
    results["value"] = rental_p
    results["value_psf"] = rental_psf
    results["cnt_beds"] = num_beds
    results["cnt_baths"] = num_baths
    results["property_size"] = rental_size
    results["latitude"] = coordinates_lat
    results["longitude"] = coordinates_lng
    results["coordinates"] = (coordinates_lat + ", " + coordinates_lng)
    results["lease_start"] = lease_start
    results["lease_type"] = lease_type
    results["property_facing"] = room_facing
    results["property_furniture"] = room_furnishing
    results["property_type"] = property_type
    results["property_name"] = property_name
    results["property_unit_types"] = property_unit_types
    results["property_unit_cnt"] = property_unit_cnt
    results["property_build_year"] = property_build_year
    results["property_gov_lease"] = property_gov_lease
    results["property_developer"] = property_developer
    results["property_neigbourhood"] = property_neigbourhood
    
    results["rental_type"] = room_type
    results["rule_pets"] = rule_pets
    results["rule_cooking"] = rule_cooking
    results["rule_guests"] = rule_guests
    results["lease_stay_in_owner"] = lease_stay_in_owner
    results["rule_smoking"] = rule_smoking
    
    results["amenities"] = amenities
        
    return results



def sale_99_co_layout_1_webpage_collection_f(url_content):
    # Get Information under Class "_1zGm8 _1vzK2" only, which contains the listing name
    title_content = url_content.find_all("h1", {"class":"_1zGm8 _1vzK2"})
    listing_name = title_content[0].text
    
    # Get Information under Class "_1oSRo" only, which contains pricing and descriptive data
    main_content = url_content.find_all("div", {"class":"_1oSRo"})
    
    
    ## Get Sale Price per Month
    ### Sale Price
    ### Remove Currency
    sale_p = re.findall("S\\$(.+)", main_content[0].contents[0].text)[0]
    ### Remove thousands separator / commas
    sale_p = re.sub(",", "", sale_p)
    
    
    ## Get Sale Price per Square Foot
    ### Remove any characters except for the amount
    sale_psf = re.findall("S\\$(.+) psf", main_content[0].contents[1].text)[0]
    sale_psf = re.sub(",", "", sale_psf)
    
    
    
    ## Get Number of Bed Spaces
    ### Get Initial Data
    num_beds = main_content[1].text
    ### Get Value Only
    if re.search("Studio", num_beds):
        num_beds = 1
    else:
        num_beds = re.sub("[A-z ]","", num_beds)
    
    
    ## Get Number of Bathrooms
    ### Get Initial Data
    num_baths = main_content[2].text
    ### Get Value Only
    num_baths = re.sub("[A-z ]","", num_baths)
    
    
    ## Get Property Size
    ### Get Initial Data
    rental_size = main_content[3].text
    ### Get Value Only
    rental_size = re.findall("([0-9]+)", re.sub(",","",rental_size))[0]
    
    
    # Get Information under Class "_2NgLW" only, which contains the listing text description
    body_content = url_content.find_all("div", {"class":"_2NgLW"})
    listing_body = body_content[0].text
    
    # Get Information under Class "dm2g6" only, which contains additional leasing info about room and property
    add_info_content_attribute = url_content.find_all("td", {"class":"_3NChA"})
    add_info_content_value = url_content.find_all("td", {"class":"dm2g6"})
    add_info_content_data = dict()
    for attribute_num in range(len(add_info_content_attribute)):
        add_info_content_data[add_info_content_attribute[attribute_num].text] = add_info_content_value[attribute_num].text
    

    lease_start = add_info_content_data.get("Availability", "N/A")
    lease_type = add_info_content_data.get("Lease", "N/A")
    room_facing = add_info_content_data.get("Facing", "N/A")
    room_furnishing = add_info_content_data.get("Furnishing", "N/A")
    
    property_type = add_info_content_data.get("Property type", "N/A")
    property_name = add_info_content_data.get("Name", "N/A")
    property_unit_types = add_info_content_data.get("Unit types", "N/A")
    property_unit_cnt = add_info_content_data.get("Total units", "N/A")
    property_build_year = add_info_content_data.get("Built year", "N/A")
    
    # for property_gov_lease, as there may be numeric and non-numeric values
    if add_info_content_data.get("Tenure", "N/A") == "Freehold":
        property_gov_lease = "Freehold"
    elif add_info_content_data.get("Tenure", "N/A") == "N/A":
        property_gov_lease = "N/A"
    else:
        property_gov_lease = re.sub("[A-z ]", "", add_info_content_data.get("Tenure", "N/A"))
        
    property_developer = add_info_content_data.get("Developer", "N/A")
    property_neigbourhood = add_info_content_data.get("Neighbourhood", "N/A")
    
    rule_pets = add_info_content_data.get("Pets", "N/A")
    rule_cooking = add_info_content_data.get("Cooking", "N/A")
    rule_guests = add_info_content_data.get("Overnight Guest", "N/A")
    lease_stay_in_owner = add_info_content_data.get("Stay In Owner", "N/A")
    rule_smoking = add_info_content_data.get("Smoking", "N/A")
    
    # Get Coordinates Data based on layout of webpage
    ## Find 1st instance of "Coordinates"
    coordinates_content_html_2 = re.findall("coordinates.+?}", url_content.prettify())[0]
    ## Isolate Coordinates
    coordinates_lat = re.findall(r'"lat":(.+)?,', coordinates_content_html_2)[0]
    coordinates_lng = re.findall(r'"lng":(.+)?}', coordinates_content_html_2)[0]
    
    #Get Amenities Data
    amenities = list()
    amenities_content = url_content.find_all("p", {"class":"_2sIc2 AIgs2 _2rhE-"})
    for item_num in range(len(amenities_content)):
        amenities.append(amenities_content[item_num].text)
    
    # Return All Data
    results = dict()
    results["listing_name"] = listing_name
    results["value"] = sale_p
    results["value_psf"] = sale_psf
    results["cnt_beds"] = num_beds
    results["cnt_baths"] = num_baths
    results["property_size"] = rental_size
    results["latitude"] = coordinates_lat
    results["longitude"] = coordinates_lng
    results["coordinates"] = (coordinates_lat + ", " + coordinates_lng)
    results["lease_start"] = lease_start
    results["lease_type"] = lease_type
    results["property_facing"] = room_facing
    results["property_furniture"] = room_furnishing
    results["property_type"] = property_type
    results["property_name"] = property_name
    results["property_unit_types"] = property_unit_types
    results["property_unit_cnt"] = property_unit_cnt
    results["property_build_year"] = property_build_year
    results["property_gov_lease"] = property_gov_lease
    results["property_developer"] = property_developer
    results["property_neigbourhood"] = property_neigbourhood
    
    results["rental_type"] = "N/A"
    results["rule_pets"] = rule_pets
    results["rule_cooking"] = rule_cooking
    results["rule_guests"] = rule_guests
    results["lease_stay_in_owner"] = lease_stay_in_owner
    results["rule_smoking"] = rule_smoking
    
    results["amenities"] = amenities
    
    return results



def sale_99_co_layout_2_webpage_collection_f(url_content):
    # Get Information under Class "_1zGm8 _1vzK2" only, which contains the listing name
    title_content = url_content.find_all("h1", {"class":"Z0npN"})
    listing_name = title_content[0].text
    
        
    ## Get Sale Price
    ### Get Information under Class "_2uceZ QjSiC" only, which contains the required data
    rpm_content = url_content.find_all("div", {"class":"_2uceZ QjSiC"})
    ### Get Sale Price
    sale_p = rpm_content[0].contents[0].text
    
    # Identify if the value contains "M" for million
    if re.search("M", sale_p):
        million_tag = 1
    else:
        million_tag = 0
        
    ### Remove Currency
    sale_p = re.findall("S\\$(.+)", sale_p)[0]
    ### Remove thousands separator / commas
    sale_p = re.sub(",", "", sale_p)
    ### Remove Millions if any
    sale_p = re.sub("M", "", sale_p)
    
    ### Convert to float then adjust for million value (if any)
    if million_tag == 1:
        sale_p = float(sale_p) * 1000000
    elif million_tag == 0:
        sale_p = float(sale_p)
        
    
    
    ## Get Sale Price per Square Foot
    ### Get Information under Class "_1W0zC" only, which contains the required data
    summary_content = url_content.find_all("div", {"class":"_1W0zC"})

    ### Allow for Dymanic Selection as Data Availability is inconsistent
    ## Create Varialbes
    sale_psf = "N/A"
    num_beds = "N/A"
    num_baths = "N/A"
    rental_size = "N/A"
    room_type = "Entire Unit/Property"
    
    for summary_content_item in summary_content:
        
        ## Get Sale per Square Foot 
        if re.search("psf", summary_content_item.text):
            sale_psf = summary_content_item.text
            ### Remove any characters except for the amount
            sale_psf = re.findall("S\\$(.+) psf", sale_psf)[0]
            sale_psf = re.sub(",", "", sale_psf)
            
        ## Get Number of Bed Spaces
        elif re.search("Bed", summary_content_item.text) or re.search("Studio", summary_content_item.text):
            ### Get Initial Data
            num_beds = summary_content_item.text
            ### Get Value Only
            if re.search("Studio", num_beds):
                num_beds = 1
            else:
                num_beds = re.sub("[A-z ]","", num_beds)
                
        ## Get Number of Bathrooms
        elif re.search("Bath", summary_content_item.text):
            ### Get Initial Data
            num_baths = summary_content_item.text
            ### Get Value Only
            num_baths = re.sub("[A-z ]","", num_baths)

        ## Get Room Type (for Room Rentals)
        elif re.search("Room", summary_content_item.text):
            ### Get Value
            room_type = summary_content_item.text
        
        ## Get Property Size
        elif re.search("sqft", summary_content_item.text):
            ### Get Initial Data
            rental_size = summary_content_item.text
            ### Get Value Only
            if room_type == "Entire Unit/Property":
                rental_size = re.findall("([0-9]+)", re.sub(",","",summary_content[1].text))[0][0]
            else:
                rental_size = re.findall("([0-9]+)", re.sub(",","",summary_content[1].text))[0]
                

    
    # Get Information under Class "lEhtw" only, which contains the listing text description
    body_content = url_content.find_all("pre", {"class":"lEhtw"})
    listing_body = body_content[0].text
    
    # Get Information under Class "_28kbc" and "_16cFj", which contains additional leasing info about room and property
    add_info_content = url_content.find_all("div", {"class":"_28kbc"})
    
    # As the class names for the property data attribute sometimes changes, we will account for 2 scenarios
    
    ## Scenario A
    add_info_content_prop_scenario = "A"
    add_info_content_prop = url_content.find_all("div", {"class":"_16cFj"})
    
    ## If Scenario A is Empty: Check Scenario B
    if len(add_info_content_prop) == 0:
        add_info_content_prop = url_content.find_all("p", {"class":"JPolj"})
        add_info_content_prop_scenario = "B"
        
    
    
    ## As the information content is dynamic, we will be collecting the attributes available
    add_info_content_data = dict()
    for attribute_num in range(len(add_info_content)):
        add_info_v = add_info_content[attribute_num]
        add_info_content_data[add_info_v.contents[0].text] = add_info_v.contents[1].text
    

    add_info_content_data_prop = dict()
    ## If Property/Developer data is not available (e.g. landed house), then skip
    if len(add_info_content_prop) == 0:
        pass
    
    ### Scenario A
    #### Note that the length was deducted by 1, since the last attribute is merely a disclaimer
    elif add_info_content_prop_scenario == "A":
        for attribute_num in range(len(add_info_content_prop[0].contents)-1): 
            add_info_v2 = add_info_content_prop[0].contents[attribute_num].text
            add_info_v2_split = re.split(": ", add_info_v2)
            add_info_content_data_prop[add_info_v2_split[0]] = add_info_v2_split[1]
    #### Scenario B
    elif add_info_content_prop_scenario == "B":
        for attribute_num in range(len(add_info_content_prop)): 
            add_info_v2 = add_info_content_prop[attribute_num].text
            add_info_v2_split = re.split(": ", add_info_v2)
            ##### If Property Data, the data should contain ":", if not ignore
            if len(add_info_v2_split) > 1:
                add_info_content_data_prop[add_info_v2_split[0]] = add_info_v2_split[1]
            else:
                pass
    
        
    ## Add information if available
    lease_start = add_info_content_data.get("Availability", "N/A")
    lease_type = add_info_content_data.get("Lease", "N/A")
    room_facing = add_info_content_data.get("Facing", "N/A")
    room_furnishing = add_info_content_data.get("Furnishing", "N/A")
    
    property_type = add_info_content_data.get("Property type", "N/A")
    property_name = add_info_content_data_prop.get("Name", "N/A")
    property_unit_types = add_info_content_data_prop.get("Unit types", "N/A")
    property_unit_cnt = add_info_content_data_prop.get("Total units", "N/A")
    property_build_year = add_info_content_data_prop.get("Built year", "N/A")
    
    # for property_gov_lease, as there may be numeric and non-numeric values
    if add_info_content_data_prop.get("Tenure", "N/A") == "Freehold":
        property_gov_lease = "Freehold"
    elif add_info_content_data_prop.get("Tenure", "N/A") == "N/A":
        property_gov_lease = "N/A"
    else:
        property_gov_lease = re.sub("[A-z ]", "", add_info_content_data_prop.get("Tenure", "N/A"))

    property_developer = add_info_content_data_prop.get("Developer", "N/A")
    property_neigbourhood = add_info_content_data_prop.get("Neighbourhood", "N/A")
    
    rule_pets = add_info_content_data.get("Pets", "N/A")
    rule_cooking = add_info_content_data.get("Cooking", "N/A")
    rule_guests = add_info_content_data.get("Overnight Guest", "N/A")
    lease_stay_in_owner = add_info_content_data.get("Stay In Owner", "N/A")
    rule_smoking = add_info_content_data.get("Smoking", "N/A")
    
    # Get Coordinates Data based on layout of webpage
    ## Find 1st instance of "Coordinates"
    coordinates_content_html_2 = re.findall("coordinates.+?}", url_content.prettify())[0]
    ## Isolate Coordinates
    coordinates_lat = re.findall(r'"lat":(.+)?,', coordinates_content_html_2)[0]
    coordinates_lng = re.findall(r'"lng":(.+)?}', coordinates_content_html_2)[0]
    
    #Get Amenities Data
    amenities = list()
    amenities_content = url_content.find_all("p", {"class":"JPolj _26v8n"})
    for item_num in range(len(amenities_content)):
        amenities.append(amenities_content[item_num].text)
    
    # Return All Data
    results = dict()
    results["listing_name"] = listing_name
    results["value"] = sale_p
    results["value_psf"] = sale_psf
    results["cnt_beds"] = num_beds
    results["cnt_baths"] = num_baths
    results["property_size"] = rental_size
    results["latitude"] = coordinates_lat
    results["longitude"] = coordinates_lng
    results["coordinates"] = (coordinates_lat + ", " + coordinates_lng)
    results["lease_start"] = lease_start
    results["lease_type"] = lease_type
    results["property_facing"] = room_facing
    results["property_furniture"] = room_furnishing
    results["property_type"] = property_type
    results["property_name"] = property_name
    results["property_unit_types"] = property_unit_types
    results["property_unit_cnt"] = property_unit_cnt
    results["property_build_year"] = property_build_year
    results["property_gov_lease"] = property_gov_lease
    results["property_developer"] = property_developer
    results["property_neigbourhood"] = property_neigbourhood
    
    results["rental_type"] = "N/A"
    results["rule_pets"] = rule_pets
    results["rule_cooking"] = rule_cooking
    results["rule_guests"] = rule_guests
    results["lease_stay_in_owner"] = lease_stay_in_owner
    results["rule_smoking"] = rule_smoking
    
    results["amenities"] = amenities
        
    return results
