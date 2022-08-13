from aiogram import types


class KeyButton:
    def __init__(self):
        self.keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        self.keyboard2 = types.ReplyKeyboardMarkup(resize_keyboard=True)
        self.keymap = types.InlineKeyboardMarkup()

    def hello_message(self):
        button = self.keyboard.add(types.KeyboardButton(text="/menu"))
        return button

    def get_location(self):
        button = self.keyboard.add(types.KeyboardButton(text="Send", request_location=True))
        return button

    def menu_message(self):
        button = self.keyboard.add(types.KeyboardButton(text=".send_location")).add(types.KeyboardButton("text"))
        return button

    def test(self):
        inline_button = types.InlineKeyboardButton('test!', callback_data='test_button')
        button = self.keymap.add(inline_button)
        return button

    def adminsRoot(self):
        self.keymap.clean()
        button = self.keymap.add(types.InlineKeyboardButton("Нажми на меня", callback_data="adminButton"))
        return button
