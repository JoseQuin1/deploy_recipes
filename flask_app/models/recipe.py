from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app.models.user import Users

db = 'recipes'

class Recipe:
    def __init__(self,data):
        self.id = data['id']
        self.name = data['name']
        self.description = data['description']
        self.instructions = data['instructions']
        self.date_cooked = data['date_cooked']
        self.under_30_minutes = data['under_30_minutes']
        self.user_id = data['user_id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.users = []

    @classmethod
    def save(cls,data):
        query = """
        INSERT INTO recipes (user_id, name, description, instructions, under_30_minutes, date_cooked)
        VALUE(%(id)s,%(name)s,%(description)s,%(instructions)s,%(under_30_minutes)s,%(date_cooked)s);
        """
        return connectToMySQL(db).query_db(query,data)
    
    @classmethod
    def get_all_recipes(cls):
        query ="""
        SELECT * FROM recipes JOIN users on recipes.user_id = users.id
        """
        results = connectToMySQL(db).query_db(query)
        recipes = []

        for row in results:
            this_recipe = cls(row)
            user_data = {
                'id': row['users.id'],
                'first_name': row['first_name'],
                'last_name': row['last_name'],
                'email': row['email'],
                'password': "",
                'created_at': row['users.created_at'],
                'updated_at': row['users.updated_at']
            }
            this_recipe.users = Users(user_data)
            recipes.append(this_recipe)

        return recipes

    @classmethod
    def get_by_id(cls,data):
        query = """ SELECT * FROM recipes JOIN users on recipes.user_id = users.id WHERE recipes.id = %(id)s; """
        results = connectToMySQL(db).query_db(query,data)
        results = results[0]

        if not results:
            return False
        else:
            this_recipe = cls(results)
            user_data = {
                'id': results['users.id'],
                'first_name': results['first_name'],
                'last_name': results['last_name'],
                'email': results['email'],
                'password': "",
                'created_at': results['users.created_at'],
                'updated_at': results['users.updated_at']
            }
            this_recipe.users.append(Users(user_data))
            return this_recipe
    
    @classmethod
    def update(cls,data):
        query = """
        UPDATE recipes 
        set name = %(name)s, 
        description = %(description)s, 
        instructions = %(instructions)s, 
        under_30_minutes = %(under_30_minutes)s, 
        date_cooked = %(date_cooked)s
        WHERE id = %(id)s;
        """
        return connectToMySQL(db).query_db(query,data)

    @classmethod
    def delete(cls,data):
        query = """
        DELETE FROM recipes WHERE id = %(id)s;
        """
        return connectToMySQL(db).query_db(query,data)

    @staticmethod
    def validate_recipe(form_data):
            is_valid = True
            if len(form_data['name']) < 3:
                    flash("Name must be at least 3 characters long.", "recipe")
                    is_valid = False
            if len(form_data['description']) < 3:
                    flash("Description must be at least 3 characters long.", "recipe")
                    is_valid = False
            if len(form_data['instructions']) < 3:
                    flash("Instructions must be at least 3 characters long.", "recipe")
                    is_valid = False
            if form_data['date_cooked'] == '':
                    flash("Please input a date.", "recipe")
                    is_valid = False
            if 'under_30_minutes' not in form_data:
                    flash("Give me cook time.", "recipe")
                    is_valid = False
            return is_valid