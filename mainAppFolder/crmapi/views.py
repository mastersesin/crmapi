from flask import request, jsonify, Blueprint, abort, send_file
from mainAppFolder.crmapi import functions, returnMsg, sqlQuery
from datetime import datetime
import qrcode
from io import BytesIO

# from mainAppFolder.crmapi import testProject3
crmapiApp = Blueprint('crmapiApp', __name__)


@crmapiApp.route('/', methods=['GET'])
def index():
    return "<h1>HYG CRM</h1>"


@crmapiApp.route('/qrcode/<couponcode>', methods=['GET'])
def qrcode(couponcode):
    temp = BytesIO()
    img = functions.random_qr(couponcode)
    img.save(temp, 'PNG')
    temp.seek(0)
    return send_file(temp, mimetype='image/png')


@crmapiApp.route('/hycheck/<cardcode>', methods=['GET'])
def inside(cardcode):
    try:
        assert (len(cardcode) == 6)
        cardcode = int(cardcode)
    except:
        return jsonify(returnMsg.returnMsgTest().four_hundred)
    msg = returnMsg.returnMsgTest().return_card_info
    record = [record for record in sqlQuery.get_card_info(cardcode)]
    print(record)
    if len(record) == 1:
        CARD_CODE, PEOPLE_ID, F_NAME, L_NAME, FULL_NAME, TEXT_PASSWORD, BIRTHDAY, SOURCE, BALANCE = record[0]
        try:
            msg['msg'] = {'BALANCE': float(BALANCE)}
        except:  # BALANCE variable can be none but float() not happy with that
            msg['msg'] = {'BALANCE': float(BALANCE)}
        BALANCE = round(BALANCE)
        return str("<h1>Số dư Giftcard:     {:,}<h1>".format(BALANCE))
    else:
        abort(500)


@crmapiApp.route('/login', methods=['POST'])
def login():
    if request.is_json:
        cardcode = request.json.get('cardcode')
        password = request.json.get('password')
        try:
            assert (len(str(cardcode)) == 6)
            cardcode = int(cardcode)
        except:
            return jsonify(returnMsg.returnMsgTest().four_hundred)
        dataReturnFromSQL = [record for record in sqlQuery.get_cardcode_password(cardcode)]
        if len(dataReturnFromSQL) == 1:
            cardcodeCheck, cardcodeCheckPassword, people_id = dataReturnFromSQL[0]
            print(cardcodeCheck, cardcodeCheckPassword, people_id)
            if not cardcodeCheckPassword:
                cardcodeCheckPassword = '19801980'
            else:
                pass
            if cardcodeCheckPassword == password:
                msg = returnMsg.returnMsgTest().return_token
                if cardcodeCheckPassword == '19801980':
                    msg['isFirstLogin'] = False
                else:
                    msg['isFirstLogin'] = False
                msg['msg'] = functions.generate_auth_token(cardcode, people_id)
                return jsonify(msg)
            else:
                return jsonify(returnMsg.returnMsgTest().username_or_password_incorrect)
        elif len(dataReturnFromSQL) == 0:
            return jsonify(returnMsg.returnMsgTest().username_or_password_incorrect)
        else:
            abort(500)
    else:
        abort(405)


@crmapiApp.route('/changepw', methods=['PUT'])
@functions.login_required
def firstlogin(guardMsg):
    if request.is_json:
        if guardMsg == 'Warn':
            return jsonify(returnMsg.returnMsgTest().four_hundred)
        else:
            password = request.json.get('password')
            sqlQuery.change_password(guardMsg, password)
            return jsonify(returnMsg.returnMsgTest().password_change_successfully)
    else:
        abort(405)


@crmapiApp.route('/transactions', methods=['GET'])
@functions.login_required
def transactions(guardMsg):
    date_from = request.args.get('from')
    date_to = request.args.get('to')
    if not date_from or not date_to:
        date_from = '1970-1-1'
        timenow = datetime.now()
        date_to = '{}-{}-{}'.format(timenow.year, timenow.month, timenow.day)
    else:
        pass
    if guardMsg == 'Warn':
        return jsonify(returnMsg.returnMsgTest().four_hundred)
    elif guardMsg == 'Expired':
        return jsonify(returnMsg.returnMsgTest().token_expired)
    else:
        msg = returnMsg.returnMsgTest().return_transaction_list
        for record in sqlQuery.get_transactions(guardMsg, date_from, date_to):
            id, value_transaction, time, location, details = [value for value in record]
            if details != None:
                details = functions.convert_xml_json(details)
                details = details['CHECK']['CHECKDATA']['CHECKLINES']['LINE']
            try:
                msg['msg'][id] = {'value': float(value_transaction), 'location': location, 'time': time[:-15],
                                  'details': details}
            except:  # value variable can be none but float() not happy with that
                msg['msg'][id] = {'value': value_transaction, 'location': location, 'time': time[:-15],
                                  'details': details}
        return jsonify(msg)


