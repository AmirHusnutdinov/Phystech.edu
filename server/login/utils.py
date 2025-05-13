from werkzeug.security import generate_password_hash, check_password_hash
from flask import render_template
from flask import session
from server.service_files.links import choose_header_links



def hash_password(password):
    return generate_password_hash(password)

def check_password(hashed_password, input_password):
    return check_password_hash(hashed_password, input_password)

def is_login():
    return session["Login"]


def data():
    return {"Login": is_login, "Name": session.get("name", None)}


def render_template_with_user(template_name_ot_list, **kwargs):
    kwargs["title"] = kwargs.get("title", "Главная страница")
    kwargs["header_links"] = kwargs.get("header_links", choose_header_links(
        "authorized") if 'user_id' in session else choose_header_links("not-authorized"))
    return render_template(
        template_name_ot_list,
        data=data(),
        **kwargs
    )
