import os
import boto3
from dotenv import load_dotenv

def main():
    # Load variables from .env
    load_dotenv()
    
    mongo_user = os.environ.get("MONGO_USER")
    mongo_password = os.environ.get("MONGO_PASSWORD")
    
    if not mongo_user or not mongo_password:
        print("ERROR: Please set a valid MONGO_USER and MONGO_PASSWORD in your .env file.")
        return

    # Use the AWS profile specified by the user
    session = boto3.Session(profile_name="portfolio-sandbox", region_name="us-east-1")
    ssm = session.client("ssm")

    parameters = {
        "/eda/mongo_user": mongo_user,
        "/eda/mongo_password": mongo_password
    }
    
    for name, value in parameters.items():
        print(f"Uploading {name} to AWS SSM Parameter Store...")
        try:
            ssm.put_parameter(
                Name=name,
                Value=value,
                Type="SecureString",
                Overwrite=True
            )
            print(f"Successfully uploaded {name} to SSM!")
        except Exception as e:
            print(f"Failed to upload {name} to SSM: {e}")

if __name__ == "__main__":
    main()
