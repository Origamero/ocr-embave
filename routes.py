from ast import List
import json
import string
from fastapi import APIRouter, Body, Request, Response, HTTPException, status
from fastapi.encoders import jsonable_encoder
from typing import List
from listscrapper import search
from models import Result, User


router = APIRouter()

@router.get("/search", response_description="Buscar usuario en lista", response_model=List[Result])
def searchInLists(request: Request):
  # users = list(request.app.database["users"].find(limit=100))
  # return resultsList
  users = list(request.app.database["users"].find(limit=100))
  resultsList = list()
  for user in users:
    result = search(user)
    if result is not None:
      resultsList.append(result)
  return resultsList


@router.post("/", response_description="Create a new User", status_code=status.HTTP_201_CREATED, response_model=User)
def create_User(request: Request, User: User = Body(...)):
    User = jsonable_encoder(User)
    new_User = request.app.database["users"].insert_one(User)
    created_User = request.app.database["users"].find_one(
        {"_id": new_User.inserted_id}
    )

    return created_User


@router.get("/", response_description="List all users", response_model=List[User])
def list_Users(request: Request):
    users = list(request.app.database["users"].find(limit=100))
    return users


@router.get("/{id}", response_description="Get a single User by id", response_model=User)
def find_User(id: str, request: Request):
    if (User := request.app.database["users"].find_one({"_id": id})) is not None:
        return User

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with ID {id} not found")


@router.put("/{id}", response_description="Update a User", response_model=User)
def update_User(id: str, request: Request, User: User = Body(...)):
    User = {k: v for k, v in User.dict().items() if v is not None}

    if len(User) >= 1:
        update_result = request.app.database["users"].update_one(
            {"_id": id}, {"$set": User}
        )

        if update_result.modified_count == 0:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with ID {id} not found")

    if (
        existing_User := request.app.database["users"].find_one({"_id": id})
    ) is not None:
        return existing_User

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with ID {id} not found")


@router.delete("/{id}", response_description="Delete a User")
def delete_User(id: str, request: Request, response: Response):
    delete_result = request.app.database["users"].delete_one({"_id": id})

    if delete_result.deleted_count == 1:
        response.status_code = status.HTTP_204_NO_CONTENT
        return response

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with ID {id} not found")