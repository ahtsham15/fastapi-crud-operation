from fastapi import FastAPI

app = FastAPI()

@app.get('/',status_code=200)
def getCar_Info():
    return {"message":"server is running"}
