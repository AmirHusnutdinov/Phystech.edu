from flask import render_template, session, redirect

from server.database.use_DataBase import *
from server.service_files.links import *
from settings import app


class Students:

    @staticmethod
    def show_students_page():
        if "user_id" in session:
            user_id = session["user_id"]
            if check_trainer(user_id):
                student_list = get_list_of_student(user_id)
                students_info = []
                for el in student_list:
                    students_info.append(get_user_data(el))
                return render_template("Trainer/students.html",
                                       header_links=choose_header_links("authorized"),
                                       title="Мои студенты",
                                       cookies=students_info
                                       )
            return redirect(main_page)
        return redirect(main_page)

    @staticmethod
    def show_one_student_page(student_id):
        if "user_id" in session:
            user_id = session["user_id"]
            if check_trainer(user_id):
                user_info = get_user_data(student_id)
                student_title = user_info["name"]
                student_image_url = user_info["avatar"]
                student_content = (f"Возраст: {user_info['age']}"
                                   f"Пол: {user_info['sex']}"
                                   f"Почта {user_info['email']}"
                                   )
                return render_template(
                    "Trainer/student.html",
                    title=f"Ученик {user_info['name']}",
                    header_links=choose_header_links("authorized"),
                    student_title=student_title,
                    student_image_url=student_image_url,
                    student_content=student_content,
                    cookies=user_info
                )

            return redirect(main_page)
        return redirect(main_page)


@app.route(all_students)
def open_all_students_page():
    return Students.show_students_page()


@app.route(student)
def open_students_page(student_id):
    return Students.show_one_student_page(student_id)
