from flask import session

from server.database.use_DataBase import get_all_day_data
from server.service_files.links import *
from settings import app
from utils import render_template_with_user


class Calendar:
    @staticmethod
    def show_calendar_page():
        if "user_id" in session:
            user_id = session["user_id"]
            user_in_all_time = get_all_day_data(user_id)
            print(user_in_all_time)
            return render_template_with_user(
                "Calendar/calendar.html",
                header_links=header_links,
                title="Календарь",
                ca_is_active="active",
                cookies=user_in_all_time
            )
        return "You are not logged in", 401

    @staticmethod
    def show_calendar_page_with_id(us_id):
        user_id = us_id
        user_in_all_time = get_all_day_data(user_id)
        print(user_in_all_time)
        return render_template_with_user(
            "Calendar/calendar.html",
            header_links=header_links,
            title="Календарь",
            ca_is_active="active",
            cookies=user_in_all_time
        )

    @staticmethod
    @app.route("/calendar/<int:student_id>")
    def calendar_page(student_id):
        return Calendar.show_calendar_page_with_id(student_id)


@app.route(calendar)
def open_calendar_page():
    return Calendar.show_calendar_page()
