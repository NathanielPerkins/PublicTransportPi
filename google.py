#Might have to import googlemaps using pip
from googlemaps import Client

#Reources
# https://developers.google.com/maps/documentation/directions/intro
# https://developers.google.com/api-client-library/python/apis/mapsengine/v1?hl=en
API_KEY = "AIzaSyDXZvtLzLPExxM6NhpfAoHZLMV-gRRX66s"

mapService  = Client(API_KEY)




#--------------------------------Get Direction Information--------------------------------#

# Get Directions between two locations
# Param: mode allows specification of transport mode (Walking, Bicylcing, Driving, Transit)
# When mode is specified, give alternative routes

# TODO: Add in validity checks, catch exceptions, ect
def get_directions(start_location, end_location, mode=None):
    if mode:
        return mapService.directions(start_location, end_location, mode,alternatives=True)
    else:
        return mapService.directions(start_location, end_location)


#------------------------------------Route Information-----------------------------------#

def get_route(directions,route=None):
    if route:
        return directions[route]
    else:
        return directions[0]

def num_routes(directions):
    return len(directions)


#-------------------------------------Trip Information------------------------------------#

#---------------------Trip Duration---------------------#
def trip_duration_str(route):
    return route['legs'][0]['duration']['text']

def trip_duration_val(route):
    return route['legs'][0]['duration']['value']

#---------------------Trip Distance---------------------#
def trip_distance_str(route):
    return route['legs'][0]['distance']['text']

def trip_distance_val(route):
    return route['legs'][0]['distance']['value']

#---------------------Arrival Time---------------------#
def arrival_time_str(route):
    return route['legs'][0]['arrival_time']['text']

def arrival_time_val(route):
    return route['legs'][0]['arrival_time']['value']

#---------------------Departure Time---------------------#
def departure_time_str(route):
    return route['legs'][0]['departure_time']['text']

def departure_time_val(route):
    return route['legs'][0]['departure_time']['value']

#---------------------Start Address---------------------#
def start_address(route):
    return route['legs'][0]['start_address']

#---------------------End Address---------------------#
def end_address(route):
    return route['legs'][0]['end_address']


#--------------------------------Steps of Journey Information------------------------------#
def get_step(route, number):
    return route['legs'][0]['steps'][number]

def num_steps(route):
    return len(route)

# Print html encoded trip instruction list
# TODO: Doesnt print substeps
def print_instructions(directions):
    for step in route['legs'][0]['steps']:
        print(step['html_instructions'])




#---------------------------Transit Information---------------------------#

def travel_type(step):
    return step['travel_mode']

def step_transit_details_long_name(step):
    if(step['travel_mode']=='TRANSIT'):
        return step['transit_details']['line']['name']
    else:
        return None

def step_transit_details_short_name(step):
    if(step['travel_mode']=='TRANSIT'):
        return step['transit_details']['line']['short_name']
    else:
        return None


print("--------------------------------------------------------------------------------------")
directions_transit = get_directions('Cavendish Road, Coorparoo','Southbank, Brisbane','transit')
transit_route = get_route(directions_transit)
transit_step = get_step(transit_route,1)
travel_type(transit_step)

