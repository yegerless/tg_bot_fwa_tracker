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
storage[450646375] = {'height': 176, 'weight': 78.0, 'age': 25, 'activity': 45, 'city': 'f', 'water_goal': 3090, 'kalories_goal': 2500, 'logged_water': {'19-01-2025': {'21:31:40': 100}}, 'logged_calories': {'20-01-2025': {'16:27:57': 445.0}}, 'burned_calories': {}}