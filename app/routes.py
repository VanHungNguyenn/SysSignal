from app.bot_tele import *
from app import app, db
import flask
from flask import request, jsonify, render_template
from flask.helpers import url_for, send_from_directory
import json
from app.database import *
from flask_cors import CORS
from app.lib_bool import *
from flask_socketio import SocketIO, emit, join_room, leave_room, close_room, rooms, disconnect
from app.request import *
from threading import Thread
import threading
from datetime import datetime


CORS(app)
async_mode = None

socketio = SocketIO(app, async_mode=async_mode, engineio_logger=True, ping_timeout=5000, ping_interval=5000)

#===================================================[ SOCKETIO ]========================================================

# get all bot name
list_bot_name = []
for i in range(len(BOT_GROUP)):
    list_bot_name.append({
        "stt": i,
        "bot": BOT_GROUP[i].get_me().first_name})
    
@socketio.event
def io_change_user_status(message):
    new_status = message['new_status']
    request_user_status([], new_status)
    socketio.emit('status_all_user', {'status': new_status})

@socketio.event
def io_test_signal(message):
    request_signal(message['signal'])
    socketio.emit('status_test_signal', {"status": True})

@socketio.event
def io_check_telegram(message):
    if is_int(message['group_id']):
        group_id = int(message['group_id'])
    else:
        group_id = 0
    is_url, is_member, gr_id, gr_title, gr_username = get_channel_info(link=message['link'],
                                                                       channel_id=group_id)

    room_id = message['room']
    socketio.emit('check_tele_result_' + room_id, {"is_url": is_url,
                                                   "is_member": is_member,
                                                   "group_id": gr_id,
                                                   "title": gr_title,
                                                   "username": gr_username})

@socketio.event
def io_add_group(message):
    result = request_add_group(message['group_id'], message['status'])
    socketio.emit('add_group_result_' + message['room'], result)

@socketio.event
def io_turn_group(message):
    room_id = message['room']
    group_id = int(message['status'].split("_")[1])
    result = request_add_group(group_id, None)

@socketio.event
def io_set_content(message):
    room_id = message['room']
    mode = message['mode']
    group_id = int(message['group_id'])
    content_type = message['type']
    content = message['content']
    print("========== GROUP: {}".format(group_id))
    result = request_update_content(mode, group_id, content_type, content)
    socketio.emit('set_content_' + room_id, result)

@socketio.event
def io_set_default_symbol(message):
    room_id = message['room']
    set_default_symbol()
    socketio.emit('set_default_symbol_' + room_id, {})

@socketio.event
def io_active_symbol(message):
    room_id = message['room']
    result = request_active_symbol(message['mode'],
                          int(message['id']),
                          int(message['type']),
                          message['symbol'],
                          int(message['number']))
    print(result)
    
@socketio.event
def io_update_symbol(message):
    room_id = message['room']
    result = request_update_symbol(message['symbol'],
                                   message['leverage'],
                                   message['entry_2'],
                                   message['tp1'],
                                   message['tp2'],
                                   message['tp3'],
                                   message['tp4'],
                                   message['tp5'],
                                   message['tp6'],
                                   None,
                                   message['sl'],
                                   message['digit']
                                   )
    socketio.emit('set_update_symbol_' + room_id, result)

@socketio.event
def io_send_report(message):
    room_id = message['room']
    result = send_signal_report(message['content_type'],
                                message['target'],
                                message['date_from'],
                                message['date_to'],
                                message['mode'],
                                message['send_end'],
                                message['end_content'])
    # print(result)
    socketio.emit('send_content_result_' + room_id, result)

@socketio.event
def io_confirm_licence(message):
    result = request_confirm_licence(int(message['ordertime']),
                                     int(message['licence']))
    socketio.emit('confirm_licence_result', result)

@socketio.event
def io_send_message(message):
    room_id = message['room']
    result = request_send_message(message['content'], 
                                  message['mode'],
                                  int(message['user']))
    socketio.emit('confirm_send_message_' + room_id, result)

