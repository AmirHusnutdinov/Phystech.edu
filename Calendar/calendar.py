from flask import render_template


class Calendar:
    @staticmethod
    def show_calendar_page():
        return render_template("Calendar/calendar.html")
