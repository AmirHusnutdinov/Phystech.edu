from flask import render_template, redirect, url_for, flash

from Login.forms import RegistrationForm


class Registration:
    @staticmethod
    def show_registration_page():
        form = RegistrationForm()
        return render_template("Login/registration.html", form=form)

    @staticmethod
    def process_registration():
        form = RegistrationForm()
        if form.validate_on_submit():
            form.username.data
            email = form.email.data
            password = form.password.data


            # Здесь должна быть ваша логика сохранения пользователя в базе данных
            # Например, сохранение в SQLite или другой БД

            flash('Registration successful! You can now log in.', 'success')
            return redirect(url_for('open_authorization_page'))

        flash('Registration failed. Please check your input.', 'danger')
        return redirect(url_for('show_registration_page'))
