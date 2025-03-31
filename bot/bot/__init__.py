from bot import *
from telegram import Update, MenuButtonWebApp
from telegram.ext import ContextTypes, CallbackContext, ExtBot, Application
from dataclasses import dataclass
from asgiref.sync import sync_to_async
from bot.utils import *
from bot.utils.bot_functions import *
from bot.utils.keyboards import *
from bot.services import *
from bot.resources.conversationList import *
from app.services import filter_objects_sync
from config import WEBAPP_URL


async def is_message_back(update: Update):
    if update.message.text == Strings(update.effective_user.id).back:
        return True
    else:
        return False


async def main_menu(update: Update, context: CustomContext):
    update = update.callback_query if update.callback_query else update
    bot = context.bot


    await check_username(update)

    bot_user: Bot_user = await get_object_by_update(update)
    webapp = WebAppInfo(url=f"{WEBAPP_URL}?user={bot_user.pk}")
    markup = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=context.words.open_catalog,
                    web_app=webapp
                )
            ]
        ]
    )
    await bot.send_message(
        update.message.chat_id,
        context.words.main_menu,
        reply_markup=markup
    )
    menu_button = MenuButtonWebApp(
        text=context.words.catalog,
        web_app=webapp
    )
    await context.bot.set_chat_menu_button(
        context._user_id, menu_button=menu_button
    )
