from flask import render_template


class Mode1:
    @staticmethod
    def show_mode1_page():
        return render_template("Mode1/mode1.html")
