from flask import session, redirect

from server.database.use_DataBase import get_user_data
from server.service_files.links import *
from settings import app
from utils import render_template_with_user


class Cabinet:
    @staticmethod
    def show_cabinet_page():
        if 'user_id' in session:
            return render_template_with_user(
                "Login/cabinet.html",
                header_links=choose_header_links("authorized"),
                title="Кабинет", user=get_user_data(session['user_id']))
        else:
            return redirect(main_page)


@app.route(cabinet, methods=['GET', 'POST'])
def open_cabinet_page():
    return Cabinet.show_cabinet_page()
