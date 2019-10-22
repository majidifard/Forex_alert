"""
    AUTHOR : Amirhosein majidi fard vatan
    EMAIL : tsp10majidi@gmail.com
"""

# Import statements
from flask import Flask, Response, jsonify, request
from email.mime.multipart import MIMEMultipart
from datetime import datetime, timedelta
from email.mime.audio import MIMEAudio
from email.mime.image import MIMEImage
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.message import Message
from email import encoders
from time import sleep
import threading
import smtplib
import flask
import sys
import ssl
import os

# Setting the current directory
abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)

# Global variables
URL = "C:\\Users\\Majidi\\AppData\\Roaming\\MetaQuotes\\Terminal\\C348917D9E28C59E863914247686464D\\MQL4\\Files\\"
ALI_GMAIL = "aliphonex1375@gmail.com"
ISA_GMAIL = "Isaadelpanah4850@gmail.com"

# Setting recursion limit
sys.setrecursionlimit(10**7)

# Sub functions

def send_email(receiver,message,to_try=1000) :
    """Sends email to report events such as signals

    parameters :
        title -> string -> the title of the email
        message -> string -> the content of the email
    """
    try :
        message = f"{datetime.now()} : {message}"
        _message = message
        subject = "An email with attachment from Python"
        body = message
        sender_email = "tsp6majidi@gmail.com"
        receiver_email = receiver
        password = "amirhxgxjxrfxzcb"
        # Create a multipart message and set headers
        message = MIMEMultipart()
        message["From"] = 'tsp6majidi@gmail.com'
        message["To"] = receiver
        message["Subject"] = 'System alert'

        # Add body to email
        message.attach(MIMEText(body, "plain"))

        text = message.as_string()

        # Log in to server using secure context and send email
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, text)
        log(f"send_email : sending email to {receiver} ... ")
    except Exception as e:
        log(f"send_email : sending email failed : {str(e)}")
        to_try = to_try - 1
        if to_try > 1 :
            send_email(_message,to_try)

def _log(message) :
    i = 0
    success = False
    while i < 1000 :
        try :
            with open('logs.txt','a') as f :
                f.write(f"{datetime.now()} : {message}\n")
            success = True
            break
        except Exception as e :
            pass
        i += 1
        if not success :
            print(f"_log --> could not open the file and write down this message\n{datetime.now()} : {message}")

def log(message) :
    try:
        _log(message)
    except Exception as e:
        print(f"log --> could not open the file and write down this message\n{datetime.now()} : {message} because : {str(e)}")

def clean_symbols(string) :
    try :
        string = string.split(",")
        i = 0
        while i < len(string) :
            string[i] = string[i].strip()
            i += 1
        return string
    except Exception as e:
        log(f"clean_symbols -> {str(e)}")
        raise

def clean_prices(string) :
    try :
        string = string.split(",")
        i = 0
        while i < len(string) :
            string[i] = float(string[i])
            i += 1
        return string
    except Exception as e:
        log(f"clean_prices -> {str(e)}")
        raise

def get_errors_line() :
    try:
        for item in range(1000) :
            try:
                with open('logs.txt','r',encoding='utf-8') as f :
                    return len(list(f))
            except Exception as e:
                if "[Errno 13] Permission denied:" not in str(e) :
                    log(f"get_errors_line -> {str(e)}")
                    raise
            return "Couldn't count the document's lines"
    except Exception as e:
        log(f"get_errors_line -> {str(e)}")
        raise

def get_errors() :
    try:
        for item in range(1000) :
            try:
                with open('logs.txt','r',encoding='utf-8') as f :
                    content = 'LOGS : \n'
                    for line in f :
                        content += line
                return content.replace('\n','<br/>')
            except Exception as e:
                if "[Errno 13] Permission denied:" not in str(e) :
                    log(f"get_errors -> {str(e)}")
                    raise
            return "Couldn't read the document"
    except Exception as e:
        log(f"get_errors -> {str(e)}")
        raise

def clean_errors() :
    try:
        for item in range(1000) :
            try:
                with open('logs.txt','w',encoding='utf-8') as f :
                    pass
                return 'OK'
            except Exception as e:
                if "[Errno 13] Permission denied:" not in str(e) :
                    log(f"clean_errors -> {str(e)}")
                    raise
            return "Couldn't clean the document"
    except Exception as e:
        log(f"clean_errors -> {str(e)}")
        raise

