import vk_api
from vk_api.longpoll import VkEventType, VkLongPoll
from vk_api.keyboard import VkKeyboardColor, VkKeyboard
import random

rand_id = random.randint(-22222222, +22222222)
zero_id = 0
token = 'cd49b26f8ce3ba8ad0308c76fecc0254afb670d4382b49d8bf2f5b97ea4e503659b672c45ec27669bd2b1'

vk_session = vk_api.VkApi(token=token)
longpoll = VkLongPoll(vk_session)
session_api = vk_session.get_api()

def create_keyboard():
    keyboard = VkKeyboard(one_time=True)

    keyboard.add_button('Привет', color=VkKeyboardColor.POSITIVE)
    keyboard.add_line()
    keyboard.add_button('Hello', color=VkKeyboardColor.PRIMARY)

    keyboard = keyboard.get_keyboard()
    return keyboard

def create_empty_keyboard():
    keyboard = VkKeyboard(one_time=True)
    keyboard = keyboard.get_empty_keyboard()
    return keyboard

def send_message(vk_session, user_id, text, random_id, attachment=None, keyboard=None):
    vk_session.method('messages.send', {'user_id' : user_id, 'message' : text, 'random_id' : random_id, 'attachment' : attachment, 'keyboard' : keyboard})

empty_keyboard = create_empty_keyboard()
for event in longpoll.listen():
    if event.type == VkEventType.MESSAGE_NEW:
        if event.from_user and not(event.from_me):
            send_message(vk_session, event.user_id, 'Hey', zero_id)
            keyboard = create_keyboard()
            send_message(vk_session, event.user_id, 'Поздоровайся!', rand_id,  keyboard=keyboard)
            response = event.text.lower()
            if response == 'hello' or response == 'Привет':
                send_message(vk_session, event.user_id, 'k', rand_id,  keyboard=empty_keyboard)

