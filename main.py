import telebot

TOKEN = '6917176054:AAF4JJIKM3za-VRtlyeo4xtVBWDbY2yoFFc'

bot = telebot.TeleBot(TOKEN)

time_slots = {
    "10:00": None,
    "12:00": None,
    "13:00": None,
    "15:00": None,
    "16:00": None,
    "17:00": None
}

user_slot = ''


@bot.message_handler(commands=['start'])
def start(message):
    image1 = open('imgs/img1.jpg', 'rb')
    # vid1 = open('vids/vid1.mp4', 'rb')
    bot.send_photo(message.chat.id, image1, 'Это отпуск на Мальдивах')
    bot.send_photo(message.chat.id, 'https://sportishka.com/uploads/posts/2023-12/1702131190_sportishka-com-p-krasivie-mesta-v-prirode-oboi-3.jpg')


    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    markup.row("10:00", "12:00", "13:00")
    markup.row("15:00", "16:00", "17:00")
    bot.send_message(message.chat.id, "Выберите время тренировки", reply_markup=markup)


@bot.message_handler(func=lambda message: message.text in time_slots and time_slots[message.text] is None)
def get_name(message:telebot.types.Message):
    slot = message.text
    global user_slot
    user_slot = slot
    markup = telebot.types.ReplyKeyboardRemove()
    bot.send_message(message.chat.id, f"Вы выбрали {slot}. Теперь введите ваше имя:")
    bot.register_next_step_handler(message, get_phone)

def get_phone(message):
    name = message.text
    bot.send_message(message.chat.id, "Введите ваш номер телефона (11 цифр без разделителей):")
    bot.register_next_step_handler(message, validate_phone, name)

def validate_phone(message, name):
    phone = message.text
    if not phone.isdigit() or len(phone) != 11:
        bot.send_message(message.chat.id, "Некорректный формат номера телефона. Пожалуйста введите 11 цифр без разделителей. Например, 88005550000")
        bot.register_next_step_handler(message, validate_phone, name)
        return

    time_slots[user_slot] = {'name': name, 'phone': phone}
    bot.send_message(message.chat.id, f"Вы успешно зареганы на {user_slot}. С вами скоро свяжутся для подтверждения.")

    bot.send_message(6632558533, f'Новая регистрация на тренировку:\nИмя: {name}\nНомер: `+{phone}`\nВремя: {user_slot}', parse_mode='MarkdownV2')


bot.polling()
