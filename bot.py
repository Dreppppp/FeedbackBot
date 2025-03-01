import telebot
from telebot import types

TOKEN = "7960653330:AAGVQwdxoM8ao_Exe37nU0Kws9eS8pKCMRc"
ADMIN_CHAT_ID = 1722040189

bot = telebot.TeleBot(TOKEN)

waiting_for_reply = {}

@bot.message_handler(commands=["start"])
def send_start(message):
    bot.send_message(message.chat.id, "CYBER GANG рад приветствовать тебя! Это бот для обратной связи с администратором CYBER GANG, отправь боту сообщение, и тебе ответят!")

@bot.message_handler(func=lambda message: message.chat.id != ADMIN_CHAT_ID and message.text)
def forward_to_admin(message):
    name = message.from_user.first_name
    username = f"@{message.from_user.username}" if message.from_user.username else "(без username)"
    text = message.text
    user_id = message.chat.id
    
    markup = types.InlineKeyboardMarkup(row_width=2)
    btn1 = types.InlineKeyboardButton(f"Ответить {name}", callback_data=f"btn1|{user_id}")
    btn2 = types.InlineKeyboardButton("Написать", callback_data=f"btn2|{username}")
    markup.add(btn1, btn2)
    
    # Отправить подтверждение пользователю
    bot.send_message(message.chat.id, "Сообщение успешно отправлено администратору CYBER GANG! Ожидайте ответа")
    
    # Переслать сообщение администратору
    bot.send_message(ADMIN_CHAT_ID, f"Сообщение от id: {user_id}, name: {name}, user: {username}\nСообщение: {text}", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: True)
def callback(call):
    callback_data = call.data.split('|')
    action = callback_data[0]
    
    if call.message:
        if action == "btn1":
            user_id = callback_data[1]
            bot.send_message(ADMIN_CHAT_ID, f"Ведите ответ пользователю с ID: {user_id}")
            waiting_for_reply[ADMIN_CHAT_ID] = user_id
            bot.answer_callback_query(call.id)

        elif action == "btn2":
            username = callback_data[1]
            bot.send_message(ADMIN_CHAT_ID, f"Click на {username}")

@bot.message_handler(func=lambda message: message.chat.id == ADMIN_CHAT_ID and message.text)
def handle_admin_reply(message):
    if message.chat.id in waiting_for_reply:
        user_id = waiting_for_reply[message.chat.id]
        text = message.text
        bot.send_message(user_id, f"Администратор ответил вам:  {text}")
        bot.send_message(ADMIN_CHAT_ID, f"Ваше сообщение '{message.text}' было отправлено пользователю с ID: {user_id}")
        del waiting_for_reply[message.chat.id]

bot.polling(none_stop=True)
