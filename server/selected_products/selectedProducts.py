from flask import render_template

from server.service_files.links import header_links


class SelectedProduct:
    @staticmethod
    def show_selected_product_page():
        return render_template(
            "SelectedProducts/selected_product.html",
            header_links=header_links,
            title="Выбор блюда"
        )
