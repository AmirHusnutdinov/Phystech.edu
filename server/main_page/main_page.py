from server.cloud.cloud_main import Cloud
from server.login.forms import RegistrationForm, LoginForm
from server.service_files.links import *
from settings import app
from utils import render_template_with_user
from flask import session


class StartPage:
    cloud_client = Cloud()

    @staticmethod
    def show_the_main_page():
        if "user_id" in session:
            header_links = choose_header_links("authorized")
        else:
            header_links = choose_header_links("not-authorized")
        
        images = StartPage.cloud_client.get_folder("images/")
        form = LoginForm()
        RegistrationForm()

        return render_template_with_user(
            "MainPage/main.html",
            title="Главная страница",
            images=images,
            header_links=header_links,
            form=form,
            form_registration=form
        )


