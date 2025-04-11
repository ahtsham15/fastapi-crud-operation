from fastapi import FastAPI, status, HTTPException
from pydantic import BaseModel
from database import SessionLocal
from models import User as UserModel

app = FastAPI()

db = SessionLocal()

# class UserSchema(BaseModel):
#     id: int
#     email: str
#     firstName: str
#     lastName: str
#     isMale: bool

#     class Config:
#         orm_mode = True

class UserCreate(BaseModel):
    email: str
    firstName: str
    lastName: str
    isMale: bool

class UserSchema(UserCreate):
    id: int  # Include the auto-generated ID for responses

    class Config:
        orm_mode = True


@app.get('/', response_model=list[UserSchema], status_code=status.HTTP_200_OK)
def getAllUser():
    getAllUsers = db.query(UserModel).all()
    return getAllUsers


@app.post('/addnewuser', response_model=UserSchema, status_code=status.HTTP_201_CREATED)
def addNewUser(user: UserCreate):  # ✅ Use UserCreate (no 'id' required)
    try:
        newUser = UserModel(
            email=user.email,        # 🚫 Omit 'id' here
            firstName=user.firstName,
            lastName=user.lastName,
            isMale=user.isMale
        )
        db.add(newUser)
        db.commit()
        db.refresh(newUser)  # Get the auto-generated ID from the database
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
        
        
@app.delete('/deleteuser/{user_id}',response_model=UserSchema, status_code=status.HTTP_200_OK)
def deleteUser(user_id:int):
    try:
        find_user = db.query(UserModel).filter(UserModel.id == user_id).first()
        if find_user is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        
        db.delete(find_user)
        db.commit()
        return find_user
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            
            detail=f"Error deleting user: {str(e)}"
        )