class Database:

    def __init__(self,URL) :
        try :
            self.data = []
            self.symbols = []
            self.URL = URL
            self.IsMqlActive = False
        except Exception as e :
            log(f"Database -> __init__ -> {str(e)}")
            raise

    def get_data(self) :
        try:
            return self.data
        except Exception as e:
            log(f"Database -> get_data -> {str(e)}")
            raise

    def update(self,data) :
        try :
            self.data = data
            symbols = []
            for item in data :
                symbols.append(item[0])
            self.symbols = symbols
        except Exception as e :
            log(f"Database -> update -> {str(e)}")
            raise

    def get_price(self,symbol) :
        try :
            symbol = symbol.strip()
            if symbol in self.symbols :
                index = self.symbols.index(symbol)
                return {symbol:self.data[index]}
            else :
                log(f"{symbol} doesn't exist in the list of symbols in database object")
                log(f"Databas list : {self.data}")
                return {symbol:"the symbol doesn't exist"}
        except Exception as e :
            log(f"Database -> get_price -> {str(e)}")
            raise

    def self_update(self) :
        try:
            for item in range(1000) :
                info = []
                try :
                    with open(self.URL+"symbol_prices.txt",'r',encoding="utf-8") as f  :
                        for line in f  :
                            info.append(self.format_data(line))
                        break
                except Exception as e :
                    if "[Errno 13] Permission denied:" not in str(e) :
                        log(f"Database -> self_update -> {str(e)}")
                        raise
            if len(info) > 0 :
                self.update(info)
        except Exception as e:
            log(f"Database -> self_update -> {str(e)}")
            raise

    def format_data(self,string) :
        try:
            string = string.strip()
            string = string.split(',')
            return (string[0],float(string[1]),float(string[2]),float(string[3]))
        except Exception as e:
            log(f"Database -> format_data -> {str(e)}")
            raise

    def get_seconds(self,string) :
        try:
            string = string.split(':')
            if len(string) < 2 :
                log(f"Database -> get_seconds -> The time must have at least two ':' characters in it")
                raise "Database -> get_seconds -> The time must have at least two ':' characters in it"
            string = string[2]
            if '.' in string :
                string = string[:string.find('.')]
            return int(string)
        except Exception as e:
            log(f"Database -> get_seconds -> {str(e)}")
            raise

    def is_mql_active(self) :
        try :
            last_modification_date = os.path.getmtime(self.URL+'symbol_prices.txt')
            last_modification_date = datetime.fromtimestamp(last_modification_date)
            now = datetime.now()
            to_sub = timedelta(seconds=10)
            if now - (last_modification_date) > to_sub :
                self.IsMqlActive = False
            else :
                self.IsMqlActive = True
        except Exception as e:
            log(f"Database -> is_mql_active -> {str(e)}")
            raise

    def get_mql_activation_statuse(self) :
        try:
            return self.IsMqlActive
        except Exception as e:
            log(f"Database -> get_mql_activation_statuse -> {str(e)}")
            raise


class Signals :

    def __init__(self,database) :
        try :
            self.signals = []
            self.statuse = []
            self.directions = []
            self.database = database
        except Exception as e:
            log(f"Signals -> __init__ -> {str(e)}")
            raise

    def signals_sender(self) :
        try:
            result = ""
            if True in self.statuse :
                i = 0
                while i < len(self.statuse) :
                    if self.statuse[i] :
                        result += f"{self.signals[i]}\n"
                        del self.signals[i]
                        del self.statuse[i]
                        del self.directions[i]
                    i += 1
            return result
        except Exception as e:
            log(f"Signals -> signals_sender -> {str(e)}")
            raise

    def reset_signals(self) :
        try:
            self.signals = []
            self.statuse = []
            self.directions = []
        except Exception as e:
            log(f"Signals -> reset_signals -> {str(e)}")
            raise

    def get_statuse(self) :
        try:
            return self.statuse
        except Exception as e:
            log(f"Signals -> get_statuse -> {str(e)}")
            raise

    def get_statuse_for(self,symbol,value) :
        try:
            i = 0
            while i < len(self.signals) :
                if self.signals[i] == (symbol,value) :
                    return self.statuse[i]
                i += 1
            return "the signal doens't exist"
        except Exception as e:
            log(f"Signals -> get_statuse_for -> {str(e)}")
            raise

    def add_signal(self,symbol,value) :
        try :
            self.signals.append((symbol,value))
            self.statuse.append(False)
            self.add_direction(symbol,value)
        except Exception as e :
            log(f"Signals -> add_signal -> {str(e)}")
            raise

    def remove_signal(self,symbol,value) :
        try :
            if (symbol,value) in self.signals :
                index = self.signals.index((symbol,value))
                del self.signals[index]
                del self.statuse[index]
                del self.directions[index]
            else :
                log(f"Signals -> remove_signal -> there is no such a symbol so removing process stopped")
        except Exception as e :
            log(f"Signals -> remove_signal -> {str(e)}")
            raise

    def remove_signal_auto(self,symbol,value) :
        try :
            if (symbol,value) in self.signals :
                index = self.signals.index((symbol,value))
                del self.signals[index]
                del self.statuse[index]
        except Exception as e :
            log(f"Signals -> remove_signal -> {str(e)}")
            raise

    def add_direction(self,symbol,price) :
        try:
            price_now = self.database.get_price(symbol)
            if price_now[symbol] == "the symbol doesn't exist" :
                log(f"Signals -> add_direction -> the symbol doesn't exist so it has been cleared the signal automaticly")
                self.remove_signal_auto(symbol,price)
                return
            price_now = price_now[symbol]
            price_now = price_now[3]
            if price >= price_now :
                self.directions.append('down')
            else :
                self.directions.append('up')
        except Exception as e:
            log(f"Signals -> add_direction -> {str(e)}")
            raise

    def get_signals(self) :
        try :
            return self.signals
        except Exception as e :
            log(f"Signals -> get_signals -> {str(e)}")
            raise

    def update_statuse(self) :
        try :
            i = 0
            while i < len(self.signals) :
                if not self.statuse[i] :
                    signal = self.signals[i]
                    direction = self.directions[i]
                    #
                    symbol = signal[0]
                    price = signal[1]
                    statuse = self.calculate_statuse(symbol,price,direction)
                    self.statuse[i] = statuse
                i += 1
        except Exception as e:
            log(f"Signals -> update_statuse -> {str(e)}")
            raise

    def calculate_statuse(self,symbol,price,direction) :
        try :
            price_now  = self.database.get_price(symbol)
            price_now = price_now[symbol]
            if direction == 'up' :
                price_now = price_now[2]
                if float(price_now) <= float(price) :
                    return True
                return False
            else :
                price_now = price_now[1]
                if float(price_now) >= float(price) :
                    return True
                return False
        except Exception as e :
            log(f"Signals -> calculate_statuse -> {str(e)}")
            raise

