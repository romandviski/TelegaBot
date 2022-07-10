import gspread
from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup


# Указываем путь к JSON (права на доступ к драйву) """
account = gspread.service_account(filename='config/private_key.json')
# Открываем таблицу по ссылке
table = account.open_by_url('https://docs.google.com/spreadsheets/xxx')


available_boi_names = ["B_1", "B_2", "B_3", "B_4", "B_5", "B_6"]


class StatusChanger(StatesGroup):
    waiting_for_boi = State()
    waiting_for_shot = State()
    

async def changer_start(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for name in available_boi_names:
        keyboard.add(name)
    await message.answer("Выберите бой:", reply_markup=keyboard)
    await StatusChanger.waiting_for_boi.set()


# Обратите внимание: есть второй аргумент
async def boi_chosen(message: types.Message, state: FSMContext):
    if message.text not in available_boi_names:
        await message.answer("Пожалуйста, введите номер боя.")
        return
    await state.update_data(chosen_boi=message.text)
    
    # Для простых шагов можно не указывать название состояния, обходясь next()
    await StatusChanger.next()
    await message.answer("Выберите номер шота:", reply_markup=types.ReplyKeyboardRemove())


async def shot_chosen(message: types.Message, state: FSMContext):
    if not is_number(message.text):
        await message.answer("Пожалуйста, выберите номер шота.")
        return
    await state.update_data(chosen_shot=int(message.text.lower()))
    user_data = await state.get_data()
    boi = user_data['chosen_boi']
    shot = user_data['chosen_shot']
    await message.answer(str(boi) + ", " + str(shot), reply_markup=types.ReplyKeyboardRemove())
    await message.answer("Статус: " + check_status(boi, shot))
    await message.answer(check_comm(boi, shot))
    await message.answer("Ссылка на таблицу: ")
    await message.answer("https://docs.google.com/spreadsheets/xxx")
    await state.finish()


def register_handlers_status(dp: Dispatcher):
    dp.register_message_handler(changer_start, commands="status", state="*")
    dp.register_message_handler(boi_chosen, state=StatusChanger.waiting_for_boi)
    dp.register_message_handler(shot_chosen, state=StatusChanger.waiting_for_shot)



""" ===== Вспомогательные функции ===== """
def is_number(str):
    try:
        float(str)
        return True
    except ValueError:
        return False

""" ===== Функции для гугл таблиц ===== """
def check_status(x, y): # запрос статуса из ячейки
    worksheet = table.worksheet(str(x))
    cell = worksheet.find(str(x) + "_" + str(y))
    myString = worksheet.cell(cell.row, cell.col + 2).value
    if myString in (None, ''):
        return "Статус пустой"
    return myString

def check_comm(x, y): # запрос статуса из ячейки
    worksheet = table.worksheet(str(x))
    cell = worksheet.find(str(x) + "_" + str(y))
    myString = worksheet.cell(cell.row, cell.col + 3).value
    if myString in (None, ''):
        return "Комментарий пустой"
    return myString
