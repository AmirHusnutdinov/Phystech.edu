from flask import render_template

from ServiceFiles.links import header_links


class Cabinet:
    @staticmethod
    def show_cabinet_page():
        return render_template(
            "Login/cabinet.html",
            header_links=header_links,
            title="Кабинет")
