from flask import render_template, session, request
from datetime import datetime, date
from server.database.use_DataBase import get_all_day_data
from settings import app
from server.service_files.links import header_links


class Calendar:
    @staticmethod
    def show_calendar_page():
        if "user_id" in session:
            user_id = session["user_id"][0][0]
            user_in_all_time = get_all_day_data(user_id)
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
            user_in_all_time = get_all_day_data(user_id)
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
