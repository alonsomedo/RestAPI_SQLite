import sqlite3
from flask_restful import Resource, reqparse

class User:
    def __init__(self, _id, username, password):
        self.id = _id
        self.username = username
        self.password = password

    @classmethod
    def find_by_username(cls, username):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        query = "SELECT * FROM USERS WHERE USERNAME = ?"
        result = cursor.execute(query, (username,)) #parameters always a tuple
        row = result.fetchone() #returns None when there is no data.
        if row:
            user = cls(*row)
        else:
            user = None
        
        connection.close()
        return user

    @classmethod
    def find_by_id(cls, _id):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        query = "SELECT * FROM USERS WHERE ID = ?"
        result = cursor.execute(query, (_id,)) #parameters always a tuple
        row = result.fetchone() #returns None when there is no data.
        if row:
            user = cls(*row)
        else:
            user = None
        
        connection.close()
        return user

class UserRegister(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('username',
                        type = str,
                        required = True,
                        help = "This field cannot be left blank!"
                        )
    parser.add_argument('password',
                        type = str,
                        required = True,
                        help = "This field cannot be left blank!"
                        )
    def post(self):

        

        data = UserRegister.parser.parse_args()
        
        user = User.find_by_username(data['username'])

        if(user is not None):
            return {'message': "This username already exists!"}, 400

        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "INSERT INTO USERS VALUES (NULL, ?, ?)"
        cursor.execute(query, (data['username'],data['password']))
        
        connection.commit()
        connection.close()

        return {'message': "User created sucessfully!"}, 201