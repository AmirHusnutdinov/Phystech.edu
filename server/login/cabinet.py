import os

from flask import session, redirect, flash
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from werkzeug.utils import secure_filename
from wtforms import (
    StringField,
    IntegerField,
    SelectField,
    SubmitField,
    FloatField,
    TextAreaField,
)
from wtforms.validators import DataRequired, NumberRange

from server.cloud.cloud_main import Cloud
from server.database.use_DataBase import (
    get_user_data,
    get_request,
    add_student,
    update_user_data,
    get_trainer_id,
    get_my_request,
    add_trainer_request,
    check_trainer,
    get_trainer_request,
    update_trainer_request,
)
from server.service_files.links import *
from settings import app, UPLOAD_FOLDER
from utils import render_template_with_user


class Cabinet:
    cloud = Cloud()

    @staticmethod
    def _upload_avatar(avatar_file, user_id, cloud):
        """Загружает файл в облачное хранилище и возвращает URL"""
        if not avatar_file:
            return None

        # Создаем уникальное имя файла
        filename = f"avatars/{user_id}"
        # Сохраняем временно на сервере
        temp_path = os.path.join(UPLOAD_FOLDER, secure_filename(avatar_file.filename))
        avatar_file.save(temp_path)

        try:
            # Загружаем в облако
            avatar_url = cloud.upload_file(temp_path, filename, True)
            return avatar_url
        finally:
            # Удаляем временный файл
            if os.path.exists(temp_path):
                os.remove(temp_path)

    @staticmethod
    def show_cabinet_page():
        if "user_id" in session:
            user = get_user_data(session["user_id"])
            if not user["is_activated"]:
                return redirect(process_registration)
            profile_form = ProfileForm(obj=user)
            profile_form.activity.data = user["activity"]
            profile_form.gender.data = user["sex"]
            nutrition_form = NutritionForm(obj=user)
            trainer_form = TrainerApplicationForm(obj=user)
            trainer_request_form = TrainerRequestForm()
            trainer_id = get_trainer_id(session["user_id"])
            has_trainer = trainer_id != 0

            trainer = {}
            trainer_avatar = None
            trainer_request = {}
            if user["is_trainer"]:
                trainer_request = get_trainer_request(session["user_id"])
            # print(trainer_request)
            if has_trainer:
                trainer = get_user_data(trainer_id)
                trainer_avatar = Cabinet.cloud.get_url(f"avatars/{trainer_id}")
            avatar = Cabinet.cloud.get_url(f"""avatars/{session['user_id']}""")
            request = get_my_request(session["user_id"])
            has_request = False
            if request:
                has_request = True

            return render_template_with_user(
                "Login/cabinet.html",
                header_links=choose_header_links("authorized"),
                title="Кабинет",
                user=user,
                profile_form=profile_form,
                nutrition_form=nutrition_form,
                trainer_form=trainer_form,
                trainer_request_form=trainer_request_form,
                avatar=avatar,
                has_trainer=has_trainer,
                has_request=has_request,
                trainer=trainer,
                trainer_avatar=trainer_avatar,
                trainer_request=trainer_request,
            )
        else:
            return redirect(main_page)

    @staticmethod
    def update_profile():
        if "user_id" not in session:
            return redirect(main_page)

        user = get_user_data(session["user_id"])

        profile_form = ProfileForm()
        if profile_form.validate_on_submit():
            # Загружаем аватар в облако
            if profile_form.avatar.data:
                Cabinet._upload_avatar(
                    profile_form.avatar.data, session["user_id"], Cabinet.cloud
                )

            # Подготавливаем данные для обновления
            update_data = {
                "name": profile_form.name.data,
                "age": profile_form.age.data,
                "weight": round(profile_form.weight.data, 2),
                "height": profile_form.height.data,
                "sex": profile_form.gender.data,
                "activity": profile_form.activity.data,
            }
            # Обновляем данные пользователя
            update_user_data(session["user_id"], update_data)
            flash("Профиль успешно обновлен!", "success")
            return redirect(cabinet)

        # Если форма не валидна, показываем ошибки
        for field, errors in profile_form.errors.items():
            for error in errors:
                flash(f"{getattr(profile_form, field).label.text}: {error}", "error")
                # print(field, error)
        return redirect(cabinet)

    @staticmethod
    def update_nutrition():
        if "user_id" not in session:
            return redirect(main_page)

        user = get_user_data(session["user_id"])
        nutrition_form = NutritionForm(obj=user)

        if nutrition_form.validate_on_submit():
            update_data = {
                "calories": nutrition_form.calories.data,
                "proteins": nutrition_form.protein.data,
                "fats": nutrition_form.fats.data,
                "carbs": nutrition_form.carbs.data,
                "water": nutrition_form.water.data,
            }

            update_user_data(session["user_id"], update_data)
            flash("Цели питания успешно обновлены!", "success")
            return redirect(cabinet)

        # Если форма не валидна, показываем ошибки
        for field, errors in nutrition_form.errors.items():
            for error in errors:
                flash(f"{getattr(nutrition_form, field).label.text}: {error}", "error")
        return redirect(cabinet)

    @staticmethod
    def request_trainer():
        """Обработка запроса на добавление тренера"""
        if "user_id" not in session:
            return redirect(main_page)

        form = TrainerRequestForm()
        if form.validate_on_submit():
            trainer_id = form.trainer_id.data
            if not check_trainer(trainer_id):
                flash("wrong id", "error")
                return redirect(cabinet)
            # Проверяем существование тренера с указанным ID
            # Здесь должна быть ваша логика проверки существования тренера
            # Например: trainer = get_trainer_data(trainer_id)

            # Добавляем запрос в базу данных
            add_trainer_request(session["user_id"], trainer_id, "no_desc")

            flash("Запрос тренеру успешно отправлен!", "success")
        else:
            # Если форма не валидна, показываем ошибки
            for field, errors in form.errors.items():
                for error in errors:
                    flash(f"{getattr(form, field).label.text}: {error}", "error")

        return redirect(cabinet)

    @staticmethod
    def approve_request(request_id):
        if "user_id" not in session:
            return redirect(main_page)

        # Check if the current user is a trainer
        user = get_user_data(session["user_id"])
        if not user.get("is_trainer", False):
            flash("Только тренеры могут выполнять это действие", "error")
            return redirect(cabinet)

        update_trainer_request(request_id, "approved")
        student_id = get_request(request_id)["id_from"]
        add_student(session["user_id"], student_id)
        flash("Запрос успешно одобрен", "success")
        return redirect(cabinet)

    @staticmethod
    def reject_request(request_id):
        if "user_id" not in session:
            return redirect(main_page)

        # Check if the current user is a trainer
        user = get_user_data(session["user_id"])
        if not user.get("is_trainer", False):
            flash("Только тренеры могут выполнять это действие", "error")
            return redirect(cabinet)

        update_trainer_request(request_id, "rejected")
        flash("Запрос отклонен", "success")
        return redirect(cabinet)

    @staticmethod
    def submit_trainer_application():
        if "user_id" not in session:
            return redirect(main_page)

        trainer_form = TrainerApplicationForm()

        if trainer_form.validate_on_submit():
            """nothing happens"""
            # # Сохраняем документы в облако
            # documents_url = None
            # if trainer_form.documents.data:
            #     # Создаем уникальное имя файла
            #     filename = f"trainer_applications/{session['user_id']}/{secure_filename(trainer_form.documents.data.filename)}"
            #     # Сохраняем временно на сервере
            #     temp_path = os.path.join(UPLOAD_FOLDER, secure_filename(
            #         trainer_form.documents.data.filename))
            #     trainer_form.documents.data.save(temp_path)

            #     try:
            #         # Загружаем в облако
            #         documents_url = Cabinet.cloud.upload_file(
            #             temp_path, filename, True)
            #     finally:
            #         # Удаляем временный файл
            #         if os.path.exists(temp_path):
            #             os.remove(temp_path)

            # Здесь можно добавить логику сохранения заявки в базу данных
            # Например:
            # save_trainer_application(
            #     user_id=session['user_id'],
            #     experience=trainer_form.experience.data,
            #     documents_url=documents_url,
            #     application_date=datetime.now()
            # )

            flash(
                "Ваша заявка успешно отправлена! Мы свяжемся с вами в ближайшее время.",
                "success",
            )
            return redirect(cabinet)

        # Если форма не валидна, показываем ошибки
        for field, errors in trainer_form.errors.items():
            for error in errors:
                flash(f"{getattr(trainer_form, field).label.text}: {error}", "error")
        return redirect(cabinet)


# Routes


# Forms


class ProfileForm(FlaskForm):
    login = StringField("Логин", render_kw={"readonly": True})
    name = StringField("Имя", validators=[DataRequired()])
    email = StringField("Почта", render_kw={"readonly": True})
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
        "Аватар",
        validators=[FileAllowed(["jpg", "png", "jpeg"], "Только изображения!")],
    )
    submit = SubmitField("Сохранить")


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
    submit = SubmitField("Сохранить")


class TrainerApplicationForm(FlaskForm):
    experience = TextAreaField(
        "Опишите ваш опыт, прикрепите подтверждающие документы",
        validators=[DataRequired()],
    )
    documents = FileField(
        "Прикрепите документы",
        validators=[
            FileAllowed(
                ["pdf", "doc", "docx", "jpg", "jpeg", "png"],
                "Поддерживаются только документы и изображения!",
            )
        ],
    )
    submit = SubmitField("Отправить")


class TrainerRequestForm(FlaskForm):
    trainer_id = StringField("ID тренера", validators=[DataRequired()])
    submit = SubmitField("Подтвердить")
