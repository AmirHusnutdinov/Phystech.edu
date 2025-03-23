from flask import render_template
from server.database.use_DataBase import get_user_data
from server.service_files.links import header_links
from utils import render_template_with_user

id = 2
class Cabinet:
    @staticmethod
    def show_cabinet_page():
        return render_template_with_user(
            "Login/cabinet.html",
            header_links=header_links,
            title="Кабинет",user = get_user_data(id))
