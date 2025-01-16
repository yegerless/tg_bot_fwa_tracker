from pydantic import BaseModel, ConfigDict



class UserData(BaseModel):
    weight: int
    height: int
    age: int
    activity: int
    city: str
    water_goal: int
    calorie_goal: int
    logged_water: int
    logged_calories: int
    burned_calories: int



class UserId(BaseModel):
    model_config = ConfigDict(frozen=True)

    user_id: int



class Storage(BaseModel):
    user: dict[UserId, UserData] | None