@socketio.event
def io_add_licence(message):
    result = request_add_licence_no_content(int(message['id']),
                                            int(message['licence']))
    # result = request_send_message(message['content'], 
    #                               message['mode'],
    #                               int(message['user']))
    socketio.emit('result_add_licence', result)
    

# Phân trang
def split_page(data, page):
    max_page = int(len(data) / PER_PAGE)
    if len(data) % PER_PAGE > max_page:
        max_page += 1

    this_page_from = page*PER_PAGE
    this_page_to = (page + 1)*PER_PAGE

    if this_page_to > len(data) - 1:
        this_page_to = len(data)

    result = []
    for i in range(len(data)):
        da = data[(len(data) - 1 - i)]
        if this_page_from <= i < this_page_to:
            result.append(da)

    if page > 0:
        last_page = page - 1
    else:
        last_page = None

    if page < max_page:
        next_page = page + 1
    else:
        next_page = None
    return result, last_page, next_page, max_page

#===================================================[ WEB SITE ]========================================================

LIST_SYMBOL = []
for symbol in DATA_SYMBOL:
    LIST_SYMBOL.append(symbol['symbol'])

@app.route('/', methods=['GET', "POST"])
@app.route('/user_active', methods=['GET'])
def index():
    if request.method == "POST":
        # Xử lý yêu cầu POST
        result = str(request.data).replace("b'", "").replace("'", "")
        
        # Định nghĩa hàm để gửi dữ liệu đến máy chủ khác
        def send_other_server():
            request_link("http://51.195.44.167/test_signal?signal=" + result)

        t1 = threading.Thread(target=send_other_server)
        t1.start()

        request_signal(result)
    elif request.method == "GET":
        # Xử lý yêu cầu GET
        
        # Xử lý phân trang
        if "page" in request.args:
            try:
                this_page = int(request.args["page"]) - 1
            except:
                this_page = 0
        else:
            this_page = 0

        # Khởi tạo biến đếm và danh sách người dùng hoạt động
        no = 0
        user_active = []

        # Tính thời gian hiện tại thành dấu thời gian
        ts_now = int(date_to_timestamp(time_now())*1000)
        
        # Lặp qua danh sách người dùng và người dùng cảnh báo
        for user in DATA_USER:
            for userr in DATA_USER_ALERT:
                if userr['tele_id'] == user['tele_id'] and userr['licence'] > ts_now:
                    no += 1
                    user_active.append({
                        "stt": no,
                        "tele_id": userr['tele_id'],
                        "username": user['tele_username'],
                        "name": user['tele_name'],
                        "join_date": str(timestamp_to_date(userr['join_date']/1000))[:19],
                        "licence_start": str(userr['full_licence_start'])[:19],
                        "licence": str(userr['full_licence'])[:19],
                        "status": userr['status']
                    })
                    
        # Xác định biểu tượng người dùng và xu hướng mặc định
        user_symbol = []
        user_trend = 99
        for active in DATA_ACTIVE_SYMBOL:
            if active['mode'] == "ALERT" and active['type'] != 99:
                user_symbol.append(active['symbol'])
                user_trend = active['type']

        # Xác định danh sách biểu tượng không nằm trong danh sách người dùng
        LIST_SYMBOL_NOT = []
        for symbol in LIST_SYMBOL:
            if symbol not in user_symbol:
                LIST_SYMBOL_NOT.append(symbol)
        
        # Xác định nội dung người dùng       
        USER_CONTENT = {}
        for form in DATA_FORM:
            if form['mode'] == "ALERT":
                USER_CONTENT = form
                break
        
        # Phân trang danh sách người dùng     
        result, last_page, next_page, max_page = split_page(user_active, this_page)
        
        # Trả về giao diện HTML với các dữ liệu và biến điều khiển
        return render_template('user.html', project="SYS Manage",
                               USER=result,
                               LIST_SYMBOL_NOT=LIST_SYMBOL_NOT,
                               USER_SYMBOL=user_symbol,
                               USER_TREND=user_trend,
                               USER_CONTENT=USER_CONTENT,
                               user_active=True,
                               page={'last_page': last_page,
                                     'next_page': next_page,
                                     'max_page': max_page,
                                     "this_page": this_page},
                               )

