from pydantic import BaseModel, Field

class UserProfile(BaseModel):
    user_id: str
    name: str
    email: str
    # The Field pattern ensures only these 3 values are accepted
    subscription_tier: str = Field(pattern="^(Free|Basic|Premium)$")

class UserActivity(BaseModel):
    user_id: str
    last_login: str
    device: str = Field(pattern="^(Mobile|Desktop|Tablet)$")
