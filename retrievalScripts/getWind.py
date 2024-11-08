import requests
import sys
import boto3
import json
import time

dynamo = boto3.resource("dynamodb") #Select DynamoDB as our resource to retrieve
table = dynamo.Table("beaches") #Retrieve our table from DynamoDB

#Function to retrieve beach coordinates from a beach name in our table
def get_beach_coordinates(beach_name):
    response = table.get_item(Key={'beach_name': beach_name,
                                    'data_type': 'metadata'
    }) #Get the metadata item from table with beach_name as key
    latitude = response.get('Item', {}).get('lat') #Get the latitude from the beach metadata object
    longitude = response.get('Item', {}).get('long') #Get the longitude from the beach metadata object
    return {'latitude': latitude, 'longitude': longitude} #Return our coordinates

def lambda_handler(event, context):
    beach_name = event['pathParameters'].get('beach_name')
    coordinates = get_beach_coordinates(beach_name)

    #Throw error if no beach name
    if not beach_name:
        return {
            'statusCode' : 400,
            'message': json.dumps({'message': 'No beach_name parameter found'})
        }
    
    #Throw error if no coords
    if not coordinates: 
        return {
            'statusCode' : 400,
            'message': json.dumps({'message': f'Could not retrieve coordinates for {beach_name}'})
        }
    
    #Try and retrieve cached data if present in DB 
    response = table.get_item(Key={
        'beach_name' : beach_name,
        'data_type' : 'wind_data'
    })

    #Try and get data from DB if cached
    try:

        #Try and retrieve cached data if present in DB 
        response = table.get_item(Key={
            'beach_name' : beach_name,
            'data_type' : 'wind_data'
        })

        cached_data = response.get('Item', None)

        if cached_data: 
            current_time = int(time.time()) #Retrieve current time in unix timestamp

            if 'ttl' in cached_data and cached_data['ttl'] > current_time: #Check that expiration token is present, and that it's not expired
                wind = cached_data.get('wind', 'N/A') #Retrieve wave data from the cache, N/A if nothing present

                #Return data if found
                return {
                    'statusCode': 200,
                    'body': json.dumps({
                        'message' : 'Returning cached wave data',
                        'beach_name' : beach_name,
                        'wind' : wind
                    })
                }
            else:
                print('ttl expired, or not present in data')
        else:
            print('No cached data found')
    except Exception as e:
        print(f'Error retrieving cached data: str{e}')

    #If no data found, call getWaves() to retrieve new data
    wind = getWind(coordinates['latitude'], coordinates['longitude'])

    #Convert waves to json object for storing in DB
    wind_json = json.dumps(wind)
    print(sys.getsizeof(wind_json))
    
    #Raise error if present in API call
    if 'error' in wind: 
        return {
            'statusCode': 500,
            'body': json.dumps({'message':'Error retrieving wind from weather API'})
        }
    
    ttl = int(time.time()) + 43200 #Calculate new expiration (12 hours)

    #Cache new data
    try: 
        table.put_item(Item={
            'beach_name' : beach_name,
            'data_type' : 'wave_data',
            'wind' : wind_json,
            'ttl' : ttl
        })

        print(f'Succesfully stored wind data for {beach_name} with 12 hour expiration')
    except Exception as e:
        print(f'Error storing wind data for {beach_name} in DB')
        return {
            'statusCode': 500,
            'message': json.dumps({'message': f'Error storing wind data for {beach_name} in DB'})
        }
    
    #Return new data
    return {
        'statusCode': 200,
        'body': {
            'message' : 'Returning wind data',
            'beach_name' : beach_name,
            'wind' : wind
        }
    }



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