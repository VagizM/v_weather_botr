import requests
from pprint import pprint
from auth import WEA_KEY
import time,datetime
ARR =["Северный","Северо-восточный","Северо-восточный","Северо-восточный","Восточный","Юго-восточный", "Юго-восточный", "Юго-восточный","Южный","Юго-западный","Юго-западный","Юго-западный","Западный","Северо-западный","Северо-западный","Северо-западный"]
#ARR =["С","ССВ","СВ","ВСВ","В","ВЮВ", "ЮВ", "ЮЮВ","Ю","ЮЮЗ","ЮЗ","ЗЮЗ","З","ЗСЗ","СЗ","ССЗ"]


def degToCompass(num):
    val=int((num/22.5)+.5)
    return (ARR[val % 16])    
    
ROOT_URL_ONE = 'https://api.openweathermap.org/data/2.5/onecall'
ROOT_URL_CUR="http://api.openweathermap.org/data/2.5/weather" 
ROOT_AIR = "http://api.openweathermap.org/data/2.5/air_pollution"
ROOT_URL_GEO="http://api.openweathermap.org/geo/1.0/direct"

def get_coord_in_name(city_name):    
    data = requests.get(ROOT_URL_GEO,
             params={'q': city_name,'units': 'metric','lang': 'ru', 'APPID': WEA_KEY}).json()
    print("get_coord_in_name:", city_name,"->", data)
    if data == []:
        print("get_coord_in_name: ответ пуст", data)
        return False 
    if ("lat" in data[0]) and ("lon" in data[0]):
        print("get_coord_in_name: возвращены координаты", data)
        return  ({"lat":data[0]["lat"],"lon":data[0]["lon"],"name":data[0]["name"]})    
        #return  data[0]["lat"],data[0]["lon"],data[0]["name"]     
        
    else:
        print("get_coord_in_name: город не найден",data)
        return False        

'''
'''             
def get_weather_сurrent(lat,lon):    
    try:        
        #data = requests.get(ROOT_URL_CUR,
        #         params={'q': city_name,'units': 'metric','lang': 'ru', 'APPID': WEA_KEY}).json()
        data = requests.get(ROOT_URL_CUR,
                 params={'lat':lat,"lon":lon,'units': 'metric','lang': 'ru', 'APPID': WEA_KEY}).json()
        
        #pprint(data)
    except Exception as e: 
        print("ERR",e)  
    if data["cod"]==200:    
        cardinal = degToCompass(data["wind"]["deg"])
        return f'Сейчас в <b>{time.strftime("%H:%M",time.localtime())}</b>, температура <b>{data["main"]["temp"]}°С</b> , влажность {data["main"]["humidity"]}, ветер {cardinal} скорость {data["wind"]["speed"]} м/с, {data["weather"][0]["description"]}'
    else:
        return f'город не найден'    
    
   
def get_weather_detail(lat,lon): 
    # current minutely hourly daily alerts
    exclude="current,daily,minutely,alerts"
    data = requests.get(ROOT_URL_ONE,
             params={'lat':lat,"lon":lon,'exclude':exclude,'units': 'metric','lang': 'ru', 'APPID': WEA_KEY}).json()
    pprint(data)
    daily = data['hourly']
    result=[]
    for count,d in enumerate(daily):        
            st = f"""{time.strftime("%d.%m в %H:%M ",time.localtime(d['dt']))},Температура {d["temp"]}°С ощущаеться как {d['feels_like']}°С, влажность {d["humidity"]}%,{d["weather"][0]["description"].capitalize()}, Облачность {d["clouds"]}%, УФ индекс {d["uvi"]}.Ветер {degToCompass(d["wind_deg"])} {d["wind_speed"]}м/с, порывы до {d["wind_gust"]}м/с"""
            result.append(st)
    return result

def get_air_one(lat,lon):
    data = requests.get(ROOT_AIR,
                        params={'lat':lat,"lon":lon,'units': 'metric','lang': 'ru', 'APPID': WEA_KEY}).json()
    pprint(data)
    return f"""Качество воздуха в данном районе {data['list'][0]["main"]["aqi"]} (1 MAX/5 MIN)
    <b>{data['list'][0]['components']["co"]}</b> Концентрация CO (монооксида углерода), мкг/м3
    <b>{data['list'][0]['components']["no"]}</b> Концентрация NO (монооксид азота), мкг/м3
    <b>{data['list'][0]['components']["no2"]}</b> КонцентрацияNO2 (диоксид азота), мкг/м3
    <b>{data['list'][0]['components']["o3"]}</b> Концентрация O3 (озона), мкг/м3
    <b>{data['list'][0]['components']["so2"]}</b> КонцентрацияSO2 (диоксида серы), мкг/м3
    <b>{data['list'][0]['components']["pm2_5"]}</b> Концентрация ТЧ2,5 (мелкодисперсные частицы ), мкг/м3
    <b>{data['list'][0]['components']["pm10"]}</b> Концентрация ТЧ10 (крупные твердые частицы), мкг/м3
    <b>{data['list'][0]['components']["nh3"]}</b> КонцентрацияNH3 (аммиака), мкг/м3
    """
def get_weather_prognoz(lat,lon): 
    # current minutely hourly daily alerts
    exclude="current,minutely,hourly,alerts"
    data = requests.get(ROOT_URL_ONE,
             params={'lat':lat,"lon":lon,'exclude':exclude,'units': 'metric','lang': 'ru', 'APPID': WEA_KEY}).json()
    pprint(data)
    daily = data['daily']
    result=[]
    #print(daily)
    for count,d in enumerate(daily):
        print(d)
        #print(time.strftime("%d.%m",time.localtime(d['dt'])))
        st = f"""<b>{time.strftime("%d.%m",time.localtime(d['dt']))}</b>,
 Температура Ночью {d["temp"]["night"]}({d["feels_like"]["night"]})°С Утром {d["temp"]["morn"]}({d["feels_like"]["morn"]})°С Днем {d["temp"]["day"]}({d["feels_like"]["day"]})°С Вечером {d["temp"]["eve"]}({d["feels_like"]["eve"]})°С
 Влажность {d["humidity"]}%, {d["weather"][0]["description"].capitalize()}, Облачность {d["clouds"]}%, УФ индекс {d["uvi"]}.Вероятность осадков{d["pop"]}%
 Ветер {degToCompass(d["wind_deg"])} {d["wind_speed"]}м/с, порывы до {d["wind_gust"]}м/с"""
        result.append(st)
        print(st)
    return result

'''

def get_air_name(city_name):
    coord = get_coord_in_name(city_name)
    return get_air_one(coord['lat'],coord['lon'])

def get_weather_name(city_name):
    coord = get_coord_in_name(city_name)
    #return 1
    return get_weather_detail(coord['lat'],coord['lon'],exclude='current,minutely,daily,alerts')

def get_weather_name_prognoz(city_name):
    coord = get_coord_in_name(city_name)
    #return 1
    return get_weather_prognoz(coord['lat'],coord['lon'],exclude='current,minutely,hourly,alerts')        


'''

if __name__ == "__main__":
    print(get_weather_сurrent(0,0)) 
    #get_weather_detail(lat=66.396693, lon=77.16208) 
    #get_air_one(lat=66.396693, lon=77.16208)
    #print(get_air_name("barnaul"))
    #print(get_coord_in_name("123"))
    #print(get_coord_in_name("OMSK"))
    #print(get_weather_name_prognoz("purpe"))
    pass

