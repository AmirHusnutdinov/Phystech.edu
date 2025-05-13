from flask import redirect, url_for, flash, session

from server.database.use_DataBase import database_query
from server.login.forms import LoginForm, RegistrationForm
from server.service_files.links import *
from server.login.utils import check_password
from settings import app
from utils import render_template_with_user


class Authorization:
    @staticmethod
    def show_authorization_page():
        if "user_id" in session:
            return redirect(main_page)

        form = LoginForm()
        RegistrationForm()
        return render_template_with_user("Login/authorization.html",
                                         header_links=choose_header_links("not-authorized"),
                                         form=form,
                                         form_registration=form,
                                         title="Авторизация")

    @staticmethod
    def process_login():
        if "user_id" in session:
            return redirect(main_page)

        form = LoginForm()
        if form.validate_on_submit():
            name = form.name.data
            password = form.password.data
            password_prov = database_query(f"""SELECT password FROM "User" WHERE email = '{name}';""", True)
            if password_prov:
               hased_password = password_prov[0][0]
            user_id = database_query(f"""SELECT id FROM "User" WHERE email = '{name}';""", True)
            if password_prov and check_password(hased_password, password):  # Пример проверки
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
        if "user_id" in session:
            session['Login'] = False
            session.pop('email', None)
            session.pop('user_id', None)  # Удаляем пользователя из сессии
            flash('You have been logged out.', 'info')
            return redirect(url_for('open_main_page'))  # Перенаправление на главную страницу
        return redirect(main_page)


@app.route(authorization, methods=['GET', 'POST'])
def open_authorization_page():
    return Authorization.show_authorization_page()


@app.route(process_login, methods=['POST'])
def process_login():
    return Authorization.process_login()


@app.route(logout)
def logout():
    return Authorization.logout()
