from server.service_files.links import *
from settings import app
from utils import render_template_with_user
from flask import redirect, session
from server.database.use_DataBase import get_user_data


class SelectedProduct:
    @staticmethod
    def show_selected_product_page():
        if "user_id" in session:
            user = get_user_data(session["user_id"])
            if not user["is_activated"]:
                return redirect(process_registration)
            return render_template_with_user(
                "SelectedProducts/selected_product.html",
                header_links=choose_header_links("authorized"),
                title="Выбор блюда",
            )
        return redirect(main_page)



