from flask import redirect, url_for, flash, session
from flask_mail import Message
from settings import mail  # Импортируйте объект mail из вашего приложения
from server.service_files.links import main_page
from server.login.forms import RegistrationForm, ConfirmationForm  # Импортируйте новую форму
from server.database.use_DataBase import database_query
from server.login.utils import hash_password
import random
import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from flask import redirect, url_for, flash, session
from flask import request
from flask import jsonify

from server.database.use_DataBase import database_query
from server.login.forms import RegistrationForm, ConfirmationForm  # Импортируйте новую форму
from server.login.utils import hash_password
from server.service_files.links import *
from settings import *
from settings import app
from utils import render_template_with_user
from flask import request, render_template
from settings import app, host
from server.service_files.links import *


def send_email(subject, recipient, body):
    msg = MIMEMultipart()
    msg['From'] = MAIL_USERNAME
    msg['To'] = recipient
    msg['Subject'] = subject

    msg.attach(MIMEText(body, 'plain'))

    try:
        server = smtplib.SMTP(MAIL_SERVER, MAIL_PORT)
        server.starttls()
        server.login(MAIL_USERNAME, MAIL_PASSWORD)
        server.send_message(msg)
        print("Email sent successfully!")
    except Exception as e:
        print(f"An error occurred: {str(e)}")
    finally:
        server.quit()


class Registration:
    @staticmethod
    def show_registration_page():
        if "user_id" in session:
            return redirect(main_page)

        form = RegistrationForm()
        return render_template_with_user("Login/registration.html",
                                         header_links=choose_header_links("not-authorized"),
                                         title="Авторизация",
                                         form=form)

    @staticmethod
    def process_registration():
        if "user_id" in session:
            return redirect(main_page)
        form = RegistrationForm()
        if form.validate_on_submit():
            name = form.name.data  # Сохраните имя пользователя
            email = form.email.data
            password_of_user = form.password.data
            hash_password(password_of_user)
            count_user = database_query(f"""SELECT COUNT(*) AS user_count 
                          FROM users
                          WHERE email = '{email}';""", True)
            if count_user[0][0] > 0:
                flash('Registration failed. Please check your input.', 'danger')
                return redirect(url_for('show_registration_page'))

            confirmation_code = ''.join([str(random.randint(0, 9)) for _ in range(6)])

            print(confirmation_code)
            send_email('Confirmation Code', email, f'Your confirmation code is: {confirmation_code}')

            session["code"] = confirmation_code  # Сохраняем код в сессии
            session["name"] = name
            session["password"] = password_of_user
            session["email"] = email

            flash('Registration successful! Please check your email for the confirmation code.', 'success')
            return redirect(url_for('confirm_code'))  # Перенаправляем на страницу подтверждения кода

        flash('Registration failed. Please check your input.', 'danger')
        return redirect(url_for('show_registration_page'))

    @staticmethod
    def show_confirmation_page():
        form = ConfirmationForm()
        return render_template_with_user("Login/confirmation.html",
                                         header_links=choose_header_links("not-authorized"),
                                         title="Подтверждение кода",
                                         form=form)

    @staticmethod
    def process_confirmation():
        print(5)
        # if "user_id" in session:
        #     return redirect(main_page)
        form = ConfirmationForm()
        print(form)
        if form.validate_on_submit():
            entered_code = form.code.data
            print(entered_code, session.get("code"))
            if str(entered_code) == str(session.get("code")):
                flash('Code confirmed successfully!', 'success')
                session["login"] = True
                database_query(f"""INSERT INTO users (name, email, password) 
                                VALUES ('{session["name"]}', '{session["email"]}', '{session["password"]}');
                                """, fetch=False)
                session["code"] = None
                session["login"] = True
                session["password"] = None
                session["email"] = None
                return jsonify({
                    'success': True,
                    'redirect_url': url_for('open_main_page')
                })
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
