base_link = ""
admin = base_link + "/admin"
authorization = base_link + "/authorization"
registration = base_link + "/registration"
calendar = base_link + "/calendar"
main_page = base_link + "/"
day_plan = base_link + "/day_plan"
selected_products = base_link + "/selected_products"
answers = base_link + '/answers'
about = base_link + '/about'
cabinet = base_link + '/cabinet'
all_news = base_link + '/all_news'
one_news = base_link + '/one_news/<int:news_id>'
make_news = base_link + '/make_news/'
save_news = base_link + '/save_news/'
add_product = base_link + "/add_product"
save_day_plan = day_plan + "/save_day_plan"
process_registration = base_link + '/process_registration'
confirm_code = base_link + '/confirm_code'
process_login = base_link + '/process_login'
logout = base_link + '/logout'
all_students = base_link + '/all_students'
student = base_link + '/student/<int:student_id>'


def choose_header_links(role):
    if role == "authorized":
        return {
            "role": "authorized",
            "/": "/",
            "day_plan": day_plan,
            "calendar": calendar,
            "cabinet": cabinet,
            "all_news": all_news,
            "all_students": all_students
        }
    elif role == "not-authorized":
        return {
            "role": "not-authorized",
            "/": "/",
            "all_news": all_news,
            "authorization": authorization,
        }
