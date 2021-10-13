from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class Recipe:
    def __init__(self, data):
        self.id = data['id']
        self.name = data['name']
        self.description = data['description']
        self.thirty_minutes = data['thirty_minutes']
        self.instructions = data['instructions']
        self.date = data['date']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_id = data['user_id']

    @classmethod
    def create(cls, data):
        query = "INSERT INTO recipes (name, description, thirty_minutes, instructions, date, user_id) VALUES (%(name)s, %(description)s, %(thirty_minutes)s, %(instructions)s, %(date)s, %(user_id)s);"
        result = connectToMySQL('recipes').query_db(query, data)
        return result

    @classmethod
    def read_all(cls):
        query = 'SELECT * FROM recipes;'
        results = connectToMySQL('recipes').query_db(query)
        recipes = []
        for row in results:
            recipes.append(cls(row))
        return recipes

    @classmethod
    def read_one(cls, data):
        query = 'SELECT * FROM recipes WHERE id = %(id)s;'
        result = connectToMySQL('recipes').query_db(query, data)
        return cls(result[0])

    @classmethod
    def update(cls, data):
        query = "UPDATE recipes SET name = %(name)s, description = %(description)s , thirty_minutes = %(thirty_minutes)s, instructions = %(instructions)s, date = %(date)s WHERE id = %(id)s;"
        result = connectToMySQL('recipes').query_db(query,data)
        return result

    @classmethod
    def delete(cls, data):
        query = "DELETE FROM recipes WHERE id = %(id)s;"
        result = connectToMySQL('recipes').query_db(query,data)
        return result

    @staticmethod
    def valid_recipe(recipe):
        is_valid = True
        if len(recipe['name']) < 3:
            is_valid = False
            flash('Recipe name must be at least 3 characters','recipe')
        if len(recipe['description']) < 3:
            is_valid = False
            flash('Recipe description must be at least 3 characters','recipe')
        if len(recipe['instructions']) < 3:
            is_valid = False
            flash('Recipe instructions must be at least 3 characters','recipe')
        if recipe['date'] == "":
            is_valid = False
            flash('Please enter a date','recipe')
        return is_valid