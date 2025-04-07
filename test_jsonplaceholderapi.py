import pytest
import requests

@pytest.fixture
def base_url():
    return "https://jsonplaceholder.typicode.com"


# GET Request Test
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

# GET Requests Test
# Test fetching all posts
@pytest.mark.jsonplaceholder
def test_getting_resource(base_url):
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

# POST Request Test
# Test creating a new resource
@pytest.mark.jsonplaceholder
@pytest.mark.xfail # Expecting to fail because I set "userId" to an integer and the response returns it as a string
def test_creating_resource(base_url):
    url = base_url + "/posts"
    data = {
        "title": 'foo',
        "body": 'bar',
        "userId": 1
    }
    response = requests.post(url, data)
    assert response.status_code == 201
    assert response.json()["id"] == 101
    assert response.json()["title"] == 'foo'
    assert response.json()["body"] == 'bar'
    assert response.json()["userId"] == 1

# GET Request Test (parameterized)
# Test fetching multiple posts
@pytest.mark.jsonplaceholder
@pytest.mark.parametrize("post_id, expected_title", [(1, "sunt aut facere repellat provident occaecati excepturi optio reprehenderit"), (2, "qui est esse")])
def test_getting_resources(base_url, post_id, expected_title):
    url = base_url + "/posts/" + str(post_id)
    response = requests.get(url)
    assert response.status_code == 200
    assert response.json()["title"] == expected_title

# DELETE Resource Test
# Test deleting a specific post
@pytest.mark.jsonplaceholder
def test_deleting_resource(base_url):
    url = base_url + "/posts/1"
    response = requests.delete(url)
    assert response.status_code == 200