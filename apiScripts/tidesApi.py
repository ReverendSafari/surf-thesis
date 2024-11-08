import requests

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



print(getTides(8531680))