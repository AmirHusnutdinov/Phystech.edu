from flask import session, redirect

from server.database.use_DataBase import get_all_day_data, get_all_trains
from server.service_files.links import choose_header_links, calendar, main_page
from settings import app
from utils import render_template_with_user


class Calendar:
    @staticmethod
    def show_calendar_page():
        if "user_id" in session:
            user_id = session["user_id"]
            user_in_all_time = get_all_day_data(user_id)
            user_train = get_all_trains(user_id)
            return render_template_with_user(
                "Calendar/calendar.html",
                header_links=choose_header_links("authorized"),
                title="Календарь",
                ca_is_active="active",
                cookies=user_in_all_time,
                cookies2=user_train
            )
        return redirect(main_page)

    @staticmethod
    def show_calendar_page_with_id(us_id):
        if "user_id" in session:
            user_id = us_id
            user_in_all_time = get_all_day_data(user_id)
            user_train = get_all_trains(user_id)
            return render_template_with_user(
                "Calendar/calendar.html",
                header_links=choose_header_links("authorized"),
                title="Календарь",
                ca_is_active="active",
                cookies=user_in_all_time,
                cookies2=user_train
            )
        return redirect(main_page)