from flask import render_template
from ServiceFiles.links import *
from settings import app, host


class Admin:
    @staticmethod
    def show_admin_page():
        return render_template("Admin/admin.html")

@app.route(admin)
def open_admin_page():
    return Admin.show_admin_page()
