import requests
import boto3
import json
import time
import sys

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
    
    #Try and get data from DB if cached
    try:

        #Try and retrieve cached data if present in DB 
        response = table.get_item(Key={
            'beach_name' : beach_name,
            'data_type' : 'wave_data'
        })

        cached_data = response.get('Item', None)

        if cached_data: 
            current_time = int(time.time()) #Retrieve current time in unix timestamp

            if 'ttl' in cached_data and cached_data['ttl'] > current_time: #Check that expiration token is present, and that it's not expired
                waves = cached_data.get('waves', 'N/A') #Retrieve wave data from the cache, N/A if nothing present

                #Return data if found
                return {
                    'statusCode': 200,
                    'body': json.dumps({
                        'message' : 'Returning cached wave data',
                        'beach_name' : beach_name,
                        'waves' : waves
                    })
                }
            else:
                print('ttl expired, or not present in data')
        else:
            print('No cached data found')
    except Exception as e:
        print(f'Error retrieving cached data: str{e}')

    #If no data found, call getWaves() to retrieve new data
    waves = getWaves(coordinates['latitude'], coordinates['longitude'])

    #Convert waves to json object for storing in DB
    waves_json = json.dumps(waves)
    print(sys.getsizeof(waves_json))
    
    #Raise error if present in API call
    if 'error' in waves: 
        return {
            'statusCode': 500,
            'body': json.dumps({'message':'Error retrieving waves from weather API'})
        }
    
    ttl = int(time.time()) + 43200 #Calculate new expiration (12 hours)

    #Cache new data
    try: 
        table.put_item(Item={
            'beach_name' : beach_name,
            'data_type' : 'wave_data',
            'waves' : waves_json,
            'ttl' : ttl
        })

        print(f'Succesfully stored wave data for {beach_name} with 12 hour expiration')
    except Exception as e:
        print(f'Error storing wave data for {beach_name} in DB')
        return {
            'statusCode': 500,
            'message': json.dumps({'message': f'Error storing wave data for {beach_name} in DB'})
        }
    
    #Return new data
    return {
        'statusCode': 200,
        'body': {
            'message' : 'Returning wave data',
            'beach_name' : beach_name,
            'waves' : waves
        }
    }

def getWaves(lat, long):
    #Define our wave api url
    waves_url = f"https://marine-api.open-meteo.com/v1/marine?latitude={lat}&longitude={long}&hourly=wave_height,wave_direction,wave_period&length_unit=imperial&timezone=America%2FNew_York&temporal_resolution=hourly_3&models=ncep_gfswave025"

    
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

