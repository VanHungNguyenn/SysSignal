import sqlite3
import requests
import json
from datetime import datetime
from app.timestamp import *
from app.glo import *
from app.lib_bool import *
from app.timestamp import *
from app.lib_def import *
from app.bot_tele import *
#=================================================================      Key: token
#=================================================================

def request_link(link):
    result = requests.get(link)
    js = json.loads(result.content.decode("utf8"))
    return js


database_binance_name = 'user_binance.db'

def binance_create_db():
    # try:
        conn = sqlite3.connect(database_binance_name)
        c = conn.cursor()


        try: #update tp_7
            c.execute('''ALTER TABLE SIGNAL ADD COLUMN tp7 float''')
            c.execute('''ALTER TABLE SIGNAL ADD COLUMN tp7_hit char[3]''')

            c.execute('''ALTER TABLE SYMBOL ADD COLUMN tp7 float''')
        except Exception as e:
            print("Signal add col tp7: {}".format(str(e)))

        try: #update group_group
            c.execute('''ALTER TABLE LIST_GROUP ADD COLUMN number int''')
        except Exception as e:
            print("Group of Group: {}".format(str(e)))

        try: #update digit
            c.execute('''ALTER TABLE SYMBOL ADD COLUMN digit float''')
        except Exception as e:
            print("Signal add col digit: {}".format(str(e)))

        conn.commit()
        conn.close()
        print("create db ok")
    # except:
    #     print("create db false")

binance_create_db()

def binance_check_table(cursor, name):
    cursor.execute("SELECT * FROM {}".format(name))
    table = cursor.fetchall()
    return table

#===================================================[    START  DATA   ]================================================

def start_list_report():
    conn = sqlite3.connect(database_binance_name)
    cursor = conn.cursor()
    all_report = binance_check_table(cursor, "REPORT")
    for signal in all_report:
        DATA_REPORT.append({
                "stt": signal[0],
                "opentime": signal[1],
                "ordertype" : signal[2],
                "symbol": signal[3],
                "entry_1": signal[4],
                "entry_2": signal[5],
                "status": signal[6],
                "sl": signal[7],
                "close_price": signal[8],
                "full_opentime": str(timestamp_to_date(signal[1]/1000))
        })
    conn.close()


def start_list_port_tradingview():
    conn = sqlite3.connect(database_binance_name)
    cursor = conn.cursor()
    all_port = binance_check_table(cursor, "LIST_PORT_TRADINGVIEW")
    for port in all_port:
        DATA_LIST_PORT_TRADINGVIEW.append({
            "stt": port[0],
            "time": port[1],
            "signal": port[2],
            "full_opentime": timestamp_to_date(port[1]/1000)
        })
    conn.close()

def start_list_signal():
    conn = sqlite3.connect(database_binance_name)
    cursor = conn.cursor()
    all_signal = binance_check_table(cursor, "SIGNAL")
    for signal in all_signal:
        DATA_SIGNAL.append({
                "stt": signal[0],
                "opentime": signal[1],
                "ordertype" : signal[2],
                "symbol": signal[3],
                "entry_1": signal[4],
                "entry_2": signal[5],
                "status": signal[6],
                "sl": signal[7],
                "sl_hit": signal[8],
                "tp1": signal[9],
                "tp1_hit": signal[10],
                "tp2": signal[11],
                "tp2_hit": signal[12],
                'tp3': signal[13],
                "tp3_hit": signal[14],
                "tp4": signal[15],
                "tp4_hit": signal[16],
                "tf": signal[17],
                "close_price": signal[18],
                "tp5": signal[19],
                "tp5_hit": signal[20],
                "tp6": signal[21],
                "tp6_hit": signal[22],
                "tp7": signal[23],
                "tp7_hit": signal[24],
                "full_opentime": str(timestamp_to_date(signal[1]/1000))
        })
    conn.close()

def start_symbol():
    conn = sqlite3.connect(database_binance_name)
    cursor = conn.cursor()
    all_symbol = binance_check_table(cursor, "SYMBOL")
    for symbol in all_symbol:
        DATA_SYMBOL.append({
            "stt": symbol[0],
            "symbol": symbol[1],
            "max_leverage": symbol[2],
            "entry_2": symbol[3],
            "tp1": symbol[4],
            "tp2": symbol[5],
            "tp3": symbol[6],
            "tp4": symbol[7],
            "sl": symbol[8],
            "status": symbol[9],
            "tp5": symbol[10],
            "tp6": symbol[11],
            "tp7": symbol[12],
            "digit": symbol[13]
        })
    conn.close()

def start_active_symbol(a = None):
    global DATA_ACTIVE_SYMBOL
    mini_result = []
    conn = sqlite3.connect(database_binance_name)
    cursor = conn.cursor()
    all_symbol = binance_check_table(cursor, "ACTIVE_SYMBOL")
    for symbol in all_symbol:
        mini_result.append({
            "stt": symbol[0],
            "symbol": symbol[1],
            "mode": symbol[2],
            "type": symbol[3],
            "id": symbol[4]
        })
    conn.close()
    DATA_ACTIVE_SYMBOL = mini_result
    if a is not None:
        DATA_ACTIVE_SYMBOL = []

def start_form():
    conn = sqlite3.connect(database_binance_name)
    cursor = conn.cursor()
    all_form = binance_check_table(cursor, "FORM")
    for form in all_form:
        DATA_FORM.append({
            "stt": form[0],
            "mode": form[1],
            "id": form[2],
            "content": form[3],
            "content_tp": form[4],
            "content_sl": form[5],
            "content_cl": form[6],
            "content_rp": form[7],
            "content_rp_cl": form[8],
            "content_rp_run": form[9]
        })
    conn.close()

def start_post_signal():
    conn = sqlite3.connect(database_binance_name)
    cursor = conn.cursor()
    all_signal = binance_check_table(cursor, "POST_SIGNAL")
    for signal in all_signal:
        DATA_POST_SIGNAL.append({
            "stt": signal[0],
            "tele_id": signal[1],
            "opentime": signal[2],
            "binance_ticket": signal[3],
            "mess_id": signal[4],
            "mode": signal[5],
            "sl": signal[6],
            "tp": signal[7]
        })
    conn.close()

def start_user():
    conn = sqlite3.connect(database_binance_name)
    cursor = conn.cursor()
    all_user = binance_check_table(cursor, "USER")
    for user in all_user:
        DATA_USER.append({
            "stt": user[0],
            "tele_id": user[1],
            "tele_username": user[2],
            "tele_name": user[3]
        })
    conn.close()

def start_user_buy_licence():
    conn = sqlite3.connect(database_binance_name)
    cursor = conn.cursor()
    all_user = binance_check_table(cursor, "USER_BUY_LICENCE")
    for user in all_user:
        DATA_USER_BUY_LICENCE.append({
            "stt": user[0],
            "tele_id": user[1],
            "mode": user[2],
            "licence_day": user[3],
            "content": user[4],
            "confirm": user[5],
            "ordertime": user[6],
            "full_ordertime": str(timestamp_to_date(user[6]/1000))
        })
    conn.close()

def start_user_alert():
    conn = sqlite3.connect(database_binance_name)
    cursor = conn.cursor()
    all_user = binance_check_table(cursor, "USER_ALERT")
    for user in all_user:
        full_licence = 0
        if user[4] != 0:
            full_licence = str(timestamp_to_date(user[4]/1000))

        full_licence_start = 0
        if user[6] != 0:
            full_licence_start = str(timestamp_to_date(user[6]/1000))

        DATA_USER_ALERT.append({
            "stt": user[0],
            "tele_id": user[1],
            "join_date": user[2],
            "remind_licence": user[3],
            "licence": user[4],
            "f0": user[5],
            "licence_start": user[6],
            "status": user[7],
            "full_licence": full_licence,
            "full_licence_start":  full_licence_start
        })
    conn.close()

def start_list_group():
    global DATA_LIST_GROUP
    DATA_LIST_GROUP = []
    conn = sqlite3.connect(database_binance_name)
    cursor = conn.cursor()
    all_group = binance_check_table(cursor, "LIST_GROUP")
    for group in all_group:
        DATA_LIST_GROUP.append({
            "stt": group[0],
            "group_id": group[1],
            "name": group[2],
            "status": group[3],
            "number": group[4]
        })
    conn.close()


start_list_port_tradingview()
start_list_signal()
start_symbol()
start_active_symbol()
start_form()
start_post_signal()
start_user()
start_user_buy_licence()
start_user_alert()
start_list_group()
start_list_report()


def content_to_send_text(content,           leverage=None,  sl=None,        tp1=None,
                         tp2=None,          tp3=None,       tp4=None,       tp5=None,
                         tp6=None,          tp7=None,       entry_1=None,   entry_2=None,
                         opentime=None,     closetime=None, checktime=None, ordertype=None,
                         timeframe=None,    percent=None,   symbol=None,    close_price=None,
                         tp=None):
    if ordertype is not None:
        if ordertype == 0:
            content = content.replace('[emoij]', "🟢")
            content = content.replace("[type]", "Long")
        else:
            content = content.replace('[emoij]', "🔴")
            content = content.replace("[type]", "Short")

    if symbol is not None: content = content.replace("[symbol]", str(symbol))
    if timeframe is not None: content = content.replace("[timeframe]", str(timeframe))
    if leverage is not None: content = content.replace("[max_leverage]", str(leverage))
    if entry_1 is not None: content = content.replace("[entry_1]", str(entry_1))
    if entry_2 is not None: content = content.replace("[entry_2]", str(entry_2))
    if sl is not None: content = content.replace("[stop_loss]", str(sl))
    if tp1 is not None: content = content.replace("[take_profit_1]", str(tp1))
    if tp2 is not None: content = content.replace("[take_profit_2]", str(tp2))
    if tp3 is not None: content = content.replace("[take_profit_3]", str(tp3))
    if tp4 is not None: content = content.replace("[take_profit_4]", str(tp4))
    if tp5 is not None: content = content.replace("[take_profit_5]", str(tp5))
    if tp6 is not None: content = content.replace("[take_profit_6]", str(tp6))
    if close_price is not None: content = content.replace("[close_price]", str(close_price))
    if tp is not None: content = content.replace("[tp]", str(tp))
    if percent is not None:
        content = content.replace("[percent]", str(percent))
        content = content.replace("[percent_x2]", str(percent*2))
    if opentime is not None:
        date_opentime = timestamp_to_date(opentime/1000)
        content = content.replace("[long_time]", str(date_opentime)[:19])
        content = content.replace("[time]", str(date_opentime)[:10])
    return content


