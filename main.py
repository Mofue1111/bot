from telegram.ext import   ApplicationBuilder
from handlers import order, recommend
from handlers.dialogs import change_dish
from handlers import start,admin,callbacks,menu
from dotenv import load_dotenv
import os

def get_all_handlers():
    return (start.get()+
            admin.get()+
            menu.get()+
            callbacks.get()+
            change_dish.get()+
            order.get()+
            recommend.get())


         
def main():
    load_dotenv()
    builder = ApplicationBuilder()
    builder.token(os.getenv("TOKEN"))
    app = builder.build()
    for handler in get_all_handlers():
        app.add_handler(handler)
    print("Бот запущен")
    return app
     