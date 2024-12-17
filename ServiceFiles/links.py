base_link = ""
admin = base_link + "/admin"
authorization = base_link + "/authorization"
registration = base_link + "/registration"
calendar = base_link + "/calendar"
main_page = base_link + "/"
day_plan = base_link + "/day_plan"
selected_products = base_link + "/selected_products"
answers = base_link + "/answers"
about = base_link + "/about"
cabinet = base_link + "/cabinet"
all_news =  base_link + "/all_news"
one_news =  base_link + "/one_news/<int:news_id>"
add_product = base_link + "/add_product"
save_day_plan = day_plan + "/save_day_plan"
# header_links = ["/", day_plan, calendar, cabinet, all_news, authorization, registration, save_day_plan] 
# хз зачем переписал на словарь
header_links = {
  "/" : "/",
  "day_plan": day_plan,
  "calendar": calendar,
  "cabinet": cabinet,
  "all_news": all_news,
  "authorization": authorization,
  "registration": registration
}