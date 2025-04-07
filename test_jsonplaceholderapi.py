import pytest
import requests

@pytest.fixture
def base_url():
    return "https://jsonplaceholder.typicode.com"

# Getting a resource
# Test fetching a specific post
@pytest.mark.jsonplaceholder
def test_getting_resource(base_url):
    url = base_url + "/posts/1"
    response = requests.get(url)
    assert response.status_code == 200
    assert response.json()["id"] == 1
    assert "title" in response.json()
    assert "body" in response.json()
    assert "userId" in response.json()

# Listing all resources
# Test fetching all posts
@pytest.mark.jsonplaceholder
def test_listing_all_resources(base_url):
    url = base_url + "/posts"
    response = requests.get(url)
    assert response.status_code == 200

    # assert that the first and last elements in the returned json array of dictionaries are as expected
    assert response.json()[0]["id"] == 1
    assert "title" in response.json()[0]
    assert "body" in response.json()[0]
    assert "userId" in response.json()[0]
    assert response.json()[-1]["id"] == 100
    assert "title" in response.json()[-1]
    assert "body" in response.json()[-1]
    assert "userId" in response.json()[-1]

# Creating a resource
# Test creating a new post
@pytest.mark.jsonplaceholder
@pytest.mark.xfail # Expecting to fail because documentation says output for userId is an integer but its really a string
def test_creating_resource(base_url):
    url = base_url + "/posts"
    body = {
        "title": 'foo',
        "body": 'bar',
        "userId": 1
    }
    response = requests.post(url, body)
    assert response.status_code == 201
    assert response.json()["id"] == 101
    assert response.json()["title"] == 'foo'
    assert response.json()["body"] == 'bar'
    assert response.json()["userId"] == 1

# Updating a resource
# Test updating a specific post
@pytest.mark.jsonplaceholder
@pytest.mark.xfail # Expecting to fail because documentation says output for userId is an integer but its really a string
def test_updating_resource(base_url):
    url = base_url + "/posts/1"
    body = {
        "id": 1,
        "title" : 'foo',
        "body": 'bar',
        "userId": 1
    }
    response = requests.put(url, body)
    assert response.status_code == 200
    assert response.json()["id"] == 1
    assert response.json()["title"] == 'foo'
    assert response.json()["body"] == 'bar'
    assert response.json()["userId"] == 1

# Patching a resource
# Test patching a specific post
@pytest.mark.jsonplaceholder
def test_patching_resource(base_url):
    url = base_url + "/posts/1"
    body = {
        "title": 'foo'
    }
    response = requests.patch(url, body)
    assert response.status_code == 200
    assert response.json()["id"] == 1
    assert response.json()["title"] == 'foo'
    assert "body" in response.json()
    assert response.json()["userId"] == 1

# Deleting a resource
# Test deleting a specific post
@pytest.mark.jsonplaceholder
def test_deleting_resource(base_url):
    url = base_url + "/posts/1"
    response = requests.delete(url)
    assert response.status_code == 200

# Filtering resources
# Test basic filtering using query parameters
@pytest.mark.jsonplaceholder
@pytest.mark.parametrize("filter, value", [("userId", 1), ("id", 1)])
def test_filtering_resources(base_url, filter, value):
    url = base_url + "/posts?" + filter + "=" + str(value)
    response = requests.get(url)
    assert response.status_code == 200

    # assert that the first and last elements in the returned json array of dictionaries have the expected parameter and value
    assert response.json()[0][filter] == value
    assert response.json()[-1][filter] == value

# Listing nested resources
# Test getting all levels of a nested route
@pytest.mark.jsonplaceholder
@pytest.mark.parametrize("route, nest", [("posts", "comments"), ("albums", "photos"), ("users", "albums"), ("users", "todos"), ("users", "posts")])
def test_listing_nested_resources(base_url, route, nest):
    url = base_url + "/" + route + "/1/" + nest
    response = requests.get(url)
    assert response.status_code == 200

# Listing multiple resources (parameterized)
# Test fetching multiple posts
@pytest.mark.jsonplaceholder
@pytest.mark.parametrize("post_id, expected_title", [(1, "sunt aut facere repellat provident occaecati excepturi optio reprehenderit"), (2, "qui est esse")])
def test_getting_resources(base_url, post_id, expected_title):
    url = base_url + "/posts/" + str(post_id)
    response = requests.get(url)
    assert response.status_code == 200
    assert response.json()["title"] == expected_title