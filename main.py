from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class User(BaseModel):
    id:int
    email:str
    firstName:str
    lastName:str
    isMale:bool

@app.get('/',status_code=200)
def getCar_Info():
    return {"message":"server is running"}

@app.get('/getuserbyid/{user_id}',status_code=200)
def getPerson_By_Id(user_id:int):
    return {"message":f"Your Person Id is {user_id}"}
    
@app.post('/adduser',status_code=200)
def add_user(user:User):
    return {
        "id":user.id,
        "email":user.email,
        "firstName":user.firstName,
        "lastName":user.lastName,
        "isMale":user.isMale
    }
    