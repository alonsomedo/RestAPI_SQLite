
import sqlite3
from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
import json

class Item(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument('price',
                    type = float,
                    required = True,
                    help = "This field cannot be left blank!"
                    )

    @jwt_required()
    def get(self, name):
       item = self.find_by_name(name)
       if item:
           return item
       return {'message': 'Item not found.'}, 404
    
    @classmethod
    def find_by_name(cls, name):
       connection = sqlite3.connect('data.db')
       cursor = connection.cursor()

       query = "SELECT * FROM ITEMS WHERE NAME = ?"
       result = cursor.execute(query,(name,))
       row = result.fetchone()
       connection.close()

       if row:
           return {'item':{'name':row[0], 'price':row[1]}}

    def post(self,name):
        
        if self.find_by_name(name):
            return {'message': "An item with name '{}' already exusts.".format(name)}, 400
       
        data = Item.parser.parse_args()

        item = {'name':name, 'price':data['price']}

        try:
            self.insert(item)
        except:
            return {"message": "An error ocurred inserting the item."}, 500 # Internal server error

        return item, 201
    
    @classmethod
    def insert(cls,item):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "INSERT INTO ITEMS VALUES(?,?)"
        cursor.execute(query,(item["name"],item["price"]))
        
        connection.commit()
        connection.close()

    
    def delete(self, name):
        
        item = Item.find_by_name(name)
        
        if item:
           connection = sqlite3.connect('data.db')
           cursor = connection.cursor()
           
           query = 'DELETE FROM ITEMS WHERE name = ?'
           cursor.execute(query,(name,))
           connection.commit()
           connection.close()
           return {'message':'The item was deleted successfully.'}


        return {'message': 'The item doesnt exists.'}

    def put(self, name):
        data = Item.parser.parse_args()
        #data = request.get_json()

        item = self.find_by_name(name)
        updated_item = {"name":name, "price": data["price"]}    

        if item is None:
            try:
                self.insert(updated_item)
            except:
                return {"message": "An error ocurred inserting the item."}, 500
        else:
            try:
                self.update(updated_item)
            except:
                return {"message": "An error ocurred updating the item."}, 500
        return updated_item
    
    @classmethod
    def update(cls, item):
        print(item)
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "UPDATE ITEMS SET PRICE=? WHERE NAME=?"

        cursor.execute(query,(item["price"], item["name"]))

        
        connection.commit()
        connection.close()

class ItemList(Resource):
    def get(self):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "SELECT * FROM ITEMS"
        result = cursor.execute(query)
        
        items = []

        for row in result:
            items.append({"name": row[0], "price":row[1]})

        connection.close()

        return {"items": items}