import json
import boto3
from boto3.dynamodb.conditions import Key

ddb_resource = boto3.resource('dynamodb')
table = ddb_resource.Table('UnicornPatientTable')


def patient_detail(payload):
    number = payload['parameters'][0]['value']
    patient = int(number)

    resp = table.query(KeyConditionExpression=Key('patient_id').eq(patient))
    for i in resp['Items']:
        return {
            "response":{
                "patient_id": i['patient_id'],
                "policy_type": i['policy_type'],
                "status": i['status'],
                "condition" :i['condition'],
                "last_activity_date": i["last_activity_date"],
            }
        }
    else:
        return {
            "response": {
                "patient_Id": "invalid",
                "policy_type": "invalid",
                "status": "invalid",
                "condition" :"invalid",
                "last_activity_date": "invalid",
            }
        }
    
def lambda_handler(event, context):
    action = event['actionGroup']
    api_path = event['apiPath']

    if api_path == '/patient/{patientId}/detail':
        body = patient_detail(event)
    else:
        body = {"{}::{} is not a valid api, try another one.".format(action, api_path)}

    response_body = {
        'application/json': {
            'body': str(body)
        }
    }

    action_response = {
        'actionGroup': event['actionGroup'],
        'apiPath': event['apiPath'],
        'httpMethod': event['httpMethod'],
        'httpStatusCode': 200,
        'responseBody': response_body
    }

    api_response = {'response': action_response}
    return api_response