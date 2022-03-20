from flask import Flask, jsonify, request
import xmltodict
import logging
import json

app = Flask(__name__)


positional_data = {}
sighting_data = {}

@app.route('/reset', methods=['POST'])
def read_data_from_file_into_dict():
    """
    This route reads in two xml files, converting them to dictionaries and confirming that the data files have been successfully read.
    """
    
    logging.info('Reading data...')
    
    global positional_data
    global sighting_data

    with open('positional.xml', 'r') as f:
        positional_data = xmltodict.parse(f.read())

    with open('sighting.xml', 'r') as f:
        sighting_data = xmltodict.parse(f.read())
    
    return f'Data has been read from file\n'



@app.route('/', methods=['GET'])
def info():
    """
    This route offers information on how to interact with the application
    """

    logging.info('Offering information about each route for reference')

    describe = "ISS Sighting Location\n"
    describe += "/                                                      (GET) print this information\n"
    describe += "/reset                                                 (POST) reset data, load from file\n"
    describe += "Routes for querying positional and velocity data:\n\n"
    describe += "/epochs                                                (GET) lists all epochs in positional and velocity data\n"
    describe += "/epochs/<epoch>                                        (GET) lists all data associated with a specific epoch\n"
    describe += "Routes for Querying Sighting Data\n\n"
    describe += "/countries                                             (GET) lists all countries in sighting data\n"
    describe += "/countries/<country>                                   (GET) lists all data for a specific country\n"
    describe += "/countries/<country>/regions                           (GET) lists all regions in a specific country\n"
    describe += "/countries/<country>/regions/<region>                  (GET) lists all data for a specific region\n"
    describe += "/countries/<country>/regions/<region>/cities           (GET) lists all cities in a specific region\n"
    describe += "/countries/<country>/regions/<region>/cities/<city>    (GET) lists all data for a specific city\n\n"

    return describe



@app.route('/epochs', methods=['GET'])
def get_epochs():

    """
    This route iterates through the positional dictionary, outputting positional information about the epochs.
    
    Returns:
    Positional data on every EPOCH.
    """     

    logging.info('Querying route to get all EPOCHS')

    epochs = []
  
    for item in positional_data['ndm']['oem']['body']['segment']['data']['stateVector']:
        epochs.append(item['EPOCH'])
    
    return json.dumps(epochs, indent=2)


@app.route('/epochs/<EPOCH>', methods=['GET'])
def get_EPOCH_data(EPOCH: str):
    
    """
    This route iterates through all the stateVectors, capturing all the information about a specific Epoch (entered by user)
 
    Args:
    EPOCH (str): String type of the specific EPOCH value 

    Returns:
    EPOCH_dict (dictionary): All the info about a specific Epoch stored in a dict
    """ 
    
    logging.info('Querying route to acquire all the info about specific Epoch: /' + EPOCH)
   
    epoch_dict = {}
    all_data = ['X', 'Y', 'Z', 'X_DOT', 'Y_DOT', 'Z_DOT']

    for item in positional_data['ndm']['oem']['body']['segment']['data']['stateVector']:
        if EPOCH == item['EPOCH']:
            epoch_place = item
            #epoch_dict = {}
            for i in all_data:
                epoch_dict[i] = epoch_place[i]
    
    return epoch_dict


@app.route('/countries', methods=['GET'])
def get_all_countries():

    """
    This route iterates through the visible passes in the sighting data and gets all the countries

    Returns:
    countries (dictionary): All of the countries
    """
    
    logging.info('Querying route to get all countries')

    countries = []
    
    for item in sighting_data['visible_passes']['visible_pass']:
        countries.append(item['country'])

    return json.dumps(countries, indent=2) 


