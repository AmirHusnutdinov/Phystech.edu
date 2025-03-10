from utils import render_template_with_user

class Admin:
    @staticmethod
    def show_admin_page():
        return render_template_with_user("Admin/admin.html")
