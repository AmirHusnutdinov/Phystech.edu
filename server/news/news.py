import os

from flask import redirect, url_for, request, session, abort, flash
from werkzeug.utils import secure_filename

from server.cloud.cloud_main import Cloud
from server.database.use_DataBase import database_query, check_admin
from server.database.use_DataBase import save_news_query, update_news, delete_news
from server.service_files.links import *
from settings import app
from utils import render_template_with_user


class News:
    @staticmethod
    def show_all_news_page():
        sql = "SELECT id, title, picture, html FROM news ORDER BY date ASC"
        all_news = database_query(sql, fetch=True)[::-1]
        for i in range(len(all_news)):
            all_news[i] = list(all_news[i])
            id = all_news[i][0]
            all_news[i][2] = Cloud().get_url(f"news/{id}.jpg")

        is_admin = False
        if 'user_id' in session:
            is_admin = check_admin(session["user_id"])

        if 'user_id' in session:
            role = "authorized"
        else:
            role = "not-authorized"
        return render_template_with_user(
            "News/all_news.html",
            title="Новости",
            news=all_news,
            header_links=choose_header_links(role),
            is_admin=is_admin
        )

    @staticmethod
    def show_one_news_page(news_id):
        if 'user_id' in session:
            is_admin = check_admin(session["user_id"])
        else:
            is_admin = False

        sql = f"SELECT id, title, html FROM news WHERE id = {news_id}"
        news_data = database_query(sql, fetch=True)

        if not news_data:
            abort(404)
            return

        news_id, news_title, news_content = news_data[0]
        news_image_url = Cloud().get_url(f"news/{news_id}.jpg")

        return render_template_with_user(
            "News/one_news.html",
            title=news_title,
            news_title=news_title,
            news_image_url=news_image_url,
            news_content=news_content,
            news_id=news_id,
            is_admin=is_admin
        )

    @staticmethod
    def show_make_news(news_id=None):
        if "user_id" not in session or not check_admin(session["user_id"]):
            abort(403)
        # if not session.get('is_admin'):
        #     abort(403)

        if news_id:  # Режим редактирования
            sql = f"SELECT title, picture, html FROM news WHERE id = {news_id}"
            news_data = database_query(sql, fetch=True)
            if not news_data:
                abort(404)
                return
            news_title, news_image_url, news_content = news_data[0]
            template = "News/edit_news.html"
        else:  # Режим создания
            news_title = news_image_url = news_content = ""
            template = "News/make_news.html"

        return render_template_with_user(
            template,
            title="Редактор новости",
            news_title=news_title,
            news_image_url=news_image_url,
            news_content=news_content,
            news_id=news_id
        )

    @staticmethod
    def handle_make_news():
        if "user_id" not in session or not check_admin(session["user_id"]):
            abort(403)
        news_id = request.form.get('news_id')
        edit = True
        if not news_id:
            edit = False
            result = database_query("SELECT MAX(id) + 1 AS next_id FROM news;", fetch=True)
            if result[0][0]:
                print(result)
                news_id = int(result[0][0])
            else:
                news_id = 1
        title = request.form.get('news-title')
        content = request.form.get('news-content')
        image = request.files.get('news-image')
        cloud = Cloud()
        # if news_id:
        #     sql = f"SELECT picture FROM news WHERE id = {news_id}"
        #     result = database_query(sql, fetch=True)
        #     if result:
        #         current_image = result[0][0]

        if image and image.filename:
            filename = secure_filename(image.filename)
            image_path = filename
            image.save(image_path)
            cloud.upload_file(image_path, f"news/{news_id}.jpg", replace=True)
            try:
                os.remove(image_path)
            except OSError:
                pass

        if edit:  # Редактирование существующей новости
            update_news(news_id, title, content)
            flash('Новость успешно обновлена', 'success')
        else:  # Создание новой новости
            save_news_query(news_id=news_id, title=title, content=content)
            flash('Новость успешно создана', 'success')

        return redirect(url_for('open_all_news_page'))

    @staticmethod
    def handle_delete_news(news_id):
        if "user_id" not in session or not check_admin(session["user_id"]):
            abort(403)
        # if not session.get('is_admin'):
        #     abort(403)
        # Cloud().
        delete_news(news_id)
        flash('Новость успешно удалена', 'success')
        return redirect(url_for('open_all_news_page'))


# Основные роутеры