@app.route('/user_inactive', methods=['GET'])
def html_inactive():
    
    # Kiểm tra nếu trang yêu cầu chứa tham số 'page'
    if "page" in request.args:
        try:
            this_page = int(request.args["page"]) - 1
        except:
            this_page = 0
    else:
        this_page = 0

    no = 0
    user_active = []

    ts_now = int(date_to_timestamp(time_now())*1000)
    for user in DATA_USER:
        for userr in DATA_USER_ALERT:
            if userr['tele_id'] == user['tele_id'] and userr['licence'] < ts_now:
                no += 1
                user_active.append({
                    "stt": no,
                    "tele_id": userr['tele_id'],
                    "username": user['tele_username'],
                    "name": user['tele_name'],
                    "join_date": str(timestamp_to_date(userr['join_date']/1000))[:19],
                    "licence_start": str(userr['full_licence_start'])[:19],
                    "licence": str(userr['full_licence'])[:19],
                    "status": userr['status']
                })
    result, last_page, next_page, max_page = split_page(user_active, this_page)
    return render_template('user.html', project="SYS Manage",
                           USER=result,
                           LIST_SYMBOL=LIST_SYMBOL,
                           user_inactive=True,
                           page={'last_page': last_page,
                                 'next_page': next_page,
                                 'max_page': max_page,
                                 "this_page": this_page},
                           )

@app.route('/group', methods=['GET'])
def html_group():
    if "page" in request.args:
        try:
            this_page = int(request.args["page"]) - 1
        except:
            this_page = 0
    else:
        this_page = 0
        
    # Lặp qua danh sách các nhóm trong DATA_LIST_GROUP
    data = []
    for group in DATA_LIST_GROUP:
        if group['number'] is None:
            numb = -1
        else:
            numb = group['number']
            
        # Khởi tạo một mini dictionary để lưu thông tin về nhóm
        mini_gr = {
            "stt": group['stt'],
            "group_id": group['group_id'],
            "name": group['name'],
            "status": group['status'],
            "number": numb,
            "content": "Empty",
            "content_tp": "Empty",
            "content_sl": "Empty",
            "content_cl": "Empty",
            "content_rp": "Empty",
            "content_rp_cl": "Empty",
            "content_rp_run": "Empty",
            "trend": 99,
            "active_symbol": []
        }
        
        
        # Lặp qua danh sách DATA_FORM để tìm thông tin về nội dung của nhóm
        for form in DATA_FORM:
            if form['mode'] == 'GROUP' and form['id'] == group['group_id']:
                mini_gr['content'] = form['content']
                mini_gr['content_tp'] = form['content_tp']
                mini_gr['content_sl'] = form['content_sl']
                mini_gr['content_cl'] = form['content_cl']
                mini_gr['content_rp'] = form['content_rp']
                mini_gr['content_rp_cl'] = form['content_rp_cl']
                mini_gr['content_rp_run'] = form['content_rp_run']
                break
        
        # Lặp qua danh sách DATA_ACTIVE_SYMBOL để tìm thông tin về các biểu tượng hoạt động trong nhóm
        for active in DATA_ACTIVE_SYMBOL:
            if active['mode'] == "GROUP" and active['id'] == group['group_id'] and active['type'] != 99:
                mini_gr['active_symbol'].append(active['symbol'])
                if active['type'] != 99:
                    mini_gr['trend'] = active['type']
        data.append(mini_gr)

    result, last_page, next_page, max_page = split_page(data, this_page)

    # Trả về giao diện HTML với các dữ liệu và biến điều khiển
    return render_template('group.html', project="SYS Manage",
                           GROUP=result,
                           room_id=create_token(),
                           group=True,
                           list_symbol=LIST_SYMBOL,
                           GROUP_BOT=list_bot_name,
                           page={'last_page': last_page,
                                 'next_page': next_page,
                                 'max_page': max_page,
                                 "this_page": this_page},
                           )

