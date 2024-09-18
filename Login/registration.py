from flask import render_template


class Registration:
    @staticmethod
    def show_registration_page():
        return render_template("Login/registration.html")
