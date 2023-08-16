import sqlite3
from app.timestamp import *
from app.lib_bool import *



def insert_port_tradingview(cursor, content):
    insert_user = """Insert INTO {} (opentime, signal) values(?, ?);""".format("LIST_PORT_TRADINGVIEW")
    info_insert = (int(date_to_timestamp(time_now())*1000), content)
    cursor.execute(insert_user, info_insert)

def round_price(last_price, now_price):
    if len(str(now_price)) > len(str(last_price)):
        return float(str(now_price)[:len(str(last_price))])
    return now_price

def request_content_to_signal(content):
    in_is_signal = True
    in_type = -1
    in_symbol = ""
    in_tf = -1
    in_entry_1 = -1
    if len(content.split(":")) == 4:
        in_signal_arr = content.split(":")

        #check order type
        if in_signal_arr[0].upper() == "SELL":
            in_type = 1
        elif in_signal_arr[0].upper() == "BUY":
            in_type = 0
        else:
            in_type = -1
            in_is_signal = False

        #check symbol
        in_symbol = in_signal_arr[1].upper()

        #check timeframe
        if is_int(in_signal_arr[2]):
            in_tf = int(in_signal_arr[2])
        else:
            in_tf = -1
            in_is_signal = False

        #check entry_1
        if is_float(in_signal_arr[3]):
            in_entry_1 = float(in_signal_arr[3])
        else:
            in_entry_1 = -1
            in_is_signal = False
    else:
        in_is_signal = False
    return in_is_signal, in_type, in_symbol, in_tf, in_entry_1

def is_old_group(cursor, group_id):
    result = False
    all_group = binance_check_table(cursor, "LIST_GROUP")
    for group in all_group:
        if group_id == group[1]:
            result = True
            break
    return result

#=================[ CALCULATOR ]================
def calculator_signal(cursor, in_symbol, in_type, in_entry_1, in_tf, in_opentime):
    all_symbol = binance_check_table(cursor, "SYMBOL")
    true_symbol = False
    result = {
        "opentime": in_opentime,
        "symbol": in_symbol,
        "type": in_type,
        "entry_1": in_entry_1,
        "entry_2": 0,
        "tp1": 0,
        "tp2": 0,
        "tp3": 0,
        "tp4": 0,
        "tp5": 0,
        "tp6": 0,
        "sl": 0,
        "max_leverage": 0,
        "tf": in_tf
    }
    for symbol in all_symbol:
        if symbol[1] == in_symbol.upper() and symbol[9] == "ON":
            result['max_leverage'] = symbol[2]
            true_symbol = True
            s_entry_1 = in_entry_1
            c_de = 1000
            if in_type == 0:
                s_entry_2 = round_price(s_entry_1, s_entry_1*(1 + symbol[3]/c_de))
                entry_avg = (s_entry_1 + s_entry_2)/2

                result['entry_2'] = s_entry_2
                result['sl']  = round_price(s_entry_1, entry_avg*(1 - symbol[8]/c_de))
                result['tp1'] = round_price(s_entry_1, entry_avg*(1 + symbol[4]/c_de))
                result['tp2'] = round_price(s_entry_1, entry_avg*(1 + symbol[5]/c_de))
                result['tp3'] = round_price(s_entry_1, entry_avg*(1 + symbol[6]/c_de))
                result['tp4'] = round_price(s_entry_1, entry_avg*(1 + symbol[7]/c_de))
                #new with tp5 tp6
                result['tp5'] = round_price(s_entry_1, entry_avg*(1 + symbol[10]/c_de))
                result['tp6'] = round_price(s_entry_1, entry_avg*(1 + symbol[11]/c_de))
            else:
                s_entry_2 = round_price(s_entry_1, s_entry_1*(1 - symbol[3]/c_de))
                entry_avg = (s_entry_1 + s_entry_2)/2
                result['entry_2'] = s_entry_2
                result['sl']  = round_price(s_entry_1, entry_avg*(1 + symbol[8]/c_de))
                result['tp1'] = round_price(s_entry_1, entry_avg*(1 - symbol[4]/c_de))
                result['tp2'] = round_price(s_entry_1, entry_avg*(1 - symbol[5]/c_de))
                result['tp3'] = round_price(s_entry_1, entry_avg*(1 - symbol[6]/c_de))
                result['tp4'] = round_price(s_entry_1, entry_avg*(1 - symbol[7]/c_de))
                #new with tp5 tp6
                result['tp5'] = round_price(s_entry_1, entry_avg*(1 - symbol[10]/c_de))
                result['tp6'] = round_price(s_entry_1, entry_avg*(1 - symbol[11]/c_de))
    return true_symbol, result

