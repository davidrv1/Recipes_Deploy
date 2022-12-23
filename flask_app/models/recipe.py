from flask_app.config.mysqlconnection import connectToMySQL
mydb = 'recipes_schema'
from flask_app.models.user import User
from flask import flash

class Recipe:
    def __init__(self,data):
        self.id = data['id']
        self.name = data['name']
        self.description = data['description']
        self.instructions = data['instructions']
        self.date_made = data['date_made']
        self.under_30 = data['under_30']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.creator = None

    @staticmethod
    def validate_create(request):
        is_valid = True
        if len(request['name']) < 4:
            flash('Name must be longer than 4 Characters')
            is_valid = False
        if len(request['description']) <4:
            flash('Description Must Be Longer Than 4 Characters')
            is_valid = False
        if len(request['instructions']) <4:
            flash('Instructions Must Be Longer Than 4 Characters')
            is_valid = False
        return is_valid

    @classmethod
    def save(cls,data):
        query = '''
        INSERT INTO recipes
        (name, description, instructions, date_made, under_30, users_id)
        VALUES (%(name)s, %(description)s, %(instructions)s,%(date_made)s,%(under_30)s, %(users_id)s);'''
        results = connectToMySQL(mydb).query_db(query,data)
        print(f"results: {results}")
        return results

    # @classmethod
    # def get_all(cls):
    #     query = "SELECT * FROM recipes;"
    #     results = connectToMySQL(mydb).query_db(query)
    #     print(results)
    #     lst = []
    #     for i in results:
    #         lst.append(cls(i))
    #     print(lst)
    #     return lst

    @classmethod
    def getById(cls,data):
        print(data)
        query = '''
        SELECT * FROM recipes
        WHERE id = %(id)s;'''
        results = connectToMySQL(mydb).query_db(query,data)
        print(f"results: {results}")
        return cls(results[0])

    @classmethod
    def deleteById(cls,data):
        query  = '''
        DELETE FROM recipes
        WHERE id = %(id)s;'''
        results = connectToMySQL(mydb).query_db(query,data)
        return results
    
    @classmethod
    def update(cls, data):
        query = '''
        UPDATE recipes
        SET name = %(name)s,
        description = %(description)s,
        instructions = %(instructions)s
        WHERE id = %(id)s;'''
        return connectToMySQL(mydb).query_db(query, data)

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM recipes LEFT JOIN users ON users.id = recipes.users_id;"
        results = connectToMySQL(mydb).query_db(query)
        # print(results)
        recipes = []
        for i in results:
            this_recipe =cls(i)
            this_recipe_creator = {
                'id':i['users.id'],
                'first_name':i['first_name'],
                'last_name':i['last_name'],
                'email':i['email'],
                'password':i['password'],
                'created_at':i['users.created_at'],
                'updated_at':i['users.updated_at'],
            }
            this_recipe.creator= User(this_recipe_creator)
            recipes.append(this_recipe)
        return recipes

    # @classmethod
    # def getById(cls,data):
    #     print(data)
    #     query = '''
    #     SELECT * FROM recipes 
    #     LEFT JOIN users ON users.id = recipes.users_id
    #     WHERE recipes.id = %(id)s;'''
    #     results = connectToMySQL(mydb).query_db(query,data)
    #     print(f"results: {results}")
    #     this_recipe =cls(results[0])
    #     this_recipe_creator = {
    #         'id':results[0]['users.id'],
    #         'first_name':results[0]['first_name'],
    #         'last_name':results[0]['last_name'],
    #         'email':results[0]['email'],
    #         'password':results[0]['password'],
    #         'created_at':results[0]['users.created_at'],
    #         'updated_at':results[0]['users.updated_at'],
    #         }
    #     this_recipe.creator= User(this_recipe_creator)
    #     return this_recipe