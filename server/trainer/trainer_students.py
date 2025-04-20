from flask import render_template, session, request, jsonify
from flask import session

from server.database.use_DataBase import *
from server.service_files.links import *
from settings import app
from datetime import datetime


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
                return render_template(
                    "Trainer/students.html",
                    header_links=header_links,
                    title="Мои студенты",
                    cookies=students_info,
                )
            return "You are not trener", 401
        return "You are not logged in", 401

    @staticmethod
    def show_one_student_page(student_id):
        if "user_id" not in session:
            return "You are not logged in", 401

        trainer_id = session["user_id"]
        if not check_trainer(trainer_id):
            return "You are not trainer", 401

        user_info = get_user_data(student_id)
        if not user_info:
            return "Student not found", 404

        # Получаем историю сообщений
        messages = get_message_history(trainer_id, student_id)

        # Форматируем сообщения для шаблона
        formatted_messages = []
        for msg in messages:
            sender = "received" if msg["id_from"] == student_id else "sent"
            formatted_messages.append(
                {
                    "type": sender,
                    "content": msg["content"],
                    "time": msg["time"].strftime("%H:%M"),
                    "sender_name": user_info["name"] if sender == "received" else "Вы",
                }
            )

        return render_template(
            "Trainer/student.html",
            title=f"Ученик {user_info['name']}",
            header_links=header_links,
            student_title=user_info["name"],
            student_image_url=user_info["avatar"],
            student_content=f"Возраст: {user_info['age']} Пол: {user_info['sex']} Почта: {user_info['email']}",
            cookies=user_info,
            messages=formatted_messages,
            student_id=student_id,
        )

    @staticmethod
    def send_message():
        if "user_id" not in session:
            return jsonify({"status": "error", "message": "Not logged in"}), 401

        trainer_id = session["user_id"]
        if not check_trainer(trainer_id):
            return jsonify({"status": "error", "message": "Not a trainer"}), 403
        data = request.json
        student_id = int(data.get("student_id"))
        message = data.get("message")

        if not student_id or not message:
            return jsonify({"status": "error", "message": "Invalid data"}), 400

        # Проверяем, что студент действительно принадлежит тренеру
        student_list = get_list_of_student(trainer_id)
        if student_id not in student_list:
            return jsonify({"status": "error", "message": "Student not found"}), 404

        # Сохраняем сообщение
        add_message(trainer_id, student_id, message)
        return jsonify(
            {
                "status": "success",
                "message": "Message sent",
                "time": datetime.now().strftime("%H:%M"),
            }
        )

    @staticmethod
    def get_new_messages(student_id):
        print('got new messages')
        if "user_id" not in session:
            return jsonify({"status": "error", "message": "Not logged in"}), 401
        trainer_id = session["user_id"]
        if not check_trainer(trainer_id):
            return jsonify({"status": "error", "message": "Not a trainer"}), 403

        # Получаем последние сообщения (например, после определенного timestamp)
        last_update = request.args.get("last_update")
        messages = get_message_history(
            trainer_id, student_id, since=last_update)

        formatted_messages = []
        for msg in messages:
            if msg["id_from"] == student_id:  # Только новые сообщения от студента
                user_info = get_user_data(student_id)
                formatted_messages.append(
                    {
                        "content": msg["content"],
                        "time": msg["time"].strftime("%H:%M"),
                        "sender_name": user_info["name"],
                    }
                )

        return jsonify(
            {
                "status": "success",
                "messages": formatted_messages,
                "last_update": datetime.now().isoformat(),
            }
        )


@app.route(all_students)
def open_all_students_page():
    return Students.show_students_page()


@app.route(student)
def open_students_page(student_id):
    return Students.show_one_student_page(student_id)


@app.route("/send_message", methods=["POST"])
def send_message():
    return Students.send_message()


@app.route("/get_new_messages/<student_id>")
def get_new_messages(student_id):
    return Students.get_new_messages(student_id)