def calculator_percent(order_type, entry_price, hit_price):
    if order_type == 0:
        percent = (hit_price - entry_price)*1000/entry_price
    elif order_type == 1:
        percent = (entry_price - hit_price)*1000/entry_price
    else:
        percent = 100
    return int(percent*100)/100

#=================[ GET INFO ]================
def get_symbol_info(cursor, in_symbol):
    all_symbol = binance_check_table(cursor, "SYMBOL")
    result = {
        "symbol": in_symbol,
        "max_leverage": 0,
        "entry_2": 0,
        "tp1": 0,
        "tp2": 0,
        "tp3": 0,
        "tp4": 0,
        "tp5": 0,
        "tp6": 0,
        "sl": 0,
        "status": ""
    }
    for symbol in all_symbol:
        if symbol[1] == in_symbol:
            result['max_leverage'] = symbol[2]
            result['entry_2'] = symbol[3]
            result['tp1'] = symbol[4]
            result['tp2'] = symbol[5]
            result['tp3'] = symbol[6]
            result['tp4'] = symbol[7]
            result['tp5'] = symbol[10]
            result['tp6'] = symbol[11]
            result['sl'] = symbol[8]
            result['status'] = symbol[9]
            break
    return result

def get_form(cursor, mode, group_id, form_type):
    all_form = binance_check_table(cursor, "FORM")
    result = None
    for form in all_form:
        if form[1] == mode and ((mode == "GROUP" and form[2] == group_id) or mode != "GROUP"):
            if form_type == "CONTENT": result = form[3]
            elif form_type == "CONTENT_TP": result = form[4]
            elif form_type == "CONTENT_SL": result = form[5]
            elif form_type == "CONTENT_CL": result = form[6]
            elif form_type == "CONTENT_RP": result = form[7]
            elif form_type == "CONTENT_RP_CL": result = form[8]
            elif form_type == "CONTENT_RP_RUN": result = form[9]
            break
    if result is None:
        return mode + " don't have form for " + form_type
    elif result == "":
        return mode + " is empty with " + form_type
    else:
        return result
    
def get_user_info(cursor, tele_id):
    all_user = binance_check_table(cursor, "USER")
    all_user_alert = binance_check_table(cursor, "USER_ALERT")
    all_user_auto = binance_check_table(cursor, "USER_AUTO")
    result = {
        "tele_id": tele_id,
        "name": "",
        "username": "",
        "alert": {
            "join_date": 0,
            "licence": 0,
            "f0": 0,
            "licence_start": 0,
            "status": ""
        },
        "auto": {}
    }
    # true_user = False
    true_user_auto = False
    true_user_alert = False
    for user in all_user:
        if user[1] == tele_id:
            # true_user = True
            result['name'] = user[3]
            result['username'] = user[2]
            break
    for user_alert in all_user_alert:
        if user_alert[1] == tele_id:
            true_user_alert = True
            result['alert']['join_date'] = user_alert[2]
            result['alert']['licence'] = user_alert[4]
            result['alert']['f0'] = user_alert[5]
            result['alert']['licence_start'] = user_alert[6]
            result['alert']['status'] = user_alert[7]
            break
            
    ###########[ FOr user auto ]==========
    return true_user_alert, true_user_auto, result
    
    
