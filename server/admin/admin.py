from flask import render_template


class Admin:
    @staticmethod
    def show_admin_page():
        return render_template("Admin/admin.html")
