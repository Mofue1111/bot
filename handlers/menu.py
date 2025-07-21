from telegram import InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup, Update
from telegram.ext import (ContextTypes,MessageHandler,filters)

from database import db
from database import models

async def show(update:Update,context:ContextTypes.DEFAULT_TYPE):
    dishes:list[models.Dish] = db.get_dishes()
    props_btn = []
    if 'admin' in context.user_data:# Если ключ находится в словаре user_data, то инлайн кнопку  "Свойства" создаем 
          props_btn.append(InlineKeyboardButton(text = "Свойства", callback_data = f"props_dish_id={d.id}"))
          
    else:
         reply_keyboard = ReplyKeyboardMarkup([
            [KeyboardButton("Персональная рекомендация")],
            [KeyboardButton("Корзина")],
            [KeyboardButton("Заказы")]
        ], resize_keyboard=True)
    await update.message.reply_text("Выберите блюдо или запросите персональную рекомендацию:", reply_markup=reply_keyboard)
    if len(dishes)==0: 
         await update.message.reply_text("Блюда отсутствуют...")
    else:   
        for d in dishes: 
            text = (
                        f"Название:{d.name}\n"
                        f"Цена 💵: {d.price}\n"
                        f"Теги: {d.tags}\n"
                        f"Характеристики📋: {d.properties if d.properties else "Пусто"}\n"
                        f"Описание:\n{d.desc}"
                    )
            keyboard = [
                 
                [InlineKeyboardButton(text = "Хочу все знать",callback_data = f"dish_id={d.id}")],
                [InlineKeyboardButton(text = "Добавить в корзину",callback_data = f"card_dish_id={d.id}")]
            ]
            if len(props_btn)>0:
                 keyboard.append(props_btn)
            await update.message.reply_photo(d.photo,text,reply_markup=InlineKeyboardMarkup(keyboard))

def get():
        show_handler = MessageHandler(filters.Text("Показать блюда👁‍🗨"),show)
        return [show_handler]