#=================[ SEND SIGNAL ]================
def send_new_signal(cursor, signal):
    #check send auto


    #check send group status ON, and ACTIVE SYMBOL
    all_group = binance_check_table(cursor, "LIST_GROUP")
    for group in all_group:
        if group[3] == "ON": #status ON
            all_active_symbol = binance_check_table(cursor, "ACTIVE_SYMBOL")
            for active_symbol in all_active_symbol:
                if active_symbol[2] == "GROUP" and active_symbol[4] == group[1] and (active_symbol[3] == -1 or active_symbol[3] == signal['type']) and active_symbol[1] == signal['symbol']:
                    #active symbol is group, same group ID, and type == -1 or == type signal
                    # print("GRoup send new:", group[1])
                    content = get_form(cursor, "GROUP", group[1], "CONTENT")
                    send_text = content
                    send_text = send_text.replace("[symbol]", signal['symbol'])
                    if signal["type"] == 0:
                        send_text = send_text.replace("[type]", "Long")
                    else:
                        send_text = send_text.replace("[type]", "Short")
                    send_text = send_text.replace("[timeframe]", str(signal['tf']))
                    send_text = send_text.replace("[max_leverage]", str(signal['max_leverage']))
                    send_text = send_text.replace("[entry_1]", str(signal['entry_1']))
                    send_text = send_text.replace("[entry_2]", str(signal['entry_2']))
                    send_text = send_text.replace("[stop_loss]", str(signal["sl"]))
                    send_text = send_text.replace("[take_profit_1]", str(signal['tp1']))
                    send_text = send_text.replace("[take_profit_2]", str(signal['tp2']))
                    send_text = send_text.replace("[take_profit_3]", str(signal['tp3']))
                    send_text = send_text.replace("[take_profit_4]", str(signal['tp4']))
                    send_text = send_text.replace("[take_profit_5]", str(signal['tp5']))
                    send_text = send_text.replace("[take_profit_6]", str(signal['tp6']))
                    mess_id = send_message_new_signal_group(group[1], send_text)
                    if mess_id != -1:
                        insert_log = """Insert INTO {} (tele_id, opentime, mess_id, mode) values(?, ?, ?, ?);""".format("POST_SIGNAL")
                        info_insert = (group[1], signal["opentime"], mess_id, "GROUP")
                        cursor.execute(insert_log, info_insert)
                        break


    #check send ALERT to active user, and ACTIVE symbol
    all_user_alert = binance_check_table(cursor, "USER_ALERT")
    for user_alert in all_user_alert:
        #check active
        if user_alert[4] > signal['opentime'] and user_alert[7] is not None and user_alert[7] == "ON":
            all_active_symbol = binance_check_table(cursor, "ACTIVE_SYMBOL")
            for active_symbol in all_active_symbol:
                # print(active_symbol[2])
                # print(active_symbol[1])
                if active_symbol[2] == "ALERT" and active_symbol[1] == signal['symbol'] and (active_symbol[3] == -1 or active_symbol[3] == signal['type']):
                    content = get_form(cursor, "ALERT", 0, "CONTENT")
                    send_text = content
                    send_text = send_text.replace("[symbol]", signal['symbol'])
                    if signal["type"] == 0:
                        send_text = send_text.replace("[type]", "Long")
                    else:
                        send_text = send_text.replace("[type]", "Short")
                    send_text = send_text.replace("[timeframe]", str(signal['tf']))
                    send_text = send_text.replace("[max_leverage]", str(signal['max_leverage']))
                    send_text = send_text.replace("[entry_1]", str(signal['entry_1']))
                    send_text = send_text.replace("[entry_2]", str(signal['entry_2']))
                    send_text = send_text.replace("[stop_loss]", str(signal["sl"]))
                    send_text = send_text.replace("[take_profit_1]", str(signal['tp1']))
                    send_text = send_text.replace("[take_profit_2]", str(signal['tp2']))
                    send_text = send_text.replace("[take_profit_3]", str(signal['tp3']))
                    send_text = send_text.replace("[take_profit_4]", str(signal['tp4']))
                    send_text = send_text.replace("[take_profit_5]", str(signal['tp5']))
                    send_text = send_text.replace("[take_profit_6]", str(signal['tp6']))
                    mess_id = send_message_new_signal_user_alert(user_alert[1], send_text)
                    if mess_id != -1:
                        insert_log = """Insert INTO {} (tele_id, opentime, mess_id, mode) values(?, ?, ?, ?);""".format("POST_SIGNAL")
                        info_insert = (user_alert[1], signal["opentime"], mess_id, "ALERT")
                        cursor.execute(insert_log, info_insert)
                        break


