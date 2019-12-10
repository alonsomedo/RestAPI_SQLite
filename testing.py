class User():
    def __init__(self, _id, username, password):
        self.id = _id
        self.username = username
        self.password = password

users = [
        User(1,'alonso', 23),
        User(2,'andres', 23),
        User(3,'gladys',40),
        User(4,'antonio',23)
]

for u in users:
    print(u.username)

username = {u.username: u for u in users}

print(username)
    