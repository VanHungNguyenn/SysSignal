LIST_PORT_TRADINGVIEW = {
    "stt": 0,
    "opentime": 1,
    "signal": 2,
    "full_opentime": "1"
}

SIGNAL = {
    "stt": 0,
    "opentime": 1,
    "ordertype": 2,
    "symbol": 3,
    "entry_1": 4,
    "entry_2": 5,
    "status": 6,
    "sl": 7,
    "sl_hit": 8,
    "tp1": 9,
    "tp1_hit": 10,
    "tp2": 11,
    "tp2_hit": 12,
    'tp3': 13,
    "tp3_hit": 14,
    "tp4": 15,
    "tp4_hit": 16,
    "tf": 17,
    "close_price": 18,
    "tp5": 19,
    "tp5_hit": 20,
    "tp6": 21,
    "tp6_hit": 22,
    "tp7": 23,
    "tp7_hit": 24,
    "full_opentime": "1"
}



SYMBOL = {
    "stt": 0,
    "symbol": 1,
    "max_leverage": 2,
    "entry_2": 3,
    "tp1": 4,
    "tp2": 5,
    "tp3": 6,
    "tp4": 7,
    "sl": 8,
    "status     xxxx": 9,
    "tp5": 10,
    "tp6": 11,
    "tp7": 12,
    "digit": 13
}

ACTIVE_SYMBOL = {
    "stt": 0,
    "symbol": 1,
    "mode": 2,
    "type [-1, 0, 1, 99]": 3,
    "id": 4
}
# 0 - BUY
# 1 - SELL
# -1 - Both
# 99 - Disable

FORM = {
    "stt": 0,
    "mode": 1,
    "id": 2,
    "content": 3,
    "content_tp": 4,
    "content_sl": 5,
    "content_cl": 6,
    "content_rp": 7,
    "content_rp_cl": 8,
    "content_rp_run": 9
}

POST_SIGNAL = {
    "stt": 0,
    "tele_id": 1,
    "opentime": 2,
    "binance_ticket     xx": 3,
    "mess_id": 4,
    "mode": 5,
    "sl        xx": 6,
    "tp        xx": 7
}

USER = {
    "stt": 0,
    "tele_id": 1,
    "tele_username": 2,
    "tele_name": 3
}

USER_BUY_LICENCE = {
    "stt": 0,
    "tele_id": 1,
    "mode": 2,
    "licence_day": 3,
    "content": 4,
    "confirm": 5,
    "ordertime": 6,
    "full_ordertime": '1'
}

USER_ALERT = {
    "stt": 0,
    "tele_id": 1,
    "join_date": 2,
    "remind_licence": 3,
    "licence": 4,
    "f0": 5,
    "licence_start": 6,
    "status": 7,
    "full_licence": '1',
    "full_licence_start": '2'
}

LIST_GROUP = {
    "stt": 0,
    "group_id": 1,
    "name": 2,
    "status": 3,
    "number": 4
}