from datetime import datetime, date

from flask import jsonify
from flask import request, render_template

from server.database.use_DataBase import get_dishes, get_user_data, database_query
from server.service_files.links import *
from settings import app
from utils import render_template_with_user

id = 2

previous_weight = 75


class DayPlan:
    @staticmethod
    def show_day_plan_page():
        dishes = get_dishes()
        user = get_user_data(id)

        return render_template_with_user(
            "DayPlan/day_plan.html",
            header_links=header_links,
            title="Дневной план",
            dishes=dishes,
            cookies=user,
            previous_weight=previous_weight,
        )

    @staticmethod
    def save_day_plan():
        data = request.json
        weight = data.get("weight")
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
        VALUES ({id}, {weight}, {user['height']}, {user['water']}, '{today}', 
                {actual_kbzhu['calories']}, {target_kbzhu['calories']}, 
                {actual_kbzhu['protein']}, {target_kbzhu['protein']}, 
                {actual_kbzhu['fats']}, {target_kbzhu['fats']}, 
                {actual_kbzhu['carbs']}, {target_kbzhu['carbs']})
        ON CONFLICT (id, date) DO UPDATE
        SET weight = {weight}, height = {user['height']}, water = {user['water']}, 
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

    @staticmethod
    def show_add_product_page():
        return render_template_with_user(
            "DayPlan/add_product.html",
            header_links=header_links,
            title="Добавить продукт",
        )


def validate_data(data):
    weight = data.get('weight')
    target_kbzhu = data.get('targetKBZHU')
    actual_kbzhu = data.get('actualKBZHU')
    try:
        if not (0 <= float(weight) <= 500):
            return False

        for kbzhu in [target_kbzhu, actual_kbzhu]:
            if not all(0 <= float(kbzhu[key]) <= (10000 if key == 'calories' else 2000) for key in kbzhu):
                return False

        return True
    except ValueError:
        return False


def validate_date(date_str):
    try:
        submitted_date = datetime.strptime(date_str, "%Y-%m-%d").date()
        return submitted_date == date.today()
    except ValueError:
        return False


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
