from flask import redirect, url_for, flash, session
from flask_mail import Message
from settings import mail  # Импортируйте объект mail из вашего приложения
from server.service_files.links import header_links, main_page
from server.login.forms import RegistrationForm, ConfirmationForm  # Импортируйте новую форму
from server.database.use_DataBase import database_query
from server.login.utils import hash_password
import random
import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from settings import *
from utils import render_template_with_user
from flask import request, render_template
from settings import app, host
from server.service_files.links import *

def send_email(subject, recipient, body):
    # Создание сообщения
    msg = MIMEMultipart()
    msg['From'] = MAIL_USERNAME
    msg['To'] = recipient
    msg['Subject'] = subject

    # Добавление текста в сообщение
    msg.attach(MIMEText(body, 'plain'))

    try:
        # Подключение к SMTP серверу и отправка письма
        server = smtplib.SMTP(MAIL_SERVER, MAIL_PORT)
        server.starttls()  # Защита соединения с помощью TLS
        server.login(MAIL_USERNAME, MAIL_PASSWORD)  # Логин на сервере
        server.send_message(msg)  # Отправка сообщения
        print("Email sent successfully!")
    except Exception as e:
        print(f"An error occurred: {str(e)}")
    finally:
        server.quit()  # Закрытие соединения


class Registration:
    @staticmethod
    def show_registration_page():
        form = RegistrationForm()
        return render_template_with_user("Login/registration.html",
                               header_links=header_links,
                               title="Авторизация",
                               form=form)

    @staticmethod
    def process_registration():
        form = RegistrationForm()
        if form.validate_on_submit():
            name = form.name.data  # Сохраните имя пользователя
            email = form.email.data
            password = form.password.data
            hash_password(password)
            count_user = database_query(f"""SELECT COUNT(*) AS user_count 
                          FROM "User"
                          WHERE email = '{email}';""")
            # print(count_user)
            if count_user[0][0]> 0:
                flash('Registration failed. Please check your input.', 'danger')
                return redirect(url_for('show_registration_page'))

            # Здесь должна быть ваша логика сохранения пользователя в базе данных
            # Например, сохранение в SQLite или другой БД

            # Генерация кода подтверждения (случайный код)
            confirmation_code = ''.join([str(random.randint(0, 9)) for _ in range(6)])

            # Отправка кода подтверждения на почту
            print(confirmation_code)
            send_email('Confirmation Code', email, f'Your confirmation code is: {confirmation_code}')

            session["code"] = confirmation_code  # Сохраняем код в сессии
            session["name"] = name
            session["password"] = password
            session["email"] = email

            flash('Registration successful! Please check your email for the confirmation code.', 'success')
            return redirect(url_for('confirm_code'))  # Перенаправляем на страницу подтверждения кода

        flash('Registration failed. Please check your input.', 'danger')
        return redirect(url_for('show_registration_page'))

    @staticmethod
    def show_confirmation_page():
        form = ConfirmationForm()
        return render_template_with_user("Login/confirmation.html",
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
                database_query(f"""INSERT INTO \"User\" (name, email, password) 
                                VALUES ('{session["name"]}', '{session["email"]}', '{session["password"]}');
                                """, Fetch=True)
                session["code"] = None
                session["login"] = True
                session["password"] = None
                session["email"] = None
                return redirect(main_page)  # Перенаправьте на нужную страницу после подтверждения
            else:
                flash('Invalid confirmation code. Please try again.', 'danger')
                return redirect(url_for('confirm_code'))  # Перенаправляем обратно на страницу подтверждения

        flash('Please enter the confirmation code.', 'warning')
        return redirect(url_for('confirm_code'))

@app.route(registration, methods=['GET', 'POST'])
def show_registration_page():
    return Registration.show_registration_page()


@app.route(process_registration, methods=['POST'])
def process_registration():
    return Registration.process_registration()


@app.route(confirm_code, methods=['GET', 'POST'])
def confirm_code():
    if request.method == 'POST':
        return Registration.process_confirmation()
    return Registration.show_confirmation_page()