@crmapiApp.route('/cardinfo', methods=['GET'])
@functions.login_required
def cardinfo(guardMsg):
    if guardMsg == 'Warn':
        return jsonify(returnMsg.returnMsgTest().four_hundred)
    elif guardMsg == 'Expired':
        return jsonify(returnMsg.returnMsgTest().token_expired)
    else:
        msg = returnMsg.returnMsgTest().return_card_info
        if int(str(guardMsg)[0]) == 6:
            cardcode_type = 'Tich luy'
            balance_type = 'ACCUMULATION'
        elif int(str(guardMsg)[0]) == 7 or int(str(guardMsg)[0]) == 9:
            cardcode_type = 'Vi uu dai'
            balance_type = 'BALANCE'
        else:
            return jsonify(returnMsg.returnMsgTest().four_hundred)
        record = [value for value in sqlQuery.get_card_info(guardMsg, cardcode_type)]
        if len(record) == 1:
            CARD_CODE, PEOPLE_ID, F_NAME, L_NAME, FULL_NAME, TEXT_PASSWORD, BIRTHDAY, SOURCE, BALANCE, HANG_THE = \
                record[0]
            try:
                msg['msg'] = {'CARD_CODE': CARD_CODE, 'PEOPLE_ID': PEOPLE_ID, 'F_NAME': F_NAME, 'L_NAME': L_NAME,
                              'BIRTHDAY': BIRTHDAY, 'SOURCE': SOURCE, balance_type: float(BALANCE),
                              'TYPE': cardcode_type,
                              'RANK': HANG_THE}
            except:  # BALANCE variable can be none but float() not happy with that
                msg['msg'] = {'CARD_CODE': CARD_CODE, 'PEOPLE_ID': PEOPLE_ID, 'F_NAME': F_NAME, 'L_NAME': L_NAME,
                              'BIRTHDAY': BIRTHDAY, 'SOURCE': SOURCE, balance_type: BALANCE, 'TYPE': cardcode_type,
                              'RANK': HANG_THE}
            print(msg)
            return jsonify(msg)
        else:
            abort(500)


@crmapiApp.route('/coupons', methods=['GET'])
@functions.login_required
def coupons(guardMsg):
    if guardMsg == 'Warn':
        return jsonify(returnMsg.returnMsgTest().four_hundred)
    elif guardMsg == 'Expired':
        return jsonify(returnMsg.returnMsgTest().token_expired)
    else:
        msg = returnMsg.returnMsgTest().return_coupons_of_card
        records = [value for value in sqlQuery.get_coupons(guardMsg)]
        for record in records:
            cardcode, peopleID, couponID, couponCode, couponName, Datefrom, Dateto, Flag = record
            if Flag == 49:  # Flag 49 mean not yet used
                msg['msg'].update(
                    {couponID: {
                        'name': couponName,
                        'couponID': couponID,
                        'Dateto': Dateto,
                        'qrlink': '/qrcode/{}'.format(couponID)
                    }})
            elif Flag == 51:
                # msg['msg'].update({couponID: {'name': couponName, 'issued': Datefrom, 'flag': 'Đã sử dụng'}})
                pass
            else:
                pass
        return jsonify(msg)


@crmapiApp.route('/logout', methods=['POST'])
@functions.login_required
def logout(guardMsg):
    if guardMsg == 'Warn':
        return jsonify(returnMsg.returnMsgTest().four_hundred)
    elif guardMsg == 'Expired':
        return jsonify(returnMsg.returnMsgTest().token_expired)
    else:
        msg = returnMsg.returnMsgTest().logout
        return jsonify(msg)


@crmapiApp.route('/data', methods=['GET'])
def setting():
    return jsonify({
        "hotline": "0934 086 638",
        "logo": "http://50.116.1.159/~hy/storage/images/aDs0Rxxau6dqjwlFh2ITPjsEhx0pcwYl2rtSh7o2.png",
        "address_type_name": "Địa chỉ",
        "default_city": None
    })
