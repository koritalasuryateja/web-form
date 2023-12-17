import json

DATA_FILE = "posts.json"

def save_posts(posts):
    with open(DATA_FILE, "w") as file:
        json.dump(posts, file)

def load_posts():
    try:
        with open(DATA_FILE, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return {}