#===================================================[   REQUEST DATA   ]================================================
def request_add_symbol(in_symbol,   in_max_level,   in_entry_2,
                       in_tp1,      in_tp2,         in_tp3,
                       in_tp4,      in_tp5,         in_tp6,
                       in_tp7,      in_sl,          in_status,
                       in_digit):
    is_new = True
    is_modi = False
    is_del = False
    for i in range(len(DATA_SYMBOL)):
        if in_symbol == DATA_SYMBOL[i]['symbol']:
            is_new = False
            if in_status == "OFF":
                is_del = True
                conn = sqlite3.connect(database_binance_name)
                cursor = conn.cursor()

                sql_delete_query = """DELETE from SYMBOL where symbol={}""".format(in_symbol)
                cursor.execute(sql_delete_query)

                conn.commit()
                conn.close()

                del DATA_SYMBOL[i]

            elif in_max_level != DATA_SYMBOL[i]['max_leverage'] or in_entry_2 != DATA_SYMBOL[i]['entry_2'] or \
                in_tp1 != DATA_SYMBOL[i]['tp1'] or in_tp2 != DATA_SYMBOL[i]['tp2'] or \
                in_tp3 != DATA_SYMBOL[i]['tp3'] or in_tp4 != DATA_SYMBOL[i]['tp4'] or \
                in_tp5 != DATA_SYMBOL[i]['tp5'] or in_tp6 != DATA_SYMBOL[i]['tp6'] or \
                    in_sl != DATA_SYMBOL[i]['sl'] or in_digit != DATA_SYMBOL[i]['digit']:
                is_modi = True

                conn = sqlite3.connect(database_binance_name)
                cursor = conn.cursor()

                update_trade = """UPDATE SYMBOL SET max_leverage=?,
                                                    entry_2=?,
                                                    tp1=?,
                                                    tp2=?,
                                                    tp3=?,
                                                    tp4=?,
                                                    tp5=?,
                                                    tp6=?,
                                                    tp7=?,
                                                    sl=?,
                                                    digit=?
                                                    WHERE symbol=?"""
                info_update = (in_max_level,        in_entry_2,     in_tp1,
                               in_tp2,              in_tp3,         in_tp4,
                               in_tp5,              in_tp6,         None,
                               in_sl,               in_digit,       in_symbol)
                cursor.execute(update_trade, info_update)

                conn.commit()
                conn.close()

                DATA_SYMBOL[i]['max_leverage'] = in_max_level
                DATA_SYMBOL[i]['entry_2'] = in_entry_2
                DATA_SYMBOL[i]['tp1'] = in_tp1
                DATA_SYMBOL[i]['tp2'] = in_tp2
                DATA_SYMBOL[i]['tp3'] = in_tp3
                DATA_SYMBOL[i]['tp4'] = in_tp4
                DATA_SYMBOL[i]['tp5'] = in_tp5
                DATA_SYMBOL[i]['tp6'] = in_tp6
                DATA_SYMBOL[i]['tp7'] = None
                DATA_SYMBOL[i]['sl'] = in_sl
                DATA_SYMBOL[i]['digit'] = in_digit

            break

    if not is_new:
        if is_del:
            return {'status': True,
                    "content": "Symbol {} has been deleted".format(in_symbol)}
        elif is_modi:
            return {'status': True,
                    "content": "Symbol {} has been modified".format(in_symbol)}
        else:
            return {'status': False,
                    "content": "Symbol {} - nothing to update".format(in_symbol)}
    else:
        conn = sqlite3.connect(database_binance_name)
        cursor = conn.cursor()

        insert_user = """Insert INTO SYMBOL (symbol,
                                             max_leverage,
                                             entry_2, 
                                             tp1,
                                             tp2,
                                             tp3,
                                             tp4,
                                             tp5,
                                             tp6,
                                             tp7,
                                             sl,
                                             status,
                                             digit) values(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);"""
        info_insert = (in_symbol,   in_max_level,   in_entry_2,
                       in_tp1,      in_tp2,         in_tp3,
                       in_tp4,      in_tp5,         in_tp6,
                       None,      in_sl,          in_status,
                       in_digit)
        cursor.execute(insert_user, info_insert)

        conn.commit()
        conn.close()

        DATA_SYMBOL.append({
            "stt": len(DATA_SYMBOL) + 1,
            "symbol": in_symbol,
            "max_leverage": in_max_level,
            "entry_2": in_entry_2,
            "tp1": in_tp1,
            "tp2": in_tp2,
            "tp3": in_tp3,
            "tp4": in_tp4,
            "tp5": in_tp5,
            "tp6": in_tp6,
            "tp7": None,
            "sl": in_sl,
            "status": in_status,
            "digit": in_digit
        })
        return {
                    "status": True,
                    "content": "New symbol {} has been added".format(in_symbol)
                }

def request_add_form(mode, group_id, data):
    is_new = True
    content = ''
    for i in range(len(DATA_FORM)):
        if DATA_FORM[i]['mode'] == mode and (mode == 'ALERT' or (mode == 'GROUP' and DATA_FORM[i]['id'] == group_id)):
            is_new = False
            is_update = False
            conn = sqlite3.connect(database_binance_name)
            cursor = conn.cursor()

            if data['type'] == 'CONTENT':
                is_update = True
                update_trade = """UPDATE FORM SET content=? WHERE stt=?"""
                DATA_FORM[i]['content'] = data['content']

            elif data['type'] == 'CONTENT_TP':
                is_update = True
                update_trade = """UPDATE FORM SET content_tp=? WHERE stt=?"""
                DATA_FORM[i]['content_tp'] = data['content']

            elif data['type'] == 'CONTENT_SL':
                is_update = True
                update_trade = """UPDATE FORM SET content_sl=? WHERE stt=?"""
                DATA_FORM[i]['content_sl'] = data['content']

            elif data['type'] == 'CONTENT_CL':
                is_update = True
                update_trade = """UPDATE FORM SET content_cl=? WHERE stt=?"""
                DATA_FORM[i]['content_cl'] = data['content']

            elif data['type'] == 'CONTENT_RP':
                is_update = True
                update_trade = """UPDATE FORM SET content_rp=? WHERE stt=?"""
                DATA_FORM[i]['content_rp'] = data['content']

            elif data['type'] == 'CONTENT_RP_CL':
                is_update = True
                update_trade = """UPDATE FORM SET content_rp_cl=? WHERE stt=?"""
                DATA_FORM[i]['content_rp_cl'] = data['content']

            elif data['type'] == 'CONTENT_RP_RUN':
                is_update = True
                update_trade = """UPDATE FORM SET content_rp_run=? WHERE stt=?"""
                DATA_FORM[i]['content_rp_run'] = data['content']
            else:
                update_trade = ""

            if is_update:
                info_update = (data['content'], DATA_FORM[i]['stt'])
                cursor.execute(update_trade, info_update)
                content = "{} - {} has been updated".format(mode, data['type'])
            else:
                content = "Data type {} not found".format(data['type'])

            conn.commit()
            conn.close()
            break

    if is_new:
        text_content = ''
        text_content_tp = ''
        text_content_sl = ''
        text_content_cl = ''
        text_content_rp = ''
        text_content_rp_cl = ''
        text_content_rp_run = ''
        conn = sqlite3.connect(database_binance_name)
        cursor = conn.cursor()

        insert_log = """Insert INTO FORM (mode, 
                                          id, 
                                          content, 
                                          content_tp, 
                                          content_sl, 
                                          content_cl, 
                                          content_rp,
                                          content_rp_cl,
                                          content_rp_run) values(?, ?, ?, ?, ?, ?, ?, ?, ?);"""
        if data['type'] == 'CONTENT':
            is_update = True
            text_content = data['content']

        elif data['type'] == 'CONTENT_TP':
            is_update = True
            text_content_tp = data['content']

        elif data['type'] == 'CONTENT_SL':
            is_update = True
            text_content_sl = data['content']

        elif data['type'] == 'CONTENT_CL':
            is_update = True
            text_content_cl = data['content']

        elif data['type'] == 'CONTENT_RP':
            is_update = True
            text_content_rp = data['content']

        elif data['type'] == 'CONTENT_RP_CL':
            is_update = True
            text_content_rp_cl = data['content']

        elif data['type'] == 'CONTENT_RP_RUN':
            is_update = True
            text_content_rp_run = data['content']
        else:
            is_update = False

        if is_update:
            info_update = (mode,                group_id,               text_content,
                           text_content_tp,     text_content_sl,        text_content_cl,
                           text_content_rp,     text_content_rp_cl,     text_content_rp_run)
            cursor.execute(insert_log, info_update)
            content = "{} - {} has been added".format(mode, data['type'])

            DATA_FORM.append({
                "stt": len(DATA_FORM) + 1,
                "mode": mode,
                "id": group_id,
                "content": text_content,
                "content_tp": text_content_tp,
                "content_sl": text_content_sl,
                "content_cl": text_content_cl,
                "content_rp": text_content_rp,
                "content_rp_cl": 8,
                "content_rp_run": 9
            })
        else:
            content = "Data type {} not found".format(data['type'])

        conn.commit()
        conn.close()

    return {'status': True,
            "content": content}

