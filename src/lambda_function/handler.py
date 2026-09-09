import json
import os
import boto3
from datetime import datetime, timezone

MONGO_USER = os.environ.get("MONGO_USER")
MONGO_PASSWORD = os.environ.get("MONGO_PASSWORD")
STATUS_TABLE_NAME = os.environ.get("STATUS_TABLE_NAME", "tb_execution_status")

if MONGO_USER and MONGO_PASSWORD:
    MONGO_URI = f"mongodb+srv://{MONGO_USER}:{MONGO_PASSWORD}@cluster0.n7ip9re.mongodb.net/?appName=Cluster0"
else:
    MONGO_URI = "mongodb://eda-mongodb:27017/"

print(f"Connecting to MongoDB Atlas... (User: {MONGO_USER})")

from pymongo import MongoClient
client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=2000)
db = client['eda_database']
collection = db['consolidated_users']

# Initialize DynamoDB client
dynamodb = boto3.resource('dynamodb')
status_table = dynamodb.Table(STATUS_TABLE_NAME)

def update_execution_status(user_id, status, error_message=None):
    try:
        item = {
            'user_id': user_id,
            'status': status,
            'updated_at': datetime.now(timezone.utc).isoformat()
        }
        if error_message:
            item['error_message'] = error_message
            
        status_table.put_item(Item=item)
        print(f"Status updated in DynamoDB: {status}")
    except Exception as e:
        print(f"Failed to update status in DynamoDB: {e}")

def lambda_handler(event, context):
    print("Received event:", json.dumps(event))
    user_id = "UNKNOWN"
    
    try:
        profile_item = event[0].get('Item', {})
        activity_item = event[1].get('Item', {})
        
        if not profile_item or not activity_item:
            print("Missing Profile or Activity data")
            # We don't have user_id if both are missing, try to extract from event structure if possible
            if profile_item: user_id = profile_item.get('user_id', {}).get('S', 'UNKNOWN')
            elif activity_item: user_id = activity_item.get('user_id', {}).get('S', 'UNKNOWN')
            
            update_execution_status(user_id, "FAILED", "Missing Data")
            return {"status": "error", "message": "Missing Data"}
        
        # Merge the dictionaries
        consolidated_doc = {**profile_item, **activity_item}
        
        # Convert DynamoDB format
        clean_doc = {}
        for key, value_dict in consolidated_doc.items():
            if isinstance(value_dict, dict):
                clean_doc[key] = list(value_dict.values())[0]
            else:
                clean_doc[key] = value_dict
                
        user_id = clean_doc.get('user_id', 'UNKNOWN')
        if 'user_id' in clean_doc:
            clean_doc['_id'] = clean_doc['user_id']
                
        collection.update_one(
            {'_id': clean_doc.get('_id')},
            {'$set': clean_doc},
            upsert=True
        )
        
        print(f"Successfully consolidated user: {user_id}")
        update_execution_status(user_id, "COMPLETED")
        
        return {"status": "success", "user_id": user_id}
        
    except Exception as e:
        print(f"Error processing event: {e}")
        update_execution_status(user_id, "FAILED", str(e))
        raise e
