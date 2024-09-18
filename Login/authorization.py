from flask import render_template


class Authorization:
    @staticmethod
    def show_authorization_page():
        return render_template("Login/authorization.html")
