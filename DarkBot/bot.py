import telebot
import random
from config import token

# Пример класса Car для дополнительного задания
class Car:
    def __init__(self, color: str, brand: str):
        self.color = color
        self.brand = brand

    def info(self) -> str:
        return f"Машина: {self.brand}, цвет: {self.color}"

bot = telebot.TeleBot(token)

# Обработчик команды /start
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, (
        "Привет! Я бот-эхо.\n"
        "Используй /info для получения информации обо мне.\n"
        "Попробуй команду /joke или /car <цвет> <марка>!"
    ))

# Обработчик команды /info
@bot.message_handler(commands=['info'])
def send_info(message):
    bot.reply_to(message, (
        "Это бот, который отвечает на сообщения и обрабатывает фото.\n"
        "Версия 1.1. Автор: ваш_никнейм\n"
        "Отправь фото, и я отвечу file_id!"
    ))

# Обработчик команды /joke - возвращает случайную шутку
@bot.message_handler(commands=['joke'])
def send_joke(message):
    jokes = [
        "Почему программисты любят природу? Потому что там нет багов! 🐛❌",
        "Как программист называет кота? NullPointerException! 😹",
        "— Я решил заняться спортом! — Ага, ты решил спортом заниматься. 😆",
    ]
    joke = random.choice(jokes)
    bot.reply_to(message, joke)

# Обработчик команды /car - создаёт объект Car и возвращает его info()
@bot.message_handler(commands=['car'])
def send_car_info(message):
    args = telebot.util.extract_arguments(message.text).split()
    if len(args) >= 2:
        color = args[0]
        brand = ' '.join(args[1:])
        car = Car(color, brand)
        bot.reply_to(message, car.info())
    else:
        bot.reply_to(message, "Использование: /car <цвет> <марка>")

# Обработчик сообщений с вложенным фото
@bot.message_handler(content_types=['photo'])
def handle_photo(message):
    file_id = message.photo[-1].file_id
    bot.reply_to(message, f"Фото получено! file_id: {file_id}\nСпасибо за фото! 📸")

# Эхо-обработчик для всех остальных сообщений
@bot.message_handler(func=lambda m: True)
def echo_all(message):
    bot.reply_to(message, message.text)

if __name__ == '__main__':
    bot.polling(none_stop=True)
