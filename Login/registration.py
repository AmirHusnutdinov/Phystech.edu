from flask import render_template, redirect, url_for, flash, session
from flask_mail import Message
from ServiceFiles.links import header_links
from Login.forms import RegistrationForm, ConfirmationForm  # Импортируйте новую форму
from settings import mail  # Импортируйте объект mail из вашего приложения
import celery

@celery.task
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

            # Здесь должна быть ваша логика сохранения пользователя в базе данных
            # Например, сохранение в SQLite или другой БД

            # Генерация кода подтверждения (например, случайный код)
            confirmation_code = "123456"  # Замените на реальную генерацию кода

            # Отправка кода подтверждения на почту
            send_email.delay('Confirmation Code', email, f'Your confirmation code is: {confirmation_code}')
            session["code"] = confirmation_code  # Сохраняем код в сессии
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
                # Здесь можно добавить логику для дальнейших действий (например, вход пользователя)
                return redirect(url_for('some_next_page'))  # Перенаправьте на нужную страницу после подтверждения
            else:
                flash('Invalid confirmation code. Please try again.', 'danger')
                return redirect(url_for('confirm_code'))  # Перенаправляем обратно на страницу подтверждения

        flash('Please enter the confirmation code.', 'warning')
        return redirect(url_for('confirm_code'))