def send_close_signal(cursor, signal):
    #check post_signal with opentime.
    all_post_signal = binance_check_table(cursor, "POST_SIGNAL")
    for post_signal in all_post_signal:
        if post_signal[2] == signal["opentime"]: #true opentime, check mode to send
            if post_signal[5] == "AUTO":
                print("Auto mode first")


            elif post_signal[5] == "GROUP" or post_signal[5] == "ALERT":
                content_cl = get_form(cursor, post_signal[5], post_signal[1], "CONTENT_CL")
                send_text = content_cl
                send_text = send_text.replace("[symbol]", signal['symbol'])
                if signal['type'] == 0:
                    send_text = send_text.replace("[type]", "Long")
                else:
                    send_text = send_text.replace("[type]", "Short")
                send_text = send_text.replace("[timeframe]", str(signal["tf"]))
                # send_text = send_text.replace("[max_leverage]", str(signal['max_leverage']))
                send_text = send_text.replace("[entry_1]", str(signal["entry_1"]))
                send_text = send_text.replace("[entry_2]", str(signal["entry_2"]))
                send_text = send_text.replace("[stop_loss]", str(signal["sl"]))
                send_text = send_text.replace("[take_profit_1]", str(signal["tp1"]))
                send_text = send_text.replace("[take_profit_2]", str(signal["tp2"]))
                send_text = send_text.replace("[take_profit_3]", str(signal["tp3"]))
                send_text = send_text.replace("[take_profit_4]", str(signal["tp4"]))
                send_text = send_text.replace("[take_profit_5]", str(signal["tp3"]))
                send_text = send_text.replace("[take_profit_6]", str(signal["tp4"]))
                
                # check mess_id
                if post_signal[5] == "GROUP":
                    send_message_close_signal_group(post_signal[1], send_text, post_signal[4])
                else:
                    send_message_close_signal_user_alert(post_signal[1], send_text, post_signal[4])

def send_tp_signal(cursor, signal):
    # check post_signal with opentime.
    all_post_signal = binance_check_table(cursor, "POST_SIGNAL")
    for post_signal in all_post_signal:
        if post_signal[2] == signal[1]:  # true opentime, check mode to send
            if post_signal[5] == "AUTO":
                print("Auto mode first")


            elif post_signal[5] == "GROUP" or post_signal[5] == "ALERT":
                content_tp = get_form(cursor, post_signal[5], post_signal[1], "CONTENT_TP")
                send_text = content_tp
                send_text = send_text.replace("[symbol]", signal[3])
                avg = ((float(signal[4]) + float(signal[5])) / 2)
                if signal[2] == 0:
                    send_text = send_text.replace("[type]", "Long")
                else:
                    send_text = send_text.replace("[type]", "Short")

                if signal[22] == "ON":
                    percent = calculator_percent(signal[2], avg, signal[21])
                    send_text = send_text.replace("[tp]", str(6))
                elif signal[20] == "ON":
                    percent = calculator_percent(signal[2], avg, signal[19])
                    send_text = send_text.replace("[tp]", str(5))
                elif signal[16] == "ON":
                    percent = calculator_percent(signal[2], avg, signal[15])
                    send_text = send_text.replace("[tp]", str(4))
                elif signal[14] == "ON":
                    percent = calculator_percent(signal[2], avg, signal[13])
                    send_text = send_text.replace("[tp]", str(3))
                elif signal[12] == "ON":
                    percent = calculator_percent(signal[2], avg, signal[11])
                    send_text = send_text.replace("[tp]", str(2))
                elif signal[10] == "ON":
                    percent = calculator_percent(signal[2], avg, signal[9])
                    send_text = send_text.replace("[tp]", str(1))
                else:
                    percent = 100

                send_text = send_text.replace("[timeframe]", str(signal[17]))
                # send_text = send_text.replace("[max_leverage]", str(in_leve))
                send_text = send_text.replace("[entry_1]", str(signal[4]))
                send_text = send_text.replace("[entry_2]", str(signal[5]))
                send_text = send_text.replace("[stop_loss]", str(signal[7]))
                send_text = send_text.replace("[take_profit_1]", str(signal[9]))
                send_text = send_text.replace("[take_profit_2]", str(signal[11]))
                send_text = send_text.replace("[take_profit_3]", str(signal[13]))
                send_text = send_text.replace("[take_profit_4]", str(signal[15]))
                send_text = send_text.replace("[take_profit_5]", str(signal[13]))
                send_text = send_text.replace("[take_profit_6]", str(signal[15]))
                send_text = send_text.replace("[percent]", str(int(percent * 100) / 100) + "%")
                send_text = send_text.replace("[percent_x2]", str(int(percent * 100 * 2) / 100) + "%")
                # check mess_id

                if post_signal[5] == "GROUP":
                    send_message_close_signal_group(post_signal[1], send_text, post_signal[4])
                else:
                    send_message_close_signal_user_alert(post_signal[1], send_text, post_signal[4])

