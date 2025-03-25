from flask import render_template

from ServiceFiles.links import *
from settings import app, host

class handlers:

    @app.errorhandler(400)
    def page_bad_request(_):
        error_phrase = ["Запрос", "неправильный", "."]
        return render_template("ErrorCodes/errors.html",
                               error_code_name="Bad request",
                               error_code="400",
                               error_phrase=error_phrase,
                               main_page=main_page), 400


    @app.errorhandler(404)
    def page_not_found(_):
        error_phrase = ["Похоже такой", "страницы", "нет"]
        return render_template("ErrorCodes/errors.html",
                               error_code_name="Not Found",
                               error_code="404",
                               error_phrase=error_phrase,
                               main_page=main_page), 404


    @app.errorhandler(500)
    def page_internal_server_error(_):
        error_phrase = ["Похоже что-то", "не очень", "хорошо."]
        return render_template("ErrorCodes/errors.html",
                               error_code_name="Internal Server Error",
                               error_code="500",
                               error_phrase=error_phrase,
                               main_page=main_page), 500


    @app.errorhandler(501)
    def page_not_implemented(_):
        error_phrase = ["Не поддерживается функция,", "необходимая", "для выполнения запроса."]
        return render_template("ErrorCodes/errors.html",
                               error_code_name="Not Implemented",
                               error_code="501",
                               error_phrase=error_phrase,
                               main_page=main_page), 501