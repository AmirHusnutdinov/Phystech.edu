from flask import render_template
from ServiceFiles.links import *
from settings import app, host

from ServiceFiles.links import header_links


class SelectedProduct:
    @staticmethod
    def show_selected_product_page():
        return render_template(
            "SelectedProducts/selected_product.html",
            header_links=header_links,
            title="Выбор блюда"
        )


@app.route(selected_products)
def open_selected_products_page():
    return SelectedProduct.show_selected_product_page()
