# The `DayPlan` class in the Python code provides methods to display a day plan page with dishes, save
# the day plan, and show an add product page.
from flask import render_template, request, jsonify
from ServiceFiles.links import header_links
from DataBase.use_DataBase import get_dishes, get_user_data

id = 2

previous_weight = 75


# cookies = {"login": "user", "password": "password", "avatar": "avatar", "email": "email",
#             "sex": "sex", "age": 20, "language": "english", "koef" : 1, "water": "0", "physical_activities":
#               1.5, "weight": 70, "height": 180, "calories_goal": 2000, "proteins": 100, "carbs": 300, "fats": 90}
class DayPlan:
    @staticmethod
    def show_day_plan_page():
        dishes = get_dishes()
        dishes = formatting_dishes(dishes)
        user_data = get_user_data(id)
        print(user_data)
        user = formatting_user(user_data)

        return render_template(
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
        targetKBZHU = data.get("targetKBZHU")
        actualKBZHU = data.get("actualKBZHU")

        sql = """
            IF NOT EXISTS (
                SELECT 1
                FROM your_table
                WHERE id = ? AND date = ?
            )
            BEGIN
                INSERT INTO your_table (id, weight, height, water, date, calories, calories_plan, proteins, proteins_plan, fats, fats_plan, carbs, carbs_plan)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
            END
            ELSE
            BEGIN
                UPDATE your_table
                SET weight = ?, height = ?, water = ?, calories = ?, calories_plan = ?, proteins = ?, proteins_plan = ?, fats = ?, fats_plan = ?, carbs = ?, carbs_plan = ?
                WHERE id = ? AND date = ?;
            END;
            """

        print(
            f"Received data: Weight: {weight}, Target KBZHU: {
                targetKBZHU}, Actual KBZHU: {actualKBZHU}"
        )

        # Возвращаем ответ
        return jsonify({"message": "Data saved successfully"}), 200

    @staticmethod
    def show_add_product_page():
        return render_template(
            "DayPlan/add_product.html",
            header_links=header_links,
            title="Добавить продукт",
        )


def formatting_dishes(dishes):
    formatted_dishes = [
        {
            "id": dish[0],
            "name": dish[1],
            "calories": dish[3],
            "protein": dish[4],
            "carbs": dish[5],
            "fats": dish[6],
            "category": dish[7],
        }
        for dish in dishes
    ]
    return formatted_dishes


def formatting_user(user_data):
    user = {
        "id": user_data[0],
        "name": user_data[1],
        "login": user_data[2],
        "password": user_data[3],
        "avatar": user_data[4],
        "email": user_data[5],
        "sex": user_data[6],
        "age": user_data[7],
        "language": user_data[8],
        "koef": user_data[9],
        "water": user_data[10],
        "physical_activities": user_data[11],
        "weight": user_data[12],
        "height": user_data[13],
        "calories": user_data[14],
        "proteins": user_data[15],
        "carbs": user_data[16],
        "fats": user_data[17],
        "eating_times": user_data[18],
    }
    return user
