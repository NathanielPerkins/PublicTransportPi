#Might have to import googlemaps using pip
from googlemaps import Client
import EpochTime

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
def get_steps(route):
    return route['legs'][0]['steps']

def get_step(route, number):
    return route['legs'][0]['steps'][number]

def num_steps(route):
    return len(route['legs'][0]['steps'])


# Print html encoded trip instruction list
# TODO: Doesnt print substeps
def print_instructions(route):
    for step in route['legs'][0]['steps']:
        print(step['html_instructions'])





#---------------------------Transit Information---------------------------#
def num_transfers(route):
    transfers = 0
    for step in route['legs'][0]['steps']:
        if(step['travel_mode']=='TRANSIT'):
            transfers += 1
    return transfers

def get_transit_steps(route):
    transitSteps = []
    counter = 0
    for step in route['legs'][0]['steps']:
        if(step['travel_mode']=='TRANSIT'):
            transitSteps.append(counter)
        counter += 1
    return transitSteps

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

def step_walking_distance_str(step):
    if(step['travel_mode']=='WALKING'):
        return step['distance']['text']
    else:
        return None

def vehicle_type(step):
    if(step['travel_mode']=='TRANSIT'):
        return step['transit_details']['line']['vehicle']['name']
    else:
        return None


#--------------------------------Steps of Journey Information------------------------------#

def routeInfo(route):
    departureTime = departure_time_str(route)
    arrivalTime = arrival_time_str(route)
    durationTime = trip_duration_str(route)
    numTransfers = num_transfers(route)
    routeInfo = {'DepartureTime':departureTime,'ArrivalTime':arrivalTime,'DurationTime':durationTime,'Transfers':numTransfers}
    routeInfo['NumberSteps'] = num_steps(route)

    stepsInfo = []
    for step in get_steps(route):
        if(travel_type(step)=='TRANSIT'):
            vehicle = vehicle_type(step)
            lineName = step_transit_details_short_name(step)
            stepInfo = {'Type':'TRANSIT','Vehicle':vehicle,'LineName':lineName}
        else:#travel type is walking
            distance = step_walking_distance_str(step)
            stepInfo = {'Type':'Walk','Distance':distance}
        stepsInfo.append(stepInfo)

    routeInfo['Steps'] = stepsInfo
    return routeInfo

def header():
    headerLength = 100
    line1 = ""
    line2 = ""
    line3 = ""
    column1 = "Departure"
    column3 = "Arrival"
    
    for i in range(0, headerLength):
        if(i==0 or i==headerLength-1):
            line1 += "|"
            line3 += "|"
        else:
            line1 += "-"
            line3 += "-"

    dividerLength = 1/5;

    stringCounter = 0;
    stringCounter3 = 0;
    for i in range(0, headerLength):
        if(i==0 or i==headerLength-1):
            line2 += "|"
        elif(i>0 and i<round(headerLength*dividerLength)):
            if(stringCounter<len(column1)):
                line2 += column1[stringCounter]
                stringCounter+=1
            else:
                line2 += " "
        elif(i>round((4*headerLength)*dividerLength) and i<headerLength):
            if(stringCounter3<len(column3)):
                line2 += column3[stringCounter3]
                stringCounter3+=1
            else:
                line2 += " "
        elif(i == round(headerLength*dividerLength) or i == round((4*headerLength)*dividerLength)):
            line2 += "|"
        else:
            line2 += " "

    print(line1)
    print(line2)
    print(line3)
    
    
def transit_timetable(directions):
    n_routes = num_routes(directions)
    n_steps = []
    departureTimes = []
    arrivalTimes = []
    step_array = []
    i = 0
    for route in directions:
        n_steps.append(num_steps(route))
        departureTimes.append(departure_time_str(route))
        arrivalTimes.append(arrival_time_str(route))
        tempList = []
        for step in get_steps(route):
            if(travel_type(step)=='TRANSIT'):
                vehicle = vehicle_type(step)
                lineName = step_transit_details_short_name(step)
                string = vehicle + " " + lineName
                tempList.append(string)
            elif(travel_type(step)=='WALKING'):
                string = step_walking_distance_str(step) + " walk."
                tempList.append(string)
            else:
                tempList.append(travel_type(step))
        step_array.append(tempList)
        print(departureTimes[i],"||",step_array[i],"||",arrivalTimes[i])
        i+=1
    

#header()
#directions_transit = get_directions('160 Central Avenue, Indroopilly','Southbank, Brisbane','transit')
#transit_timetable(directions_transit)
#transit_route = get_route(directions_transit)
#transit_step = get_step(transit_route,1)
#travel_type(transit_step)

