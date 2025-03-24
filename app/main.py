from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from . import crud, schemas, database

app = FastAPI()

# Dependency to get DB session
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Routes
@app.post("/swagger_api_data/")
def create_swagger_api_data(data: schemas.SwaggerApiDataCreate, db: Session = Depends(get_db)):
    return crud.create_swagger_api_data(db=db, data=data)

@app.post("/input_data/")
def create_input_data(data: schemas.InputDataCreate, db: Session = Depends(get_db)):
    return crud.create_input_data(db=db, data=data)

@app.post("/group_name/")
def create_group_name(data: schemas.GroupNameCreate, db: Session = Depends(get_db)):
    return crud.create_group_name(db=db, data=data)

@app.post("/results/")
def create_results(data: schemas.ResultsCreate, db: Session = Depends(get_db)):
    return crud.create_results(db=db, data=data)

@app.get("/swagger_api_data/{api_id}")
def get_swagger_api_data(api_id: int, db: Session = Depends(get_db)):
    db_data = crud.get_swagger_api_data(db, api_id)
    if db_data is None:
        raise HTTPException(status_code=404, detail="SwaggerApiData not found")
    return db_data
