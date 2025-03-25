from flask import render_template
from ServiceFiles.links import header_links
from ServiceFiles.links import *
from settings import app, host


class News:
    @staticmethod
    def show_all_news_page():
        return render_template(
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
        return render_template(
            "News/one_news.html",
            title=f"Новость {str(news_id)}",
            header_links=header_links,
            news_title=news_title,
            news_image_url=news_image_url,
            news_content=news_content
        )


@app.route(all_news)
def open_all_news_page():
    return News.show_all_news_page()


@app.route(one_news)
def open_one_news_page(news_id):
    return News.show_one_news_page(news_id)
