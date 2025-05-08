from flask import session, redirect, flash, request
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, IntegerField, SelectField, SubmitField, FloatField
from wtforms.validators import DataRequired, NumberRange
from werkzeug.utils import secure_filename

from server.cloud.cloud_main import Cloud
from server.database.use_DataBase import get_user_data, update_user_data
from server.service_files.links import *
from settings import app, UPLOAD_FOLDER
from utils import render_template_with_user

import os


class ProcessRegistration:
    cloud = Cloud()

    @staticmethod
    def show_ProcessRegistration_page():
        if "user_id" not in session:
            return redirect(main_page)

        user = get_user_data(session["user_id"])

        # Если пользователь уже активирован, перенаправляем в кабинет
        if user.get("is_activated", False):
            return redirect(cabinet)

        # Создаем формы с предварительно заполненными данными, если они есть
        ProcessRegistration_form = ProcessRegistrationForm(obj=user)
        nutrition_form = NutritionForm(obj=user)

        submit_registration = process_registration + "/submit"

        return render_template_with_user(
            "Login/process_registration.html",
            title="Завершение регистрации",
            user=user,
            ProcessRegistration_form=ProcessRegistration_form,
            nutrition_form=nutrition_form,
            submit_registration=submit_registration,
        )

    @staticmethod
    def process_Registration():
        if "user_id" not in session:
            return redirect(main_page)

        user = get_user_data(session["user_id"])

        # Если пользователь уже активирован, перенаправляем в кабинет
        if user.get("is_activated", False):
            return redirect(cabinet)

        ProcessRegistration_form = ProcessRegistrationForm()
        nutrition_form = NutritionForm()

        if (
            ProcessRegistration_form.validate_on_submit()
            and nutrition_form.validate_on_submit()
        ):
            # Загружаем аватар в облако, если он предоставлен
            avatar_url = None
            if ProcessRegistration_form.avatar.data:
                # Создаем уникальное имя файла
                filename = f"avatars/{session['user_id']}"
                # Сохраняем временно на сервере
                temp_path = os.path.join(
                    UPLOAD_FOLDER,
                    secure_filename(ProcessRegistration_form.avatar.data.filename),
                )
                ProcessRegistration_form.avatar.data.save(temp_path)

                try:
                    # Загружаем в облако
                    avatar_url = ProcessRegistration.cloud.upload_file(
                        temp_path, filename, True
                    )
                finally:
                    # Удаляем временный файл
                    if os.path.exists(temp_path):
                        os.remove(temp_path)

            # Подготавливаем данные для обновления
            update_data = {
                "name": ProcessRegistration_form.name.data,
                "age": ProcessRegistration_form.age.data,
                "weight": round(ProcessRegistration_form.weight.data, 2),
                "height": ProcessRegistration_form.height.data,
                "sex": ProcessRegistration_form.gender.data,
                "activity": ProcessRegistration_form.activity.data,
                "calories": nutrition_form.calories.data,
                "proteins": nutrition_form.protein.data,
                "fats": nutrition_form.fats.data,
                "carbs": nutrition_form.carbs.data,
                "water": nutrition_form.water.data,
                "is_activated": True,  # Отмечаем пользователя как активированного
            }

            # Обновляем данные пользователя
            update_user_data(session["user_id"], update_data)

            flash("Регистрация успешно завершена!", "success")
            return redirect(cabinet)

        # Если форма не валидна, показываем ошибки
        for form in [ProcessRegistration_form, nutrition_form]:
            for field, errors in form.errors.items():
                for error in errors:
                    flash(f"{getattr(form, field).label.text}: {error}", "error")

        return redirect(process_registration)


# Routes
@app.route(process_registration, methods=["GET"])
def show_ProcessRegistration_page():
    return ProcessRegistration.show_ProcessRegistration_page()


@app.route(process_registration + "/submit", methods=["POST"])
def submit_registration():
    return ProcessRegistration.submit()


class ProcessRegistrationForm(FlaskForm):
    name = StringField("Имя", validators=[DataRequired()])
    age = IntegerField(
        "Возраст", validators=[DataRequired(), NumberRange(min=1, max=120)]
    )
    weight = FloatField(
        "Вес (кг)", validators=[DataRequired(), NumberRange(min=30, max=300)]
    )
    height = IntegerField(
        "Рост (см)", validators=[DataRequired(), NumberRange(min=100, max=250)]
    )
    gender = SelectField(
        "Пол",
        choices=[("male", "Мужской"), ("female", "Женский")],
        validators=[DataRequired()],
    )
    activity = SelectField(
        "Уровень активности",
        choices=[
            ("sedentary", "Сидячий образ жизни"),
            ("light", "Легкая активность"),
            ("moderate", "Умеренная активность"),
            ("active", "Активный образ жизни"),
            ("very_active", "Очень активный образ жизни"),
        ],
        validators=[DataRequired()],
    )
    avatar = FileField(
        "Аватар (необязательно)",
        validators=[FileAllowed(["jpg", "png", "jpeg"], "Только изображения!")],
    )


class NutritionForm(FlaskForm):
    calories = IntegerField(
        "Калории", validators=[DataRequired(), NumberRange(min=1000, max=10000)]
    )
    protein = IntegerField(
        "Белки (г)", validators=[DataRequired(), NumberRange(min=0, max=500)]
    )
    fats = IntegerField(
        "Жиры (г)", validators=[DataRequired(), NumberRange(min=0, max=500)]
    )
    carbs = IntegerField(
        "Углеводы (г)", validators=[DataRequired(), NumberRange(min=0, max=1000)]
    )
    water = IntegerField(
        "Вода (мл)", validators=[DataRequired(), NumberRange(min=0, max=10000)]
    )
    submit = SubmitField("Завершить регистрацию")
