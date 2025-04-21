from server.service_files.links import *
from settings import app
from utils import render_template_with_user
from flask import redirect, session


class SelectedProduct:
    @staticmethod
    def show_selected_product_page():
        if "user_id" in session:
            return render_template_with_user(
                "SelectedProducts/selected_product.html",
                header_links=choose_header_links("authorized"),
                title="Выбор блюда"
            )
        return redirect(main_page)


@app.route(selected_products)
def open_selected_products_page():
    return SelectedProduct.show_selected_product_page()