def database_process(database) :
    while True :
        try :
            sleep(2)
            database.self_update()
            database.is_mql_active()
            print(f"{datetime.now()} updating the database ...",end="\r")
        except Exception as e :
            log(f"database_process -> {str(e)}\n--------------------------------")

def signals_process(signals,receiver) :
    while True :
        try :
            sleep(2)
            signals.update_statuse()
            result = signals.signals_sender()
            if len(result) > 0 :
                print(result)
                send_email(receiver,result,to_try=1000)
            print(f"{datetime.now()} updating the signals ...",end="\r")
        except Exception as e :
            log(f"signals_process -> {str(e)}\n--------------------------------")


# Main Actions

database = Database(URL)
signals = Signals(database)
signals_1 = Signals(database)
threading.Thread(target=database_process,args=(database,)).start()
sleep(3)
threading.Thread(target=signals_process,args=(signals,ALI_GMAIL,)).start()
threading.Thread(target=signals_process,args=(signals_1,ISA_GMAIL,)).start()
# API

app = Flask(__name__)

@app.errorhandler(404)
def page_not_found(error):
    return 'Page Not Found'

@app.errorhandler(400)
def page_not_found(error):
    return jsonify({"KeyError":"You must enter the keys like this {?key=value}"})

@app.route("/",methods=['GET'])
def Response_call():
    # return jsonify(result)
    action = request.args.get('action').strip()
    key = request.args.get('key').strip()

    if key == "ALI6444" :
        if action == "is_mql_active" :
            try:
                return str(database.get_mql_activation_statuse())
            except Exception as e:
                log(f"Response_call action=is_mql_active -> {str(e)}")
                return "NO"
        if action == "check_statuse" :
            try:
                symbols = request.args.get('symbols').strip()
                prices = request.args.get('prices').strip()
                symbols = clean_symbols(symbols)
                prices = clean_prices(prices)
                statuses = []
                for symbol,price in zip(symbols,prices) :
                    statuses.append(signals.get_statuse_for(symbol,price))
                return str(statuses).replace(']','').replace('[','').strip()
            except Exception as e:
                log(f"Response_call action=check_statuse -> {str(e)}")
                return "NO"
        if action == "get_statuse_for" :
            try :
                symbol = request.args.get('symbol').strip()
                price = request.args.get('price').strip()
                return str(signals.get_statuse_for(symbol,float(price)))
            except Exception as e:
                log(f"Response_call action=get_statuse_for -> {str(e)}")
                return "NO"
        if action == "get_signals" :
            try :
                return str(signals.get_signals())
            except Exception as e:
                log(f"Response_call action=get_signals -> {str(e)}")
                return "NO"
        if action == "get_database" :
            try :
                return str(database.get_data())
            except Exception as e:
                log(f"Response_call action=get_database -> {str(e)}")
                return "NO"
        if action == "get_statuse" :
            try :
                return str(signals.get_statuse())
            except Exception as e:
                log(f"Response_call action=get_statuse -> {str(e)}")
                return "NO"
        if action == "add_signal" :
            try :
                symbol = request.args.get('symbol').strip()
                price = request.args.get('price').strip()
                price = float(price)
                signals.add_signal(symbol,price)
                return 'OK'
            except Exception as e:
                log(f"Response_call action=add_signal -> {str(e)}")
                return 'NO'
        if action == "remove_signal" :
            try:
                symbol = request.args.get('symbol').strip()
                price = request.args.get('price').strip()
                price = float(price)
                signals.remove_signal(symbol,price)
                return 'OK'
            except Exception as e:
                log(f"Response_call action=remove_signal -> {str(e)}")
                return 'NO'
        if action == "reset_signals" :
            try:
                signals.reset_signals()
                return 'OK'
            except Exception as e:
                log(f"Response_call action=reset_signals -> {str(e)}")
                return 'NO'
        if action == "read_logs" :
            try:
                return get_errors()
            except Exception as e:
                log(f"Response_call action=read_errors -> {str(e)}")
                return 'NO'
        if action =="clean_logs" :
            try:
                return clean_errors()
            except Exception as e:
                log(f"Response_call action=clean_errors -> {str(e)}")
                return 'NO'
        if action =="get_errors_line" :
            try:
                return str(get_errors_line())
            except Exception as e:
                log(f"Response_call action=clean_errors -> {str(e)}")
                return 'NO'

    if key == "ISA6444" :
        if action == "is_mql_active" :
            try:
                return str(database.get_mql_activation_statuse())
            except Exception as e:
                log(f"Response_call action=is_mql_active -> {str(e)}")
                return "NO"
        if action == "check_statuse" :
            try:
                symbols = request.args.get('symbols').strip()
                prices = request.args.get('prices').strip()
                symbols = clean_symbols(symbols)
                prices = clean_prices(prices)
                statuses = []
                for symbol,price in zip(symbols,prices) :
                    statuses.append(signals_1.get_statuse_for(symbol,price))
                return str(statuses).replace(']','').replace('[','')
            except Exception as e:
                log(f"Response_call action=check_statuse -> {str(e)}")
                return "NO"
        if action == "get_statuse_for" :
            try :
                symbol = request.args.get('symbol').strip()
                price = request.args.get('price').strip()
                return str(signals_1.get_statuse_for(symbol,float(price)))
            except Exception as e:
                log(f"Response_call action=get_statuse_for -> {str(e)}")
                return "NO"
        if action == "get_signals" :
            try :
                return str(signals_1.get_signals())
            except Exception as e:
                log(f"Response_call action=get_signals -> {str(e)}")
                return "NO"
        if action == "get_database" :
            try :
                return str(database.get_data())
            except Exception as e:
                log(f"Response_call action=get_database -> {str(e)}")
                return "NO"
        if action == "get_statuse" :
            try :
                return str(signals_1.get_statuse())
            except Exception as e:
                log(f"Response_call action=get_statuse -> {str(e)}")
                return "NO"
        if action == "add_signal" :
            try :
                symbol = request.args.get('symbol').strip()
                price = request.args.get('price').strip()
                price = float(price)
                signals_1.add_signal(symbol,price)
                return 'OK'
            except Exception as e:
                log(f"Response_call action=add_signal -> {str(e)}")
                return 'NO'
        if action == "remove_signal" :
            try:
                symbol = request.args.get('symbol').strip()
                price = request.args.get('price').strip()
                price = float(price)
                signals_1.remove_signal(symbol,price)
                return 'OK'
            except Exception as e:
                log(f"Response_call action=remove_signal -> {str(e)}")
                return 'NO'
        if action == "reset_signals_1" :
            try:
                signals_1.reset_signals()
                return 'OK'
            except Exception as e:
                log(f"Response_call action=reset_signals -> {str(e)}")
                return 'NO'
        if action == "read_logs" :
            try:
                return get_errors()
            except Exception as e:
                log(f"Response_call action=read_errors -> {str(e)}")
                return 'NO'
        if action =="clean_logs" :
            try:
                return clean_errors()
            except Exception as e:
                log(f"Response_call action=clean_errors -> {str(e)}")
                return 'NO'
        if action =="get_errors_line" :
            try:
                return str(get_errors_line())
            except Exception as e:
                log(f"Response_call action=clean_errors -> {str(e)}")
                return 'NO'

    key = request.args.get('key')
    symbols = request.args.get('symbols')
    symbol = request.args.get('symbol')
    prices = request.args.get('prices')
    price = request.args.get('price')
    log(f"\n--------------\nNOTE: No Response to request\naction={action}\nsymbols={symbols}\nsymbol={symbol}\nprices={prices}\nprice={price}\nkey={key}\n--------------")
    return 'No Response'
if __name__ == '__main__':
    app.run(host='127.0.0.1',debug=True)







#
