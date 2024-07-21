import time
import subprocess
import pytest
import requests
from datetime import datetime, timedelta, timezone

discount_id = None
server_process = None
BASE_URL = "http://localhost:8000"

# IDK what's wrong with this

# def setup_server():
#     global server_process
#     server_process = subprocess.Popen(
#         ["uvicorn", "discount_service.main:app", "--host", "localhost", "--port", "8000"],
#         stdout=subprocess.PIPE,
#         stderr=subprocess.PIPE
#     )
    
#     # Wait for the server to start
#     import time
#     time.sleep(17) 
    
#     try:
#         response = requests.get("http://localhost:8000/discounts/?limit=10&skip=0")
#         print("Server status:", response.status_code)
#     except Exception as e:
#         print("Error checking server status:", e)

#     yield

#     # Terminate the server
#     server_process.terminate()
#     time.sleep(3) 
#     server_process.wait()

@pytest.fixture
def client():
    class Client:
        def __init__(self, base_url):
            self.base_url = base_url

        def post(self, endpoint, json=None):
            return requests.post(f"{self.base_url}{endpoint}", json=json)

        def get(self, endpoint):
            return requests.get(f"{self.base_url}{endpoint}")

        def put(self, endpoint, json=None):
            return requests.put(f"{self.base_url}{endpoint}", json=json)

        def delete(self, endpoint):
            return requests.delete(f"{self.base_url}{endpoint}")

    return Client(base_url=BASE_URL)


def create_discount(client, discount_data):
    response = client.post("/discounts/", json=discount_data)
    assert response.status_code == 200
    return response.json()

def read_discount(client, discount_id):
    response = client.get(f"/discounts/{discount_id}")
    return response.json()

def update_discount(client, discount_id, update_data):
    response = client.put(f"/discounts/{discount_id}", json=update_data)
    return response.json()

def delete_discount(client, discount_id):
    response = client.delete(f"/discounts/{discount_id}")
    return response.json()

def list_discounts(client):
    response = client.get("/discounts/?limit=10&skip=0")
    return response.json()

# Create discount to save the id for further operations
@pytest.mark.asyncio
def test_setup(client):
    global discount_id
    discount_data = {
        "code": "TEST",
        "use_count": 29999,
        "start_date": (datetime.now(timezone.utc) + timedelta(days=1)).isoformat(),
        "end_date": (datetime.now(timezone.utc) + timedelta(days=10)).isoformat(),
        "percentage": 10.0
    }
    create_response = create_discount(client, discount_data)
    discount_id = create_response.get("id")
    assert discount_id is not None
    assert create_response.get('status') == True
    
@pytest.mark.asyncio
def test_read_discount(client):
    test_setup(client)
    response = read_discount(client, discount_id)
    assert response["code"] == "TEST"

@pytest.mark.asyncio
def test_update_discount(client):
    test_setup(client)
    update_data = {"code": "UPDATED10"}
    response = update_discount(client, discount_id, update_data)
    assert response["code"] == "UPDATED10"

@pytest.mark.asyncio
def test_delete_discount(client):
    test_setup(client)
    response = delete_discount(client, discount_id)
    assert response["detail"] == "Discount deleted"

@pytest.mark.asyncio
def test_list_discounts(client):
    response = list_discounts(client)
    print(client)
    assert len(response) > 0
    assert response[0]['code'] == "TEST"