def request_active_symbol(mode, group_id, order_type, list_symbol, gr_number=0):
    """
    :param mode: GROUP/ALERT
    :param group_id: ALERT = 0, GROUP != 0
    :param order_type: 0 - BUY,     1 - SELL,   -1 - Both,      99 - Disable
    :param list_symbol: []
    :return:    {}
    """

    if mode in ["GROUP", "ALERT"]:
        # set group number
        if mode == 'GROUP' and gr_number is not None:
            for i in range(len(DATA_LIST_GROUP)):
                if DATA_LIST_GROUP[i]['group_id'] == group_id and DATA_LIST_GROUP[i]['number'] != gr_number:
                    DATA_LIST_GROUP[i]['number'] = gr_number
                    conn = sqlite3.connect(database_binance_name)
                    cursor = conn.cursor()

                    update_trade = """UPDATE LIST_GROUP SET number=? WHERE group_id=?"""
                    info_update = (gr_number, group_id)
                    cursor.execute(update_trade, info_update)

                    conn.commit()
                    conn.close()

        if order_type in [-1, 0, 1, 99]:
            conn = sqlite3.connect(database_binance_name)
            cursor = conn.cursor()

            #check disabled symbol
            for i in range(len(DATA_ACTIVE_SYMBOL)):
                if DATA_ACTIVE_SYMBOL[i]['mode'] == mode and \
                        (mode == "ALERT" or (mode == "GROUP" and group_id == DATA_ACTIVE_SYMBOL[i]['id'])):
                    true_change = False
                    set_type = None
                    if list_symbol is None or DATA_ACTIVE_SYMBOL[i]['symbol'] not in list_symbol and DATA_ACTIVE_SYMBOL[i]['type'] != 99:
                        true_change = True
                        set_type = 99
                    elif DATA_ACTIVE_SYMBOL[i]['type'] != order_type and DATA_ACTIVE_SYMBOL[i]['symbol'] in list_symbol and order_type != DATA_ACTIVE_SYMBOL[i]['type']:
                        true_change = True
                        set_type = order_type
                    if true_change and set_type is not None:
                        DATA_ACTIVE_SYMBOL[i]['type'] = set_type

                        update_trade = """UPDATE ACTIVE_SYMBOL SET type=? WHERE stt=?"""
                        info_update = (set_type, DATA_ACTIVE_SYMBOL[i]['stt'])
                        cursor.execute(update_trade, info_update)

            #check new - insert type symbol
            if list_symbol is not None:
                for symbol in list_symbol:
                    true_new = True
                    for i in range(len(DATA_ACTIVE_SYMBOL)):
                        if DATA_ACTIVE_SYMBOL[i]['mode'] == mode and (mode == "ALERT" or (mode == "GROUP" and group_id == DATA_ACTIVE_SYMBOL[i]['id'])) and DATA_ACTIVE_SYMBOL[i]['symbol'] == symbol:
                            true_new = False
                            break
                    if true_new:
                        insert_log = """Insert INTO ACTIVE_SYMBOL (symbol, mode, type, id) values(?, ?, ?, ?);"""
                        info_insert = (symbol, mode, order_type, group_id)
                        cursor.execute(insert_log, info_insert)

                        DATA_ACTIVE_SYMBOL.append({
                            "stt": DATA_ACTIVE_SYMBOL[len(DATA_ACTIVE_SYMBOL) - 1]['stt'] + 1,
                            "symbol": symbol,
                            "mode": mode,
                            "type": order_type,
                            "id": group_id
                        })
            conn.commit()
            conn.close()

            return {"status": True, 'content': "Complete"}
        else:
            return {"status": False, 'content': "Order Type {} not correct".format(order_type)}
    else:
        return {'status': False, "content": "Mode {} not correct".format(mode)}

def request_change_status(mode, tele_id, status):
    """
    :param mode:    GROUP / ALERT
    :param tele_id: == 0 -> all
    :param status: ON/OFF
    :return:
    """
    if mode in ['GROUP', 'ALERT']:
        if status in ['ON', "OFF"]:
            conn = sqlite3.connect(database_binance_name)
            cursor = conn.cursor()

            if mode == 'ALERT':
                for i in range(len(DATA_USER_ALERT)):
                    if tele_id == 0 or tele_id == DATA_USER_ALERT[i]['tele_id']:
                        DATA_USER_ALERT[i]['status'] = status

                        update_trade = """UPDATE USER_ALERT SET status=? WHERE stt=?"""
                        info_update = (status, DATA_USER_ALERT[i]['stt'])
                        cursor.execute(update_trade, info_update)
                        if tele_id != 0:
                            break
            elif mode == 'GROUP':
                for j in range(len(DATA_LIST_GROUP)):
                    if tele_id == 0 or tele_id == DATA_LIST_GROUP[j]['group_id']:
                        DATA_LIST_GROUP[j]['status'] = status

                        update_trade = """UPDATE LIST_GROUP SET status=? WHERE stt=?"""
                        info_update = (status, DATA_LIST_GROUP[j]['stt'])
                        cursor.execute(update_trade, info_update)
                        if tele_id != 0:
                            break

            conn.commit()
            conn.close()

            if tele_id == 0:
                content = "New status has been change for all {}".format(mode)
            else:
                content = "New status has been change for {} with id {}".format(mode, tele_id)
            return {"status": True, 'content': content}
        else:
            return {"status": False, 'content': "status {} not correct".format(status)}
    else:
        return {"status": False, 'content': "Mode {} not correct".format(mode)}

