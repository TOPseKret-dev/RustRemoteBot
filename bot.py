import threading
from time import sleep
import os
import telebot
from telebot import types
from game_controls import (
    launch_rust, anti_afk, auto_server_in, trader_mode, shutdown_pc, is_rust_running
)
from utils import log_action

from config import BOT_TOKEN, CHAT_ID

bot = telebot.TeleBot(BOT_TOKEN)

# Используем словарь-флаги для контроля запущенных функций
run_flags = {
    "anti_afk": False,
    "trader": False,
    "auto_server": False
}
# Флаг, что бот ждет ввод IP сервера
server_input_flag = {"active": False}

standard_markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
standard_markup.add("Включить ПК")
standard_markup.add("Получить скриншот")
standard_markup.add("Авто заход на сервер")
standard_markup.add("Анти афк")
standard_markup.add("Режим 'Трейдер Валера'")
standard_markup.add("Выключить бота")
standard_markup.add("Alt F4")
standard_markup.add("Выключить ПК")

def send_screenshot(message):
    try:
        from PIL import ImageGrab
        import tempfile
        path = os.path.join(tempfile.gettempdir(), 'screenshot.png')
        screen = ImageGrab.grab()
        screen.save(path, "PNG")
        bot.send_photo(message.chat.id, open(path, 'rb'))
    except Exception as e:
        bot.send_message(message.chat.id, "Ошибка создания скриншота")
        log_action(f"Ошибка в send_screenshot: {e}")

@bot.message_handler(commands=['start'])
def send_welcome(message):
    if message.chat.id == CHAT_ID:
        bot.send_message(message.chat.id, 'Бот готов к использованию', reply_markup=standard_markup)
    else:
        bot.send_message(message.chat.id, 'Вы не владелец данного ПК')

@bot.message_handler(func=lambda message: message.text.lower() == "включить пк")
def handle_power_on(message):
    if message.chat.id == CHAT_ID:
        bot.send_message(message.chat.id, 'ПК и так включен', reply_markup=standard_markup)
    else:
        bot.send_message(message.chat.id, 'Вы не владелец данного ПК')

@bot.message_handler(func=lambda message: message.text.lower() == "получить скриншот")
def handle_screenshot(message):
    if message.chat.id == CHAT_ID:
        send_screenshot(message)
    else:
        bot.send_message(message.chat.id, 'Вы не владелец данного ПК')

@bot.message_handler(func=lambda message: message.text.lower() == "выкл анти афк")
def handle_stop_afk(message):
    if message.chat.id == CHAT_ID:
        if run_flags["anti_afk"]:
            run_flags["anti_afk"] = False
            bot.send_message(message.chat.id, "Выключаю анти афк", reply_markup=standard_markup)
        else:
            bot.send_message(message.chat.id, "Анти афк уже выключено", reply_markup=standard_markup)
    else:
        bot.send_message(message.chat.id, 'Вы не владелец данного ПК')

@bot.message_handler(func=lambda message: message.text.lower() == "авто заход на сервер")
def handle_auto_server(message):
    if message.chat.id == CHAT_ID:
        server_input_flag["active"] = True
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add("Включить ПК")
        markup.add("Получить скриншот")
        markup.add("Выкл авто заход на сервер")
        markup.add("Выключить бота")
        markup.add("Alt F4")
        markup.add("Выключить ПК")
        bot.send_message(message.chat.id, "Введите IP сервера", reply_markup=markup)
    else:
        bot.send_message(message.chat.id, 'Вы не владелец данного ПК')

@bot.message_handler(func=lambda message: message.text.lower() == "выкл авто заход на сервер")
def handle_stop_auto_server(message):
    if message.chat.id == CHAT_ID:
        run_flags["auto_server"] = False
        server_input_flag["active"] = False
        bot.send_message(message.chat.id, "Выключаю автозаход", reply_markup=standard_markup)
    else:
        bot.send_message(message.chat.id, 'Вы не владелец данного ПК')

@bot.message_handler(func=lambda message: message.text.lower() == "анти афк")
def handle_afk(message):
    if message.chat.id == CHAT_ID:
        if run_flags["trader"]:
            bot.send_message(message.chat.id, "Режим Трейдера уже включен", reply_markup=standard_markup)
        elif run_flags["anti_afk"]:
            bot.send_message(message.chat.id, "Анти афк уже включено", reply_markup=standard_markup)
        else:
            run_flags["anti_afk"] = True
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            markup.add("Включить ПК")
            markup.add("Получить скриншот")
            markup.add("Выкл анти афк")
            markup.add("Выключить бота")
            markup.add("Выключить ПК")
            bot.send_message(message.chat.id, "Включаю анти афк", reply_markup=markup)
            threading.Thread(target=anti_afk, args=(message, bot, run_flags)).start()
    else:
        bot.send_message(message.chat.id, 'Вы не владелец данного ПК')

