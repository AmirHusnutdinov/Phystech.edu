from flask import render_template

from server.service_files.links import header_links


class Calendar:
    @staticmethod
    def show_calendar_page():
        return render_template(
            "Calendar/calendar.html",
            header_links=header_links,
            title="Календарь",
            ca_is_active="active"
            )
