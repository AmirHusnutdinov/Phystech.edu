from ServiceFiles.links import header_links
from utils import render_template_with_user
from flask import request, redirect, url_for
from DataBase.use_DataBase import save_news


class News:
    @staticmethod
    def show_all_news_page():
        return render_template_with_user(
            "News/all_news.html",
            header_links=header_links,
            title="Новости"
        )

    @staticmethod
    def show_one_news_page(news_id):
        news_title = "Заголовок новости"
        news_image_url = "https://via.placeholder.com/800x400"
        news_content = """
            <p>Я знаю, что id этой странички""" + str(news_id) + """</p>
            <p>Здесь будет текст статьи. Это пример текста, который может быть в статье. Здесь будет текст статьи. Это пример текста, который может быть в статье. Здесь будет текст статьи. Это пример текста, который может быть в статье.</p>
            <p>Здесь будет текст статьи. Это пример текста, который может быть в статье. Здесь будет текст статьи. Это пример текста, который может быть в статье. Здесь будет текст статьи. Это пример текста, который может быть в статье.</p>
            <p>Здесь будет текст статьи. Это пример текста, который может быть в статье. Здесь будет текст статьи. Это пример текста, который может быть в статье. Здесь будет текст статьи. Это пример текста, который может быть в статье.</p>
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
