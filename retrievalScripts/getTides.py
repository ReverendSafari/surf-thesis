import boto3 
import json
import time
import requests

#Get DB
dynamo = boto3.resource('dynamodb')
#Get table
table = dynamo.Table('beaches')

#Function to get a station id from a beach name (Which is passed in to request to backend API)
def get_station_id(beach_name):
    response = table.get_item(Key={'beach_name': beach_name}) #Get the metadata item from table with beach_name as key
    station_id = response.get('Item', {}).get('station_id') #Get the station_id from the beach metadata object
    return station_id 

def lambda_handler(event, context):
    #Retrieve beach name from path parameters
    beach_name = event['pathParameters'].get('beach_name')
    station_id = get_station_id(beach_name)

    #If no beach name is returned throw an error 
    if not beach_name:
        return {
            'statusCode': 400,
            'body': json.dumps({'message': "No beach_name parameter found"})
        }
    
    #If no station_id is found throw an error
    if not station_id:
        return {
            'statusCode': 400,
            'body': json.dumps({'message': 'No station_id parameter found'})
        }    

    try:

        #Try and retrieve the data, in case it's already cached in our DB
        response = table.get_item(
            Key={
                'beach_name':beach_name,
                'data_type':'_data'
            }
        )

        #Attempt to save the cached data if it was retrieved, if not assign a default value of none
        cached_data = response.get('Item', None)

        #If the cached data exists
        if cached_data:
            #Get current time
            current_time = int(time.time())
            #Check if expiration token in is in cached data, and if it is expired (AWS takes up to 48 hours so cached data could persist in DB past expiration)
            if 'ttl' in cached_data and cached_data['ttl'] > current_time:
                #Retrieve tide data from cache, N/A if it is not present in cache
                tides = cached_data.get('tides', 'N/A')
                
                #Cached data is valid, so we return it
                return {
                    'statusCode': 200,
                    'body': json.dumps({'message': 'Returning cached data',
                                        'beach_name': beach_name,
                                        'tides': tides,
                                        })
                }
            else:
                print("Cache is expired or missing ttl token")
        else:
            print("No cached data found")
    except Exception as e:
        print(f"Error retrieving cached data: {str(e)}")

    #Cache is missing retrieve new data from weather api
    tides = getTides(station_id)

    #Raise error if their an issue getting the temperatures 
    if 'error' in tides:
        return {
            'statusCode' : 500,
            'body': json.dumps({'message': 'Error trying to retrieve temperature data from API'})
        }

    #Calculate a new ttl for the temperature data (12 hours)
    ttl = int(time.time()) + 43200

    #Attempt to store new data in DB
    try: 
        table.put_item(
            Item={
                'beach_name': beach_name,
                'data_type': 'tide_data',
                'tides': tides,
                'ttl': ttl #Set 12 hour expiration date
            }
        )

        print(f"Stored new temperature data for {beach_name} with 12 hour expiration")

    #Catch any errors when trying to store the data  
    except Exception as e:
        print(f"Error trying to store temperature data in DB: {str(e)}")
        return {
            'statusCode': 500,
            'body': json.dumps({'message': 'Error trying to store temperature data in DB'})
        }
    
    #Finally, return the new data 
    return {
        'statusCode': 200,
        'body': json.dumps({
            'message' : "Returning temperature data",
            'beach_name': beach_name,
            'tides': tides
        })
    }

#Function to retrieve new tide predictions from the NOAA api
def getTides(station_id):
    #Define our tide api url
    tides_url = f"https://api.tidesandcurrents.noaa.gov/api/prod/datagetter?date=today&station={station_id}&product=predictions&datum=STND&time_zone=lst&interval=hilo&units=english&format=json"

    #Try and call API endpoint to retrieve tide data
    try:

        tide_reponse = requests.get(tides_url) #Request data from the tide api using our formatted url
        tide_reponse.raise_for_status() #Raise HTTP error if response has one
        tide_data = tide_reponse.json() #Convert the response to json
        tide_predictions = tide_data.get('predictions', []) #Pull out the predictions from the data

        formatted_data = [] #Create a list to store formatted tide predictions
        
        #loop through data, format it, and append to our list
        for tides in tide_predictions: 
            formatted_data.append({
                'time': tides['t'],
                'height': tides['v'],
                'type': 'high' if tides['type'] == 'H' else 'low'
            })

        #return the tide prediction data      
        return formatted_data

    #If an HTTP error occurs report it
    except requests.exceptions.HTTPError as http_error:
        print(f"HTTP Error has occured: {http_error}")
        return {'error': f"HTTP Error has occured: {http_error}"}
    #If some other non HTTP general error occurs report it
    except Exception as err:
        print(f"General Error has ocured: {err}")
        return {'error': f"General error has occured"}
