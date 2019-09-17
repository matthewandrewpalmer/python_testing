import requests

post_req = requests.get("http://jsonplaceholder.typicode.com/posts")
user_req = requests.get("https://jsonplaceholder.typicode.com/users")

posts = post_req.json()
users = user_req.json()

# for user in users:
#     print(f'Name: {user["name"]} ({user["username"]}), City: {user["address"]["city"]}')

# for post in posts:
#     userID = post["userId"]
#     for user in users:
#         if user["id"] == userID:
#             print(f'{post["title"]} by {user["name"]}')

# OR

userDict = {}

for user in users:
    userDict[user["id"]] = user["name"]

for post in posts:
    print(f'{post["title"]} by {userDict[post["userId"]]}')
