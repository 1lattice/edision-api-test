
import pytest
import requests
import sys
import os
import time
from sqlalchemy.orm import joinedload

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'app')))

from database import SessionLocal
from models import SwaggerApiData, InputData, Results, GroupName, TestHistory

# Function to get a database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Function to get all group names' ids from the database
def get_all_group_name_ids(db):
    groups = db.query(GroupName).all()
    return [group.id for group in groups]

# Function to log the test history to the database
def log_test_history(db, group_name, group_id, api, status, response=None, error_message=None, time_taken=None):
    test_history = TestHistory(
        group_name=group_name,
        group_id=group_id,
        api_name=api.api,
        status=status,
        response_status_code=response.status_code if response else None,
        error_message=error_message,
        response_body=response.text if response else None,
        time_taken=time_taken
    )
    db.add(test_history)
    db.commit()

# Function to get API data and input/result data
def get_api_data(db, group_ids):
    if not group_ids:
        pytest.fail(f"No groups found in the database!")

    # Fetch all APIs belonging to this GroupName, sorted by priority, with eager loading of 'group_names'
    apis = db.query(SwaggerApiData).filter(SwaggerApiData.group_name_id.in_(group_ids)) \
        .options(joinedload(SwaggerApiData.group_names)).order_by(SwaggerApiData.priority).all()

    api_data = []
    for api in apis:
        input_data = db.query(InputData).filter(InputData.swagger_api_id == api.id).first()
        result_data = db.query(Results).filter(Results.swagger_api_id == api.id).first()
        if input_data and result_data:
            api_data.append((api, input_data, result_data))
        else:
            pytest.fail(f"API {api.api}, input data or result data not found in the database!")
    return api_data

@pytest.mark.parametrize("api, input_data, result_data", get_api_data(next(get_db()), get_all_group_name_ids(next(get_db()))))
def test_call_api(api, input_data, result_data):
    start_time = time.time()
    db = next(get_db())
    try:
        if not input_data or not result_data:
            pytest.fail(f"Input data or result data not found in the database for API {api.api}!")

        url = api.api
        params = input_data.data
        headers = {
            "Platform": api.platform,
        }

        # Make the API request based on the method
        if api.method_name.upper() == "GET":
            response = requests.get(url, params=params, headers=headers)
        elif api.method_name.upper() == "POST":
            response = requests.post(url, json=params, headers=headers)
        elif api.method_name.upper() == "PUT":
            response = requests.put(url, json=params, headers=headers)
        elif api.method_name.upper() == "DELETE":
            response = requests.delete(url, json=params, headers=headers)
        elif api.method_name.upper() == "PATCH":
            response = requests.patch(url, json=params, headers=headers)
        else:
            pytest.fail(f"Invalid method name: {api.method_name}")

        end_time = time.time()
        time_taken = end_time - start_time

        assert response.status_code == result_data.status_code
        log_test_history(db, api.group_names.group_name, api.group_name_id, api, "Pass", response, time_taken=time_taken)

    except Exception as e:
        end_time = time.time()
        time_taken = end_time - start_time
        error_message = str(e)

        if response:
            log_test_history(db, api.group_names.group_name, api.group_name_id, api, "Fail", response, error_message, time_taken)
        else:
            log_test_history(db, api.group_names.group_name, api.group_name_id, api, "Fail", response, error_message, time_taken)
        pytest.fail(error_message)

