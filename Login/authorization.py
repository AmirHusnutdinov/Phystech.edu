from flask import render_template, redirect, url_for, flash, session
from ServiceFiles.links import header_links
from Login.forms import LoginForm
from DataBase.use_DataBase import database_query


class Authorization:
    @staticmethod
    def show_authorization_page():
        form = LoginForm()
        return render_template("Login/authorization.html",
                               header_links=header_links,
                               form=form,
                               title="Авторизация")

    @staticmethod
    def process_login():
        form = LoginForm()
        if form.validate_on_submit():  # Проверка на валидность формы
            username = form.username.data
            password = form.password.data
            password_prov = database_query(f"""SELECT password FROM users WHERE username = {username}""")[0]

            # Здесь должна быть ваша логика проверки пользователя
            if password == password_prov:  # Пример проверки
                session['login'] = True
                session['username'] = username  # Сохраняем пользователя в сессии
                flash('Login successful!', 'success')
                return redirect(url_for('open_main_page'))  # Перенаправление на главную страницу
            else:
                flash('Invalid username or password', 'danger')
                return redirect(url_for('open_authorization_page'))  # Перенаправление обратно на страницу авторизации

        flash('Please fill out the form.', 'danger')
        return redirect(url_for('open_authorization_page'))  # Перенаправление обратно на страницу авторизации

    @staticmethod
    def logout():
        session['Login'] = False
        session.pop('username', None)  # Удаляем пользователя из сессии
        flash('You have been logged out.', 'info')
        return redirect(url_for('open_main_page'))  # Перенаправление на главную страницу
