from flask_wtf import FlaskForm
from wtforms import StringField, EmailField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo


class RegistrationForm(FlaskForm):
    name = StringField("Login", validators=[DataRequired()])
    email = EmailField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    confirm_password = PasswordField(
        "Confirm Password", validators=[DataRequired(), EqualTo("password")]
    )
    submit = SubmitField("Register")


class LoginForm(FlaskForm):
    name = StringField("Login or Email", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Login")


class ConfirmationForm(FlaskForm):
    code = StringField("Confirmation Code", validators=[DataRequired()])
    submit = SubmitField("Confirm")
