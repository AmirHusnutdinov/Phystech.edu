from flask import render_template

from ServiceFiles.links import header_links


class DayPlan:
    @staticmethod
    def show_day_plan_page():
        return render_template(
            "DayPlan/day_plan.html",
            header_links=header_links,
            to_is_active="active",
            title="Дневной план"
        )
