import requests
import sys

def getWaves(lat, long):
    #Define our wave api url
    waves_url = f"https://marine-api.open-meteo.com/v1/marine?latitude={lat}&longitude={long}&hourly=wave_height,wave_direction,wave_period&length_unit=imperial&timezone=America%2FNew_York&temporal_resolution=hourly_6&models=ncep_gfswave025"

    
    try: #Try and retrieve and return data from wave API
        wave_response = requests.get(waves_url) #Call our wave API with our formatted URL and store the response
        wave_response.raise_for_status() #Check the reponse for any HTTP errors
        wave_data = wave_response.json() #Convert the API response to json

        return wave_data #Return out wave data

    #Return HTTP Error if found in response
    except requests.exceptions.HTTPError as http_error:
        print(f"HTTP Error Occured: {http_error}")
        return {'error': f"HTTP error occured: {http_error}"}
    #Return any other error that occurs in function
    except Exception as err:
        print(f"General Error has Occured: {err}")
        return {'error': f"General error occured: {err}"}

print(sys.getsizeof(getWaves(40.168,-70.123)))