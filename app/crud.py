from sqlalchemy.orm import Session
from . import models, schemas

# Create SwaggerApiData
def create_swagger_api_data(db: Session, data: schemas.SwaggerApiDataCreate):
    db_data = models.SwaggerApiData(**data.dict())
    db.add(db_data)
    db.commit()
    db.refresh(db_data)
    return db_data

# Create InputData
def create_input_data(db: Session, data: schemas.InputDataCreate):
    db_data = models.InputData(**data.dict())
    db.add(db_data)
    db.commit()
    db.refresh(db_data)
    return db_data

# Create GroupName
def create_group_name(db: Session, data: schemas.GroupNameCreate):
    db_data = models.GroupName(**data.dict())
    db.add(db_data)
    db.commit()
    db.refresh(db_data)
    return db_data

# Create Results
def create_results(db: Session, data: schemas.ResultsCreate):
    db_data = models.Results(**data.dict())
    db.add(db_data)
    db.commit()
    db.refresh(db_data)
    return db_data

# Get SwaggerApiData by ID
def get_swagger_api_data(db: Session, api_id: int):
    return db.query(models.SwaggerApiData).filter(models.SwaggerApiData.id == api_id).first()
