from fastapi import FastAPI, status, HTTPException
from pydantic import BaseModel
from database import SessionLocal
from models import User as UserModel

app = FastAPI()

db = SessionLocal()

class UserSchema(BaseModel):
    id: int
    email: str
    firstName: str
    lastName: str
    isMale: bool

    class Config:
        orm_mode = True

@app.get('/', response_model=list[UserSchema], status_code=status.HTTP_200_OK)
def getAllUser():
    getAllUsers = db.query(UserModel).all()
    return getAllUsers

@app.post('/addnewuser', response_model=UserSchema, status_code=status.HTTP_201_CREATED)
def addNewUser(user:UserSchema):
    try:
        newUser = UserModel(
            id=user.id,
            email=user.email,
            firstName=user.firstName,
            lastName=user.lastName,
            isMale=user.isMale
        )
        find_person = db.query(UserModel).filter(UserModel.id == newUser.id).first()
        if find_person is not None:
            raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail="Person with this id Already exist")
        db.add(newUser)
        db.commit()
        # db.refresh(newUser)
        return newUser
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error creating user: {str(e)}"
        )

@app.patch('/updateuser/{user_id}',response_model=UserSchema,status_code=status.HTTP_202_ACCEPTED)
def updateUser(user_id:int,user:UserSchema):
    try:
        find_user = db.query(UserModel).filter(UserModel.id == user_id).first()
        if find_user is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        
        db.query(UserModel).filter(UserModel.id == user_id).update({
            "email": user.email,
            "firstName": user.firstName,
            "lastName": user.lastName,
            "isMale": user.isMale
        })
        
        db.commit()
        db.refresh(find_user)
        return find_user
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error updating user: {str(e)}"
        )