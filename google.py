#Might have to import googlemaps using pip
from googlemaps import Client

#Reources
# https://developers.google.com/maps/documentation/directions/intro
# https://developers.google.com/api-client-library/python/apis/mapsengine/v1?hl=en
API_KEY = "AIzaSyDXZvtLzLPExxM6NhpfAoHZLMV-gRRX66s"

mapService  = Client(API_KEY)


# Get Directions
# TODO: Add in validity checks, catch exceptions, ect
def get_directions(start_location, end_location, mode=None):
    if mode is not None:
        return mapService.directions(start_location, end_location, mode)[0]
    else:
        return mapService.directions(start_location, end_location)[0]

# Print html encoded trip instruction list
def print_instructions(directions):
    for step in directions['legs'][0]['steps']:
        print(step['html_instructions'])


# Get leg of the journey
def get_step(directions, number):
    return directions['legs'][0]['steps'][number]

#---------------------------Trip Duration---------------------------#
def trip_duration_str(directions):
    return directions['legs'][0]['duration']['text']

def trip_duration_val(directions):
    return directions['legs'][0]['duration']['value']

#---------------------------Trip Distance---------------------------#
def trip_distance_str(directions):
    return directions['legs'][0]['distance']['text']

def trip_distance_val(directions):
    return directions['legs'][0]['distance']['value']

#---------------------------Train Information---------------------------#

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


print("----------------------------------------------------------------------")
directions_transit = get_directions('Brisbane','Gold Coast','transit')
train = get_step(directions_transit,3)
print(step_transit_details_short_name(train))


#print_instructions(directions_transit)
#print(trip_duration_str(directions_transit))