@app.route('/countries/<country>', methods=['GET'])
def get_country_info(country):

    """
    This route iterates through the visible passes in the sighting data and obtains all information about a specific country, stated by the user.

    Args:
    country (str): String containing specific country user wants information about.

    Returns:
    country_list (list): list of dicts containing all info about a specific country
    """

    logging.info('Querying route to get all info on /' + country)

    country_dict = {}
    country_list = []
    country_data = ['country', 'region', 'city', 'spacecraft', 'sighting_date','duration_minutes','max_elevation','enters','exits','utc_offset','utc_time', 'utc_date']

    for item in sighting_data['visible_passes']['visible_pass']:
        specific_country = item['country']
        if country == specific_country:
            country_place = item
            for data in country_data:
                country_dict[data] = country_place[data]
            country_list.append(country_dict)

    return json.dumps(country_list, indent=2) 


@app.route('/countries/<country>/regions', methods=['GET'])
def get_all_regions(country):

    """
    This route iterates through all the visible passes in the sighting data and obtains all Regions associated with a given Country. 

    Args:
    country (str): String containing specific country the user wants to find regions for

    Returns:
    regions (dict): Dictionary containing all regions associated with a given country in the sighting data 
    """

    logging.info("Querying route to get list of regions in /" + country)

    regions = {}

    for item in sighting_data['visible_passes']['visible_pass']:
        if country == item['country']:
            specific_region = item['region']
            if specific_region in regions:
                regions[specific_region] += 1
            else:
                regions[specific_region] = 1

    return regions


@app.route('/countries/<country>/regions/<region>', methods=['GET'])
def get_region_data(country, region):

    """
    This route iterates through all the visible passes in the sighting data, capturing information about a specific region the user provided.

    Args:
    country (str): String containing specific country the user provides
    region (str): String containing specific region the user wants information about

    Returns:
    region_list (list): List of dicts containing all information about specific region in sighting data.
    """

    logging.info('Querying route to get all info about /' +region)

    region_dict = {}
    region_list = []
    region_data = ['city', 'spacecraft', 'sighting_date','duration_minutes','max_elevation','enters', 'exits','utc_offset','utc_time', 'utc_date']    

    for item in sighting_data['visible_passes']['visible_pass']:
        if country == item['country']:
            specific_region = item['region']
            if region == specific_region:
                for data in region_data:
                    region_dict[data] = item[data]
                region_list.append(region_dict)  

    return json.dumps(region_list, indent=2)


@app.route('/countries/<country>/regions/<region>/cities', methods=['GET'])
def get_all_cities(country, region):

    """
    This route iterates through all the visible passes in the sighting data, capturing all the cities associated with the given country and region.

    Args:
    country (str): String containing specific country the user provides
    region (str): String containing specific region the user provides

    Returns:
    cities_dict (dict): Dictionary containing all cities associated with a given country and region in the sighting data.
    """

    logging.info('Querying route to get all cities of /' +region)

    cities_dict = {}

    for item in sighting_data['visible_passes']['visible_pass']:
        if country == item['country']: 
            specific_region = item['region']
            if region == specific_region:
                specific_cities = item['city']
                if specific_cities in cities_dict:
                    cities_dict[specific_cities] += 1   
                else:
                    cities_dict[specific_cities] = 1
    
    return cities_dict 


@app.route('/countries/<country>/regions/<region>/cities/<city>', methods=['GET'])
def get_city_data(country, region, city):

    """
    This route iterates through all the visible passes in the sighting data, capturing all the info about a specific city within a given country and region.

    Args:
    country (str): String containing specific country the user provides
    region (str): String containing specific region the user provides
    city (str): String containing specific city the user wants info for

    Returns:
    city_list (list): List containing dicts with all info about a specific city in the sighting data.
    """

    logging.info('Querying route to get all info of /' +city)

    city_dict = {} 
    city_list = []
    city_data = ['city','spacecraft','sighting_date','duration_minutes','max_elevation','enters','exits','utc_offset','utc_time','utc_date']

    for item in sighting_data['visible_passes']['visible_pass']:
        if country == item['country']:
            specific_region = item['region']
            if region == specific_region:
                specific_city = item['city']
                if city == specific_city:
                    for data in city_data:
                        city_dict[data] = item[data]
                    city_list.append(city_dict)

    return json.dumps(city_list, indent=2)




# the next statement should usually appear at the bottom of a flask app
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
