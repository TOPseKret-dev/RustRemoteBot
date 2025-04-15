import os
import psutil
from time import sleep
from pynput.keyboard import Controller as KeyboardController, Key
import pynput.mouse
from PIL import ImageGrab
from utils import log_action

keyboard = KeyboardController()
mouse = pynput.mouse.Controller()

def is_rust_running():
    for proc in psutil.process_iter(['name']):
        if proc.info['name'] and ('Rust.exe' in proc.info['name'] or 'RustClient.exe' in proc.info['name']):
            return True
    return False

def launch_rust():
    if not is_rust_running():
        log_action("Запускаю Rust через Steam...")
        os.system("start steam://rungameid/252490")
        sleep(50)
        return True
    else:
        log_action("Rust уже запущен")
        return False

def anti_afk(message, bot, run_flags):
    try:
        while run_flags["anti_afk"]:
            keyboard.press(Key.space)
            keyboard.release(Key.space)
            mouse.position = (1775, 1000)
            mouse.press(pynput.mouse.Button.left)
            mouse.release(pynput.mouse.Button.left)
            sleep(5)
    except Exception as e:
        bot.send_message(message.chat.id, "Ошибка анти афк")
        log_action(f"Ошибка в anti_afk: {e}")
        run_flags["anti_afk"] = False

def auto_server_in(message, bot, server_address):
    try:
        bot.send_message(message.chat.id, "Пытаюсь зайти на сервер")
        keyboard.press(Key.f1)
        keyboard.release(Key.f1)
        command = f"connect {server_address}"
        sleep(1)
        keyboard.type(command)
        keyboard.press(Key.enter)
        keyboard.release(Key.enter)
        keyboard.press(Key.f1)
        keyboard.release(Key.f1)
        sleep(2)
        while True:
            if ImageGrab.grab().load()[1492, 997] == (143, 50, 13):
                bot.send_message(message.chat.id, "Захожу на сервер")
                break
            else:
                mouse.position = (1251, 902)
                mouse.click(pynput.mouse.Button.left)
            sleep(1)
    except Exception as e:
        bot.send_message(message.chat.id, "Ошибка автозахода")
        log_action(f"Ошибка в auto_server_in: {e}")

def trader_mode(message, bot, run_flags):
    try:
        while run_flags["trader"]:
            mouse.position = (1770, 850)
            mouse.click(pynput.mouse.Button.left)
            keyboard.press(Key.shift)
            keyboard.press('w')
            sleep(0.00001)
    except Exception as e:
        bot.send_message(message.chat.id, "Ошибка трейдера")
        log_action(f"Ошибка в trader_mode: {e}")
        run_flags["trader"] = False

def shutdown_pc(message, bot):
    bot.send_message(message.chat.id, "Выключаю ПК")
    import os
    os.system("shutdown -f -s -t 0")
