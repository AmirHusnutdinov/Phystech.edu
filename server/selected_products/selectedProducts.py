from server.service_files.links import *
from settings import app
from utils import render_template_with_user


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
