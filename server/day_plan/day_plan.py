# The `DayPlan` class in the Python code provides methods to display a day plan page with dishes, save
# the day plan, and show an add product page.
from flask import render_template, request, jsonify
from server.service_files.links import header_links
from server.database.use_DataBase import get_dishes, get_user_data,database_query
from datetime import datetime,date

id = 2

previous_weight = 75


# cookies = {"login": "user", "password": "password", "avatar": "avatar", "email": "email",
#             "sex": "sex", "age": 20, "language": "english", "koef" : 1, "water": "0", "physical_activities":
#               1.5, "weight": 70, "height": 180, "calories_goal": 2000, "proteins": 100, "carbs": 300, "fats": 90}
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
        targetKBZHU = data.get("targetKBZHU")
        actualKBZHU = data.get("actualKBZHU")
        date = data.get("date")
        print(date)

        if(not validate_data(data)):
            return jsonify({"message": "Incorrect Data"}), 400
        if not validate_date(data.get('date')):
            return jsonify({"message": "wrong date"}), 400
        user = get_user_data(id)
        sql = f"""
        INSERT INTO user_daily_metrics (id, weight, height, water, date, calories, calories_plan, proteins, proteins_plan, fats, fats_plan, carbs, carbs_plan)
        VALUES ({id}, {weight}, {user['height']}, {user['water']}, '{date}', 
                {actualKBZHU['calories']}, {targetKBZHU['calories']}, 
                {actualKBZHU['protein']}, {targetKBZHU['protein']}, 
                {actualKBZHU['fats']}, {targetKBZHU['fats']}, 
                {actualKBZHU['carbs']}, {targetKBZHU['carbs']})
        ON CONFLICT (id, date) DO UPDATE
        SET weight = {weight}, height = {user['height']}, water = {user['water']}, 
            calories = {actualKBZHU['calories']}, calories_plan = {targetKBZHU['calories']}, 
            proteins = {actualKBZHU['protein']}, proteins_plan = {targetKBZHU['protein']}, 
            fats = {actualKBZHU['fats']}, fats_plan = {targetKBZHU['fats']}, 
            carbs = {actualKBZHU['carbs']}, carbs_plan = {targetKBZHU['carbs']};
        """

        print(
            f"Received data: Weight: {weight}, Target KBZHU: {targetKBZHU}, Actual KBZHU: {actualKBZHU}"
        )

        try:
            database_query(sql)
        except Exception as ex:
            print(f"Error while saving day plan: {ex}")
            return jsonify({"message": "Error while saving day plan"}), 500
        

        # Возвращаем ответ
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