def send_sl_signal(cursor, signal):
    # check post_signal with opentime.
    all_post_signal = binance_check_table(cursor, "POST_SIGNAL")
    for post_signal in all_post_signal:
        if post_signal[2] == signal[1]:  # true opentime, check mode to send
            if post_signal[5] == "AUTO":
                print("Auto mode first")


            elif post_signal[5] == "GROUP" or post_signal[5] == "ALERT":
                content_sl = get_form(cursor, post_signal[5], post_signal[1], "CONTENT_SL")
                send_text = content_sl
                send_text = send_text.replace("[symbol]", signal[3])
                if signal[2] == 0:
                    send_text = send_text.replace("[type]", "Long")
                else:
                    send_text = send_text.replace("[type]", "Short")
                send_text = send_text.replace("[timeframe]", str(signal[17]))
                # send_text = send_text.replace("[max_leverage]", str(signal['max_leverage']))
                send_text = send_text.replace("[entry_1]", str(signal[4]))
                send_text = send_text.replace("[entry_2]", str(signal[5]))
                send_text = send_text.replace("[stop_loss]", str(signal[7]))
                send_text = send_text.replace("[take_profit_1]", str(signal[9]))
                send_text = send_text.replace("[take_profit_2]", str(signal[11]))
                send_text = send_text.replace("[take_profit_3]", str(signal[13]))
                send_text = send_text.replace("[take_profit_4]", str(signal[15]))
                send_text = send_text.replace("[take_profit_5]", str(signal[19]))
                send_text = send_text.replace("[take_profit_6]", str(signal[21]))

                # check mess_id
                if post_signal[5] == "GROUP":
                    send_message_close_signal_group(post_signal[1], send_text, post_signal[4])
                else:
                    send_message_close_signal_user_alert(post_signal[1], send_text, post_signal[4])


def is_new_signal(cursor, in_symbol, in_type):
    all_signal = binance_check_table(cursor, "SIGNAL")
    true_new = True
    bool_close_signal = False
    bool_close_info = {}
    for i in range(len(all_signal)):
        signal = all_signal[len(all_signal) - i - 1]
        signal_stt = signal[0]
        signal_time = signal[1]
        signal_symbol = signal[3]
        signal_type = signal[2]
        # check nguoc, if != type ->  close, break, = type -> false + break

        if signal_symbol == in_symbol:
            if signal_type == in_type:
                true_new = False
                break
            elif signal[6] == "ON":
                # close last order
                bool_close_info = {
                    "opentime": signal_time,
                    "symbol": signal_symbol,
                    "type": signal_type,
                    "entry_1": signal[4],
                    "entry_2": signal[5]
                }
                bool_close_signal = True
                update_trade = """UPDATE SIGNAL SET status=? WHERE stt=?"""
                info_update = ("OFF", signal_stt)
                cursor.execute(update_trade, info_update)
                symbol_info = get_symbol_info(cursor, in_symbol)
                if signal[12] == "OFF":
                    send_close_signal(cursor, {"symbol": in_symbol,
                                               "opentime": signal_time,
                                               "type": signal_type,
                                               "entry_1": signal[4],
                                               "entry_2": signal[5],
                                               "sl": signal[7],
                                               "tp1": signal[9],
                                               "tp2": signal[11],
                                               "tp3": signal[13],
                                               "tp4": signal[15],
                                               "tp5": signal[19],
                                               "tp6": signal[21],
                                               "tf": signal[17],
                                               "max_leverage": symbol_info["max_leverage"]})
                break
            else:
                break
    return true_new, bool_close_signal, bool_close_info