from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, IntegerField, FieldList, FormField, DateField
from wtforms.validators import DataRequired

class ProductInDishForm(FlaskForm):
    product_id = IntegerField(name='product_id', validators=[DataRequired])
    weight = IntegerField(name='weight', validators=[DataRequired])

class AddDishForm(FlaskForm):
    name = StringField(name='name', validators=[DataRequired])
    owner = IntegerField(name='owner', validators=[DataRequired])
    calories = IntegerField(name='calories', validators=[DataRequired])
    proteins = FloatField(name='proteins', validators=[DataRequired])
    carbohydrates = FloatField(name='carbohydrates', validators=[DataRequired])
    fats = FloatField(name='fats', validators=[DataRequired])
    category = StringField(name='category', validators=[DataRequired])
    products = FieldList(FormField(ProductInDishForm), min_entries=1)

class AddProductForm(FlaskForm):
    name = StringField(name='name', validators=[DataRequired])
    calories = IntegerField(name='calories', validators=[DataRequired])
    proteins = FloatField(name='proteins', validators=[DataRequired])
    carbohydrates = FloatField(name='carbohydrates', validators=[DataRequired])
    fats = FloatField(name='fats', validators=[DataRequired])

class DishesInDietForm(FlaskForm):
    dish_id = IntegerField(name='dish_id', validators=[DataRequired])
    weight = IntegerField(name='weight', validators=[DataRequired])
    time_of_day = DateField(name="time_of_day", validators=[DataRequired])

class AddDietForm(FlaskForm):
    name = StringField(name='name', validators=[DataRequired])
    owner = IntegerField(name='owner', validators=[DataRequired])
    description = StringField(name='description', validators=[DataRequired])
    dishes = FieldList(FormField(DishesInDietForm), min_entries=1)

class DTUForm(FlaskForm):
    trainer_id = IntegerField(nane='trainer_id', validators=[DataRequired])
    diet_id = IntegerField(name='diet_id', validators=[DataRequired])
    date = DateField(name="date", validators=[DataRequired])