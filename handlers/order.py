import datetime
import sqlite3
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import (CallbackContext,MessageHandler,CallbackQueryHandler,filters)
from utils.logger import log_action
from database.db import get_dish_by_id


async def view_cart(update: Update, context: CallbackContext):
    user_data = context.user_data
    if 'card' not in user_data or not user_data['card']:
        await update.message.reply_text("Ваша корзина пуста 🧺")
        return

    cart = user_data['card']
    summary = {}
    total_price = 0

    for dish_id in cart:
        summary[dish_id] = summary.get(dish_id, 0) + 1

    text = "🧺 *Ваша корзина:*\n"
    for dish_id, count in summary.items():
        dish = get_dish_by_id(dish_id)
        price = dish['price'] * count
        total_price += price
        text += f"- {dish['name']} x {count} = {price}₽\n"

    text += f"\n*Итого:* {total_price}₽"
    keyboard = [[InlineKeyboardButton("Оформить заказ 📝", callback_data="checkout")]]
    await update.message.reply_text(text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode='Markdown')


async def checkout(update: Update, context: CallbackContext):
    query = update.callback_query
    cart = context.user_data.get("card", [])
    if not cart:
        await query.answer("Корзина пуста")
        return

    summary = {}
    total_price = 0
    for dish_id in cart:
        summary[dish_id] = summary.get(dish_id, 0) + 1

    conn = sqlite3.connect("app.db")
    cursor = conn.cursor()

    # сохраняем заказ
    total_count = sum(summary.values())
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    user_name = query.from_user.full_name
    cursor.execute("INSERT INTO orders (count, total_price, date, user_name, status) VALUES (?, ?, ?, ?, ?)",
                   (total_count, total_price, now, user_name, "в работе"))
    order_id = cursor.lastrowid

    for dish_id, count in summary.items():
        dish = get_dish_by_id(dish_id)
        total_price += dish['price'] * count
        cursor.execute("INSERT INTO orders_dishes (id_order, id_dish, count) VALUES (?, ?, ?)",
                       (order_id, dish_id, count))

    conn.commit()
    conn.close()

    context.user_data['card'] = []  # очистка корзины
    await query.edit_message_text("✅ Заказ оформлен и отправлен в работу!")

    #логирование 
    log_action(user=update.effective_user.username, action=f"Оформление заказа клиентом. Id заказа = {order_id}", level = "WARNING")


async def view_orders(update: Update, context: CallbackContext):
    user = update.message.from_user
    conn = sqlite3.connect("app.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM orders WHERE user_name = ?", (user.full_name,))
    orders = cursor.fetchall()

    if not orders:
        await update.message.reply_text("Сделайте заказ 🙂")
        return

    text = "📋 *Ваши заказы:*\n"
    for order in orders:
        text += f"\n🆔 Заказ №{order[0]} — {order[1]} блюд, {order[2]}₽, статус: {order[5]}\n"

    await update.message.reply_text(text, parse_mode='Markdown')


def get():
    return [
        MessageHandler(filters.Text("Корзина"), view_cart),
        CallbackQueryHandler(checkout, pattern=r"^checkout"),
        MessageHandler(filters.Text("Заказы"), view_orders),
    ]