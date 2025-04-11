from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, IntegerField, FieldList, FormField
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