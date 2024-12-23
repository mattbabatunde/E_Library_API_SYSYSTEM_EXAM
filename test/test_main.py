from fastapi.testclient import TestClient
from main import app  

client = TestClient(app)

def test_home_endpoint():

    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to the E-Library API System!"}

def test_users_endpoint():
 
    response = client.get("/users")
    assert response.status_code in [200, 404] 
    
def test_books_endpoint():

    response = client.get("/books")
    assert response.status_code in [200, 404]  

def test_borrow_records_endpoint():
 
    response = client.get("/borrow_records")
    assert response.status_code in [200, 404]  