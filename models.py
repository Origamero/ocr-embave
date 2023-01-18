from json import JSONEncoder
from typing import Optional
import uuid

from pydantic import BaseModel, Field

def check_user(user, line):
  return line.__contains__(user["ci"]) or line.__contains__(user["name"])

class User(BaseModel):
  id: str = Field(default_factory=uuid.uuid4, alias="_id")
  ci: str = Field(...) 
  name: str = Field(...) 
  phone: str = Field(...)

  
  class Config:
    allow_population_by_field_name = True
    schema_extra = {
        "example": {
            "_id": "066de609-b04a-4b30-b46c-32537c7f1f6e",
            "ci": "19.764.347",
            "name": "Miguel de Cervantes",
            "phone": "+569414193309"
        }
    }

  def from_string(valueString):
    valuesArray = valueString.split(',')
    return User(valuesArray[0],valuesArray[1],valuesArray[2])

class Result(BaseModel):
    listInfo: Optional[str]
    row: Optional[str]
    cover: Optional[str]

    class Config:
      allow_population_by_field_name = True
      schema_extra = {
          "example": {
              "_id": "066de609-b04a-4b30-b46c-32537c7f1f6e",
              "listInfo": "Don Quixote",
              "row": "Miguel de Cervantes",
              "cover": "..."
          }
      }