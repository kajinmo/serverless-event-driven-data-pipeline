from typing import List, Tuple
from datetime import datetime
import uuid
from faker import Faker
from src.models.contracts import UserProfile, UserActivity

# Using US locale for English synthetic data
fake = Faker('en_US')

def generate_mock_data(amount: int = 25) -> Tuple[List[dict], List[dict]]:
    profiles, activities = [], []
    
    for _ in range(amount):
        u_id = str(uuid.uuid4())
        
        # Pydantic magic: if Faker generates an invalid tier, 
        # the code throws a ValidationError immediately.
        profile = UserProfile(
            user_id=u_id,
            name=fake.name(),
            email=fake.email(),
            subscription_tier=fake.random_element(elements=('Free', 'Basic', 'Premium'))
        )
        
        activity = UserActivity(
            user_id=u_id,
            last_login=datetime.now().isoformat(),
            device=fake.random_element(elements=('Mobile', 'Desktop', 'Tablet'))
        )
        
        # model_dump() converts the model back to a dictionary for Boto3
        profiles.append(profile.model_dump())
        activities.append(activity.model_dump())
        
    return profiles, activities
