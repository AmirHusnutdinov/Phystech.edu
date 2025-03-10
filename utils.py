from flask import session
from flask import render_template

def is_login():
    return session["Login"]

def data():
    return {"Login": is_login, "Name": session.get("name", None)}

def render_template_with_user(template_name_ot_list, *args, **kwargs):
    kwargs["title"] = kwargs.get("title", "Главная страница")
    return render_template(
        template_name_ot_list,
        data=data(),
        *args,  # Передаем неименованные аргументы
        **kwargs  # Передаем именованные аргументы
    )
