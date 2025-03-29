from flask import render_template
from flask import session


def is_login():
    return session["Login"]


def data():
    return {"Login": is_login, "Name": session.get("name", None)}


def render_template_with_user(template_name_ot_list, **kwargs):
    kwargs["title"] = kwargs.get("title", "Главная страница")
    return render_template(
        template_name_ot_list,
        data=data(),
        **kwargs  # Передаем именованные аргументы
    )