@app.route('/symbol', methods=['GET'])
def html_symbol():
    # Kiểm tra nếu trang yêu cầu chứa tham số 'page'
    if "page" in request.args:
        try:
            this_page = int(request.args["page"]) - 1
        except:
            this_page = 0
    else:
        this_page = 0

    # Phân trang danh sách thông tin về các biểu tượng
    result, last_page, next_page, max_page = split_page(DATA_SYMBOL, this_page)
    
    # Lặp qua danh sách DATA_SYMBOL để trích xuất thông tin cần thiết và thêm vào danh sách data_symbol
    data_symbol = []
    for sym in DATA_SYMBOL:
        mini_sym = {
            "stt": sym['stt'],
            "symbol": sym['symbol']}
        if sym['max_leverage'] is not None:
            mini_sym['max_leverage'] = sym['max_leverage']
        else:
            mini_sym['max_leverage'] = 'None'
        if sym['entry_2'] is not None:
            mini_sym['entry_2'] = sym['entry_2']
        else:
            mini_sym['entry_2'] = 'None'
        if sym['tp1'] is not None:
            mini_sym['tp1'] = sym['tp1']
        else:
            mini_sym['tp1'] = 'None'
        if sym['tp2'] is not None:
            mini_sym['tp2'] = sym['tp2']
        else:
            mini_sym['tp2'] = 'None'
        if sym['tp3'] is not None:
            mini_sym['tp3'] = sym['tp3']
        else:
            mini_sym['tp3'] = 'None'
        if sym['tp4'] is not None:
            mini_sym['tp4'] = sym['tp4']
        else:
            mini_sym['tp4'] = 'None'
        if sym['tp5'] is not None:
            mini_sym['tp5'] = sym['tp5']
        else:
            mini_sym['tp5'] = 'None'
        if sym['tp6'] is not None:
            mini_sym['tp6'] = sym['tp6']
        else:
            mini_sym['tp6'] = 'None'
        if sym['tp7'] is not None:
            mini_sym['tp7'] = sym['tp7']
        else:
            mini_sym['tp7'] = 'None'
        if sym['sl'] is not None:
            mini_sym['sl'] = sym['sl']
        else:
            mini_sym['sl'] = 'None'
        if sym['digit'] is not None:
            mini_sym['digit'] = sym['digit']
        else:
            mini_sym['digit'] = 'None'
        data_symbol.append(mini_sym)
    
    # Trả về giao diện HTML với các dữ liệu và biến điều khiển        
    return render_template('symbol.html', project="SYS Manage",
                           SYMBOL=result,
                           SYMBOLS=data_symbol,
                           room_id=create_token(),
                           symbol=True,
                           page={'last_page': last_page,
                                 'next_page': next_page,
                                 'max_page': max_page,
                                 "this_page": this_page},
                           )

@app.route('/active_symbol', methods=['GET'])
def html_active_symbol():
    if "page" in request.args:
        try:
            this_page = int(request.args["page"]) - 1
        except:
            this_page = 0
    else:
        this_page = 0

    result, last_page, next_page, max_page = split_page(DATA_ACTIVE_SYMBOL, this_page)
    return render_template('active_symbol.html', project="SYS Manage",
                           ACTIVE_SYMBOL=result,
                           active_symbol=True,
                           page={'last_page': last_page,
                                 'next_page': next_page,
                                 'max_page': max_page,
                                 "this_page": this_page},
                           )

