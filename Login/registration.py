from flask import render_template, redirect, url_for, flash, session
from flask_mail import Message
from ServiceFiles.links import header_links
from Login.forms import RegistrationForm, ConfirmationForm  # Импортируйте новую форму
from settings import mail  # Импортируйте объект mail из вашего приложения
from DataBase.use_DataBase import database_query
import random


def send_email(subject, recipient, body):
    msg = Message(subject, recipients=[recipient])
    msg.body = body
    mail.send(msg)


class Registration:
    @staticmethod
    def show_registration_page():
        form = RegistrationForm()
        return render_template("Login/registration.html",
                               header_links=header_links,
                               title="Авторизация",
                               form=form)

    @staticmethod
    def process_registration():
        form = RegistrationForm()
        if form.validate_on_submit():
            username = form.username.data  # Сохраните имя пользователя
            email = form.email.data
            password = form.password.data
            password = form.password.data
            count_user = database_query(f"""SELECT COUNT(*) AS user_count 
                          FROM users
                          WHERE email = {email};""")["user_count"][0]
            if count_user > 0:
                flash('Registration failed. Please check your input.', 'danger')
                return redirect(url_for('show_registration_page'))

            # Здесь должна быть ваша логика сохранения пользователя в базе данных
            # Например, сохранение в SQLite или другой БД

            # Генерация кода подтверждения (случайный код)
            confirmation_code = ''.join([str(random.randint(0, 9)) for _ in range(6)])

            # Отправка кода подтверждения на почту
            send_email('Confirmation Code', email, f'Your confirmation code is: {confirmation_code}')
            session["code"] = confirmation_code  # Сохраняем код в сессии
            session["username"] = username
            session["password"] = password
            session["email"] = email

            flash('Registration successful! Please check your email for the confirmation code.', 'success')
            return redirect(url_for('confirm_code'))  # Перенаправляем на страницу подтверждения кода

        flash('Registration failed. Please check your input.', 'danger')
        return redirect(url_for('show_registration_page'))

    @staticmethod
    def show_confirmation_page():
        form = ConfirmationForm()
        return render_template("Login/confirmation.html",
                               header_links=header_links,
                               title="Подтверждение кода",
                               form=form)

    @staticmethod
    def process_confirmation():
        form = ConfirmationForm()
        if form.validate_on_submit():
            entered_code = form.code.data
            if entered_code == session.get("code"):
                flash('Code confirmed successfully!', 'success')
                session["login"] = True
                database_query(f"""INSERT INTO users (username, email, password) 
                                VALUES ({session["username"]}, {session["email"]}, {session["password"]});
                                """)
                session["code"] = None
                session["username"] = None
                session["password"] = None
                session["email"] = None
                return redirect(url_for('main_page'))  # Перенаправьте на нужную страницу после подтверждения
            else:
                flash('Invalid confirmation code. Please try again.', 'danger')
                return redirect(url_for('confirm_code'))  # Перенаправляем обратно на страницу подтверждения

        flash('Please enter the confirmation code.', 'warning')
        return redirect(url_for('confirm_code'))
