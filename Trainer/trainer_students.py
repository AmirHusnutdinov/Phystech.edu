from flask import render_template

from ServiceFiles.links import header_links


class Students:
    @staticmethod
    def show_students_page():
        return render_template(
            "Trainer/students.html",
            header_links=header_links,
            title="Мои студенты"
        )

    @staticmethod
    def show_one_student_page(student_id):
        student_title = "Имя чела"
        student_image_url = "https://via.placeholder.com/800x400"
        student_content = """
                <p>Я знаю, что id этой странички""" + str(student_id) + """</p>
                <p>Здесь будет текст. Это пример текста, который может быть</p>
                <p>Здесь будет текст. Это пример текста, который может быть</p>
                <p>Здесь будет текст. Это пример текста, который может быть</p>
                """
        return render_template(
            "Trainer/student.html",
            title=f"Мое имя {str(student_title)}, а мой id-{str(student_id)}",
            header_links=header_links,
            student_title=student_title,
            student_image_url=student_image_url,
            student_content=student_content
        )
