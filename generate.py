import os
import requests
from datetime import datetime, timezone, timedelta
import calendar

def get_weather():
    url = "https://api.open-meteo.com/v1/forecast?latitude=36.67&longitude=117.00&current=temperature_2m,weather_code,wind_speed_10m&timezone=Asia%2FShanghai"
    try:
        response = requests.get(url, timeout=10)
        data = response.json()['current']
        temp = data['temperature_2m']
        wind = f"风速 {data['wind_speed_10m']} km/h"
        code = data['weather_code']
        weather_map = {0: "晴", 1: "晴", 2: "多云", 3: "阴", 45: "雾", 48: "雾", 51: "毛毛雨", 61: "小雨", 71: "小雪", 95: "雷阵雨"}
        desc = weather_map.get(code, "阴晴")
        return desc, f"{temp}", wind
    except Exception:
        return "未知", "--", "未知"

def generate_calendar():
    tz = timezone(timedelta(hours=8))
    now = datetime.now(tz)
    year = now.year
    month = now.month
    today = now.day

    cal = calendar.HTMLCalendar(calendar.SUNDAY)
    cal_html = cal.formatmonth(year, month)
    cal_html = cal_html.replace('<table border="0" cellpadding="0" cellspacing="0" class="month">', '<table class="calendar-table">')
    
    today_str = f'>{today}<'
    current_day_str = f' class="current-day">{today}<'
    cal_html = cal_html.replace(today_str, current_day_str)
    return cal_html

def main():
    desc, temp, wind = get_weather()
    cal_html = generate_calendar()
    
    tz = timezone(timedelta(hours=8))
    now = datetime.now(tz)
    weekdays = ["星期一", "星期二", "星期三", "星期四", "星期五", "星期六", "星期日"]
    weekday_str = weekdays[now.weekday()]
    
    with open("template.html", "r", encoding="utf-8") as f:
        template = f.read()
        
    output = template.replace("{{WEATHER_DESC}}", desc)
    output = output.replace("{{TEMPERATURE}}", temp)
    output = output.replace("{{WIND}}", wind)
    output = output.replace("{{DAY}}", str(now.day))
    output = output.replace("{{WEEKDAY}}", weekday_str)
    output = output.replace("{{YEAR_MONTH}}", f"{now.year}年{now.month}月")
    output = output.replace("{{CALENDAR_TABLE}}", cal_html)
    output = output.replace("{{UPDATE_TIME}}", now.strftime("%Y-%m-%d %H:%M:%S"))
    
    with open("index.html", "w", encoding="utf-8") as f:
        f.write(output)

if __name__ == "__main__":
    main()
