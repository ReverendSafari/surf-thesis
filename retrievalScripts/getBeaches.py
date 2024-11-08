import json
import boto3
import decimal as Decimal

#Get the DB object, and then retrieve the beach table
dynamo = boto3.resource('dynamodb')
table = dynamo.Table('beaches')

def decimal_converter(obj):
    #If object is an instance of the Decimal class
    #if isinstance(obj, Decimal):
    return float(obj) if obj % 1 else int(obj)
    raise TypeError
    
#This is lambda's entry point, and where the logic and response for the api is generated
def lambda_handler(event, context):
    #We will try to retrieve the beach objects to return
    try:
        #Scan the table to get the objects we want to return
        response = table.scan(
            #Filter out any objects that arent == to :type
            #Dynamo doesn't except raw values so we need to use a placeholder in our filtering
            FilterExpression='data_type = :type',

            #Now we actually set the value of our placeholder :type as 'metadata' - we use a dictionary to set the value
            ExpressionAttributeValues={':type': 'metadata'}
        )

        #Retrieve the objects (beaches) that passed our filter criteria
        #When we perform a db scan it returns a dict that includes a lot of info, Items is the dict item that contains our ACTUAL data
        #The nullset is the default value to return if Items CANT be found in the response
        beaches = response.get('Items', [])

        #Check if the list is empty (No beaches were returned) and if so return a HTTP error
        if not beaches:
            return {
                'statusCode': 404,
                'body': json.dumps({'message': 'No beaches returned'}) #Convert out message to json
            }
        
        #If we did get beaches from our scan, return them
        return {
            'statusCode': 200,
            'body': json.dumps({'beaches':beaches}, default=decimal_converter) #Converts our list of beaches to JSON
        }

    #If there is some error along the way, return an error code
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)}) #Converts our error to json
        }