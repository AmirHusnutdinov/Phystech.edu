import os
from ServiceFiles.settings import app
from ServiceFiles.links import main_page
from MainPage.main_page import StartPage
from flask import render_template


@app.route(main_page)
def open_main_page():
    return StartPage.show_the_main_page()


port = int(os.environ.get("PORT", 8181))
app.run(host="0.0.0.0", port=port)
