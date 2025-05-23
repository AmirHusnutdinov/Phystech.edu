import os
from datetime import timedelta

from apscheduler.schedulers.background import BackgroundScheduler
from flask import request, url_for
from flask import session, redirect, render_template

from server.admin.admin import Admin
from server.calendar.calendar import Calendar
from server.database.use_DataBase import database_query, get_user_data
from server.day_plan.day_plan import DayPlan
from server.food_controler.food_controller import food_blueprint, delete_old_diets
from server.login.authorization import Authorization
from server.login.cabinet import Cabinet
from server.login.process_registration import ProcessRegistration
from server.login.registration import Registration
from server.main_page.main_page import StartPage
from server.news.news import News
from server.selected_products.selectedProducts import SelectedProduct
from server.service_files.links import *;
from server.trainer.trainer_students import Students
from settings import app

app = app

app.secret_key = os.urandom(24)
app.register_blueprint(food_blueprint)

scheduler = BackgroundScheduler()
scheduler.add_job(delete_old_diets, "cron", hour=0, minute=0)
scheduler.start()


@app.route(admin)
def open_admin_page():
    return Admin.show_admin_page()


@app.route("/calendar/<int:student_id>")
def calendar_page(student_id):
    return Calendar.show_calendar_page_with_id(student_id)


@app.route(calendar)
def open_calendar_page():
    return Calendar.show_calendar_page()


@app.route(add_product, methods=['GET', 'POST'])
def open_add_product():
    if "user_id" in session:
        return DayPlan.show_add_product_page()
    return redirect(main_page)


@app.route(add_recipes, methods=['GET', 'POST'])
def open_add_recipes():
    if "user_id" in session:
        return DayPlan.show_add_recipes()
    return redirect(main_page)


@app.route(day_plan)
def open_day_plan_page():
    return DayPlan.show_day_plan_page()


@app.route(save_day_plan, methods=["POST"])
def save_data():
    if "user_id" in session:
        return DayPlan.save_food_intake()
    return redirect(main_page)


exercise_met = {
    "Ходьба": 3.5,
    "Бег": 8.0,
    "Езда на велосипеде": 8.0,
    "Эллипсоид": 6.0,
    "Эргометр": 6.0,
    "Степпер": 7.0,
    "HIIT": 9.0,
    "Пеший туризм": 5.0,
    "Йога": 2.5,  # Йога
    "Функционально-силовая тренировка": 6.0,
    "Танцы": 5.0,
    "Плавание": 6.0
}

exercise_images = {
    "Ходьба": "exercises/exercise_walking.png",
    "Бег": "exercises/exercise_running.png",
    "Езда на велосипеде": "exercises/exercise_cycling.png",
    "Эллипсоид": "exercises/exercise_ellipsoid.png",
    "Эргометр": "exercises/exercise_ergometer.png",
    "Степпер": "exercises/exercise_stepper.png",
    "HIIT": "exercises/exercise_hiit.png",
    "Пеший туризм": "exercises/exercise_hiking.png",
    "Йога": "exercises/exercise_yoga.png",
    "Функционально-силовая тренировка": "exercises/exercise_strength.png",
    "Танцы": "exercises/exercise_dance.png",
    "Плавание": "exercises/exercise_swimming.png",
}


@app.route(physical_exercises, methods=["GET", "POST"])
def open_physical_exercises_page():
    if "user_id" in session:
        user = get_user_data(session["user_id"])

        if request.method == "POST":
            data = request.get_json()
            exercise_name = data.get('exercise')
            date_str = data.get('date')
            duration_seconds = data.get('duration')

            calories = float(user["weight"]) * exercise_met[exercise_name] * duration_seconds / 3600
            td = timedelta(seconds=duration_seconds)
            hours, remainder = divmod(td.seconds, 3600)
            minutes, seconds = divmod(remainder, 60)
            total_duration = f"{hours:02d}:{minutes:02d}:{seconds:02d}"

            database_query(f"""Insert into train
            (id, date, calories, type, time) values (
                {user["id"]},
                '{date_str.split("T")[0]}',
                {calories},
                '{exercise_name}',
                '{total_duration}')""", fetch=False)

            return redirect(physical_exercises)

        workout_history = database_query(f"""Select * from train 
        where id={user["id"]} and date >= CURRENT_DATE - INTERVAL '7 days'""", fetch=True)
        total_seconds = 0
        total_calories = 0

        for i in range(len(workout_history)):
            workout_history[i] = list(workout_history[i])
            workout_history[i].append(exercise_images[workout_history[i][3]])
            total_calories += workout_history[i][2]
            h, m, s = map(int, str(workout_history[i][4]).split(':'))
            total_seconds += h * 3600 + m * 60 + s

        hours = total_seconds // 3600
        minutes = (total_seconds % 3600) // 60
        seconds = total_seconds % 60
        total_time = f"{hours:02d}:{minutes:02d}:{seconds:02d}"
        images = DayPlan.cloud.get_folder('exercises')
        return render_template(
            "DayPlan/physical_exercises.html",
            header_links=choose_header_links("authorized"),
            title="Трекер Физических Упражнений",
            day_plan=day_plan,
            images=images,
            workout_history=workout_history,
            len_workout_history=len(workout_history),
            total_time=total_time,
            total_calories=total_calories
        )
    return redirect(main_page)


