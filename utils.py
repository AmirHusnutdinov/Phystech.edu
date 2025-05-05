from flask import render_template
from flask import session
from server.service_files.links import choose_header_links


def is_login():
    return session["Login"]


def data():
    return {"Login": is_login, "Name": session.get("name", None)}


def render_template_with_user(template_name_ot_list, **kwargs):
    kwargs["title"] = kwargs.get("title", "Главная страница")
    kwargs["header_links"] = kwargs.get("header_links", choose_header_links("not-authorized") if 'user_id' in session else choose_header_links("not-authorized"))
    return render_template(
        template_name_ot_list,
        data=data(),
        # header_links=choose_header_links("not-authorized"),
        **kwargs  # Передаем именованные аргументы
    )

# debug stuff

def debug_print(header, *args):
    BOLD = "\033[1m"  # Жирный текст
    RESET = "\033[0m"  # Сброс форматирования
    
    print(f"{BOLD}[DEBUG] -{header}-{RESET}")
    
    if args:
        for arg in args:
            print(arg)
    else:
        print("\nTEST STUFF\n")
    
    print(f"{BOLD}--------------{RESET}")