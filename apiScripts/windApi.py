import requests
import sys

def getWind(lat, long):
    #Define our wind api url
    wind_url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={long}&hourly=wind_speed_10m,wind_direction_10m&temperature_unit=fahrenheit&wind_speed_unit=kn&timezone=America%2FNew_York&temporal_resolution=hourly_3&cell_selection=sea"

    
    try: #Try and retrieve and return data from wind API
        wind_response = requests.get(wind_url) #Call our wind API with our formatted URL and store the response
        wind_response.raise_for_status() #Check the reponse for any HTTP errors
        wind_data = wind_response.json() #Convert the API response to json

        return wind_data #Return out wind data

    #Return HTTP Error if found in response
    except requests.exceptions.HTTPError as http_error:
        print(f"HTTP Error Occured: {http_error}")
        return {'error': f"HTTP error occured: {http_error}"}
    #Return any other error that occurs in function
    except Exception as err:
        print(f"General Error has Occured: {err}")
        return {'error': f"General error occured: {err}"}

print(sys.getsizeof(getWind(40.168,-70.123)))