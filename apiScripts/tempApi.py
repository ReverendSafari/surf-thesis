import requests

def get_temps(station_id):
    #Define our urls
    air_temp_url = f"https://api.tidesandcurrents.noaa.gov/api/prod/datagetter?date=latest&station={station_id}&product=air_temperature&datum=STND&time_zone=lst&units=english&format=json"
    water_temp_url = f"https://api.tidesandcurrents.noaa.gov/api/prod/datagetter?date=latest&station={station_id}&product=water_temperature&datum=STND&time_zone=lst&units=english&format=json"

    #Try and call the api endpoints to retrieve the data 
    try:
        #Send request to water temp api and store the response
        water_temp_response = requests.get(water_temp_url)
        water_temp_response.raise_for_status()  #Check the response for errors
        water_temp_data = water_temp_response.json() #Get water temp response data as json object
        water_temp = water_temp_data['data'][0]['v'] #Retrieve the actual water temperature from the response data

        air_temp_response = requests.get(air_temp_url)
        air_temp_response.raise_for_status()
        air_temp_data = air_temp_response.json()
        air_temp = air_temp_data['data'][0]['v']

        return {
            "station_id": station_id,
            "water_temp": water_temp,
            "air_temp": air_temp
        }
    
    #If an HTTP error occurs report it
    except requests.exceptions.HTTPError as http_error:
        print(f"HTTP Error has occured: {http_error}")
        return {'error': f"HTTP Error has occured: {http_error}"}
    #If some other non HTTP general error occurs report it
    except Exception as err:
        print(f"General Error has ocured: {err}")
        return {'error': f"General error has occured"}

#8531680

print(get_temps(8531680))