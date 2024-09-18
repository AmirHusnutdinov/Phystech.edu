from flask import render_template


class SelectedProduct:
    @staticmethod
    def show_selected_product_page():
        return render_template("SelectedProducts/selected_product.html")
