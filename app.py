from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy 
from dotenv import load_dotenv, dotenv_values
import datetime
import os

load_dotenv()


DB_USERNAME = os.getenv('DB_USERNAME')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_NAME = os.getenv('DB_NAME')
DB_HOST = os.getenv('DB_HOST')
DB_PORT = os.getenv('DB_PORT')

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Define the models based on your existing database structure

class Recipe(db.Model):
    __tablename__ = 'fct_recipes'
    recipe_id = db.Column(db.BigInteger, primary_key=True)
    recipe_name = db.Column(db.String(250), nullable=False)
    recipe_desc = db.Column(db.String(25000))
    creation_date = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    created_by = db.Column(db.BigInteger)
    modified_date = db.Column(db.DateTime, onupdate=datetime.datetime.utcnow)
    modified_by = db.Column(db.BigInteger)
    is_private = db.Column(db.SmallInteger, default=1)

    ingredients = db.relationship('RecipeIngredient', backref='recipe', lazy=True)
    instructions = db.relationship('RecipeInstruction', backref='recipe', lazy=True)

class RecipeIngredient(db.Model):
    __tablename__ = 'fct_recipe_ingredients'
    recipe_ingredient_id = db.Column(db.BigInteger, primary_key=True)
    recipe_id = db.Column(db.BigInteger, db.ForeignKey('fct_recipes.recipe_id'), nullable=False)
    ingredient_id = db.Column(db.BigInteger, db.ForeignKey('dim_ingredients.ingredient_id'), nullable=False)
    quantity = db.Column(db.String(250))
    unit_of_measure = db.Column(db.String(250))

class RecipeInstruction(db.Model):
    __tablename__ = 'fct_recipe_instructions'
    recipe_instruction_id = db.Column(db.BigInteger, primary_key=True)
    recipe_id = db.Column(db.BigInteger, db.ForeignKey('fct_recipes.recipe_id'), nullable=False)
    instruction = db.Column(db.Text, nullable=False)
    step_number = db.Column(db.Integer, nullable=False)

class Ingredient(db.Model):
    __tablename__ = 'dim_ingredients'
    ingredient_id = db.Column(db.BigInteger, primary_key=True)
    ingredient_name = db.Column(db.String(500), nullable=False)
    ingredient_type = db.Column(db.String(500))
    creation_date = db.Column(db.DateTime, default=datetime.datetime.utcnow)

# SETUP ROUTES TO ADD RECIPE, INGREDIENTS, AND INSTRUCTIONS

@app.route('/add/', methods=['GET', 'POST'])
def add_recipe():
    if request.method == 'POST':
        recipe_name = request.form['name']
        recipe_desc = request.form.get('description')
        is_private = request.form.get('is_private', 1)
        
        # Create a new recipe
        new_recipe = Recipe(
            recipe_name=recipe_name,
            recipe_desc=recipe_desc,
            is_private=is_private
        )
        
        db.session.add(new_recipe)
        db.session.commit()

        # Add ingredients
        ingredients = request.form.getlist('ingredients[]')
        quantities = request.form.getlist('quantities[]')
        units = request.form.getlist('units[]')
        
        for i in range(len(ingredients)):
            ingredient_name = ingredients[i]
            quantity = quantities[i]
            unit = units[i]

            # Check if ingredient already exists
            ingredient = Ingredient.query.filter_by(ingredient_name=ingredient_name).first()
            if not ingredient:
                ingredient = Ingredient(ingredient_name=ingredient_name)
                db.session.add(ingredient)
                db.session.commit()

            new_ingredient = RecipeIngredient(
                recipe_id=new_recipe.recipe_id,
                ingredient_id=ingredient.ingredient_id,
                quantity=quantity,
                unit_of_measure=unit
            )
            db.session.add(new_ingredient)

        # Add instructions
        instructions = request.form.getlist('instructions[]')
        for idx, instruction in enumerate(instructions, start=1):
            new_instruction = RecipeInstruction(
                recipe_id=new_recipe.recipe_id,
                instruction=instruction,
                step_number=idx
            )
            db.session.add(new_instruction)

        db.session.commit()

        return redirect(url_for('add_recipe'))

    return render_template('add_recipe.html', title="Add Recipe")


# APP RUN

if __name__ == "__main__":
    app.run(debug=True)


