from telegram.ext import CommandHandler,ContextTypes
from telegram import Update,ReplyKeyboardMarkup

async def start(update:Update, context: ContextTypes.DEFAULT_TYPE):
   keyboard = [
                ["Показать блюда👁‍🗨"],
                ["Корзина🧺"],
                ["Заказы 📋"]
            ]
   await update.message.reply_text("""
👋 Добро пожаловать в ресторан FitFood! 
 Я помогу вам выбрать идеальное блюдо, рассчитать калории и оформить заказ 🍽️""",reply_markup=ReplyKeyboardMarkup(keyboard))
    

def get():
    return [CommandHandler("start",start)]


    