#############################
def request_signal(in_signal):
    def def_content_to_signal(content):
        n_is_signal = True
        n_type = -1
        n_symbol = ""
        n_tf = -1
        n_entry_1 = -1
        if len(content.split(":")) == 4:
            in_signal_arr = content.split(":")

            # check order type
            if in_signal_arr[0].upper() == "SELL":
                n_type = 1
            elif in_signal_arr[0].upper() == "BUY":
                n_type = 0
            else:
                n_type = -1
                n_is_signal = False

            # check symbol
            n_symbol = in_signal_arr[1].upper()

            # check timeframe
            if is_int(in_signal_arr[2]):
                n_tf = int(in_signal_arr[2])
            else:
                n_tf = -1
                n_is_signal = False

            # check entry_1
            if is_float(in_signal_arr[3]):
                n_entry_1 = float(in_signal_arr[3])
            else:
                n_entry_1 = -1
                n_is_signal = False
        else:
            n_is_signal = False
        return n_is_signal, n_type, n_symbol, n_tf, n_entry_1

    def round_price(price, adigit):
        return int(price * adigit) / adigit

    in_is_signal, in_type, in_symbol, in_tf, in_entry_1 = def_content_to_signal(in_signal)
    if in_is_signal:
        opentime = int(date_to_timestamp(time_now())*1000)
        is_new = True
        data_close = []
        data_close_2 = []
        for i in range(len(DATA_SIGNAL)):
            signal_index = len(DATA_SIGNAL) - 1 - i
            if DATA_SIGNAL[signal_index]['symbol'] == in_symbol:
                if DATA_SIGNAL[signal_index]['ordertype'] == in_type:
                    is_new = False
                else:
                    data_close.append(signal_index)
                break

            signal_index_2 = len(DATA_REPORT) - 1 - i
            if DATA_REPORT[signal_index_2]['symbol'] == in_symbol:
                if DATA_REPORT[signal_index_2]['ordertype'] == in_type:
                    is_new = False
                else:
                    data_close_2.append(signal_index_2)
                break
        if is_new:
            for symbol in DATA_SYMBOL:
                if symbol['symbol'] == in_symbol and symbol['status'] == "ON":
                    digit = symbol['digit']
                    leverage = symbol['max_leverage']
                    entry_1 = in_entry_1
                    c_de = 1000
                    if in_type == 0:#buy

                        entry_2 = round_price(entry_1*(1 - symbol['entry_2']/c_de), digit)
                        entry_avg = (entry_1 + entry_2)/2

                        sl = round_price(entry_avg*(1 - symbol['sl']/c_de), digit)
                        tp1 = round_price(entry_avg*(1 + symbol['tp1']/c_de), digit)
                        tp2 = round_price(entry_avg*(1 + symbol['tp2']/c_de), digit)
                        tp3 = round_price(entry_avg*(1 + symbol['tp3']/c_de), digit)
                        tp4 = round_price(entry_avg*(1 + symbol['tp4']/c_de), digit)
                        tp5 = round_price(entry_avg*(1 + symbol['tp5']/c_de), digit)
                        tp6 = round_price(entry_avg*(1 + symbol['tp6']/c_de), digit)
                        # tp7 = round_price(entry_avg*(1 + symbol['tp7']/c_de), digit)
                    else: #sell
                        entry_2 = round_price(entry_1*(1 + symbol['entry_2']/c_de), digit)
                        entry_avg = (entry_1 + entry_2)/2
                        sl = round_price(entry_avg*(1 + symbol['sl']/c_de), digit)
                        tp1 = round_price(entry_avg*(1 - symbol['tp1']/c_de), digit)
                        tp2 = round_price(entry_avg*(1 - symbol['tp2']/c_de), digit)
                        tp3 = round_price(entry_avg*(1 - symbol['tp3']/c_de), digit)
                        tp4 = round_price(entry_avg*(1 - symbol['tp4']/c_de), digit)
                        tp5 = round_price(entry_avg*(1 - symbol['tp5']/c_de), digit)
                        tp6 = round_price(entry_avg*(1 - symbol['tp6']/c_de), digit)
                        # tp7 = round_price(entry_avg*(1 - symbol['tp7']/c_de), digit)

                    """:param order_type: 0 - BUY,     1 - SELL,   -1 - Both,      99 - Disable"""
                    #========================[ SEND TO GROUP ]=========================
                    send_result_group = []
                    for group in DATA_LIST_GROUP:
                        if group['status'] == "ON":

                            for active in DATA_ACTIVE_SYMBOL:
                                if active['mode'] == 'GROUP' and active['id'] == group['group_id'] \
                                        and active['symbol'] == in_symbol and \
                                        (active['type'] == -1 or active['type'] == in_type):
                                    #get group form
                                    is_form = False
                                    for form in DATA_FORM:
                                        if form['mode'] == 'GROUP' and form['id'] == group['group_id']:
                                            is_form = True
                                            send_result_group.append({
                                                "id": group['group_id'],
                                                "number": group['number'],
                                                "content": content_to_send_text(form['content'], leverage=leverage, sl=sl,  tp1=tp1,
                                                                                tp2=tp2,    tp3=tp3,    tp4=tp4,    tp5=tp5,    tp6=tp6,    tp7=None,
                                                                                entry_1=entry_1,        entry_2=entry_2,        opentime=opentime,
                                                                                ordertype=in_type,      symbol=in_symbol,       timeframe=in_tf)
                                            })
                                            break
                                    if not is_form:
                                        send_result_group.append({
                                            "id": group['group_id'],
                                            "number": group['number'],
                                            "content": "Form CONTENT not fount"
                                        })
                                    break
                    #========================[ SEND TO USER ]=========================
                    send_result_alert = []
                    for user in DATA_USER_ALERT:
                        if user['licence'] >= opentime and user['status'] == 'ON':
                            for active in DATA_ACTIVE_SYMBOL:
                                if active['mode'] == "ALERT" and active['symbol'] == in_symbol and (active['type'] == -1 or active['type'] == in_type):
                                    send_result_alert.append(user['tele_id'])
                                    break

                    #========================[ SEND TELEGRAM ]=========================
                    list_send_tele = []
                    result_send = {'total': 0,
                                   "complete": 0,
                                   "error": 0}
                    for gr in send_result_group:
                        if gr['number'] is not None and gr['number'] != -1:
                            try:
                                mess_id, send_err = send_signal(BOT_GROUP[gr['number']], gr['id'], gr['content'])
                                result_send['total'] += 1
                                if mess_id != -1:
                                    list_send_tele.append({"tele_id": gr['id'],
                                                           "opentime": opentime,
                                                           "mess_id": mess_id,
                                                           "mode": "GROUP"})
                                    result_send['complete'] += 1
                                else:
                                    result_send['error'] += 1
                            except:
                                pass
                    if send_result_alert:
                        content = 'Empty'
                        for form in DATA_FORM:
                            if form['mode'] == 'ALERT':
                                content = content_to_send_text(form['content'], leverage=leverage, sl=sl, tp1=tp1,
                                                               tp2=tp2, tp3=tp3, tp4=tp4, tp5=tp5, tp6=tp6,
                                                               tp7=None,
                                                               entry_1=entry_1, entry_2=entry_2, opentime=opentime,
                                                               ordertype=in_type, symbol=in_symbol,
                                                               timeframe=in_tf)
                                break
                        for ale in send_result_alert:
                            try:
                                mess_id, send_err = send_signal(BOT_ALERT, ale, content)
                                result_send['total'] += 1
                                if mess_id != -1:
                                    list_send_tele.append({"tele_id": ale,
                                                           "opentime": opentime,
                                                           "mess_id": mess_id,
                                                           "mode": "ALERT"})
                                    result_send['complete'] += 1
                                else:
                                    result_send['error'] += 1
                            except:
                                pass

                    conn = sqlite3.connect(database_binance_name)
                    cursor = conn.cursor()
                    #add signal

                    DATA_SIGNAL.append({
                        "stt": DATA_SIGNAL[len(DATA_SIGNAL) - 1]['stt'] + 1,
                        "opentime": opentime,
                        "ordertype": in_type,
                        "symbol": in_symbol,
                        "entry_1": entry_1,
                        "entry_2": entry_2,
                        "status": "ON",
                        "sl": sl,
                        "sl_hit": "OFF",
                        "tp1": tp1,
                        "tp1_hit": "OFF",
                        "tp2": tp2,
                        "tp2_hit": "OFF",
                        'tp3': tp3,
                        "tp3_hit": "OFF",
                        "tp4": tp4,
                        "tp4_hit": "OFF",
                        "tf": in_tf,
                        "close_price": 0,
                        "tp5": tp5,
                        "tp5_hit": "OFF",
                        "tp6": tp6,
                        "tp6_hit": "OFF",
                        "tp7": None,
                        "tp7_hit": "OFF",
                        "full_opentime": str(timestamp_to_date(opentime/1000))
                    })

                    insert_log = """Insert INTO SIGNAL (opentime,   ordertype,  symbol, entry_1,    entry_2,
                                                        status,     sl,         sl_hit, tp1,        tp1_hit,
                                                        tp2,        tp2_hit,    tp3,    tp3_hit,    tp4,
                                                        tp4_hit,    tp5,        tp5_hit,tp6,        tp6_hit,
                                                        tp7,        tp7_hit,    tf,     close_price) values(?, ?, ?, ?, ?,
                                                                                                            ?, ?, ?, ?, ?,
                                                                                                            ?, ?, ?, ?, ?,
                                                                                                            ?, ?, ?, ?, ?,
                                                                                                            ?, ?, ?, ?);"""
                    info_insert = (opentime,    in_type,    in_symbol,  entry_1,    entry_2,
                                   "ON",        sl,         "OFF",      tp1,        "OFF",
                                   tp2,         "OFF",      tp3,        "OFF",      tp4,
                                   "OFF",       tp5,        "OFF",      tp6,        "OFF",
                                   None,         "OFF",      in_tf,      0)
                    cursor.execute(insert_log, info_insert)

                    #add post_signal
                    if list_send_tele:
                        for sended in list_send_tele:
                            insert_log = """Insert INTO POST_SIGNAL (tele_id, opentime, mess_id, mode) values(?, ?, ?, ?);"""
                            info_insert = (sended['tele_id'], sended['opentime'], sended['mess_id'], sended['mode'])
                            cursor.execute(insert_log, info_insert)

                            DATA_POST_SIGNAL.append({
                                "stt": DATA_POST_SIGNAL[len(DATA_POST_SIGNAL) - 1]['stt'] + 1,
                                "tele_id": sended['tele_id'],
                                "opentime": sended['opentime'],
                                "binance_ticket": None,
                                "mess_id": sended['mess_id'],
                                "mode": sended['mode'],
                                "sl": None,
                                "tp": None
                            })

                    conn.commit()
                    conn.close()


                    timedone = int(date_to_timestamp(time_now())*1000)
                    end = int(((timedone - opentime)/1000)*1000)/1000
                    send_text = "<code>" + str(in_signal) + "</code>\n"\
                                                          "<b>Total:</b> {}\n"\
                                                          "<b>Complete:</b> {}\n"\
                                                          "<b>Time:</b> {}s".format(result_send['total'], result_send['complete'], end)
                    send_signal(BOT_GROUP[0], LOG_SIGNAL, send_text)
        if data_close:
            for data in data_close:
                old_opentime = DATA_SIGNAL[data]['opentime']
                if DATA_SIGNAL[data]['tp1_hit'] != "ON" and DATA_SIGNAL[data]['tp2_hit'] != "ON" and DATA_SIGNAL[data]['tp3_hit'] != "ON" and\
                        DATA_SIGNAL[data]['tp4_hit'] != "ON" and DATA_SIGNAL[data]['tp5_hit'] != "ON" and DATA_SIGNAL[data]['tp6_hit'] != "ON":
                    #close order
                    #get post signal
                    url_check_m1 = "https://www.binance.com/fapi/v1/klines?symbol={}&interval=1m&limit=1".format(DATA_SIGNAL[data]['symbol'].replace(".P",""))
                    try:
                        symbol_price_info = request_link(url_check_m1)
                        token_price = float(symbol_price_info[0][4])
                    except:
                        token_price = 0
                else:
                    token_price = 0
                list_close_post_signal = []
                for post in DATA_POST_SIGNAL:
                    if post['opentime'] == old_opentime:
                        list_close_post_signal.append(post)

                DATA_SIGNAL[data]['status'] = "OFF"
                DATA_SIGNAL[data]['close_price'] = token_price
                DATA_REPORT[data]['close_price'] = token_price

                conn = sqlite3.connect(database_binance_name)
                cursor = conn.cursor()
                #add signal

                update_trade = """UPDATE SIGNAL SET status=?, close_price=? WHERE opentime=?"""
                info_update = ("OFF", token_price, old_opentime)
                cursor.execute(update_trade, info_update)

                conn.commit()
                conn.close()

                for post_signal in list_close_post_signal:

                    user_content_cl = 'Empty'
                    for form in DATA_FORM:
                        if form['mode'] == post_signal['mode'] and \
                                ((post_signal['mode'] == 'GROUP' and post_signal['tele_id'] == form['id']) or post_signal['mode'] == 'ALERT'):
                            user_content_cl = content_to_send_text(form['content_cl'],
                                                                   sl=DATA_SIGNAL[data]['sl'],
                                                                   tp1=DATA_SIGNAL[data]['tp1'],
                                                                   tp2=DATA_SIGNAL[data]['tp2'],
                                                                   tp3=DATA_SIGNAL[data]['tp3'],
                                                                   tp4=DATA_SIGNAL[data]['tp4'],
                                                                   tp5=DATA_SIGNAL[data]['tp5'],
                                                                   tp6=DATA_SIGNAL[data]['tp6'],
                                                                   entry_1=DATA_SIGNAL[data]['entry_1'],
                                                                   entry_2=DATA_SIGNAL[data]['entry_2'],
                                                                   opentime=old_opentime,
                                                                   ordertype=DATA_SIGNAL[data]['ordertype'],
                                                                   symbol=DATA_SIGNAL[data]['symbol'],
                                                                   timeframe=DATA_SIGNAL[data]['tf'],
                                                                   close_price=token_price)
                            break
                    if token_price != 0:
                        if post_signal['mode'] == 'ALERT':
                            send_signal(BOT_ALERT, post_signal['tele_id'], user_content_cl, post_signal['mess_id'])
                        elif post_signal['mode'] == "GROUP":
                            for gr in DATA_LIST_GROUP:
                                if gr['group_id'] == post_signal['tele_id'] and gr['number'] is not None:
                                    try:
                                        send_signal(BOT_GROUP[gr['number']], post_signal['tele_id'], user_content_cl, post_signal['mess_id'])
                                    except:
                                        pass

