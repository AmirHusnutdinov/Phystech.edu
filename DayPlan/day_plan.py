from flask import render_template
from ServiceFiles.links import header_links


class DayPlan:
    @staticmethod
    def show_day_plan_page():
        return render_template(
            "DayPlan/day_plan.html",
            header_links=header_links,
            title="Дневной план"
        )

    @staticmethod
    def show_add_product_page():
        return render_template(
            "DayPlan/add_product.html",
            header_links=header_links,
            title="Добавить продукт"
        )
