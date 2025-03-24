from flask import render_template, session
from server.database.use_DataBase import get_user_data
from server.service_files.links import header_links
from utils import render_template_with_user

lesha_fixed_auth = False # he will do this once...
class Cabinet:
    @staticmethod
    def show_cabinet_page():
        if(not lesha_fixed_auth):
            session['user_id'] = 1
        if 'user_id' in session:
            return render_template_with_user(
                "Login/cabinet.html",
                header_links=header_links,
                title="Кабинет",user = get_user_data(session['user_id']))
        else:
            return "You are not logged in", 401
