from utils import render_template_with_user
from settings import app
from server.service_files.links import *


class Admin:
    @staticmethod
    def show_admin_page():
        return render_template_with_user("Admin/admin.html")


