from telegram.ext import(
                    CallbackContext,
                    CallbackQueryHandler
                    )
                    

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from ai import dish_describer
from utils.logger import log_action
from database import db
from database.models import Dish

async def want_all_know_handler(update:Update,context:CallbackContext):
        query = update.callback_query
        dish_id = int(query.data.split('=')[-1])
        dish = Dish()
        dish.from_tuple(db.get_dish_by_id(dish_id))
        #в первую очередь будет в будущем обращаться к кешу
        processing_msg = await context.bot.send_message(
        chat_id=query.message.chat_id,
        text="Идет обработка 💾..."
        )
        result = db.get_ans_neurlink(dish_id)
        if result == None:
                result = await dish_describer.run(dish)
                db.update_dish_by_id(dish_id,result,"ans_neurlink")
                
        if result:
                await context.bot.edit_message_text(
                chat_id=query.message.chat_id,
                message_id=processing_msg.message_id,
                text=result
            )
        else: 
                await context.bot.edit_message_text(
                chat_id=query.message.chat_id,
                message_id=processing_msg.message_id,
                text="К нашему сожалению, описание блюда недоступно, обратитесь к официанту😃"
            )
        
        #логирование
        log_action(user=update.effective_user.username, action=f"Клиент нажал на кнопку 'Хочу все знать' для блюда '{dish.name}' ", level="INFO")
        
        #нужно обязательно добавить столбец properties, 
        #для характеристик блюда от самого заведения

async def show_properties(update:Update,context:CallbackContext):
        query = update.callback_query
        dish_id = int(query.data.split('=')[-1])
        dish = Dish()
        dish.from_tuple(db.get_dish_by_id(dish_id))
        props_info="Пусто"
        if dish.properties:
                props_info = dish.properties
        keyboard = [
                [InlineKeyboardButton(text = "Редактировать",callback_data = f"change_dish_id={dish.id}")]
               
            ]
        await context.bot.send_message(chat_id = query.message.chat_id, text = props_info,reply_markup=InlineKeyboardMarkup(keyboard))

async def add_dish_to_card(update:Update,context:CallbackContext):
       query = update.callback_query
       dish_id = int(query.data.split('=')[-1])
       if 'card' in  context.user_data:
         context.user_data['card'].append(dish_id)
       else:
         context.user_data['card'] = [dish_id]
       await  query.answer("Блюдо добавлено ✅")




def get():
    neurlink_handler = CallbackQueryHandler(pattern=r"^dish_id",callback=want_all_know_handler)
    show_props_handler = CallbackQueryHandler(pattern=r"^props_dish_id",callback=show_properties)
    add_to_card_handler = CallbackQueryHandler(pattern=r"^card_dish_id",callback=add_dish_to_card)
    return [neurlink_handler,show_props_handler,add_to_card_handler]