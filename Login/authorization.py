from flask import redirect, url_for, flash, session
from ServiceFiles.links import header_links
from Login.forms import LoginForm, RegistrationForm
from DataBase.use_DataBase import database_query
import utils
from utils import render_template_with_user


class Authorization:
    @staticmethod
    def show_authorization_page():
        form = LoginForm()
        form_registration = RegistrationForm()
        return render_template_with_user("Login/authorization.html",
                               header_links=header_links,
                               form=form,
                              form_registration = form,
                               title="Авторизация")

    @staticmethod
    def process_login():
        form = LoginForm()
        if form.validate_on_submit():  # Проверка на валидность формы
            name = form.name.data
            password = form.password.data
            password_prov = database_query(f"""SELECT password FROM "User" WHERE email = '{name}';""")
            # Здесь должна быть ваша логика проверки пользователя
            if password_prov and password == password_prov[0][0]:  # Пример проверки
                session['login'] = True
                session['email'] = name  # Сохраняем пользователя в сессии
                flash('Login successful!', 'success')
                return redirect(url_for('open_main_page'))  # Перенаправление на главную страницу
            else:
                flash('Invalid name or password', 'danger')
                return redirect(url_for('open_authorization_page'))  # Перенаправление обратно на страницу авторизации

        flash('Please fill out the form.', 'danger')
        return redirect(url_for('open_authorization_page'))  # Перенаправление обратно на страницу авторизации

    @staticmethod
    def logout():
        session['Login'] = False
        session.pop('name', None)  # Удаляем пользователя из сессии
        flash('You have been logged out.', 'info')
        return redirect(url_for('open_main_page'))  # Перенаправление на главную страницу