""" @app.route('/running_signal', methods=['GET'])
def html_running_signal(): 
    if "page" in request.args:
        try:
            this_page = int(request.args["page"]) - 1
        except:
            this_page = 0
    else:
        this_page = 0

    no = 0
    data = []
    
    for signal in DATA_SIGNAL:
        if signal['status'] == "ON":
            no += 1
            abc_signal = signal
            abc_signal['stt'] = no
            data.append(abc_signal)

    for signal in DATA_REPORT:
        no += 1
        abc_signal = signal
        abc_signal['stt'] = no
        data.append(abc_signal)
    list_group = []
    for group in DATA_LIST_GROUP:
        list_group.append({
            'id': group['group_id'],
            'name': group['name']
        })

    result, last_page, next_page, max_page = split_page(data, this_page)
    return render_template('signal.html', project="SYS Manage",
                           SIGNAL=result,
                           GROUP=list_group,
                           room_id=create_token(),
                           running_signal=True,
                           page={'last_page': last_page,
                                 'next_page': next_page,
                                 'max_page': max_page,
                                 "this_page": this_page},
                           ) """
    
@app.route('/running_signal', methods=['GET'])
def html_running_signal():
    date_from = request.args.get("date_from")
    date_to = request.args.get("date_to") 
    
    if "page" in request.args:
        try:
            this_page = int(request.args["page"]) - 1
        except:
            this_page = 0
    else:
        this_page = 0

    no = 0
    data = []
    
    for signal in DATA_SIGNAL:
        if signal['status'] == "ON":
            signal_time = datetime.strptime(signal["full_opentime"][:10], "%Y-%m-%d")
            if date_from and date_to and date_from <= signal_time <= date_to:
                no += 1
                abc_signal = signal
                abc_signal['stt'] = no
                data.append(abc_signal)
            elif not date_from and not date_to:
                no += 1
                abc_signal = signal
                abc_signal['stt'] = no
                data.append(abc_signal)

    for signal in DATA_REPORT:
        signal_time = datetime.strptime(signal["full_opentime"][:10], "%Y-%m-%d")
        if date_from and date_to and date_from <= signal_time <= date_to:
            no += 1
            abc_signal = signal
            abc_signal['stt'] = no
            data.append(abc_signal)
        elif not date_from and not date_to:
            no += 1
            abc_signal = signal
            abc_signal['stt'] = no
            data.append(abc_signal)
            
    list_group = []
    for group in DATA_LIST_GROUP:
        list_group.append({
            'id': group['group_id'],
            'name': group['name']
        })

    result, last_page, next_page, max_page = split_page(data, this_page)
    return render_template('signal.html', project="SYS Manage",
                           SIGNAL=result,
                           GROUP=list_group,
                           room_id=create_token(),
                           running_signal=True,
                           page={'last_page': last_page,
                                 'next_page': next_page,
                                 'max_page': max_page,
                                 "this_page": this_page},
                           )


""" @app.route('/closed_signal', methods=['GET'])
def html_closed_signal():
    if "page" in request.args:
        try:
            this_page = int(request.args["page"]) - 1
        except:
            this_page = 0
    else:
        this_page = 0

    data = []
    for signal in DATA_SIGNAL:
        if signal['status'] == "OFF":
            data.append(signal)

    for signal in DATA_REPORT:
        data.append(signal)

    result, last_page, next_page, max_page = split_page(data, this_page)
    return render_template('signal.html', project="SYS Manage",
                           SIGNAL=result,
                           closed_signal=True,
                           page={'last_page': last_page,
                                 'next_page': next_page,
                                 'max_page': max_page,
                                 "this_page": this_page},
                           ) """


def filter_signals_by_date(signals, date_from, date_to):
    filtered_signals = []
    for signal in signals:
        signal_time = datetime.strptime(signal['full_opentime'][:10], '%Y-%m-%d')
        if date_from <= signal_time <= date_to:
            filtered_signals.append(signal)
    return filtered_signals
                        
