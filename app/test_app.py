import pytest
from unittest.mock import patch
import mongomock
from app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        # Create a fake MongoDB collection using mongomock
        fake_collection = mongomock.MongoClient().test_db.items
        
        # We "patch" the 'collection' variable inside 'app.py' 
        # so it uses our fake one instead of trying to connect to 'database:27017'
        with patch('app.collection', fake_collection):
            yield client

def test_index_page(client):
    """Test that the home page loads without hitting the real DB."""
    rv = client.get('/')
    assert rv.status_code == 200
    assert b"Three-Tier Docker Application Demo" in rv.data

def test_add_item(client):
    """Test that submitting the form 'works' in the mock."""
    response = client.post('/', data={'content': 'Test Item'}, follow_redirects=True)
    assert response.status_code == 200
    assert b"Test Item" in response.data

def test_update_item(client):
    """Test updating an existing item."""
    # Insert an item into the mock
    from app import collection
    obj = collection.insert_one({'content': 'Old Text'})
    obj_id = str(obj.inserted_id)

    # Call the update route
    response = client.post(f'/update/{obj_id}', data={'content': 'Updated Text'}, follow_redirects=True)
    assert response.status_code == 200
    assert b"Updated Text" in response.data
    assert b"Old Text" not in response.data

def test_delete_item(client):
    """Test deleting an item."""
    # Insert an item into the mock
    from app import collection
    obj = collection.insert_one({'content': 'To Be Deleted'})
    obj_id = str(obj.inserted_id)

    # Call the delete route
    response = client.post(f'/delete/{obj_id}', follow_redirects=True)
    assert response.status_code == 200
    assert b"To Be Deleted" not in response.data