from datetime import datetime, timezone, date

from flask import render_template, redirect, request, jsonify
from flask import session

from server.cloud.cloud_main import Cloud
from server.database.use_DataBase import *
from server.database.use_DataBase import get_dishes
from server.service_files.links import *


class Students:
    cloud = Cloud()

    @staticmethod
    def show_students_page():
        if "user_id" in session:
            user_id = session["user_id"]
            user = get_user_data(session["user_id"])
            if not user["is_activated"]:
                return redirect(process_registration)
            if user["is_trainer"]:
                student_list = get_list_of_student(user_id)
                students_info = []
                student_photo = []
                for el in student_list:
                    students_info.append(get_user_data(el))
                    students_info[-1]["avatar"] = Students.cloud.get_url(
                        f"""avatars/{students_info[-1]['id']}"""
                    )
                print(students_info)
                return render_template(
                    "Trainer/students.html",
                    header_links=choose_header_links("authorized"),
                    title="Мои студенты",
                    cookies=students_info,
                    cookiesPhoto=student_photo,
                )
            return redirect(main_page)
        return redirect(main_page)

    @staticmethod
    def show_one_student_page(student_id):
        if "user_id" not in session:
            return redirect(main_page)

        if request.method == "POST":
            data = request.get_json()
            database_query(sql=f"""
            insert into diets (name, owner, description) 
            values ('диета', {student_id}, '{str(data).replace("'", '"')}')
            """, fetch=False)

        trainer_id = session["user_id"]
        if not check_trainer(trainer_id):
            return redirect(main_page)

        user_info = get_user_data(student_id)
        if not user_info:
            return redirect(main_page)

        avatar = Students.cloud.get_url(f"""avatars/{user_info['id']}""")
        messages = get_message_history(trainer_id, student_id)
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
        today = date.today()
        today_str = today.strftime('%Y-%m-%d')
        user_daily_metrics = list(database_query(sql=f"""select * from user_daily_metrics
        where id={student_id} and date='{today_str}'""", fetch=True)[0])
        return render_template(
            "Trainer/student.html",
            title=f"Ученик {user_info['name']}",
            header_links=choose_header_links("authorized"),
            student_title=user_info["name"],
            student_image_url=avatar,
            student_content=f"Возраст: {user_info['age']} Пол: {user_info['sex']} Почта: {user_info['email']}",
            cookies=user_info,
            messages=formatted_messages,
            student_id=student_id,
            nutrition_was=user_daily_metrics[7],
            nutrition_needed=user_daily_metrics[8],
            fats_was=user_daily_metrics[9],
            fats_needed=user_daily_metrics[10],
            carbohydrates_was=user_daily_metrics[11],
            carbohydrates_needed=user_daily_metrics[12],
            calories_was=user_daily_metrics[5],
            calories_needed=user_daily_metrics[6],
            dishes=get_dishes()
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
        if "user_id" not in session:
            return jsonify({"status": "error", "message": "Not logged in"}), 401
        trainer_id = session["user_id"]
        if not check_trainer(trainer_id):
            return jsonify({"status": "error", "message": "Not a trainer"}), 403

        last_update = request.args.get("last_update")
        # debug_print('request for new messages, last update', last_update)

        since_dt = datetime.strptime(last_update, "%Y-%m-%dT%H:%M:%S.%fZ")
        since_sql = since_dt.strftime("%Y-%m-%d %H:%M:%S.%f")
        last_update = since_sql

        messages = get_message_history(trainer_id, student_id, since=last_update)
        formatted_messages = []
        # debug_print('student_id', student_id)
        for msg in messages:
            if str(msg["id_from"]) == str(
                    student_id
            ):  # Только новые сообщения от студента
                user_info = get_user_data(student_id)
                formatted_messages.append(
                    {
                        "content": msg["content"],
                        "time": msg["time"].strftime("%H:%M"),
                        "sender_name": user_info["name"],
                    }
                )
        # reducing to form 2025-04-22T13:54:07.343Z
        current_time = (
                datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z"
        )

        # debug_print('CURRENT TIME', current_time)
        # debug_print('MESSAGES', formatted_messages)
        return jsonify(
            {
                "status": "success",
                "messages": formatted_messages,
                "last_update": current_time,
            }
        )