def request_user_status(list_user, new_status):
    conn = sqlite3.connect(database_binance_name)
    cursor = conn.cursor()
    if new_status in ['ON', "OFF"]:
        if not list_user:
            update_status = """Update USER_ALERT set status='{}'""".format(new_status)
            cursor.execute(update_status)

            for i in range(len(DATA_USER_ALERT)):
                DATA_USER_ALERT[i]['status'] = new_status

        else:
            for i in range(len(DATA_USER_ALERT)):
                if DATA_USER_ALERT[i]['tele_id'] in list_user:
                    pass


    conn.commit()
    conn.close()

def request_add_group(group_id, status):
    if status in ['ON', "OFF", None]:
        result = {}
        if status is None:
            is_new = True
            for i in range(len(DATA_LIST_GROUP)):
                if DATA_LIST_GROUP[i]['group_id'] == group_id:
                    is_new = False
                    if DATA_LIST_GROUP[i]['status'] == "ON":
                        new_status = "OFF"
                    else:
                        new_status = "ON"
                    conn = sqlite3.connect(database_binance_name)
                    cursor = conn.cursor()

                    update_trade = """UPDATE LIST_GROUP SET name=?, status=? WHERE stt=?"""
                    info_update = (DATA_LIST_GROUP[i]['name'], new_status, DATA_LIST_GROUP[i]['stt'])
                    cursor.execute(update_trade, info_update)

                    conn.commit()
                    conn.close()

                    DATA_LIST_GROUP[i]['status'] = new_status

                    result = {'status': True, 'content': "Group {} status has been updated".format(DATA_LIST_GROUP[i]['name'])}
                    break
            if is_new:
                result = {'status': False, 'content': "Group not found"}

        else:
            is_url, is_member, gr_id, gr_title, gr_username = get_channel_info(link="",
                                                                               channel_id=group_id)
            """
                check id, old -> modify name / status
                if new -> insert
            """
            is_new = True
            for i in range(len(DATA_LIST_GROUP)):
                if DATA_LIST_GROUP[i]['group_id'] == gr_id:
                    is_new = False
                    if DATA_LIST_GROUP[i]['name'] != gr_title or DATA_LIST_GROUP[i]['status'] != status:
                        conn = sqlite3.connect(database_binance_name)
                        cursor = conn.cursor()

                        update_trade = """UPDATE LIST_GROUP SET name=?, status=? WHERE stt=?"""
                        info_update = (gr_title, status, DATA_LIST_GROUP[i]['stt'])
                        cursor.execute(update_trade, info_update)

                        conn.commit()
                        conn.close()

                        DATA_LIST_GROUP[i]['name'] = gr_title
                        DATA_LIST_GROUP[i]['status'] = status

                        result = {'status': True, 'content': "Group {} has been updated".format(gr_title)}
                        break
            if is_new:
                if status is None:
                    status = "ON"
                conn = sqlite3.connect(database_binance_name)
                cursor = conn.cursor()

                insert_log = """Insert INTO LIST_GROUP (group_id, name, status) values(?, ?, ?);"""
                info_insert = (gr_id, gr_title, status)
                cursor.execute(insert_log, info_insert)

                conn.commit()
                conn.close()

                DATA_LIST_GROUP.append({
                    "stt": len(DATA_LIST_GROUP) + 1,
                    "group_id": gr_id,
                    "name": gr_title,
                    "status": status,
                    "number": 0
                })
                result = {"status": True, "content": "Group {} has been added".format(gr_title)}

        return result
    else:
        return {"status": False, "content": "Status not correct"}

def request_update_content(mode, group_id, content_type, content):
    if mode in ['GROUP', "ALERT"] and content_type in ['content', 'content_tp', 'content_sl', 'content_cl', 'content_rp', 'content_rp_cl', 'content_rp_run']:
        true_set = False
        if mode == "GROUP":
            for group in DATA_LIST_GROUP:
                if group['group_id'] == group_id:
                    true_set = True
                    break
        else:
            true_set = True
        if not true_set:
            return {"status": False, 'content': "Group ID not found"}
        else:
            is_new = True
            for i in range(len(DATA_FORM)):
                if (mode == DATA_FORM[i]['mode'] == "GROUP" and DATA_FORM[i]['id'] == group_id) or mode == DATA_FORM[i]['mode'] == "ALERT":
                    is_new = False
                    conn = sqlite3.connect(database_binance_name)
                    cursor = conn.cursor()

                    update_trade = """UPDATE FORM SET {}=? WHERE stt=?""".format(content_type)
                    info_update = (content, DATA_FORM[i]['stt'])
                    cursor.execute(update_trade, info_update)

                    DATA_FORM[i][content_type] = content

                    conn.commit()
                    conn.close()
                    break
            if is_new:
                content_z = content_tp = content_sl = content_cl = content_rp = content_rp_cl = content_rp_run = "Empty"
                if content_type == 'content': content_z = content
                elif content_type == 'content_tp': content_tp = content
                elif content_type == 'content_sl': content_sl = content
                elif content_type == 'content_cl': content_cl = content
                elif content_type == 'content_rp': content_rp = content
                elif content_type == 'content_rp_cl': content_rp_cl = content
                elif content_type == 'content_rp_run': content_rp_run = content

                conn = sqlite3.connect(database_binance_name)
                cursor = conn.cursor()

                insert_user = """Insert INTO FORM (mode,        id,             content, 
                                                   content_tp,  content_sl,     content_cl, 
                                                   content_rp,  content_rp_cl,  content_rp_run) 
                                                   values(?, ?, ?, ?, ?, ?, ?, ?, ?);"""
                info_insert = (mode,        group_id,       content_z,
                               content_tp,  content_sl,     content_cl,
                               content_rp,  content_rp_cl,  content_rp_run)
                cursor.execute(insert_user, info_insert)

                DATA_FORM.append({
                    "stt": len(DATA_FORM) + 1,
                    "mode": mode,
                    "id": group_id,
                    "content": content_z,
                    "content_tp": content_tp,
                    "content_sl": content_sl,
                    "content_cl": content_cl,
                    "content_rp": content_rp,
                    "content_rp_cl": content_rp_cl,
                    "content_rp_run": content_rp_run
                })
                conn.commit()
                conn.close()
                return {'status': True, "content": "New content has been added"}
            else:
                return {'status': True, "content": "Content has been updated"}

    else:
        return {'status': False, "content": "Mode or content type not found"}

def request_update_symbol(symbol, leverage, entry_2, tp1, tp2, tp3, tp4, tp5, tp6, tp7, sl, digit):
    result = {}
    is_update = False
    for i in range(len(DATA_SYMBOL)):
        if DATA_SYMBOL[i]['symbol'] == symbol:
            is_update = True
            if is_int(leverage) and is_int(entry_2) and is_int(tp1) and is_int(tp2) and is_int(tp3) and is_int(tp4) and\
                is_int(tp5) and is_int(tp6) and is_int(tp7) and is_int(sl) and is_int(digit):
                DATA_SYMBOL[i]['max_leverage'] = int(leverage)
                DATA_SYMBOL[i]['entry_2'] = int(entry_2)
                DATA_SYMBOL[i]['tp1'] = int(tp1)
                DATA_SYMBOL[i]['tp2'] = int(tp2)
                DATA_SYMBOL[i]['tp3'] = int(tp3)
                DATA_SYMBOL[i]['tp4'] = int(tp4)
                DATA_SYMBOL[i]['tp5'] = int(tp5)
                DATA_SYMBOL[i]['tp6'] = int(tp6)
                DATA_SYMBOL[i]['tp7'] = None
                DATA_SYMBOL[i]['sl'] = int(sl)
                DATA_SYMBOL[i]['digit'] = int(digit)

                conn = sqlite3.connect(database_binance_name)
                cursor = conn.cursor()

                update_trade = """UPDATE SYMBOL SET max_leverage=?, 
                                                        entry_2=?, 
                                                        tp1=?, 
                                                        tp2=?, 
                                                        tp3=?, 
                                                        tp4=?, 
                                                        tp5=?, 
                                                        tp6=?, 
                                                        tp7=?, 
                                                        sl=?, 
                                                        digit=? WHERE stt=?"""
                info_update = (int(leverage), int(entry_2), int(tp1), int(tp2),
                               int(tp3), int(tp4), int(tp5), int(tp6), None,
                               int(sl), int(digit), DATA_SYMBOL[i]['stt'])
                cursor.execute(update_trade, info_update)

                conn.commit()
                conn.close()
                result = {
                    "status": True,
                    "content": "Symbol {} updated".format(symbol)
                }
            else:
                result = {"status": False, "content": "Wrong input type"}
            break
    if not is_update:
        if is_int(leverage) and is_int(entry_2) and is_int(tp1) and is_int(tp2) and is_int(tp3) and is_int(tp4) and \
                is_int(tp5) and is_int(tp6) and is_int(sl) and is_int(digit):
            conn = sqlite3.connect(database_binance_name)
            cursor = conn.cursor()

            insert_log = """Insert INTO SYMBOL (symbol, max_leverage, entry_2,
                                                tp1, tp2, tp3,
                                                tp4, tp5, tp6, 
                                                tp7, sl, digit) values(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);"""
            info_insert = (symbol.upper(), int(leverage), int(entry_2),
                           int(tp1), int(tp2), int(tp3),
                           int(tp4), int(tp5), int(tp6),
                           None, int(sl), int(digit))
            cursor.execute(insert_log, info_insert)

            conn.commit()
            conn.close()

            DATA_SYMBOL.append({
                "stt": DATA_SYMBOL[len(DATA_SYMBOL) - 1]['stt'] + 1,
                'symbol': symbol.upper(),
                'max_leverage': int(leverage),
                'entry_2': int(entry_2),
                'tp1': int(tp1),
                'tp2': int(tp2),
                'tp3': int(tp3),
                'tp4': int(tp4),
                'tp5': int(tp5),
                'tp6': int(tp6),
                'tp7': None,
                'sl': int(sl),
                'digit': int(digit)
            })
            result = {'status': False, "content": "New symbol added"}
        else:
            result = {'status': False, "content": "Input Not correct"}

    if result == {}:
        return {"status": False, "content": "Not found"}
    else: return result