@bot.message_handler(func=lambda message: message.text.lower() == "выкл трейдера")
def handle_stop_trader(message):
    if message.chat.id == CHAT_ID:
        if run_flags["trader"]:
            run_flags["trader"] = False
            bot.send_message(message.chat.id, "Выключаю Трейдера", reply_markup=standard_markup)
            sleep(3)
        else:
            bot.send_message(message.chat.id, "Режим Трейдера уже выключен", reply_markup=standard_markup)
    else:
        bot.send_message(message.chat.id, 'Вы не владелец данного ПК')

@bot.message_handler(func=lambda message: message.text.lower() == "режим 'трейдер валера'")
def handle_trader(message):
    if message.chat.id == CHAT_ID:
        if run_flags["trader"]:
            bot.send_message(message.chat.id, "Трейдер уже включен", reply_markup=standard_markup)
        else:
            # Отключаем анти афк, если он был запущен
            run_flags["anti_afk"] = False
            run_flags["trader"] = True
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            markup.add("Включить ПК")
            markup.add("Получить скриншот")
            markup.add("Выкл трейдера")
            markup.add("Выключить бота")
            markup.add("Выключить ПК")
            bot.send_message(message.chat.id, "Трейдер включен", reply_markup=markup)
            threading.Thread(target=trader_mode, args=(message, bot, run_flags)).start()
    else:
        bot.send_message(message.chat.id, 'Вы не владелец данного ПК')

@bot.message_handler(func=lambda message: message.text.lower() == "alt f4")
def handle_alt_f4(message):
    if message.chat.id == CHAT_ID:
        try:
            from pynput.keyboard import Controller, Key
            keyboard = Controller()
            keyboard.press(Key.alt)
            keyboard.press(Key.f4)
            sleep(0.1)
            keyboard.release(Key.f4)
            keyboard.release(Key.alt)
            bot.send_message(message.chat.id, "Комбинация Alt+F4 выполнена", reply_markup=standard_markup)
        except Exception as e:
            bot.send_message(message.chat.id, "Ошибка при выполнении Alt+F4", reply_markup=standard_markup)
    else:
        bot.send_message(message.chat.id, 'Вы не владелец данного ПК')

@bot.message_handler(func=lambda message: message.text.lower() == "выключить бота")
def handle_bot_shutdown(message):
    if message.chat.id == CHAT_ID:
        bot.send_message(message.chat.id, "Выключаюсь...", reply_markup=standard_markup)
        os._exit(0)
    else:
        bot.send_message(message.chat.id, 'Вы не владелец данного ПК')

@bot.message_handler(func=lambda message: message.text.lower() == "выключить пк")
def handle_shutdown_pc(message):
    if message.chat.id == CHAT_ID:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add("Подтверждаю")
        markup.add("Отмена")
        bot.send_message(message.chat.id, "Вы уверены? Несохраненные данные исчезнут", reply_markup=markup)
        run_flags["anti_afk"] = False
        run_flags["trader"] = False
    else:
        bot.send_message(message.chat.id, 'Вы не владелец данного ПК')

@bot.message_handler(func=lambda message: message.text.lower() == "отмена")
def handle_cancel(message):
    if message.chat.id == CHAT_ID:
        bot.send_message(message.chat.id, "Операция отменена, все функции выключены", reply_markup=standard_markup)
    else:
        bot.send_message(message.chat.id, 'Вы не владелец данного ПК')

@bot.message_handler(func=lambda message: message.text.lower() == "подтверждаю")
def handle_confirm_shutdown(message):
    if message.chat.id == CHAT_ID:
        shutdown_pc(message, bot)
    else:
        bot.send_message(message.chat.id, 'Вы не владелец данного ПК')

@bot.message_handler(func=lambda message: True)
def handle_text(message):
    if message.chat.id == CHAT_ID:
        # Если бот ждет IP сервера
        if server_input_flag["active"]:
            server_input_flag["active"] = False
            run_flags["auto_server"] = True
            threading.Thread(target=auto_server_in, args=(message, bot, message.text)).start()
        else:
            if not is_rust_running():
                if launch_rust():
                    bot.send_message(message.chat.id, "Запускаю Rust")
            else:
                bot.send_message(message.chat.id, "Rust уже запущен")
            try:
                from pynput.keyboard import Controller, Key
                keyboard = Controller()
                import pynput.mouse
                mouse = pynput.mouse.Controller()
                mouse.position = (960, 540)
                mouse.click(pynput.mouse.Button.left)
                sleep(1)
                keyboard.press(Key.f1)
                keyboard.release(Key.f1)
                command = f"connect {message.text}"
                sleep(1)
                keyboard.type(command)
                keyboard.press(Key.enter)
                keyboard.release(Key.enter)
                keyboard.press(Key.f1)
                keyboard.release(Key.f1)
                bot.send_message(message.chat.id, "Встал в очередь")
                sleep(3)
                send_screenshot(message)
            except Exception as e:
                bot.send_message(message.chat.id, "Ошибка при попытке входа на сервер")
                log_action(f"Ошибка в handle_text: {e}")
    else:
        bot.send_message(message.chat.id, 'Вы не владелец данного ПК')

if __name__ == '__main__':
    while True:
        try:
            bot.polling(none_stop=True, interval=0)
        except Exception as e:
            log_action(f"Ошибка ТГ бота: {e}")
            sleep(10)
