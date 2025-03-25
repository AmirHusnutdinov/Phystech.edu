from flask import render_template
from Cloud.cloud_main import urls_files_cloud_list
from ServiceFiles.links import header_links
from ServiceFiles.links import *
from settings import app, host

class StartPage:
    @staticmethod
    def show_the_main_page():

        return render_template(
            "MainPage/main.html",
            main_image=urls_files_cloud_list['images/4k-mountain.jpg'],
            urls_files_cloud_list = urls_files_cloud_list,
            header_links=header_links,
            title="Главная страница")

@app.route(main_page)
def open_main_page():
    return StartPage.show_the_main_page()


