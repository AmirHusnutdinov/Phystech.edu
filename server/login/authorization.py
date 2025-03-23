from flask import render_template, redirect, url_for, flash, session
from server.service_files.links import header_links
from server.login.forms import LoginForm
from server.database.use_DataBase import database_query
import bcrypt


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
            name = form.name.data
            password = form.password.data.encode('utf-8')
            password_prov = database_query(f"""SELECT password FROM "User" WHERE email = '{name}';""")
            if password_prov:
                stored_hash = password_prov[0][0].encode('utf-8')

                if bcrypt.checkpw(password, stored_hash):
                    session['login'] = True
                    session['email'] = name 
                    flash('Login successful!', 'success')
                    return redirect(url_for('open_main_page'))
                
                else:
                    flash('Invalid name or password', 'danger')
                    return redirect(url_for('open_authorization_page'))

            else:
                flash('Invalid name or password', 'danger')
                return redirect(url_for('open_authorization_page'))

        flash('Please fill out the form.', 'danger')
        return redirect(url_for('open_authorization_page'))

    @staticmethod
    def logout():
        session['Login'] = False
        session.pop('name', None)  # Удаляем пользователя из сессии
        flash('You have been logged out.', 'info')
        return redirect(url_for('open_main_page'))  # Перенаправление на главную страницу
