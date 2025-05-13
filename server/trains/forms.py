from flask_wtf import FlaskForm
from wtforms import IntegerField, DateField, StringField
from wtforms.validators import DataRequired, NumberRange

class TrainForm(FlaskForm):
    train_id = IntegerField(name = "integer_id", validators=[DataRequired])
    date = DateField(name = "date", validators=[DataRequired])
    time = StringField(name = "time", validators=[DataRequired, NumberRange(min=1)])