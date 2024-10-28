from flask import render_template
from Cloud.cloud_main import urls_files_cloud_list
from ServiceFiles.links import mode1, mode2, header_links

from ServiceFiles.links import mode1, mode2, header_links


class StartPage:
    @staticmethod
    def show_the_main_page():
        return render_template(
            "MainPage/main.html",
            urls_files_cloud_list = urls_files_cloud_list,
            header_links=header_links,
            mode1=mode1,
            mode2=mode2,
            title="Главная страница")