@app.route('/closed_signal', methods=['GET'])
def html_closed_signal():
    date_from_str = request.args.get('date_from')
    date_to_str = request.args.get('date_to')
    
    date_from = None
    date_to = None
    
    if date_from_str and date_to_str:
        date_from = datetime.strptime(date_from_str, '%Y-%m-%d')
        date_to = datetime.strptime(date_to_str, '%Y-%m-%d')
    
    if "page" in request.args:
        try:
            this_page = int(request.args["page"]) - 1
        except:
            this_page = 0
    else:
        this_page = 0

    data = []
    
    for signal in DATA_SIGNAL:
        if signal['status'] == "OFF":
            data.append(signal)

    for signal in DATA_REPORT:
        data.append(signal)
    
    filtered_data = data  # Initialize with all data

    if date_from and date_to:
        filtered_data = filter_signals_by_date(data, date_from, date_to)
    
    result, last_page, next_page, max_page = split_page(filtered_data, this_page)
    
    print("Result: " + str(result))
    print("Last Page: " + str(last_page))
    print("next_page: ", str(next_page))
    print("Max page: " + str(max_page))
    
    return render_template('signal.html', project="SYS Manage",
                           SIGNAL=result,
                           closed_signal=True,
                           page={'last_page': last_page,
                                 'next_page': next_page,
                                 'max_page': max_page,
                                 "this_page": this_page},
                           )




@app.route('/licence', methods=['GET'])
def html_licence():
    if "page" in request.args:
        try:
            this_page = int(request.args["page"]) - 1
        except:
            this_page = 0
    else:
        this_page = 0

    data = []
    for licence in DATA_USER_BUY_LICENCE:
        for user in DATA_USER:
            if licence['tele_id'] == user['tele_id']:
                data.append({
                    "stt": licence['stt'],
                    "tele_id": licence['tele_id'],
                    "full_ordertime": licence['full_ordertime'],
                    "ordertime": licence['ordertime'],
                    "mode": licence['mode'],
                    "licence_day": licence['licence_day'],
                    "content": licence['content'],
                    "confirm": licence['confirm'],
                    "name": user['tele_name'],
                    "username": user['tele_username']
                })
    result, last_page, next_page, max_page = split_page(data, this_page)
    return render_template('licence.html', project="SYS Manage",
                           LICENCE=result,
                           licence=True,
                           page={'last_page': last_page,
                                 'next_page': next_page,
                                 'max_page': max_page,
                                 "this_page": this_page},
                           )


#===================================================[ BOT USER ]========================================================
@app.route('/request_sltp', methods=['POST'])
def server_request_post_sltp():
    # Nhận dữ liệu JSON từ yêu cầu POST
    result = request.json

    # Kiểm tra tùy chọn được truyền trong dữ liệu JSON
    if result['option'] == "RUNNING_ORDER":
        data = []
        for signal in DATA_SIGNAL:
            if signal['status'] == 'ON':
                data.append(signal)
        for signal in DATA_REPORT:
            data.append(signal)               
        return jsonify(data)
    elif result['option'] == "RUNNING_CHECKED":
        hit_sl_tp(result['opentime'], result['data'])
        # data = {
        #     "symbol": "",
        #     "tp1-6_hit": ""
        # }
        return jsonify(["Done"])

@app.route('/bot_request', methods=['POST'])
def server_request_post():
    result = request.json
    
    # Tạo một biến để chứa dữ liệu trả về
    retu = {}
    
    if result['option'] == "REQUEST_GET_RUN":
        return jsonify({
            'token': {
                "alert": TOKEN_ALERT,
                "group": TOKEN_GROUP
            },
            "admin": TELE_ADMIN
        })
    elif result['option'] == "REQUEST_USER":
        retu = bot_request_user(result['tele_id'], result['username'], result['name'])
    elif result['option'] == "REQUEST_ADD_LICENCE":
        retu = request_add_licence(result['tele_id'], result['name'], result['content'])
    elif result['option'] == "REQUEST_CHECK_TRADE":
        retu = send_signal_report(result['content_type'],
                                   "alert:active",
                                   result['from'],
                                   result['to'],
                                   "CHECK", "NO_SEND", "")
    elif result['option'] == "REQUEST_USER_STATUS":
        request_user_status([], result['status'])
        retu = {'status': True}
    elif result['option'] == "REQUEST_USER_STATUS":
        request_user_status([], result['status'])
        retu = {'status': True}
    elif result['option'] == "REQUEST_TREND":
        retu = bot_request_trend(result['mode'],
                                 result['trend'],
                                 result['group_id'])
    return jsonify(retu)

    
