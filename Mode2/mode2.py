from flask import render_template


class Mode2:
    @staticmethod
    def show_mode2_page():
        return render_template("Mode2/mode2.html")
