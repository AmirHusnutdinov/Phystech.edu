from flask import redirect, url_for, request, session

from server.database.use_DataBase import save_news
from server.service_files.links import *
from settings import app
from utils import render_template_with_user


class News:
    @staticmethod
    def show_all_news_page():
        if "user_id" in session:
            header_links = choose_header_links("authorized")
        else:
            header_links = choose_header_links("not-authorized")

        return render_template_with_user(
            "News/all_news.html",
            header_links=header_links,
            title="Новости"
        )

    @staticmethod
    def show_one_news_page(news_id):
        if "user_id" in session:
            header_links = choose_header_links("authorized")
        else:
            header_links = choose_header_links("not-authorized")
        news_title = "Заголовок новости"
        news_image_url = "https://via.placeholder.com/800x400"
        news_content = """
            <p>Я знаю, что id этой странички""" + str(news_id) + """</p>
            <p>Здесь будет текст статьи. Это пример текста, который может быть в статье. Здесь будет текст статьи. 
            Это пример текста, который может быть в статье. Здесь будет текст статьи. 
            Это пример текста, который может быть в статье.</p>
            <p>Здесь будет текст статьи. Это пример текста, который может быть в статье. Здесь будет текст статьи. 
            Это пример текста, который может быть в статье. Здесь будет текст статьи. Это пример текста, который может 
            быть в статье.</p>
            <p>Здесь будет текст статьи. Это пример текста, который может быть в статье. Здесь будет текст статьи. 
            Это пример текста, который может быть в статье. Здесь будет текст статьи. Это пример текста, который может 
            быть в статье.</p>
            """
        return render_template_with_user(
            "News/one_news.html",
            title=f"Новость {str(news_id)}",
            header_links=header_links,
            news_title=news_title,
            news_image_url=news_image_url,
            news_content=news_content
        )

    @staticmethod
    def show_make_news():
        if "user_id" in session:
            header_links = choose_header_links("authorized")
        else:
            header_links = choose_header_links("not-authorized")
        return render_template_with_user(
            "News/make_news.html",
            title=f"Новостной редактор",
            header_links=header_links,
        )

    @staticmethod
    def handle_make_news():
        title = request.form.get('news-title')
        content = request.form.get('news-content')
        image = request.files.get('news-image')
        if image:
            image_path = f"static/uploads/{image.filename}"
            image.save(image_path)
        else:
            image_path = None
        save_news(title=title, image_path=image_path, content=content)
        return redirect(url_for('open_all_news_page'))


@app.route(all_news)
def open_all_news_page():
    return News.show_all_news_page()


@app.route(one_news)
def open_one_news_page(news_id):
    return News.show_one_news_page(news_id)


@app.route(make_news, methods=['GET'])
def open_make_news_page():
    return News.show_make_news()


@app.route(save_news, methods=['POST'])
def handle_make_news():
    return News.handle_make_news()
