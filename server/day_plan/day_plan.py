from datetime import datetime, date, timezone

from flask import request, render_template, session, jsonify, redirect

from server.cloud.cloud_main import Cloud
from server.database.use_DataBase import (
    get_dishes,
    get_user_data,
    database_query,
    get_day_data,
    get_message_history,
    add_message,
    get_trainer_id,
)
from server.service_files.links import *
from settings import app
from utils import render_template_with_user, debug_print


class DayPlan:
    cloud = Cloud()

    @staticmethod
    def show_day_plan_page():
        if "user_id" in session:
            dishes = get_dishes()
            user = get_user_data(session["user_id"])
            if (user["calories"] == None):
                return redirect(cabinet)
            daily = get_day_data(session["user_id"], date.today())
            print(daily)

            cookies2 = {"water": 0, "carbs": 0,
                        "calories": 0, "protein": 0, "fats": 0}
            if daily:
                cookies2["water"] = daily[0][3]
                cookies2["calories"] = daily[0][5]
                cookies2["protein"] = daily[0][7]
                cookies2["carbs"] = daily[0][11]
                cookies2["fats"] = daily[0][9]

            trainer_id = get_trainer_id(session["user_id"])
            has_trainer = trainer_id != 0

            formatted_messages = []
            if has_trainer:
                user_info = get_user_data(trainer_id)
                messages = get_message_history(session["user_id"], trainer_id)

                formatted_messages = []
                for msg in messages:
                    sender = "received" if msg["id_from"] == trainer_id else "sent"
                    formatted_messages.append(
                        {
                            "type": sender,
                            "content": msg["content"],
                            "time": msg["time"].strftime("%H:%M"),
                            "sender_name": user_info["name"] if sender == "received" else "Вы",
                        }
                    )

            return render_template_with_user(
                "DayPlan/day_plan.html",
                header_links=choose_header_links("authorized"),
                title="Дневной план",
                dishes=dishes,
                cookies=user,
                cookies2=cookies2,
                messages=formatted_messages,
                has_trainer=has_trainer,
                save_day_plan=save_day_plan,
                add_product=add_product,
                add_recipes=add_recipes,
                physical_exercises=physical_exercises

            )
        return redirect(main_page)

    @staticmethod
    def save_food_intake():
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
            if not validate_date(data.get("date")):
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
    def show_add_recipes():
        if "user_id" in session:
            if request.method == "POST":
                dish_name = request.form.get('dish_name')
                total_calories = int(request.form.get('total_calories').split(".")[0])
                total_proteins = float(request.form.get('total_proteins'))
                total_fats = float(request.form.get('total_fats'))
                total_carbs = float(request.form.get('total_carbs'))
                total_weight = request.form.get('total_weight')
                user = session["user_id"]
                coefficient = int(total_weight) / 100
                sql = f""" Insert into dish
                                        (name, owner, calories, proteins, carbohydrates, fats, category)
                                         values ('{dish_name}', {user},
                                        {int(total_calories / coefficient)},
                                        {int(total_proteins / coefficient)},
                                        {int(total_carbs / coefficient)},
                                        {int(total_fats / coefficient)}, 'Castom')
                                        """
                database_query(sql=sql, fetch=False)
            return render_template_with_user(
                "DayPlan/add_recipe.html",
                header_links=choose_header_links("authorized"),
                title="Добавить блюдо",
                dishes=get_dishes()
            )
        return redirect(main_page)

    @staticmethod
    def show_add_product_page():
        if "user_id" in session:
            if request.method == "POST":
                product_name = request.form.get('product-name')
                protein = request.form.get('protein')
                fat = request.form.get('fat')
                carbs = request.form.get('carbs')
                calories = request.form.get('calories')
                user = session["user_id"]
                sql = f""" Insert into dish
                        (name, owner, calories, proteins, carbohydrates, fats, category)
                         values ('{product_name}', {user}, {calories}, {protein}, {carbs}, {fat}, 'Castom')
                        """
                database_query(sql=sql, fetch=False)

            return render_template_with_user(
                "DayPlan/add_product.html",
                header_links=choose_header_links("authorized"),
                title="Добавить продукт",
                add_product=add_product
            )

        return redirect(main_page)

    @staticmethod
    def send_message():
        if "user_id" not in session:
            return jsonify({"status": "error", "message": "Not authorized"}), 401

        data = request.json
        message_text = data.get("message")
        trainer_id = get_trainer_id(session["user_id"])
        if trainer_id == 0:
            return jsonify({"status": "error", "message": "User have no trainer"}), 403
        if not message_text or not trainer_id:
            return jsonify({"status": "error", "message": "Invalid data"}), 400

        try:
            add_message(
                id_from=session["user_id"],
                id_to=trainer_id,
                content=message_text,
            )
            return jsonify(
                {
                    "status": "success",
                    "message": "Message sent",
                    "time": datetime.now().strftime("%H:%M"),
                }
            )
        except Exception as e:
            debug_print('error', e)
            return jsonify({"status": "error", "message": str(e)}), 500

    @staticmethod
    def get_new_messages():
        if "user_id" not in session:
            return jsonify({"status": "error", "message": "Not authorized"}), 401

        trainer_id = get_trainer_id(session["user_id"])
        if trainer_id == 0:
            return jsonify({"status": "error", "message": "User has no trainer"}), 403
        last_update = request.args.get("last_update")

        since_dt = datetime.strptime(last_update, "%Y-%m-%dT%H:%M:%S.%fZ")
        since_sql = since_dt.strftime("%Y-%m-%d %H:%M:%S.%f")
        last_update = since_sql
        # debug_print('LAST TIME UPDATE', last_update)
        if not trainer_id:
            return jsonify({"status": "error", "message": "No trainer assigned"}), 400

        try:
            messages = get_message_history(
                first_id=session["user_id"], second_id=trainer_id, since=last_update
            )
            formatted_messages = []
            for msg in messages:
                if str(msg["id_from"]) == str(trainer_id):  # Только новые сообщения от trainer
                    user_info = get_user_data(trainer_id)
                    formatted_messages.append(
                        {
                            "content": msg["content"],
                            "time": msg["time"].strftime("%H:%M"),
                            "sender_name": user_info["name"],
                        }
                    )
            # debug_print('MESSAGES', formatted_messages)
            current_time = datetime.now(timezone.utc).strftime(
                '%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z'
            return jsonify(
                {
                    "status": "success",
                    "messages": formatted_messages,
                    "last_update": current_time,
                }
            )
        except Exception as e:
            print(e)
            return jsonify({"status": "error", "message": str(e)}), 500


def validate_data(data):
    if "user_id" in session:
        target_kbzhu = data.get("targetKBZHU")
        actual_kbzhu = data.get("actualKBZHU")
        try:
            for kbzhu in [target_kbzhu, actual_kbzhu]:
                if not all(
                        0 <= float(kbzhu[key]) <= (
                                10000 if key == "calories" else 2000)
                        for key in kbzhu
                ):
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

