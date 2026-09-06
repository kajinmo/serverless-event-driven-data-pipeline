import sys
import os

# Add the root directory to the python path so 'src' can be imported
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.infra.dynamodb import tb_profile, tb_activity
from src.services.data_generator import generate_mock_data
from src.services.data_loader import load_data_to_dynamo

if __name__ == "__main__":
    print("Generating synthetic data...")
    profiles_data, activities_data = generate_mock_data(30)
    
    print("Starting load into Local DynamoDB (Floci)...")
    load_data_to_dynamo(tb_profile, profiles_data)
    load_data_to_dynamo(tb_activity, activities_data)
