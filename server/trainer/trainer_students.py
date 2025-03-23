from flask import render_template, session

from server.database.use_DataBase import *
from server.service_files.links import header_links
from settings import app


class Students:

    @staticmethod
    def show_students_page():
        if "user_id" in session:
            user_id = session["user_id"][0][0]
            if check_trener(user_id):
                student_list = get_list_of_student(user_id)
                students_info = []
                for el in student_list:
                    students_info.append(get_user_data(el))
                return render_template(
                    "Trainer/students.html",
                    header_links=header_links,
                    title="Мои студенты",
                    cookies=students_info
                )
            return "You are not trener", 401
        return "You are not logged in", 401
       

    @staticmethod
    def show_one_student_page(student_id):
        user_info = get_user_data(student_id)
        student_title = user_info["name"]
        student_image_url = user_info["avatar"]
        student_content = (f"Возраст: {user_info["age"]}"
                           f"Пол: {user_info["sex"]}"
                           f"Почта {user_info["email"]}"
                           )
        print(user_info)
        return render_template(
            "Trainer/student.html",
            title=f"Ученик {user_info["name"]}",
            header_links=header_links,
            student_title=student_title,
            student_image_url=student_image_url,
            student_content=student_content,
            cookies=user_info
        )

    @app.route("/student/<int:student_id>")
    def student_page(student_id):
        return Students.show_one_student_page(student_id)
