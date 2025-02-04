import logging
import os
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram import Bot, Dispatcher, types
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.fsm.state import State
from aiogram.fsm.state import StatesGroup
from aiogram.fsm.context import FSMContext
from dotenv import load_dotenv
from bot_class import EventBot

# loads environment variables, initializes bot, dispatcher, and logging
load_dotenv()
TOKEN = os.getenv('TOKEN')
bot = Bot(token=TOKEN)
dp = Dispatcher()
logging.basicConfig(level=logging.INFO)
logging.info("starting bot")

# creates an instance of EventBot
bot_instance = EventBot()


# FSM class to track user states and handle command duplication during interaction.
class Form(StatesGroup):
    category = State()
    date = State()
    location = State()


# Creates an inline keyboard with buttons based on the provided options
# and sets callback data for each button based on the category.
def create_keyboard(categories, category_type):
    keyboard_buttons = [[InlineKeyboardButton(text=category, callback_data=f'{category_type}_{category}')] for category
                        in categories]
    # attaches restart button to every keyboard
    keyboard_buttons.append([InlineKeyboardButton(text="🔄НАЧАТЬ ЗАНОВО🔄", callback_data="start_over")])
    keyboard = InlineKeyboardMarkup(inline_keyboard=keyboard_buttons)
    return keyboard


# handles the /start command and initializes the interaction flow
@dp.message(Command("start"))
async def start_handler(message: Message, state: FSMContext):
    await state.set_state(Form.category)
    bot_instance.open_main_page()
    categories = bot_instance.get_categories_list()
    # creates keyboard based on received list
    keyboard = create_keyboard(categories, 'category')
    # passes keyboard to the user
    await message.answer('Привет! Выбери категорию мероприятия из списка:', reply_markup=keyboard)


# handles the 'start_over' command: resets the state and passes the keyboard with categories
@dp.callback_query(lambda c: c.data == 'start_over')
async def start_over(callback: types.CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.message.answer("Начинаем новый поиск...")
    bot_instance.open_main_page()
    categories = bot_instance.get_categories_list()
    keyboard = create_keyboard(categories, 'category')
    await callback.message.answer('Выбери категорию мероприятия из списка:', reply_markup=keyboard)
    await state.set_state(Form.category)  # changes state to category selecting


# handles the event category selection and passes the keyboard with available dates
@dp.callback_query(lambda c: c.data and c.data.startswith('category_'))
async def category_handler(callback_data: types.CallbackQuery, state: FSMContext):
    category = callback_data.data.split('category_')[1]
    await callback_data.message.answer(f'Выбор: {category}')
    bot_instance.open_selected_category(category)

    await state.set_state(Form.date)  # changes state to date selecting
    available_dates = bot_instance.get_available_dates()
    dates_keyboard = create_keyboard(available_dates, 'date')
    await callback_data.message.answer('Выбери дату из списка:', reply_markup=dates_keyboard)


# handles the date selection and passes the keyboard with available locations
@dp.callback_query(lambda c: c.data and c.data.startswith('date_'))
async def date_handler(callback_data: types.CallbackQuery, state: FSMContext):
    date = callback_data.data.split('date_')[1]
    await callback_data.message.answer(f'Выбор: {date}')  # new

    # checks if the date is available to selection
    if bot_instance.select_date(date):
        await state.set_state(Form.location)  # changes state to location selecting
        available_locations = bot_instance.get_locations_list()
        locations_keyboard = create_keyboard(available_locations, 'location')
        await callback_data.message.answer('Выбери локацию из списка:', reply_markup=locations_keyboard)
    else:
        await callback_data.message.answer('Не найдено информации о мероприятиях на выбранную дату. Поробуй снова.')
        await start_over(callback_data, state)


# handles the date selection, displays result information and offers to start over
@dp.callback_query(lambda c: c.data and c.data.startswith('location_'))
async def location_handler(callback_data: types.CallbackQuery):
    location = callback_data.data.split('location_')[1]
    await callback_data.message.answer(f'Выбор: {location}')  # new
    bot_instance.select_location(location)

    result = bot_instance.get_result_events()
    if result is False:
        result_message = 'Ничего не найдено'
    else:
        result_message = '\n'.join(result)

    await callback_data.message.answer(f"Найденные события для {location}:\n\n{result_message}")
    # creates and passes the keyboard for a new search
    start_button = [[InlineKeyboardButton(text="Новый поиск", callback_data="start_over")]]
    start_keyboard = InlineKeyboardMarkup(row_width=1, inline_keyboard=start_button)
    await callback_data.message.answer('Нажми кнопку, чтобы начать новый поиск:', reply_markup=start_keyboard)
