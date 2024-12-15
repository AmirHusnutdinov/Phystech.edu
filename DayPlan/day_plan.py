from flask import render_template
from ServiceFiles.links import header_links
from DataBase.use_DataBase import get_dishes

cookies = {"login": "user", "password": "password", "avatar": "avatar", "email": "email", "sex": "sex", "age": 20, "language": "english", "koef" : 1, "water": "0", "physical_activities": 1.5, "weight": 70, "height": 180, "calories_goal": 2000, "proteins": 100, "carbonohydrates": 300, "triglycerides": 90}
class DayPlan:
    @staticmethod
    def show_day_plan_page():
        dishes = get_dishes()  # Предполагается, что эта функция возвращает список кортежей
        formatted_dishes = [
            {
                "id": dish[0],
                "name": dish[1],
                "calories": dish[3],
                "protein": dish[4],
                "carbs": dish[5],
                "fats": dish[6],
                "category": dish[7]
            }
            for dish in dishes
        ]
        return render_template(
            "DayPlan/day_plan.html",
            header_links=header_links,
            title="Дневной план", dishes = formatted_dishes, cookies = cookies)

    @staticmethod
    def show_add_product_page():
        return render_template(
            "DayPlan/add_product.html",
            header_links=header_links,
            title="Добавить продукт"
        )
