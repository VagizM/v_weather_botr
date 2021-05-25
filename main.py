from auth import TG_KEY
import SQL
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from aiogram.types import ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, \
    InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData
from weather import get_coord_in_name,   \
                    get_weather_сurrent, \
                    get_weather_prognoz, \
                    get_air_one, get_weather_detail
from pprint import pprint
#last_name=""
cd = CallbackData("fab", "action", "name",'lon','lat')  # <= надо так

bot = Bot(token=TG_KEY, parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot)


def get_keboard_city(lat,lon,name,add:bool):
    buttons1 = [types.InlineKeyboardButton(text="прогноз на сегодня",            callback_data=cd.new(name=name,lon=lon,lat=lat, action="detailed")),
               types.InlineKeyboardButton(text="прогноз на 3 дня",              callback_data=cd.new(name=name,lon=lon,lat=lat, action="prognoz")),
               types.InlineKeyboardButton(text="Состояние воздуха",             callback_data=cd.new(name=name,lon=lon,lat=lat, action="air")),]
    if add:
        buttons2 =[types.InlineKeyboardButton(text="добавить в базу на расписание", callback_data=cd.new(name=name,lon=lon,lat=lat, action="add_base")),]
    else: 
        buttons2 =[types.InlineKeyboardButton(text="Удалить из базы на расписание", callback_data=cd.new(name=name,lon=lon,lat=lat, action="remove")),]           
    keyboard = types.InlineKeyboardMarkup(resize_keyboard=True, row_width=2)
    keyboard.add(*buttons1)
    keyboard.add(*buttons2)
    return keyboard

def get_key_main():
    key_main = ReplyKeyboardMarkup(resize_keyboard=True)
    key_main.add(KeyboardButton(text = "Текущие координаты",request_location=True))
    key_main.add(KeyboardButton(text = 'Список в БД'))
    return key_main

'''
def get_keboard_unknown(lat,lon,name):
    buttons = [types.inline_query.Location( text="Текущее местоположение", request_location=True,callback_data=cd.new(name=name,lon=lat,lat=lat, action="get_loc")) ]
                # фором перебрать города из базы 
               
    keyboard = types.InlineKeyboardMarkup(resize_keyboard=True, row_width=2)
    keyboard.add(*buttons)
    return keyboard

'''
@dp.message_handler(commands=["help"])
async def start_command(message: types.Message):
    await message.reply("""Это погодный бот.
    Напишите название города
    Умеет показывать погоду по городу, по координатам
    (запрашивает данные с телеграмм). Умеет присылать
    погоду по расписанию,/n
    Сюда меню с командами
    *список городов базе напоминания*</lb>
    *прогноз на послений город*</dp>""")
    
@dp.message_handler(content_types=['location'])
async def handle_loc(message):
    r = get_weather_сurrent(message['location']['latitude'],message['location']['longitude'])
    await message.reply(r,reply_markup=ReplyKeyboardRemove() )
    await message.answer("""Добавить callback клавиатуру на добавление текущего местоположения в базе
    types.InlineKeyboardButton(text="добавить в базу на расписание", callback_data=cd.new(name=name,lon=lat,lat=lat,action="add_base")),""" )

'''
'''
@dp.message_handler(text='Список в БД')
async def echo_message_baza(message: types.Message):
    result = SQL.get_records(message.from_user.id)
    print("echo_message_baza:", result)
    if result!=False:
        for r in result:
            print("echo_message_baza step: ", )
            st = get_weather_сurrent(r["lat"],r["lon"])
            await message.answer(f'Запись с ID{r["id"]} именем {r["name"]}, время напоминания {r["time"]}\n {st}', reply_markup=get_keboard_city(r["lat"],r["lon"],r["id"],False))  
    await message.answer(f'База пуста')  
@dp.message_handler()
async def echo_message(message: types.Message):
    result = get_coord_in_name(message.text)
    print(result)
    if result:
        #print(message.text)
        #print(result)
        await message.reply(get_weather_сurrent(result["lat"],result["lon"]), reply_markup=get_keboard_city(result["lat"],result["lon"],result["name"],True))  
    else:
        #print(message.text)
        await message.reply("""Город не найден
        добавить сюда клавиатуру с последними городами и запросом на локальные координаты""",reply_markup=get_key_main())
    # !!! Предложить пользователю передать координаты ???
 
'''
'''
@dp.callback_query_handler(cd.filter(action=["air"]))
async def repl_air(call: types.CallbackQuery, callback_data: dict):
    print(callback_data)
    await call.message.answer(get_air_one(callback_data['lat'],callback_data['lon']))
    
@dp.callback_query_handler(cd.filter(action=["detailed"]))
async def reply_detail(call: types.CallbackQuery, callback_data: dict):
    result= get_weather_detail(callback_data['lat'],callback_data['lon'])    
    for r in result:                         
        await call.message.answer(r)
       
@dp.callback_query_handler(cd.filter(action=["prognoz"]))
async def repli_prognoz(call: types.CallbackQuery, callback_data: dict):
    result = get_weather_prognoz(callback_data['lat'],callback_data['lon']) 
    for r in result:                         
        await call.message.answer(r)
        
@dp.callback_query_handler(cd.filter(action=["add_base"]))
async def repli_add_baze(call: types.CallbackQuery, callback_data: dict):
    print("repli_add_baze: callback_data ",callback_data)       
    result = SQL.add_base(call.from_user.id,callback_data['name'],callback_data['lat'],callback_data['lon'])
    print("repli_add_baze: result ",result)  
    if result:
        print("repli_add_baze: внесена  ", result)
        await call.message.answer(f"запись  {callback_data['name'] } внесена")
    else:
        print("repli_add_baze: типа дубль ")
        await call.message.answer(f'Запись есть в базе')
@dp.callback_query_handler(cd.filter(action=["remove"]))
async def repli_del_record(call: types.CallbackQuery, callback_data: dict):
    print("repli_del_record: callback_data ",callback_data)       
    result = SQL.del_record(callback_data['name'])
    print("repli_del_record: result ",result)  
    #if result:
        #print("repli_add_baze: внесена  ", result)
        #await call.message.answer(f"запись  {callback_data['name'] } внесена")
    #else:
        #print("repli_add_baze: типа дубль ")
        #await call.message.answer(f'Запись есть в базе')

'''
'''
def show():
    print("!!!!!!!!!!")
    pass
'''
@dp.callback_query_handler(cd.filter(action=["get_loc"]))
async def repli_location(call: types.CallbackQuery, callback_data: dict):
    await call.message.answer(MES)
'''
'''
'''
if __name__ == "__main__":
    SQL.creat_base()
    print("main: start Polling")
    executor.start_polling(dp)

    