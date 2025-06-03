# imports
import telebot
from telebot import types
import os
import random
import config  # Файл с конфигурационными данными (токен бота и т.д.)



# Инициализация бота
bot = telebot.TeleBot(config.TOKEN)

progress = 0

# handle /start
@bot.message_handler(commands=['start'])
def send_start(message):
    start_text = f"""
Добро пожаловать, {message.from_user.first_name}!
Этот бот может помочь каждому осуществить свой вклад в решение проблемы глобального потепления на планете!
                """

    bot.send_message(message.chat.id, start_text)
    


@bot.message_handler(commands=['help'])
def send_help_message(message):
    help_text = """
< 0 0 >  Небольшая справка о работе с ботом  < 0 0 >  
Доступные команды:
/start - Начало работы с ботом
/help - Получить справку
/about - Информация о боте
/task - Ежедневные задания
/materials - Образовательные материалы
/done - Отметка выполненного задания
""" 
    bot.send_message(message.chat.id, help_text)


@bot.message_handler(commands=['task'])
def send_random_task(message):
    global today_task
    tasks_list = ['Сегодня постарайся вюключать за собой свет, когда выходишь из комнаты.', 
                'Сегодня попробуй использовать меньше воды, чем ты использовал до этого',
                'У меня для тебя челлендж! Выключи воду пока ты чистишь зубы!',
                'Сегодня пробуй выкидывать мусор в урну, а не бросать его на улице!)',
                'Будет круто, если сегодня ты выбросишь мусор в сортировочный контейнер!',
                'Пройдись-ка сегодня пешком, на транспорте ты еще успеешь покататься!', 
                ]
    


    # Создаем Inline-клавиатуру
    markup = types.InlineKeyboardMarkup()
    
    # Добавляем кнопку с текстом
    button = types.InlineKeyboardButton("👍Хорошо!", callback_data="button_clicked")
    markup.add(button)  # Добавляем кнопку в клавиатуру
    
    today_task = random.choice(tasks_list)
    bot.send_message(message.chat.id, "(:!ЗАДАНИЕ НА ДЕНЬ!:)\n\n" + today_task + "\n\nИменно так ты поможешь человечеству справиться с проблемой глобального потепления", reply_markup=markup)



@bot.message_handler(commands=['materials'])
def send_materials(message):
    pre_materials_text = "Ниже в сообщении будет несколько интересных статей о глобальном потеплении! Уверен, что ты не пожалеешь, если ознакомишься!\n\n!Welcome!"
    materials_text = """
1. NASA – Climate Change: Vital Signs of the Planet
🔗 https://climate.nasa.gov/
📌 Официальный сайт NASA с актуальными данными о климате, графиками, статьями и интерактивными картами. Здесь можно найти информацию о причинах и последствиях глобального потепления, а также о мерах по его смягчению.

2. IPCC (Межправительственная группа экспертов по изменению климата)
🔗 https://www.ipcc.ch/
📌 Официальный сайт IPCC, где публикуются научные доклады о климатических изменениях. Здесь собраны самые авторитетные исследования по теме, включая прогнозы и рекомендации для политиков.

3. National Geographic – Climate Change
🔗 https://www.nationalgeographic.com/environment/topic/climate-change
📌 Статьи, фоторепортажи и видео о глобальном потеплении в доступном формате. National Geographic объясняет сложные процессы простым языком и показывает реальные последствия изменения климата.

4. NOAA Climate.gov
🔗 https://www.climate.gov/
📌 Сайт Национального управления океанических и атмосферных исследований (США) с данными о климатических трендах, интерактивными картами и образовательными материалами.

5. BBC Future – Climate Change
🔗 https://www.bbc.com/future/tags/climate-change
📌 Подборка статей и аналитики от BBC о климатических изменениях, новых технологиях и решениях экологических проблем.

6. Carbon Brief
🔗 https://www.carbonbrief.org/
📌 Сайт с глубоким анализом климатической политики, научных исследований и дебатов вокруг глобального потепления. Особенно полезен для понимания связи между экономикой и экологией.

7. WWF – Climate Change
🔗 https://www.worldwildlife.org/threats/effects-of-climate-change
📌 Всемирный фонд дикой природы рассказывает о влиянии потепления на биоразнообразие и о том, как можно снизить антропогенное воздействие."""
    bot.send_message(message.chat.id, pre_materials_text)
    bot.send_message(message.chat.id, materials_text)


@bot.callback_query_handler(func=lambda call: True)
def handle_button_click(call):
    global today_task
    if call.data == "button_clicked":
        # Ответим в всплывающем уведомлении (alert)
        bot.answer_callback_query(call.id, "Удачи!")
        

        # Изменим исходное сообщение
        bot.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            text= today_task + "\n\nУверен, что у тебя все получится!!!",
            reply_markup=None  # Убираем клавиатуру после нажатия
        )



@bot.message_handler(commands=['done'])
def mark_done_task(message): 
    global progress
    progress += 1
    bot.send_message(message.chat.id, "ВЫ выполнили задание! ВЫ огромный молодей!\n Вы продвигаетесь в своей линии прогресса на целую единицу!" +  "\n\nВаш прогресс: " + str(progress))




# Запуск бота
if __name__ == '__main__':
    print("Бот запущен!")
    bot.infinity_polling()
