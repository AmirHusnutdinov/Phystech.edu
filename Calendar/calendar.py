from flask import render_template, session, request
from datetime import datetime, date

from ServiceFiles.links import header_links
import DataBase
from settings import app


class Calendar:
    @staticmethod
    def show_calendar_page():
        if "user_id" in session:
            user_id = session["user_id"][0][0]
            user_in_all_time = DataBase.use_DataBase.get_all_day_data(user_id)
            print(user_in_all_time)
            return render_template(
                "Calendar/calendar.html",
                header_links=header_links,
                title="Календарь",
                ca_is_active="active",
                cookies=user_in_all_time
            )
        return "You are not logged in", 401

    def show_calendar_page_with_id(us_id):
            user_id = us_id
            user_in_all_time = DataBase.use_DataBase.get_all_day_data(user_id)
            print(user_in_all_time)
            return render_template(
                "Calendar/calendar.html",
                header_links=header_links,
                title="Календарь",
                ca_is_active="active",
                cookies=user_in_all_time
            )
    @app.route("/calendar/<int:student_id>")
    def calendar_page(student_id):
        return Calendar.show_calendar_page_with_id(student_id)
