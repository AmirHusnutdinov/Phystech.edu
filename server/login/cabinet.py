from flask import session, redirect, flash
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SelectField, FileField, SubmitField, FloatField
from wtforms.validators import DataRequired, NumberRange, Email
from werkzeug.utils import secure_filename
from flask_wtf.file import FileField, FileAllowed

import os
from server.database.use_DataBase import get_user_data, update_user_data
from server.service_files.links import *
from settings import app, UPLOAD_FOLDER
from utils import render_template_with_user
from datetime import datetime
from server.cloud.cloud_main import Cloud
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
        if 'user_id' in session:
            user = get_user_data(session['user_id'])
            profile_form = ProfileForm(obj=user)
            nutrition_form = NutritionForm(obj=user)

            avatar = Cabinet.cloud.get_url(f'avatars/{session['user_id']}')
            
            return render_template_with_user(
                "Login/cabinet.html",
                header_links=choose_header_links("authorized"),
                title="Кабинет",
                user=user,
                profile_form=profile_form,
                nutrition_form=nutrition_form,
                avatar = avatar)
        else:
            return redirect(main_page)
        
    @staticmethod
    def update_profile():
        if 'user_id' not in session:
            return redirect(main_page)
            
        user = get_user_data(session['user_id'])

        profile_form = ProfileForm()
        if profile_form.validate_on_submit():
            # Загружаем аватар в облако
            avatar_url = None
            if profile_form.avatar.data:
                avatar_url = Cabinet._upload_avatar(
                    profile_form.avatar.data, 
                    session['user_id'],
                    Cabinet.cloud
                )
            
            # Подготавливаем данные для обновления
            update_data = {
                'name': profile_form.name.data,
                'age': profile_form.age.data,
                'weight': profile_form.weight.data,
                'height': profile_form.height.data,
                'sex': profile_form.gender.data,
                'activity': profile_form.activity.data
            }
            
            if avatar_url:
                update_data['avatar'] = avatar_url
            
            # Обновляем данные пользователя
            update_user_data(session['user_id'], update_data)
            flash('Профиль успешно обновлен!', 'success')
            return redirect(cabinet)
        
        # Если форма не валидна, показываем ошибки
        for field, errors in profile_form.errors.items():
            for error in errors:
                flash(f"{getattr(profile_form, field).label.text}: {error}", 'error')
                # print(field, error)
        return redirect(cabinet)

    @staticmethod
    def update_nutrition():
        if 'user_id' not in session:
            return redirect(main_page)
            
        user = get_user_data(session['user_id'])
        nutrition_form = NutritionForm(obj=user)
        
        if nutrition_form.validate_on_submit():
            update_data = {
                'calories': nutrition_form.calories.data,
                'proteins': nutrition_form.protein.data,
                'fats': nutrition_form.fats.data,
                'carbs': nutrition_form.carbs.data
            }
            
            update_user_data(session['user_id'], update_data)
            flash('Цели питания успешно обновлены!', 'success')
            return redirect(cabinet)
        
        # Если форма не валидна, показываем ошибки
        for field, errors in nutrition_form.errors.items():
            for error in errors:
                flash(f"{getattr(nutrition_form, field).label.text}: {error}", 'error')
        return redirect(cabinet)


# Routes
@app.route(cabinet, methods=['GET', 'POST'])
def open_cabinet_page():
    return Cabinet.show_cabinet_page()

@app.route(cabinet + '/update_profile', methods=['POST'])
def update_profile():
    return Cabinet.update_profile()

@app.route(cabinet + '/update_nutrition', methods=['POST'])
def update_nutrition():
    return Cabinet.update_nutrition()

# Forms
class ProfileForm(FlaskForm):
    login = StringField('Логин', render_kw={'readonly': True})
    name = StringField('Имя', validators=[DataRequired()])
    email = StringField('Почта', render_kw={'readonly': True})
    age = IntegerField('Возраст', validators=[DataRequired(), NumberRange(min=1, max=120)])
    weight = FloatField('Вес (кг)', validators=[DataRequired(), NumberRange(min=30, max=300)])
    height = IntegerField('Рост (см)', validators=[DataRequired(), NumberRange(min=100, max=250)])
    gender = SelectField('Пол', choices=[
        ('male', 'Мужской'),
        ('female', 'Женский')
    ], validators=[DataRequired()])
    activity = SelectField('Уровень активности', choices=[
        ('sedentary', 'Сидячий образ жизни'),
        ('light', 'Легкая активность'),
        ('moderate', 'Умеренная активность'),
        ('active', 'Активный образ жизни'),
        ('very_active', 'Очень активный образ жизни')
    ], validators=[DataRequired()])
    avatar = FileField('Аватар', validators=[FileAllowed(['jpg', 'png', 'jpeg'], 'Только изображения!')])
    submit = SubmitField('Сохранить')

class NutritionForm(FlaskForm):
    calories = IntegerField('Калории', validators=[DataRequired(), NumberRange(min=1000, max=10000)])
    protein = IntegerField('Белки (г)', validators=[DataRequired(), NumberRange(min=0, max=500)])
    fats = IntegerField('Жиры (г)', validators=[DataRequired(), NumberRange(min=0, max=500)])
    carbs = IntegerField('Углеводы (г)', validators=[DataRequired(), NumberRange(min=0, max=1000)])
    submit = SubmitField('Сохранить')