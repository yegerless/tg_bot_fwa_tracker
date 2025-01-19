from pydantic import BaseModel, ConfigDict, Field


'''
class UserData(BaseModel):
    height: int = Field(default=None, gt=100, lt=250)
    weight: float = Field(default=None)
    age: int = Field(default=None, gt=0, lt=110)
    activity: int = Field(default=None)
    city: str = Field(default=None)
    water_goal: int = Field(default=None)
    calorie_goal: int = Field(default=None)
    logged_water: int = Field(default=None)
    logged_calories: int = Field(default=None)
    burned_calories: float = Field(default=None)



class UserId(BaseModel):
    model_config = ConfigDict(frozen=True)

    user_id: int = Field()



class Storage(BaseModel):
    users: dict[UserId, UserData] | None = Field(default=None)


storage = Storage()
'''

storage = {}