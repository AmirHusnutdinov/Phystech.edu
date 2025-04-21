from datetime import datetime, date

from flask import request, render_template, session, jsonify, redirect

from server.database.use_DataBase import get_dishes, get_user_data, database_query, get_day_data
from server.service_files.links import *
from settings import app
from utils import render_template_with_user




class DayPlan:
    @staticmethod
    def show_day_plan_page():
        if "user_id" in session:
            dishes = get_dishes()
            user = get_user_data(session["user_id"])
            daily = get_day_data(session["user_id"], date.today())
            print(date.today())
            print(daily)
            print(user)
            cookies2 = {"water": 0, "carbs": 0, "calories": 0, "protein": 0, "fats": 0}
            if (daily):
                cookies2["water"] = daily[0][3]
                cookies2["calories"] = daily[0][5]
                cookies2["protein"] = daily[0][7]
                cookies2["carbs"] = daily[0][9]
                cookies2["fats"] = daily[0][11]


            return render_template_with_user(
                "DayPlan/day_plan.html",
                header_links=choose_header_links("authorized"),
                title="Дневной план",
                dishes=dishes,
                cookies=user,
                cookies2=cookies2
            )
        return redirect(main_page)

    @staticmethod
    def save_day_plan():
        if "user_id" in session:
            id = session["user_id"]
            data = request.json
            print(data)
            weight = data.get("weight")
            water = data.get("water")
            target_kbzhu = data.get("targetKBZHU")
            actual_kbzhu = data.get("actualKBZHU")
            today = data.get("date")

            if not validate_data(data):
                return jsonify({"message": "Incorrect Data"}), 400
            if not validate_date(data.get('date')):
                return jsonify({"message": "wrong date"}), 400
            user = get_user_data(id)
            sql = f"""
            INSERT INTO user_daily_metrics (id, weight, height, water, date, calories, calories_plan, proteins,
             proteins_plan, fats, fats_plan, carbs, carbs_plan)
            VALUES ({id}, {weight}, {user['height']}, {water}, '{today}', 
                    {actual_kbzhu['calories']}, {target_kbzhu['calories']}, 
                    {actual_kbzhu['protein']}, {target_kbzhu['protein']}, 
                    {actual_kbzhu['fats']}, {target_kbzhu['fats']}, 
                    {actual_kbzhu['carbs']}, {target_kbzhu['carbs']})
            ON CONFLICT (id, date) DO UPDATE
            SET weight = {weight}, height = {user['height']}, water = {water}, 
                calories = {actual_kbzhu['calories']}, calories_plan = {target_kbzhu['calories']}, 
                proteins = {actual_kbzhu['protein']}, proteins_plan = {target_kbzhu['protein']}, 
                fats = {actual_kbzhu['fats']}, fats_plan = {target_kbzhu['fats']}, 
                carbs = {actual_kbzhu['carbs']}, carbs_plan = {target_kbzhu['carbs']};
            """

            print(
                f"Received data: Weight: {weight}, Target KBZHU: {target_kbzhu}, Actual KBZHU: {actual_kbzhu}"
            )

            try:
                database_query(sql)
            except Exception as ex:
                print(f"Error while saving day plan: {ex}")
                return jsonify({"message": "Error while saving day plan"}), 500

            return jsonify({"message": "Data saved successfully"}), 200
        return redirect(main_page)

    @staticmethod
    def show_add_product_page():
        if "user_id" in session:
            return render_template_with_user(
                "DayPlan/add_product.html",
                header_links=choose_header_links("authorized"),
                title="Добавить продукт",
            )
        return redirect(main_page)


def validate_data(data):
    if "user_id" in session:
        target_kbzhu = data.get('targetKBZHU')
        actual_kbzhu = data.get('actualKBZHU')
        try:
            for kbzhu in [target_kbzhu, actual_kbzhu]:
                if not all(0 <= float(kbzhu[key]) <= (10000 if key == 'calories' else 2000) for key in kbzhu):
                    return False

            return True
        except ValueError:
            return False
    return redirect(main_page)


def validate_date(date_str):
    if "user_id" in session:
        try:
            submitted_date = datetime.strptime(date_str, "%Y-%m-%d").date()
            return submitted_date == date.today()
        except ValueError:
            return False
    return redirect(main_page)


@app.route(day_plan)
def open_day_plan_page():
    return DayPlan.show_day_plan_page()


@app.route(save_day_plan, methods=['POST'])
def save_data():
    return DayPlan.save_day_plan()


@app.route(add_product)
def open_add_product():
    return DayPlan.show_add_product_page()


@app.route("/physical_exercises")
def open_physical_exercises_page():
    return render_template("DayPlan/physical_exercises.html")
