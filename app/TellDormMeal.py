import datetime
import requests
import pdfplumber
import json
import os
from dateutil.relativedelta import relativedelta

PDF_NAME = "ryoumenu.pdf"
JSON_NAME = "ryoumenu.json"

def get_MealData():
    date = datetime.date.today()
    weekday = date.weekday()
    monday = (date + relativedelta(days=-weekday)).strftime("%Y/%m%d")
    Year,MonthDay = monday.split("/")

    pdf_url = "https://www.tsuyama-ct.ac.jp/images/hokushinryou/menu/ryoumenu-R06" + MonthDay + ".pdf"

    res = requests.get(pdf_url, allow_redirects=True, verify=False)

    if res.status_code == 200:
        open(PDF_NAME, "wb").write(res.content)
        print("HTTP_SUCCESS")
        return True
    else:
        print("HTTP_ERROR")
        return False


def analysis_pdf():
    with pdfplumber.open(PDF_NAME) as pdf:
        for page in pdf.pages:
            tables = page.extract_tables()
            dates = tables[0][0]
            breakfast = tables[0][1]
            lunchA = tables[0][9]
            lunchB = tables[0][12]
            dinnerA = tables[0][17]
            dinnerB = tables[0][20]
            return dates,breakfast,lunchA,lunchB,dinnerA,dinnerB


def make_json():
    dataList = []
    

    dates,breakfast,lunchA,lunchB,dinnerA,dinnerB =  analysis_pdf()

    for i in range(7):
        data = {
            "date" : str,
            "breakfast" : str,
            "lunchA" : str,
            "lunchB" : str,
            "dinnerA" : str,
            "dinnerB" : str
        }
        data["date"] = dates[i+2]
        if isinstance(breakfast[i+2], str):
            data["breakfast"] = breakfast[i+2]
        else:
            data["breakfast"] = ""
        
        if isinstance(lunchA[i+2], str):
            data["lunchA"] = lunchA[i+2]
        else:
            data["lunchA"] = ""
        
        if isinstance(lunchB[i+2], str):
            data["lunchB"] = lunchB[i+2]
        else:
            data["lunchB"] = ""
        
        if isinstance(dinnerA[i+2], str):
            data["dinnerA"] = dinnerA[i+2]
        else:
            data["dinnerA"] = ""
        
        if isinstance(dinnerB[i+2], str):
            data["dinnerB"] = dinnerB[i+2]
        else:
            data["dinnerB"] = ""
        dataList.append(data)
    with open(JSON_NAME, "w") as json_file:
        json.dump(dataList, json_file, indent=4)
    os.remove(PDF_NAME)


def read_json(weekday):
    f = open(JSON_NAME, "r")
    now_json = json.load(f)
    f.close()
    date = now_json[weekday]["date"]
    breakfast = now_json[weekday]["breakfast"]
    lunchA = now_json[weekday]["lunchA"]
    lunchB = now_json[weekday]["lunchB"]
    dinnerA = now_json[weekday]["dinnerA"]
    dinnerB = now_json[weekday]["dinnerB"]

    return date,breakfast,lunchA,lunchB,dinnerA,dinnerB


def notice_update():
    print(datetime.datetime.now())

    if json_already_update():
        return False
    else:
        if get_MealData():
            return True
        else:
            return False


def json_already_update():
    f = open(JSON_NAME, "r")
    now_json = json.load(f)
    f.close()

    weekday = datetime.date.today().weekday()
    thisWeekMonDate = datetime.date.today() + relativedelta(days=-weekday)
    thisWeekMon = thisWeekMonDate.strftime("%Y/%m%d").split("/")[1]
    
    MonOrigin = now_json[0]["date"].split("月")
    month = MonOrigin[0]
    date = MonOrigin[1].split("日")[0]
    if len(month) == 1:
        month = "0" + month
    if len(date) == 1:
        date = "0" + date
    WJsonMonday = month + date

    if WJsonMonday == thisWeekMon:
        return True
    else:
        return False


def manual_update():
    get_MealData()
    make_json()


def today():
    weekday = datetime.date.today().weekday()
    date,breakfast,lunchA,lunchB,dinnerA,dinnerB = read_json(weekday= weekday)
    return date,breakfast,lunchA,lunchB,dinnerA,dinnerB


def tomorrow():
    tomorrow = datetime.date.today() + relativedelta(days=1)
    tomorrowWeekday = tomorrow.weekday()
    date,breakfast,lunchA,lunchB,dinnerA,dinnerB = read_json(weekday= tomorrowWeekday)
    return date,breakfast,lunchA,lunchB,dinnerA,dinnerB