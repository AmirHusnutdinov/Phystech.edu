from flask import render_template, redirect, url_for, flash, session
from server.service_files.links import header_links
from server.login.forms import LoginForm
from server.database.use_DataBase import database_query
import bcrypt
from server.service_files.links import header_links
from server.login.forms import LoginForm, RegistrationForm
from server.database.use_DataBase import database_query
import utils
from utils import render_template_with_user
from flask import request, render_template
from settings import app, host
from server.service_files.links import *


class Authorization:
    @staticmethod
    def show_authorization_page():
        form = LoginForm()
        form_registration = RegistrationForm()
        return render_template_with_user("Login/authorization.html",
                                         header_links=header_links,
                                         form=form,
                                         form_registration=form,
                                         title="Авторизация")

    @staticmethod
    def process_login():
        form = LoginForm()
        if form.validate_on_submit():
            name = form.name.data
            password = form.password.data
            password_prov = database_query(f"""SELECT password FROM "User" WHERE email = '{name}';""", True)
            user_id = database_query(f"""SELECT id FROM "User" WHERE email = '{name}';""", True)
            if password_prov and password == password_prov[0][0]:  # Пример проверки
                session['Login'] = True
                session['email'] = name
                session["user_id"] = user_id[0][0]
                flash('Login successful!', 'success')
                return redirect(url_for('open_main_page'))
            else:
                flash('Invalid name or password', 'danger')
                return redirect(url_for('open_authorization_page'))

        flash('Please fill out the form.', 'danger')
        return redirect(url_for('open_authorization_page'))

    @staticmethod
    def logout():
        session['Login'] = False
        session.pop('email', None)
        session.pop('user_id', None)  # Удаляем пользователя из сессии
        flash('You have been logged out.', 'info')
        return redirect(url_for('open_main_page'))  # Перенаправление на главную страницу


@app.route(authorization, methods=['GET', 'POST'])
def open_authorization_page():
    return Authorization.show_authorization_page()


@app.route(process_login, methods=['POST'])
def process_login():
    return Authorization.process_login()


@app.route(logout)
def logout():
    return Authorization.logout()
