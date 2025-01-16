from getgauge.python import step, data_store
import requests
import json

API_BASE_URL = "https://jsonplaceholder.typicode.com"

@step("Get all posts from JSONPlaceholder")
def get_all_posts():
    response = requests.get(f"{API_BASE_URL}/posts")
    assert response.status_code == 200, f"Expected status code 200, but got {response.status_code}"
    posts = response.json()
    assert len(posts) > 0, "No posts were returned"
    # Store the number of posts for later verification
    data_store.scenario["initial_posts_count"] = len(posts)

@step("Create a new post")
def create_new_post():
    new_post = {
        "title": "Test Post",
        "body": "This is a test post created by Gauge automation",
        "userId": 1
    }
    response = requests.post(f"{API_BASE_URL}/posts", json=new_post)
    assert response.status_code == 201, f"Expected status code 201, but got {response.status_code}"
    created_post = response.json()
    # Store the created post for later verification
    data_store.scenario["created_post"] = created_post

@step("Verify the created post details")
def verify_post_details():
    created_post = data_store.scenario["created_post"]
    assert created_post["title"] == "Test Post", "Post title does not match"
    assert created_post["body"] == "This is a test post created by Gauge automation", "Post body does not match"
    assert created_post["userId"] == 1, "User ID does not match"
    assert "id" in created_post, "Post ID was not generated"