def request_confirm_licence(ordertime, licence):
    result = {}
    for i in range(len(DATA_USER_BUY_LICENCE)):
        if DATA_USER_BUY_LICENCE[i]['ordertime'] == ordertime and DATA_USER_BUY_LICENCE[i]['confirm'] == 0:
            if licence == -1:
                DATA_USER_BUY_LICENCE[i]['confirm'] = -1
                conn = sqlite3.connect(database_binance_name)
                cursor = conn.cursor()

                update_trade = """UPDATE USER_BUY_LICENCE SET confirm=? WHERE ordertime=?"""
                info_update = (-1, ordertime)
                cursor.execute(update_trade, info_update)

                conn.commit()
                conn.close()
                result = {"status": True,
                          "content": "Order licence has been Deny",
                          "licence": licence,
                          "ordertime": ordertime}
            else:
                ts_now = int(date_to_timestamp(time_now())*1000)
                true_user = False
                for j in range(len(DATA_USER_ALERT)):
                    if DATA_USER_ALERT[j]['tele_id'] == DATA_USER_BUY_LICENCE[i]['tele_id']:
                        if DATA_USER_ALERT[j]['licence'] == 0 or DATA_USER_ALERT[j]['licence'] < ts_now:
                            new_licence_start = ts_now
                        else:
                            new_licence_start = DATA_USER_ALERT[j]['licence']
                        new_licence = new_licence_start + licence*24*60*60*1000
                        DATA_USER_BUY_LICENCE[i]['confirm'] = 1
                        DATA_USER_BUY_LICENCE[i]['licence_day'] = licence
                        DATA_USER_ALERT[j]['licence'] = new_licence
                        DATA_USER_ALERT[j]['licence_start'] = ts_now
                        DATA_USER_ALERT[j]['full_licence'] = str(timestamp_to_date(new_licence/1000))[:19]
                        DATA_USER_ALERT[j]['full_licence_start'] = str(timestamp_to_date(ts_now/1000))[:19]

                        conn = sqlite3.connect(database_binance_name)
                        cursor = conn.cursor()

                        update_trade = """UPDATE USER_BUY_LICENCE SET confirm=?, licence_day=? WHERE ordertime=?"""
                        info_update = (1, licence, ordertime)
                        cursor.execute(update_trade, info_update)

                        update_trade = """UPDATE USER_ALERT SET licence=?, licence_start=? WHERE tele_id=?"""
                        info_update = (new_licence, ts_now, DATA_USER_ALERT[j]['tele_id'])
                        cursor.execute(update_trade, info_update)

                        conn.commit()
                        conn.close()

                        send_signal(BOT_ALERT, DATA_USER_ALERT[j]['tele_id'], 
                                    "🏆 Status: ACTIVE\n\n"
                                    "⏰ Expiration Date: {}".format(str(timestamp_to_date(new_licence/1000))[:19]))

                        for u in DATA_USER:
                            if u['tele_id'] == DATA_USER_ALERT[j]['tele_id']:
                                send_signal(BOT_ALERT, LOG_USER_LICENCE,
                                            "🆔 ID: <a href='tg://user?id={}'>{}</a>\n"
                                            "🏆 USER: <a href='tg://user?id={}'>{}</a>\n\n"
                                            "⏰ Expiration Date: {}".format(DATA_USER_ALERT[j]['tele_id'], DATA_USER_ALERT[j]['tele_id'],
                                                                           DATA_USER_ALERT[j]['tele_id'], u['tele_name'],
                                                                           str(timestamp_to_date(new_licence/1000))[:19]))
                        
                        result = {'status': True,
                                  "content": "Licence confirmed",
                                  "licence": licence,
                                  "ordertime": ordertime}
                        break
    if result == {}:
        result = {"status": False,
                  "content": "Err",
                  "licence": licence,
                  "ordertime": ordertime}
    return result

def request_add_licence(tele_id, name, content, mode='ALERT'):
    timenow = time_now()
    ts_now = int(date_to_timestamp(timenow)*1000)
    DATA_USER_BUY_LICENCE.append({
        "stt": DATA_USER_BUY_LICENCE[len(DATA_USER_BUY_LICENCE) - 1]['stt'] + 1,
        "tele_id": tele_id,
        "mode": mode,
        "licence_day": 0,
        "content": content,
        "confirm": 0,
        "ordertime": int(ts_now),
        "full_ordertime": str(timenow)[:19]
    })
    
    conn = sqlite3.connect(database_binance_name)
    cursor = conn.cursor()

    insert_user = """Insert INTO USER_BUY_LICENCE (tele_id,
                                                   mode,
                                                   licence_day,
                                                   content,
                                                   confirm,
                                                   ordertime) values(?, ?, ?, ?, ?, ?);"""
    info_insert = (tele_id, mode, 0, content, 0, int(ts_now))
    cursor.execute(insert_user, info_insert)

    conn.commit()
    conn.close()

    send_name = "==[ ADD LICENCE ]==\n" \
                "ID: <a href='tg://user?id=" + str(tele_id) + "'>" + str(tele_id) + "</a>\n"\
                "Name: <a href='tg://user?id=" + str(tele_id) + "'>" + name + "</a>\n"
    text = send_name + "\nAdd request licence: " + content
    send_signal(BOT_ALERT, LOG_USER_LICENCE, text)
    return {'status': True}

def request_add_licence_no_content(tele_id, licence):
    result = None
    for i in range(len(DATA_USER_ALERT)):
        if DATA_USER_ALERT[i]['tele_id'] == tele_id:
            DATA_USER_ALERT[i]['licence'] += licence*24*60*60*1000

            conn = sqlite3.connect(database_binance_name)
            cursor = conn.cursor()
            update_trade = """UPDATE USER_ALERT SET licence=? WHERE tele_id=?"""
            info_update = (DATA_USER_ALERT[i]['licence'], tele_id)
            cursor.execute(update_trade, info_update)

            conn.commit()
            conn.close()
            result = {'status': True, 
                      'content': "Done, new licence: " + str(timestamp_to_date(DATA_USER_ALERT[i]['licence']/1000))[:19]}
            break
    if result is None:
        return {'status': False, 'content': "ID not found"}
    else:
        return result
    
def request_send_message(content, mode, user_id):
    ts_now = int(date_to_timestamp(time_now()))
    total_send = 0
    total_done = 0
    for user in DATA_USER_ALERT:
        is_active = ts_now*1000 < user['licence']
        if (mode == 'active' and is_active) or (mode == "inactive" and not is_active) \
                or (mode == "one" and user['tele_id'] == user_id):
            total_send += 1
            mess_id, send_err = send_signal(BOT_ALERT, user['tele_id'], content)
            if mess_id != -1:
                total_done += 1
            if mode == "one":
                break
                
    ts_end = int(date_to_timestamp(time_now()))
    text_rs = "Send total: {}<br>" \
              "Send complete: {}<br>" \
              "Time: {}s".format(total_send, total_done, ts_end - ts_now)
    return {'status': True,
            "content": text_rs}
#===================================================[      DEFAULT     ]================================================
def set_default_symbol():
    result = []
    for info in info_of_symbol:
        add_result = request_add_symbol(info['symbol'],
                                        info['max_leve'],
                                        info['entry2'],
                                        info['tp1'],
                                        info['tp2'],
                                        info['tp3'],
                                        info['tp4'],
                                        info['tp4'] + 15,
                                        info['tp4'] + 30,
                                        info['tp4'] + 45,
                                        info['sl'],
                                        "ON",
                                        info['digit']
                                        )
        result.append({
            "status": add_result['status'],
            "symbol": info['symbol']
        })
    return result
#===================================================[      HIT SLTP    ]================================================

def calculator_percent(order_type, entry_price, hit_price):
    if order_type == 0:
        percent = (hit_price - entry_price) * 1000 / entry_price
    elif order_type == 1:
        percent = (entry_price - hit_price) * 1000 / entry_price
    else:
        percent = 100
    return int(percent * 100) / 100

