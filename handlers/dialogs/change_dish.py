
from telegram.ext import(
                    CallbackContext,
                    CallbackQueryHandler,
                    ConversationHandler,
                    ContextTypes,
                    MessageHandler,filters
                    )
from telegram import Update

from database import db



async def change_properties(update:Update,context:CallbackContext):
        query = update.callback_query
        context.user_data["dish_id"] = query.data.split("=")[-1]
        await context.bot.delete_message(
            chat_id=query.message.chat_id,
            message_id=query.message.message_id
        )
        query.answer()
        await context.bot.send_message(chat_id = query.message.chat_id, text = "Добавьте свойства блюду")
        return "PROPS"



async def get_props_dish(update:Update,context:ContextTypes.DEFAULT_TYPE):
    new_props = update.message.text
    if db.update_dish_by_id(context.user_data["dish_id"],new_props,"properties"):
        await update.message.reply_text("Блюдо успешно отредактировано ✔️")
    else:
        await update.message.reply_text("Ошибка ❌")
    return ConversationHandler.END

def get():
    handler = ConversationHandler(
          entry_points=[CallbackQueryHandler(pattern=r"^change_dish_id",callback=change_properties)],
          states={
               "PROPS": [MessageHandler(filters.TEXT,get_props_dish)]
          },
          fallbacks=[]            
        )
    return [handler]