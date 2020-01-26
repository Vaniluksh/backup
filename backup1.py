# -*- coding: utf-8 -*-
from telegram import Bot, Update
from telegram.ext import Updater, MessageHandler, Filters
# from telegram import Update, Bot, WebhookInfo, Message, update
# from telegram.update import Update
# from telegram.ext import Dispatcher, CommandHandler
import telegram.ext
import json
import config
import database as db
# from telegram.error import NetworkError, Unauthorized
import pymysql
import keyboards


ADDRESS, PERSONS, COMPLEX, DISHES, DIET, TIME, COST = range(7)

# dispatcher = telegram.ext.Dispatcher(bot, None, workers=0, use_context=True)


REQUEST_KWARGS={
    'proxy_url': 'socks4://171.103.9.22:4145/',
    # Optional, if you need authentication:
    'urllib3_proxy_kwargs': {
        'assert_hostname': 'False',
        'cert_reqs': 'CERT_NONE'
        # 'username': 'user',
        # 'password': 'password'
    }
}



def start(update, context):  # создаем функцию и передаем ей update
    if db.users_app_id(update.message.chat.id) is not 0:
        user_fav_adds = db.users_app_id(update.message.chat.id)  # получаем адреса пользователя из БД
        keyboard_adds = list(user_fav_adds)  # создаем список кнопок
        update.message.reply_text('Здравствуйте ' + update.message.chat.first_name + '!')  # приветствие
        update.message.reply_text('Выберите или введите свой адрес:',  # отправляем клавиатуру с адресами
                              reply_markup=telegram.ReplyKeyboardMarkup(keyboard_adds, one_time_keyboard=True))
    else:
        print("новый юзерь")
        update.message.reply_text('Приятно познакомиться ' + update.message.chat.first_name + '!\nВведите пожалуйста свой адрес:')  # приветствие

    return ADDRESS

def address_handler(update, context):
    keyboard_pers = [['1', '2'], ['3', '4']]
    address = update.message.text
    user_id = update.message.chat.id
    if db.adds_check(address, user_id) != 1:
        db.adds_update(address, user_id)
    update.message.reply_text('Ваш адрес '+address)
    update.message.reply_text('\n Укажите количество персон:', reply_markup = telegram.ReplyKeyboardMarkup(keyboard_pers, one_time_keyboard=True))

    return PERSONS


def persons_handler(update, context):
    persons=update.message.text
    keyboard_complex = [['Завтрак', 'Обед'], ['Перекус', 'Ужин'], ['Хочу есть']]
    update.message.reply_text("Вас будет "+persons)
    update.message.reply_text('\n Укажите комплекс:',
                              reply_markup=telegram.ReplyKeyboardMarkup(keyboard_complex, one_time_keyboard=True))

    return COMPLEX

def complex_handler(update, context):
    complex=update.message.text
    keyboard_dishes = [['Диеты', 'Популярное']]
    update.message.reply_text("Вы решили приготовить на "+complex)

    update.message.reply_text("СПИСОК РЕЦЕПТОВ", reply_markup=dishes_inline_keyboard())
    update.message.reply_text('\n Укажите какие блюда вы хотите приготовить:',
                              reply_markup=telegram.ReplyKeyboardMarkup(keyboard_dishes, one_time_keyboard=True))

    return DISHES


def dishes_handler(update, context):
    dishes = update.message.text
    keyboard_diet = [['Правильное питание', 'Веган'], ['Здоровый образ жизни', 'Каллорийная диета']]
    update.message.reply_text("Вы хотите выбрать блюжа по " + dishes)
    update.message.reply_text('\n Укажите какой диете вы хотите следовать сегодня:',
                              reply_markup=telegram.ReplyKeyboardMarkup(keyboard_diet, one_time_keyboard=True))

    return DIET


def diet_handler(update, context):
    diet = update.message.text
    keyboard_time = [['15 минут', '30 минут'], ['1 час', '1,5 часа']]
    update.message.reply_text("О, как классно что вы придерживаетесь " + diet)
    update.message.reply_text('\n Сколько вы можете потратить времени на приготовление блюда?',
                              reply_markup=telegram.ReplyKeyboardMarkup(keyboard_time, one_time_keyboard=True))

    return TIME