def hit_sl_tp(opentime, hit_data):
    true_send_tele = None
    false_send_tele = 0
    starttime = date_to_timestamp(time_now())
    for i in range(len(DATA_SIGNAL)):
        if DATA_SIGNAL[i]['opentime'] == opentime and DATA_SIGNAL[i]['symbol'] == hit_data['symbol']:
            true_send = None
            tp = -1
            if hit_data['tp6_hit'] == "ON" and DATA_SIGNAL[i]['tp6_hit'] == "OFF":
                true_send = calculator_percent(DATA_SIGNAL[i]['ordertype'], DATA_SIGNAL[i]['entry_1'], DATA_SIGNAL[i]['tp6'])
                DATA_SIGNAL[i]['tp1_hit'] = DATA_SIGNAL[i]['tp2_hit'] = DATA_SIGNAL[i]['tp3_hit'] \
                    = DATA_SIGNAL[i]['tp4_hit'] = DATA_SIGNAL[i]['tp5_hit'] = DATA_SIGNAL[i]['tp6_hit'] = "ON"
                DATA_SIGNAL[i]['status'] = "OFF"
                tp = 6
                conn = sqlite3.connect(database_binance_name)
                cursor = conn.cursor()

                update_trade = """UPDATE SIGNAL SET status=?, 
                                                    tp1_hit=?,
                                                    tp2_hit=?,
                                                    tp3_hit=?,
                                                    tp4_hit=?,
                                                    tp5_hit=?,
                                                    tp6_hit=?
                                                    WHERE opentime=?"""
                info_update = ("OFF", "ON", "ON", "ON", "ON", "ON", "ON", opentime)
                cursor.execute(update_trade, info_update)

                conn.commit()
                conn.close()
            elif hit_data['tp5_hit'] == "ON" and DATA_SIGNAL[i]['tp5_hit'] == "OFF":
                true_send = calculator_percent(DATA_SIGNAL[i]['ordertype'], DATA_SIGNAL[i]['entry_1'], DATA_SIGNAL[i]['tp5'])
                DATA_SIGNAL[i]['tp1_hit'] = DATA_SIGNAL[i]['tp2_hit'] = DATA_SIGNAL[i]['tp3_hit'] \
                    = DATA_SIGNAL[i]['tp4_hit'] = DATA_SIGNAL[i]['tp5_hit'] = "ON"
                tp = 5

                conn = sqlite3.connect(database_binance_name)
                cursor = conn.cursor()

                update_trade = """UPDATE SIGNAL SET tp1_hit=?,
                                                    tp2_hit=?,
                                                    tp3_hit=?,
                                                    tp4_hit=?,
                                                    tp5_hit=?
                                                    WHERE opentime=?"""
                info_update = ("ON", "ON", "ON", "ON", "ON", opentime)
                cursor.execute(update_trade, info_update)

                conn.commit()
                conn.close()
            elif hit_data['tp4_hit'] == "ON" and DATA_SIGNAL[i]['tp4_hit'] == "OFF":
                true_send = calculator_percent(DATA_SIGNAL[i]['ordertype'], DATA_SIGNAL[i]['entry_1'], DATA_SIGNAL[i]['tp4'])
                DATA_SIGNAL[i]['tp1_hit'] = DATA_SIGNAL[i]['tp2_hit'] = DATA_SIGNAL[i]['tp3_hit'] \
                    = DATA_SIGNAL[i]['tp4_hit'] = "ON"
                tp = 4

                conn = sqlite3.connect(database_binance_name)
                cursor = conn.cursor()

                update_trade = """UPDATE SIGNAL SET tp1_hit=?,
                                                    tp2_hit=?,
                                                    tp3_hit=?,
                                                    tp4_hit=?
                                                    WHERE opentime=?"""
                info_update = ("ON", "ON", "ON", "ON", opentime)
                cursor.execute(update_trade, info_update)

                conn.commit()
                conn.close()
            elif hit_data['tp3_hit'] == "ON" and DATA_SIGNAL[i]['tp3_hit'] == "OFF":
                true_send = calculator_percent(DATA_SIGNAL[i]['ordertype'], DATA_SIGNAL[i]['entry_1'], DATA_SIGNAL[i]['tp3'])
                DATA_SIGNAL[i]['tp1_hit'] = DATA_SIGNAL[i]['tp2_hit'] = DATA_SIGNAL[i]['tp3_hit'] = "ON"
                tp = 3

                conn = sqlite3.connect(database_binance_name)
                cursor = conn.cursor()

                update_trade = """UPDATE SIGNAL SET tp1_hit=?,
                                                    tp2_hit=?,
                                                    tp3_hit=?
                                                    WHERE opentime=?"""
                info_update = ("ON", "ON", "ON", opentime)
                cursor.execute(update_trade, info_update)

                conn.commit()
                conn.close()
            elif hit_data['tp2_hit'] == "ON" and DATA_SIGNAL[i]['tp2_hit'] == "OFF":
                true_send = calculator_percent(DATA_SIGNAL[i]['ordertype'], DATA_SIGNAL[i]['entry_1'], DATA_SIGNAL[i]['tp2'])
                DATA_SIGNAL[i]['tp1_hit'] = DATA_SIGNAL[i]['tp2_hit'] = "ON"
                tp = 2

                conn = sqlite3.connect(database_binance_name)
                cursor = conn.cursor()

                update_trade = """UPDATE SIGNAL SET tp1_hit=?,
                                                    tp2_hit=?
                                                    WHERE opentime=?"""
                info_update = ("ON", "ON", opentime)
                cursor.execute(update_trade, info_update)
            elif hit_data['tp1_hit'] == "ON" and DATA_SIGNAL[i]['tp1_hit'] == "OFF":
                true_send = calculator_percent(DATA_SIGNAL[i]['ordertype'], DATA_SIGNAL[i]['entry_1'], DATA_SIGNAL[i]['tp1'])
                DATA_SIGNAL[i]['tp1_hit'] = "ON"
                tp = 1

                conn = sqlite3.connect(database_binance_name)
                cursor = conn.cursor()

                update_trade = """UPDATE SIGNAL SET tp1_hit=?
                                                    WHERE opentime=?"""
                info_update = ("ON", opentime)
                cursor.execute(update_trade, info_update)

                conn.commit()
                conn.close()
            elif hit_data['sl_hit'] == "ON" and DATA_SIGNAL[i]['sl_hit'] == "OFF":
                true_send = calculator_percent(DATA_SIGNAL[i]['ordertype'], DATA_SIGNAL[i]['entry_1'], DATA_SIGNAL[i]['sl'])
                DATA_SIGNAL[i]['sl_hit'] = "ON"
                DATA_SIGNAL[i]['status'] = "OFF"

                conn = sqlite3.connect(database_binance_name)
                cursor = conn.cursor()

                update_trade = """UPDATE SIGNAL SET sl_hit=?,
                                                    status=?
                                                    WHERE opentime=?"""
                info_update = ("ON", "OFF", opentime)
                cursor.execute(update_trade, info_update)

                conn.commit()
                conn.close()

            if true_send is not None:
                for post in DATA_POST_SIGNAL:
                    if post['opentime'] == opentime:
                        for form in DATA_FORM:
                            if post['mode'] == form['mode'] and (post['mode'] == "ALERT" or (post['mode'] == 'GROUP' and post['tele_id'] == form['id'])):
                                if true_send >= 0:
                                    content_tp = content_to_send_text(form['content_tp'],
                                                                      sl=DATA_SIGNAL[i]['sl'],
                                                                      tp1=DATA_SIGNAL[i]['tp1'],
                                                                      tp2=DATA_SIGNAL[i]['tp2'],
                                                                      tp3=DATA_SIGNAL[i]['tp3'],
                                                                      tp4=DATA_SIGNAL[i]['tp4'],
                                                                      tp5=DATA_SIGNAL[i]['tp5'],
                                                                      tp6=DATA_SIGNAL[i]['tp6'],
                                                                      entry_1=DATA_SIGNAL[i]['entry_1'],
                                                                      entry_2=DATA_SIGNAL[i]['entry_2'],
                                                                      opentime=opentime,
                                                                      ordertype=DATA_SIGNAL[i]['ordertype'],
                                                                      symbol=hit_data['symbol'],
                                                                      timeframe=DATA_SIGNAL[i]['tf'],
                                                                      percent=true_send,
                                                                      tp=str(tp))
                                else:
                                    content_tp = content_to_send_text(form['content_sl'],
                                                                      sl=DATA_SIGNAL[i]['sl'],
                                                                      tp1=DATA_SIGNAL[i]['tp1'],
                                                                      tp2=DATA_SIGNAL[i]['tp2'],
                                                                      tp3=DATA_SIGNAL[i]['tp3'],
                                                                      tp4=DATA_SIGNAL[i]['tp4'],
                                                                      tp5=DATA_SIGNAL[i]['tp5'],
                                                                      tp6=DATA_SIGNAL[i]['tp6'],
                                                                      entry_1=DATA_SIGNAL[i]['entry_1'],
                                                                      entry_2=DATA_SIGNAL[i]['entry_2'],
                                                                      opentime=opentime,
                                                                      ordertype=DATA_SIGNAL[i]['ordertype'],
                                                                      symbol=hit_data['symbol'],
                                                                      timeframe=DATA_SIGNAL[i]['tf'],
                                                                      percent=true_send)
                                if true_send_tele is None:
                                    true_send_tele = 1
                                else:
                                    true_send_tele += 1
                                if post['mode'] == 'ALERT':
                                    send_result, send_err = send_signal(BOT_ALERT, post['tele_id'], content_tp, post['mess_id'])
                                    if send_result == -1:
                                        false_send_tele += 1
                                elif post['mode'] == "GROUP":
                                    for gr in DATA_LIST_GROUP:
                                        if gr['group_id'] == post['tele_id']:

                                            mess_id, send_err = send_signal(BOT_GROUP[gr['number']], gr['group_id'], content_tp, post['mess_id'])
                                            if mess_id == -1:
                                                false_send_tele += 1
                                            break

            break
