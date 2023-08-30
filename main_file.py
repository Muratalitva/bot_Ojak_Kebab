from aiogram import Bot, Dispatcher, types, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.storage import FSMContext
from aiogram.dispatcher.filters.state import State, FSMContext
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
from config import token
import logging, sqlite3

bot = Bot(token)
dp = Dispatcher(bot)

buttons = [
    KeyboardButton("Меню"),
    KeyboardButton("О нас"),
    KeyboardButton("Адрес"),
    KeyboardButton("Заказать еду"),
]

butts = ReplyKeyboardMarkup().add(*buttons)

@dp.message_handler(commands='start')
async def start(message:types.Message):
    await message.answer("Привет это бот Ожак Кебаб!", reply_markup=butts)

@dp.message_handler(text="Меню")
async def about_us(message:types.Message):
    await message.answer("Вали кебаб на 4 человек - 3200 с\nШефим кебаб 420 с\nСимит кебаб 420 с\nФорель на мангале целиком 700 с")

@dp.message_handler(text="О нас")
async def about_us(message:types.Message):
    await message.answer("Кафе Ожак Кебап на протяжении 18 лет радует своих гостей с изысканными турецкими блюдами в особенности своим кебабом. Наше кафе отличается от многих кафе своими доступными ценами и быстрым сервисом. В 2016 году по голосованию на сайте Horeca были удостоены Лучшее кафе на каждый день и мы стараемся оправдать доверие наших гостей. Мы не добавляем консерванты, усилители вкуса, красители, ароматизаторы, растительные и животные жиры, вредные добавки с маркировкой «Е». У нас строгий контроль качества: наши филиалы придерживаются норм Кырпотребнадзор и санэпидемстанции. Мы используем только сертифицированную мясную и рыбную продукцию от крупных поставщиков.")

@dp.message_handler(text="Адрес")
async def about_us(message:types.Message):
    await message.answer("Фаиза, Бегемот, Дияр, Burger House, Чайхана Navat, Ассорти Бухара")

class Orders(StatesGroup):
    name = State()
    phone = State()
    adress = State()

@dp.message_handler(text="Заказать еду")
async def about_us(message:types.Message):
    await message.answer("Оставьте ваши данные для доставки")
    await message.answer("Ваше имя:")
    await Orders.name.set()

@dp.message_handler(state=Orders.name)
async def get_phone_number(message:types.Message, state):
    await state.update_data(name=message.text)
    await message.answer("Ваш телефонный номер:")
    await Orders.phone.set()

@dp.message_handler(state=Orders.phone)
async def get_address(message:types.Message, state):
    await state.update_data(phone=message.text)
    await message.answer("Адрес доставки:")
    await Orders.address.set()

@dp.message_handler(state=EnrollState.course)
async def get_all(message:types.Message, state:FSMContext):
    await state.update_data(course=message.text)
    res = await storage.get_data(user=message.from_user.id)
    print(res)
    await bot.send_message(-940254780, f"Заявка на закак\nИмя: {res['name']}\nНомер: {res['phone']}\nАдрес: {res['address']}")
    await message.answer("Данные были успешно записаны, скоро с вами свяжутся")
executor.start_polling(dp)