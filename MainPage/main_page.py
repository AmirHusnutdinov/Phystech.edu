from flask import render_template

from ServiceFiles.links import mode1, mode2, header_links


class StartPage:
    @staticmethod
    def show_the_main_page():
        return render_template(
            "MainPage/main.html",
            header_links=header_links,
            mode1=mode1,
            mode2=mode2,
            title="Главная страница")
