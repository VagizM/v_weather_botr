from auth import TG_KEY
import SQL
import asyncio
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
import datetime

state_add_mark=" " # плохая реализация через переменную надо бы через State
cd = CallbackData("fab", "action", "name",'lon','lat','time')  # <= надо так
bot = Bot(token=TG_KEY, parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot)


def get_keboard_city(lat,lon,name,time=25,add=False):
    buttons1 = [types.InlineKeyboardButton(text="на сегодня",            callback_data=cd.new(name=name,lon=lon,lat=lat,time=time, action="detailed")),
               types.InlineKeyboardButton(text="на 3 дня",              callback_data=cd.new(name=name,lon=lon,lat=lat, time=time,action="prognoz")),
               types.InlineKeyboardButton(text="Состояние воздуха",             callback_data=cd.new(name=name,lon=lon,lat=lat,time=time,action="air")),]
    if add:
        buttons2 =[types.InlineKeyboardButton(text="добавить в базу на расписание", callback_data=cd.new(name=name,lon=lon,lat=lat,time=time, action="add_base")),]
    else: 
        buttons2 =[types.InlineKeyboardButton(text="Удалить из базы на расписание", callback_data=cd.new(name=name,lon=lon,lat=lat,time=time, action="remove")),]           
    keyboard = types.InlineKeyboardMarkup(resize_keyboard=True, row_width=2)
    keyboard.row(*buttons1)
    keyboard.add(*buttons2)
    return keyboard
def get_keboard_add(lat,lon,name,time=25,add=False):
    buttons2 =[types.InlineKeyboardButton(text="добавить в базу на расписание", callback_data=cd.new(name=name,lon=lon,lat=lat,time=time, action="add_base")),
               #types.InlineKeyboardButton(text="Повторить  ввод", callback_data=cd.new(name=name,lon=lon,lat=lat,time=time, action="ignored")),
               ]           
    keyboard = types.InlineKeyboardMarkup(resize_keyboard=True, row_width=2)
    keyboard.row(*buttons2)
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
async def start_command_h(message: types.Message):
    global state_add_mark
    state_add_mark=" "    
    await message.reply("Погодный бот, для того чтобы узнать погоду введи название города",reply_markup=get_key_main())

@dp.message_handler(commands=['start'])
async def start_command_s(message: types.Message):
    global state_add_mark
    state_add_mark=" "    
    await message.reply("Погодный бот, для того чтобы узнать погоду введи название города",reply_markup=get_key_main())
    
@dp.message_handler(content_types=['location'])
async def handle_loc(message):
    global state_add_mark
    state_add_mark=" "    
    result= get_weather_сurrent(message['location']['latitude'],message['location']['longitude'])
    print(message['location']['latitude'],message['location']['longitude'])    
    await message.reply(result, reply_markup=get_keboard_city(message['location']['latitude'],message['location']['longitude'],'uncnoun',add=True))

'''
'''
@dp.message_handler(text='Список в БД')
async def echo_message_baza(message: types.Message):
    global state_add_mark
    state_add_mark=" "    
    result = SQL.get_records(message.from_user.id)
    print("echo_message_baza:", result)
    if result!=False:
        for r in result:
            print("echo_message_baza step: ", )
            st = get_weather_сurrent(r["lat"],r["lon"])
            await message.answer(f'Запись с ID{r["id"]} именем {r["name"]}, время напоминания {r["time"]}\n {st}', reply_markup=get_keboard_city(r["lat"],r["lon"],r["id"],False))  
    else:
        await message.answer(f'База пуста')  
@dp.message_handler()
async def echo_message(message: types.Message): #all message
    text = message.text.split(" ")
    print(f'echo_message:{message.text}')    
    global state_add_mark
    
    print("glob:",state_add_mark)
    if state_add_mark==" ":  
        result = get_coord_in_name(message.text[0])
        if result:
        #print(message.text)
        #print(result)
            await message.reply(get_weather_сurrent(result["lat"],result["lon"]), reply_markup=get_keboard_city(result["lat"],result["lon"],result["name"],add=True))  
        else:
        #print(message.text)
            await message.reply("Город не найден. Попробуйте ввести еще раз или выберете текущие координаты",reply_markup=get_key_main())
    else:
        if len(text)==1:
            await message.reply(f"Время не указано. Запись с именем {text[0]}\n c координатами lat={state_add_mark['lat']} lon={state_add_mark['lon']}"
                            ,reply_markup=get_keboard_add(state_add_mark['lat'],state_add_mark['lon'],text[0],add=True))
            state_add_mark=""
        if len(text)==2:
            if text[1].isdigit() and int(text[1])>=0 and int(text[1])<=23 :
                await message.reply(f"Запись с именем {text[0]} Время напоминания{text[1]}\n c координатами lat={state_add_mark['lat']} lon={state_add_mark['lon']}"
                            ,reply_markup=get_keboard_add(state_add_mark['lat'],state_add_mark['lon'],text[0],time=text[1],add=True))     

            else:
                await message.reply(f"Время не указано. Запись с именем {text[0]}\n c координатами lat={state_add_mark['lat']} lon={state_add_mark['lon']}"
                            ,reply_markup=get_keboard_add(state_add_mark['lat'],state_add_mark['lon'],text[0],add=True))                
                           
            state_add_mark=""            
'''
'''
@dp.callback_query_handler(cd.filter(name=["uncnoun"]))
async def repli_del_record(call: types.CallbackQuery, callback_data: dict):
    global state_add_mark
    state_add_mark=callback_data
    await call.message.answer(f'Ввведите метку В формате имя время напоминания.\n Например Москва 8\n для добавления в Базу данных\n Текущие координаты lat={callback_data["lat"]} lon={callback_data["lon"]}')



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
    global state_add_mark
    state_add_mark=" "    
    print("repli_add_baze: callback_data ",callback_data)       
    result = SQL.add_base(call.from_user.id,callback_data['name'],callback_data['lat'],callback_data['lon'],callback_data['time'])
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
async def show(tm=60): # 60 секунд
    while True:
        await asyncio.sleep(tm)
        t = datetime.datetime.now().second
       #print(t)
        #print(SQL.get_time_record(t))
'''
'''

if __name__ == "__main__":
    print("main: Создаем базу")
    SQL.creat_base()
    #print("main: Старт расписания")
    #loop = asyncio.get_event_loop()
    #loop.create_task(show(11)) #
 
    print("main: start Polling")
    executor.start_polling(dp)

    