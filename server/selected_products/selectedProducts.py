from server.service_files.links import header_links
from utils import render_template_with_user
from flask import request, render_template
from settings import app, host
from server.service_files.links import *

class SelectedProduct:
    @staticmethod
    def show_selected_product_page():
        return render_template_with_user(
            "SelectedProducts/selected_product.html",
            header_links=header_links,
            title="Выбор блюда"
        )


@app.route(selected_products)
def open_selected_products_page():
    return SelectedProduct.show_selected_product_page()

