import requests


# get the events data
def get_data():
    response = requests.get("https://eonet.gsfc.nasa.gov/api/v3/events")
    events = response.json()['events']
    return events


# get the current categories data
def get_categories():
    response = requests.get('https://eonet.gsfc.nasa.gov/api/v3/categories')
    categories = response.json()['categories']
    return categories
