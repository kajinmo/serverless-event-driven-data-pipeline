import json
import os
import socket

MONGO_URI = os.environ.get("MONGO_URI", "mongodb://eda-mongodb:27017/")
print(f"Connecting to MongoDB at: {MONGO_URI}")
print(f"Env vars: {dict(os.environ)}")

from pymongo import MongoClient
client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=2000)
db = client['eda_database']
collection = db['consolidated_users']

def lambda_handler(event, context):
    print("Received event:", json.dumps(event))
    
    # Step Functions Parallel state outputs an array with the results of both branches
    try:
        # Check if the items actually exist in the event payload
        profile_item = event[0].get('Item', {})
        activity_item = event[1].get('Item', {})
        
        if not profile_item or not activity_item:
            print("Missing Profile or Activity data")
            return {"status": "error", "message": "Missing Data"}
        
        # Merge the dictionaries
        consolidated_doc = {**profile_item, **activity_item}
        
        # For simplicity, convert DynamoDB format (e.g. {'S': 'value'}) to normal dict
        clean_doc = {}
        for key, value_dict in consolidated_doc.items():
            if isinstance(value_dict, dict):
                clean_doc[key] = list(value_dict.values())[0]
            else:
                clean_doc[key] = value_dict
                
        # Set MongoDB _id
        if 'user_id' in clean_doc:
            clean_doc['_id'] = clean_doc['user_id']
                
        collection.update_one(
            {'_id': clean_doc.get('_id')},
            {'$set': clean_doc},
            upsert=True
        )
        
        print(f"Successfully consolidated user: {clean_doc.get('_id')}")
        return {"status": "success", "user_id": clean_doc.get('_id')}
    except Exception as e:
        print(f"Error processing event: {e}")
        raise e