def time_handler(update, context):
    time = update.message.text
    keyboard_cost = [['150 руб', '400 руб'], ['700 руб', '1000 руб']]
    update.message.reply_text("Ок. У нас есть ровно " + time)
    update.message.reply_text('\n Укажите ваш бюджет на данный прием пищи:',
                                  reply_markup=telegram.ReplyKeyboardMarkup(keyboard_cost, one_time_keyboard=True))

    return COST

def cost_handler(update, context):
    cost = update.message.text
    update.message.reply_text("Нам точно хватит " + cost)
    update.message.reply_text('Пошел искать продукты, я быстро!')

    print("conv_handler закончился")
    return telegram.ext.ConversationHandler.END


def cancel_handler(update, context):
    update.message.reply_text("До скорой встречи, до скорой встречи!")


CALLBACK_BUTTON1_TIME = 'callback_button1_time'
CALLBACK_BUTTON2_COST = 'callback_button2_cost'
CALLBACK_BUTTON3_NEXT = 'callback_button3_next'
CALLBACK_BUTTON4_PREV = 'callback_button4_prev'


TITLES = {
    CALLBACK_BUTTON1_TIME: "Время",
    CALLBACK_BUTTON2_COST: "Цена",
    CALLBACK_BUTTON3_NEXT: "Next",
    CALLBACK_BUTTON4_PREV: "Prev"
}


def dishes_inline_keyboard():
    keyboard = [
        [
            telegram.InlineKeyboardButton(TITLES[CALLBACK_BUTTON1_TIME], callback_data=CALLBACK_BUTTON1_TIME),
            telegram.InlineKeyboardButton(TITLES[CALLBACK_BUTTON2_COST], callback_data=CALLBACK_BUTTON2_COST),
        ],
        [
            telegram.InlineKeyboardButton(TITLES[CALLBACK_BUTTON3_NEXT], callback_data=CALLBACK_BUTTON3_NEXT),
            telegram.InlineKeyboardButton(TITLES[CALLBACK_BUTTON4_PREV], callback_data=CALLBACK_BUTTON4_PREV),
        ]
    ]
    return telegram.InlineKeyboardMarkup(keyboard)


def dishes_callback_handler(update, context, chat_data = None, **kwargs):
    query = update.callback_query
    data = query.data

    if data == CALLBACK_BUTTON1_TIME:
        # return TIME
        print("Была нажата кнопка Time")
    elif data == CALLBACK_BUTTON2_COST:
        print("Была нажата кнопка Cost")
    elif data == CALLBACK_BUTTON3_NEXT:
        print("Была нажата кнопка Next")
    elif data == CALLBACK_BUTTON4_PREV:
        print("Была нажата кнопка Prev")



def main():
    bot = Bot(config.token, base_url='https://telegg.ru/orig/bot')
    updater = Updater(bot=bot, use_context=True,request_kwargs=REQUEST_KWARGS)
    print("start")
    conv_handler = telegram.ext.ConversationHandler(
        entry_points=[
            telegram.ext.CommandHandler("start", start)
        ],
        states={
            ADDRESS: [
                telegram.ext.MessageHandler(telegram.ext.Filters.text, address_handler, pass_user_data=True)
            ],
            PERSONS: [
                telegram.ext.MessageHandler(telegram.ext.Filters.text, persons_handler, pass_user_data=True)
            ],
            COMPLEX: [
                telegram.ext.MessageHandler(telegram.ext.Filters.text, complex_handler, pass_user_data=True),

            ],
            DISHES: [
                telegram.ext.MessageHandler(telegram.ext.Filters.text, dishes_handler, pass_user_data=True)
            ],
            DIET: [
                telegram.ext.MessageHandler(telegram.ext.Filters.text, diet_handler, pass_user_data=True)
            ],
            TIME: [
                telegram.ext.MessageHandler(telegram.ext.Filters.text, time_handler, pass_user_data=True)
            ],
            COST: [
                telegram.ext.MessageHandler(telegram.ext.Filters.text, cost_handler, pass_user_data=True)
            ]
        },
        fallbacks =[
            telegram.ext.CommandHandler('cancel', cancel_handler)
        ]

    )
    test_handler = telegram.ext.CallbackQueryHandler(callback=dishes_callback_handler, pass_chat_data=True)
    updater.dispatcher.add_handler(test_handler)
    updater.dispatcher.add_handler(conv_handler)


    updater.start_polling()
    updater.idle()
    print("finish")


if __name__=="__main__":
    main()