#===================================================[       REPORT      ]================================================
def send_signal_report(content_type, target, date_from, date_to, mode, send_end, end_content):
    result = {}
    if content_type in ['content_rp', 'content_rp_run', 'content_rp_cl']:
        if len(target.split(":")) == 2 and target.split(":")[0] in ['alert', 'group'] and\
                ((target.split(":")[0] == 'alert' and target.split(":")[1] in ['active', 'inactive'])
                 or (target.split(":")[0] == 'group' and is_int(target.split(":")[1]))):
            try:
                from_date = datetime.strptime(date_from + ' 00:00:00', '%Y-%m-%d %H:%M:%S')
                ts_from = date_to_timestamp(from_date)*1000

                to_date = datetime.strptime(date_to + ' 23:59:59', '%Y-%m-%d %H:%M:%S')
                ts_to = date_to_timestamp(to_date)*1000
            except Exception as e:
                from_date = to_date = ''
                ts_from = ts_to = 0
            if ts_to > ts_from != 0:
                content = "Empty"
                for form in DATA_FORM:
                    if form['mode'] == target.split(":")[0].upper() and (form['mode'] == 'ALERT' or
                             (form['mode'] == "GROUP" and form['id'] == int(target.split(":")[1]))):
                        content = form[content_type]
                        break
                if send_end == "SEND":
                    content += end_content

                total_percent = 0
                total_win = 0
                total_order = 0

                content_1 = content.split("{")[0]
                content_1 = content_1.replace("[from_date]", str(from_date)[:10])
                content_1 = content_1.replace("[to_date]", str(to_date)[:10])
                try:
                    content_2 = content.split("{")[1].split("}")[0]
                except:
                    content_2 = ''
                content_2_result = ''

                LIST_POST_SIGNAL_DATA = []
                for iii in range(len(DATA_POST_SIGNAL)):
                    post = DATA_POST_SIGNAL[iii]
                    if post['mode'] == target.split(":")[0].upper() and (post['mode'] == 'ALERT' or
                             (post['mode'] == 'GROUP' and post['tele_id'] == int(target.split(":")[1]))):
                        LIST_POST_SIGNAL_DATA.append(post['opentime'])

                for signal in DATA_SIGNAL:
                    if ts_from <= signal['opentime'] <= ts_to and\
                        ((signal['status'] == "OFF" and content_type in ['content_rp', 'content_rp_cl']) or
                         (signal['status'] == "ON" and content_type in ['content_rp', 'content_rp_run'])) and\
                         signal['opentime'] in LIST_POST_SIGNAL_DATA:

                        total_order += 1
                        if signal['tp6_hit'] == "ON": end_price = signal['tp6']
                        elif signal['tp5_hit'] == "ON": end_price = signal['tp5']
                        elif signal['tp4_hit'] == "ON": end_price = signal['tp4']
                        elif signal['tp3_hit'] == "ON": end_price = signal['tp3']
                        elif signal['tp2_hit'] == "ON": end_price = signal['tp2']
                        elif signal['tp1_hit'] == "ON": end_price = signal['tp1']
                        elif signal['sl_hit'] == "ON": end_price = signal['sl']
                        elif signal['close_price'] != 0: end_price = signal['close_price']
                        else: end_price = -9999

                        if end_price == -9999: percent = "Run"
                        else:
                            # if end_price > 0:
                            #     total_win += 1
                            percent = calculator_percent(signal['ordertype'], signal['entry_1'], end_price)

                            total_percent += percent
                            if percent > 0:
                                total_win += 1
                                percent = "+" + str(percent)
                            percent = str(percent) + "%"


                        ordertime = str(timestamp_to_date(signal['opentime']/1000))[:19]
                        mini_content = content_2
                        mini_content = mini_content.replace("[symbol]", signal['symbol'])
                        mini_content = mini_content.replace("[percent]", str(percent))
                        mini_content = mini_content.replace("[long_time]", ordertime)
                        mini_content = mini_content.replace("[time_minute]", ordertime[11:])
                        mini_content = mini_content.replace("[time]", ordertime[:10])
                        if signal['ordertype'] == 0:
                            mini_content = mini_content.replace("[type]", "Long")
                            mini_content = mini_content.replace('[emoij]', "🟢")
                        elif signal['ordertype'] == 1:
                            mini_content = mini_content.replace("[type]", "Short")
                            mini_content = mini_content.replace('[emoij]', "🔴")

                        content_2_result += mini_content + "\n"
                        
                try:
                    content_3 = content.split("}")[1]
                except:
                    content_3 = ''

                if total_percent < 0:
                    content_3 = content_3.replace("[total_percent]", str(int(total_percent * 100) / 100) + "%")
                    content_3 = content_3.replace("[total_percent_2x]", str(int(total_percent * 2 * 100) / 100) + "%")
                    content_3 = content_3.replace("[this_pnl]", str(int(total_percent*100)/100) + "%")
                else:
                    content_3 = content_3.replace("[total_percent]", "+" + str(int(total_percent*100)/100) + "%")
                    content_3 = content_3.replace("[total_percent_2x]", "+" + str(int(total_percent*2*100)/100) + "%")
                    content_3 = content_3.replace("[this_pnl]", "+" + str(int(total_percent*100)/100) + "%")
                content_3 = content_3.replace("[total_signal]", str(total_order))
                content_3 = content_3.replace("[total_win]", str(total_win))
                content_3 = content_3.replace("[total_loss]", str(int(total_order - total_win)))
                content_3 = content_3.replace("[from_date]", str(from_date)[:10])
                content_3 = content_3.replace("[to_date]", str(to_date)[:10])

                content_3 = content_3.replace("[check_time]", str(time_now())[:19])

                content_send = content_1 + content_2_result + content_3
                if mode == "TEST":
                    mess_id, send_err = send_signal(BOT_ALERT, LOG_TEST_REPORT, content_send)
                    result = {'status': True,
                              'content_html': content_send.replace("\n", "<br>"),
                              "content_tele": content_send,
                              "send_result": send_err}
                elif mode == "CHECK":
                    result = {'status': True,
                              "content_tele": content_send}
                elif target.split(":")[0] == 'alert':
                    user_type = target.split(":")[1]
                    ts_now = date_to_timestamp(time_now())*1000
                    total_send = 0
                    total_complete = 0
                    
                    timest = int(date_to_timestamp(time_now()))
                    for user in DATA_USER_ALERT:
                        if (user_type == "active" and user['licence'] > ts_now) or \
                                (user_type == "inactive" and user['licence'] < ts_now):
                            mess_id, send_err = send_signal(BOT_ALERT, user['tele_id'], content_send)
                            total_send += 1
                            if mess_id != -1: total_complete += 1

                    timeend = int(date_to_timestamp(time_now()))
                    report_text = "Total: {}<br>" \
                                  "Complete: {}<br>" \
                                  "Time: {}s".format(total_send, total_complete, str(timeend - timest))
                    result = {'status': True,
                              'content_html': content_send.replace("\n", "<br>"),
                              "content_tele": content_send,
                              "send_result": report_text}
                elif target.split(":")[0] == 'group':
                    group_id = int(target.split(":")[1])
                    send_res = ''
                    ts_now = date_to_timestamp(time_now())*1000
                    for group in DATA_LIST_GROUP:
                        if group['group_id'] == group_id:
                            try:
                                mess_id, send_err = send_signal(BOT_GROUP[group['number']], group_id, content_send)
                                if mess_id != -1:
                                    send_res = "Send completed ! GROUP: {}".format(group['name'])
                                else:
                                    send_res = send_err
                                send_res = send_err
                            except Exception as e:
                                send_res = str(e)
                            break
                    result = {'status': True,
                              'content_html': content_send.replace("\n", "<br>"),
                              "content_tele": content_send,
                              "send_result": send_res}

            else:
                result = {'status': False, 'content': 'Date to must be > Date from'}

        else: result = {'status': False, 'content': 'Target not correct'}
    else: result = {'status': False, 'content': 'Content type not found'}
    return result

#===================================================[    BOT Request   ]================================================
def bot_request_user(tele_id, username, name):
    user_data = {}
    is_new = True
    for i in range(len(DATA_USER)):
        if DATA_USER[i]['tele_id'] == tele_id:
            is_new = False
            is_edit = False
            if DATA_USER[i]['tele_username'] != username:
                is_edit = True
                DATA_USER[i]['tele_username'] = username
            if DATA_USER[i]['tele_name'] != name:
                is_edit = True
                DATA_USER[i]['tele_name'] = name
            if is_edit:
                conn = sqlite3.connect(database_binance_name)
                cursor = conn.cursor()

                update_trade = """UPDATE USER SET tele_username=?, tele_name WHERE tele_id=?"""
                info_update = (username, name, tele_id)
                cursor.execute(update_trade, info_update)

                conn.commit()
                conn.close()
            for user in DATA_USER_ALERT:
                if user['tele_id'] == tele_id:
                    user_data = user
                    break
            break
    if is_new:
        join_date = date_to_timestamp(time_now())*1000
        DATA_USER.append({
            "stt": DATA_USER[len(DATA_USER) - 1]['stt'] + 1,
            "tele_id": tele_id,
            "tele_username": username,
            "tele_name": name
        })
        old_status = DATA_USER_ALERT[len(DATA_USER_ALERT) - 1]['status']
        user_data = {
            "stt": DATA_USER_ALERT[len(DATA_USER_ALERT) - 1]['stt'] + 1,
            "tele_id": tele_id,
            "join_date": int(join_date),
            "remind_licence": 3,
            "licence": 0,
            "f0": 0,
            "licence_start": 0,
            "status": old_status,
            "full_licence": '',
            "full_licence_start": ''
        }
        DATA_USER_ALERT.append(user_data)

        conn = sqlite3.connect(database_binance_name)
        cursor = conn.cursor()

        insert_user = """Insert INTO USER (tele_id,
                                           tele_username,
                                           tele_name) values(?, ?, ?);"""
        info_insert = (tele_id, username, name)
        cursor.execute(insert_user, info_insert)

        insert_user = """Insert INTO USER_ALERT (
                                            tele_id,
                                            join_date,
                                            remind_licence,
                                            licence,
                                            f0,
                                            licence_start,
                                            status) values(?, ?, ?, ?, ?, ?, ?);"""
        info_insert = (tele_id, int(join_date), 3, 0, 0, 0, old_status)
        cursor.execute(insert_user, info_insert)

        conn.commit()
        conn.close()

        send_text = "<b>==[ New join ]==</b>\n\n" + \
                    "ID: " + str(tele_id) + "\n"
        if username == "":
            send_text += "Name: <a href='tg://user?id=" + str(tele_id) + "'>" + name + "</a>\n"
        else:
            send_text += "Name: <a href='https://t.me/" + username + "'>" + name + "</a>\n"

        send_text += "Join: " + str(timestamp_to_date(join_date/1000))[:19]
        send_signal(BOT_ALERT, LOG_USER_JOIN, send_text)
    return user_data

def bot_request_trend(mode, new_trend, group_id):
    is_edited = False
    if mode in ['ALERT', "GROUP"] and new_trend in [-1, 0, 1, 99]:
        for i in range(len(DATA_ACTIVE_SYMBOL)):
            print("{} = {}".format(DATA_ACTIVE_SYMBOL[i]['id'], group_id))
            if DATA_ACTIVE_SYMBOL[i]['mode'] == mode and (mode == 'ALERT' or
                 (mode == 'GROUP' and DATA_ACTIVE_SYMBOL[i]['id'] == group_id)):
                is_edited = True
                DATA_ACTIVE_SYMBOL[i]['type'] = new_trend

    conn = sqlite3.connect(database_binance_name)
    cursor = conn.cursor()
    if mode == "ALERT":
        update_trade = """UPDATE ACTIVE_SYMBOL SET type=? WHERE mode=?"""
        info_update = (new_trend, "ALERT")
        cursor.execute(update_trade, info_update)
    if mode == "GROUP" and is_int(group_id):
        print("GROUP - set ====================== {} - {}".format(mode, group_id))
        update_trade = """UPDATE ACTIVE_SYMBOL SET type=? WHERE id=?"""
        info_update = (new_trend, group_id)
        cursor.execute(update_trade, info_update)

    conn.commit()
    conn.close()
    return {'status': is_edited}