@app.route("/day_plan/get_new_messages", methods=["GET"])
def get_chat_messages_route():
    return DayPlan.get_new_messages()


@app.route("/day_plan/send_message", methods=["POST"])
def send_message_route():
    return DayPlan.send_message()


@app.route(authorization, methods=['GET', 'POST'])
def open_authorization_page():
    return Authorization.show_authorization_page()


@app.route(process_login, methods=['POST'])
def process_login():
    return Authorization.process_login()


@app.route(logout)
def logout():
    return Authorization.logout()


@app.route(cabinet, methods=["GET", "POST"])
def open_cabinet_page():
    return Cabinet.show_cabinet_page()


@app.route(cabinet + "/update_profile", methods=["POST"])
def update_profile():
    return Cabinet.update_profile()


@app.route(cabinet + "/update_nutrition", methods=["POST"])
def update_nutrition():
    return Cabinet.update_nutrition()


@app.route(cabinet + "/submit_trainer_application", methods=["POST"])
def submit_trainer_application():
    return Cabinet.submit_trainer_application()


@app.route(cabinet + "/request_trainer", methods=["POST"])
def request_trainer():
    return Cabinet.request_trainer()


@app.route(cabinet + "/approve_request/<int:request_id>", methods=["POST"])
def approve_request(request_id):
    return Cabinet.approve_request(request_id)


@app.route(cabinet + "/reject_request/<int:request_id>", methods=["POST"])
def reject_request(request_id):
    return Cabinet.reject_request(request_id)


@app.route(process_registration, methods=["GET"])
def show_ProcessRegistration_page():
    return ProcessRegistration.show_ProcessRegistration_page()


@app.route(process_registration + "/submit", methods=["POST"])
def submit_registration():
    return ProcessRegistration.submit()


@app.route(registration, methods=["GET", "POST"])
def show_registration_page():
    return Registration.show_registration_page()


@app.route(process_registration, methods=["POST"])
def process_registration():
    return Registration.process_registration()


@app.route(confirm_code, methods=["GET", "POST"])
def confirm_code():
    if request.method == "POST":
        return Registration.process_confirmation()
    return Registration.show_confirmation_page()


@app.route(main_page)
def open_main_page():
    return StartPage.show_the_main_page()


@app.route(all_news)
def open_all_news_page():
    return News.show_all_news_page()


@app.route(one_news)
def open_one_news_page(news_id):
    return News.show_one_news_page(news_id)


@app.route(make_news, methods=['GET'])
def open_make_news_page():
    return News.show_make_news()


@app.route(save_news, methods=['POST'])
def handle_make_news():
    return News.handle_make_news()


@app.route('/news/<int:news_id>/edit', methods=['GET'])
def edit_news_page(news_id):
    return News.show_make_news(news_id)


@app.route('/news/<int:news_id>/delete', methods=['POST'])
def delete_news_page(news_id):
    return News.handle_delete_news(news_id)


@app.route(selected_products)
def open_selected_products_page():
    return SelectedProduct.show_selected_product_page()


@app.route(all_students)
def open_all_students_page():
    return Students.show_students_page()


@app.route(student, methods=["GET", "POST"])
def open_students_page(student_id):
    return Students.show_one_student_page(student_id)


@app.route("/send_message", methods=["POST"])
def send_message():
    return Students.send_message()


@app.route("/get_new_messages/<student_id>")
def get_new_messages(student_id):
    pass
    return Students.get_new_messages(student_id)


port = int(os.environ.get("PORT", 8000))
app.run(host="0.0.0.0", port=port, debug=False)
