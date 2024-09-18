from flask import render_template


class StartPage:
    @staticmethod
    def show_the_main_page():
        return render_template("MainPage/main.html")
