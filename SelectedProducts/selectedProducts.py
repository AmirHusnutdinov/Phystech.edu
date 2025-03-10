

from ServiceFiles.links import header_links
from utils import render_template_with_user

class SelectedProduct:
    @staticmethod
    def show_selected_product_page():
        return render_template_with_user(
            "SelectedProducts/selected_product.html",
            header_links=header_links,
            title="Выбор блюда"
        )
