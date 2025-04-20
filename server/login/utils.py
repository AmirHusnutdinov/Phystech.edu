import bcrypt
from flask import render_template
from flask import session


def hash_password(password):
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_password.decode('utf-8')


def is_login():
    return session["Login"]


def data():
    return {"Login": is_login, "Name": session.get("name", None)}


def render_template_with_user(template_name_ot_list, **kwargs):
    kwargs["title"] = kwargs.get("title", "Главная страница")
    return render_template(
        template_name_ot_list,
        data=data(),
        **kwargs
    )
