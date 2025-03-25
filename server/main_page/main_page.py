from flask import render_template
from server.cloud.cloud_main import urls_files_cloud_list
from server.service_files.links import header_links
import utils
from utils import render_template_with_user
from settings import app, host
from server.service_files.links import *

class StartPage:
    @staticmethod
    def show_the_main_page():

        return render_template_with_user(
            "MainPage/main.html",
            title="Главная страница",
            main_image=urls_files_cloud_list['images/4k-mountain.jpg'],
            urls_files_cloud_list = urls_files_cloud_list,
            header_links=header_links,
            )

@app.route(main_page)
def open_main_page():
    return StartPage.show_the_main_page()