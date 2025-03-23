from server.service_files.links import header_links
from utils import render_template_with_user

class Calendar:
    @staticmethod
    def show_calendar_page():
        return render_template_with_user(
            "Calendar/calendar.html",
            header_links=header_links,
            title="Календарь",
            ca_is_active="active"
            )
