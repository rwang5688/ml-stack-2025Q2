import boto3
import os
import streamlit as st
import datetime
import random

target_region = os.environ.get("AWS_REGION")  
ddb_resource = boto3.resource('dynamodb', region_name = target_region)
table_name = "UnicornPatientTable"

 
def random_date():
    start_dt = datetime.date(2019, 2, 1)
    end_dt = datetime.date(2024, 1, 1)
    time_between_dates = end_dt - start_dt
    days_between_dates = time_between_dates.days
    random_number_of_days = random.randrange(days_between_dates)
    random_date = start_dt + datetime.timedelta(days=random_number_of_days)
    new_date = random_date.strftime('%m-%d-%Y')
    return new_date
    

def create_patient_table():
    
    params = {
        "TableName": table_name,
        "KeySchema": [
            {"AttributeName": "patient_id", "KeyType": "HASH"},
        ],
        "AttributeDefinitions": [
            {"AttributeName": "patient_id", "AttributeType": "N"},
        ],
        "ProvisionedThroughput": {"ReadCapacityUnits": 10, "WriteCapacityUnits": 10},
    }
    table = ddb_resource.create_table(**params)
    print(f"Creating {table_name}...")
    table.wait_until_exists()
    return table
    
    
def write_patient_data(key_count):    
    table = ddb_resource.Table(table_name)
    policies = ['Gold', 'Silver', 'Bronze', 'Platinum']
    status = ['active','inactive']
    problems = ['alzheimer', 'arthritis', 'asthma', 'covid-19','ear infection', 'fibromyalgia', 'high blood pressure', 'kidney disease', 'lung cancer', 'stroke']

    for partition_key in range(1, key_count + 1):
        
        policy_type = random.choice(policies)
        patient_status = random.choice(status)
        condition = random.choice(problems)
        last_activity_date = random_date()
        
        table.put_item(
            Item={
                "patient_id": partition_key,
                "policy_type": policy_type,
                "status": patient_status,
                "condition": condition,
                "last_activity_date": last_activity_date,
            }
        )
        print(f"Put item ({partition_key}) succeeded.")



if __name__ == "__main__":
    patient_table = create_patient_table()
    print(f"Created patients table.")
    
    write_key_count = 100
    print(f"Writing {write_key_count} items to the table.")

    write_patient_data(write_key_count)
    print("Done!")

        
