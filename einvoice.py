import hashlib
import hmac
import json
import re
import time
import datetime
import base64
import random
import requests

class Einvoice():
    args = {}
    api_endpoint = 'https://api.einvoice.nat.gov.tw'

    def __init__(self, app_id=None, api_key=None, url_list=None, version_list=None, action_list=None):
        self.args['appID'] = app_id
        self.api_key = api_key
        self.url_list = url_list
        self.version_list = version_list
        self.action_list = action_list

    def handle_message(self, args_dict, url, sign_or_not=False, special=False, blank=False):
        if not special:
            url = self.api_endpoint + url
        args_str = ''
        args_pairs = []

        for i, j in args_dict.items():
            args_pairs.append(str(i) + '=' + str(j))
        for i in sorted(args_pairs, key=str.lower):
            args_str += i + '&'
        args_str = args_str[0: len(args_str)-1]
        
        if sign_or_not:
            args_str = self.sign(args_str, self.api_key)
        url += args_str
        
        print('request url : ' + url)
        response = requests.post(url)
        if response.status_code != 200:
            print('ERROR 1, ' + str(response.status_code))
            msg = {'code': response.status_code, 'msg': response.status_code}
            return msg
        if blank:
            return response.text
        res = json.loads(response.text)
        if int(res['code']) == 200:
            return res
        else:
            print('ERROR 2, ' + str(res['code']) + ' ' + res['msg'])
            msg = {'code': res['code'], 'msg': res['msg']}
            return msg
            
    @staticmethod
    def sign(msg, key):
        h = hmac.new(key.encode(), msg.encode('UTF-8'), hashlib.sha256)
        signature = base64.b64encode(h.digest()).decode()

        return msg + "&signature=" + signature
        
    @staticmethod
    def check_invoice_number(inv_num):
        if len(inv_num) != 11 and len(inv_num) != 10:
            return False
        elif len(inv_num) == 11 and '-' not in inv_num:
            return False
        else:
            inv_num = inv_num.replace('-', '')
        if len(inv_num) != 10:
            return False
        inv_num = inv_num.upper()
        if not re.search(r'[A-Z]{2}[0-9]{8}', inv_num):
            return False
        return inv_num

    @staticmethod
    def check_invoice_date(inv_date): 
        inv_date = inv_date.replace('-', '/')
        try:
            datetime.datetime.strptime(inv_date, '%Y/%m/%d')
        except:
            return False
        first_slash = inv_date.find('/')
        second_slash = inv_date.find('/', first_slash+1)
        
        if len(inv_date) - second_slash == 2:
            inv_date = inv_date[0: second_slash+1] + '0' + inv_date[second_slash+1: len(inv_date)]
        if second_slash - first_slash == 2:
            inv_date = inv_date[0: first_slash+1] + '0' + inv_date[first_slash+1: len(inv_date)]
        try:
            inv_date = datetime.datetime.strptime(inv_date, '%Y/%m/%d')
        except:
            return False
        return inv_date
    
    @staticmethod
    def invoice_date_to_term(inv_date):
        term = str(int(inv_date[0:4]) - 1911)
        if int(inv_date[5:7]) % 2 == 0:
            term += inv_date[5:7]
        elif int(inv_date[5:7]) < 9:
            term += '0' + str(int(inv_date[5:7]) + 1)
        else:
            term += str(int(inv_date[5:7]) + 1)
        print('term : ' + term)
        return term

    @staticmethod
    def format_number(num):
        num = float(num)
        num = str(num)
        num = num[0: len(num)-2] if num.find('.0') != -1 else num
        return num
    
    @staticmethod
    def format_date(month, date, inv_time):
        msg = ''
        if int(month/10) == 0:
            msg += '0' + str(month)
        else:
            msg += str(month)
        msg += '/'
        if int(date/10) == 0:
            msg += '0' + str(date)
        else:
            msg += str(date)
        msg += ' ' + str(inv_time)[0:5]
        return msg

    def winning_list_query(self, inv_term):
        args_dict = self.args
        url = self.url_list['query_winning_list']
        args_dict['version'] = self.version_list['query_winning_list']
        args_dict['action'] = self.action_list['query_winning_list']
        args_dict['invTerm'] = inv_term
        return self.handle_message(args_dict, url)

    def winning_list_get(self, inv_term):
        winning = self.winning_list_query(inv_term)
        if int(winning['code']) != 200:
            msg = '查詢失敗... ' + winning['msg']
            return msg
        msg = '特別獎(8位號碼皆同) NT$ 10,000,000\n'
        msg += winning['superPrizeNo'] + '\n'
        msg += '特獎(8位號碼皆同) NT$ 2,000,000\n'
        for i in winning.keys():
            if re.search(r'spcPrizeN.', i):
                if winning[i]:
                    msg += winning[i] + '\n'
        msg += '頭獎(8位號碼皆同) NT$200,000\n'
        for i in winning.keys():
            if re.search(r'firstPrizeN.', i):
                if winning[i]:
                    msg += winning[i] + '\n' 
        msg += '二獎(後位號碼相同) NT$ 40,000\n'
        msg += '三獎(後位號碼相同) NT$ 10,000\n'
        msg += '四獎(後位號碼相同) NT$ 4,000\n'
        msg += '五獎(後位號碼相同) NT$ 1,000\n'
        msg += '六獎(後位號碼相同) NT$ 200\n'
        for i in winning.keys():
            if re.search(r'sixthPrizeN.', i):
                if winning[i]:
                    msg += winning[i] + '\n' 
        msg += '※ 中四獎(含)以上，扣繳20﹪所得稅款。\n※ 中五獎(含)以上，繳納0.4%印花稅款。'
        return msg

    def invoice_header_query(self, inv_num, inv_date, query_type='QRCode', uuid=8899757, generation='V2', only_seller_id=False):
        args_dict = self.args
        url = self.url_list['query_invoice_header']
        args_dict['version'] = self.version_list['query_invoice_header']
        args_dict['action'] = self.action_list['query_invoice_header']

        inv_num = self.check_invoice_number(inv_num)
        inv_date = self.check_invoice_date(inv_date)
        if inv_num:
            args_dict['invNum'] = inv_num
        else:
            return {'code': -1, 'msg': '發票格式錯誤...'}
        if inv_date:
            args_dict['invDate'] = inv_date.strftime('%Y/%m/%d')
        else:
            return {'code': -1, 'msg': '日期格式錯誤...'}

        args_dict['type'] = query_type
        args_dict['generation'] = generation
        args_dict['UUID'] = uuid

        if only_seller_id:
            msg = self.handle_message(args_dict, url)
            if msg['invStatus'] != '已確認':
                return {'code': -1, 'msg': msg['invStatus']}
            return {'code': 200, 'msg': msg['sellerBan']}
        else:
            return self.handle_message(args_dict, url)

    def invoice_header_get(self, inv_num, inv_date, query_type='QRCode', uuid=8899757, generation='V2'):
        info = self.invoice_header_query(inv_num, inv_date, query_type, uuid, generation)
        
        if int(info['code']) != 200:
            msg = '查詢失敗... ' + info['msg']
            return msg

        if info['invStatus'] != '已確認' and info['invStatus'] != '2':
            msg = '查詢失敗, 發票狀態 : ' + info['invStatus']
            return msg

        msg = info['invNum'][0:2] + '-' + info['invNum'][2:10] + '\n'
        msg += info['invDate'][0:4] + '-' + info['invDate'][4:6] + '-' + info['invDate'][6:8]
        msg += ' ' + info['invoiceTime'] + '\n'
        msg += info['sellerName'] + ' (' + info['sellerBan'] + ')\n'
        msg += info['sellerAddress']
        return msg

    def invoice_detail_query(self, inv_num, inv_date, random_number, encrypt=None, seller_id=None, query_type='QRCode', uuid=8899757, generation='V2'):
        args_dict = self.args
        url = self.url_list['query_invoice_detail']
        if query_type == 'QRCode':
            if not encrypt:
                return '請輸入發票檢驗碼...'
            args_dict['encrypt'] = encrypt
            if seller_id:
                args_dict['sellerID'] = seller_id
            else:
                seller_id = self.invoice_header_query(inv_num, inv_date, only_seller_id=True)
                if seller_id['code'] == 200:
                    args_dict['sellerID'] = seller_id['msg']
                else:
                    return seller_id
        elif query_type == 'Barcode':
            args_dict['invTerm'] = self.invoice_date_to_term(inv_date)

        args_dict['action'] = self.action_list['query_invoice_detail']
        args_dict['version'] = self.version_list['query_invoice_detail']

        inv_num = self.check_invoice_number(inv_num)
        inv_date = self.check_invoice_date(inv_date)
        if inv_num:
            args_dict['invNum'] = inv_num
        else:
            return {'code': -1, 'msg': '發票格式錯誤...'}
        if inv_date:
            args_dict['invDate'] = inv_date.strftime('%Y/%m/%d')
        else:
            return {'code': -1, 'msg': '日期格式錯誤...'}

        args_dict['type'] = query_type
        args_dict['randomNumber'] = random_number
        args_dict['generation'] = generation
        args_dict['UUID'] = uuid
        return self.handle_message(args_dict, url)

    def invoice_detail_get(self, inv_num, inv_date, random_number, encrypt=None, seller_id=None, query_type='QRCode', uuid=8899757, generation='V2'):
        info = self.invoice_detail_query(inv_num, inv_date, random_number, encrypt, seller_id, query_type, uuid, generation)

        if int(info['code']) != 200:
            msg = '查詢失敗... ' + info['msg']
            return msg

        if not info.get('details', False):
            return '查詢失敗... 可能是隨機碼錯誤'
        msg = info['invNum'][0:2] + '-' + info['invNum'][2:10] + '\n'
        msg += info['invDate'][0:4] + '-' + info['invDate'][4:6] + '-' + info['invDate'][6:8]
        msg += ' ' + info['invoiceTime'] + '\n'
        msg += info['sellerName'] + ' (' + info['sellerBan'] + ')\n'
        msg += info['sellerAddress'] + '\n'

        for i in info['details']:
            msg += i['description'] + ' ' + self.format_number(i['unitPrice']) + 'x' + self.format_number(i['quantity'])
            msg += ' = ' + self.format_number(i['amount']) + '\n'
        return msg[0: len(msg)-1]

    def love_code_query(self, query_key, uuid=8899757):
        args_dict = self.args
        url = self.url_list['query_love_code']
        args_dict['action'] = self.action_list['query_love_code']
        args_dict['version'] = self.version_list['query_love_code']
        args_dict['qKey'] = query_key
        args_dict['UUID'] = uuid
        return self.handle_message(args_dict, url)

    def love_code_get(self, query_key, uuid=8899757):
        info = self.love_code_query(query_key, uuid)
        if not info.get('details', False):
            return '沒有找到相符合的受贈機關或團體...'
        msg = '查詢成功...\n'
        for i in info['details']:
            msg += str(i['rowNum']+1) + '. ' + i['SocialWelfareName'] + ', ' + i['LoveCode'] + '\n'
        return msg[0: len(msg)-1]

    def carrier_header_query(self, card_type, card_encrypt, card_no, start_time=None, end_time=None, only_winning='N', uuid=8899757):
        args_dict = self.args
        url = self.url_list['carrier_invoice_header']
        args_dict['action'] = self.action_list['carrier_invoice_header']
        args_dict['version'] = self.version_list['carrier_invoice_header']

        args_dict['onlyWinningInv'] = only_winning
        args_dict['cardType'] = card_type
        args_dict['cardNo'] = card_no
        args_dict['cardEncrypt'] = card_encrypt
        args_dict['uuid'] = uuid

        current = int(time.time())
        today = datetime.datetime.now()
        if not end_time:
            end_time = today
        else:
            end_time = self.check_invoice_date(end_time)
        if not start_time:
            start_time = datetime.datetime(today.year, today.month, 1)
        else:
            start_time = self.check_invoice_date(start_time)

        #print(start_time)
        #print(end_time)
        if start_time == False or end_time == False:
            return {'code': -1, 'msg': '日期格式錯誤...'}
        if start_time.timestamp() - end_time.timestamp() > 0:
            return {'code': -1, 'msg': '結束時間早於起始時間...'}

        args_dict['startDate'] = start_time.strftime('%Y/%m/%d')
        args_dict['endDate'] = end_time.strftime('%Y/%m/%d')
        args_dict['timeStamp'] = current+20
        args_dict['expTimeStamp'] = current+87
        return self.handle_message(args_dict, url)

    def carrier_header_get(self, card_encrypt, card_no, start_time=None, end_time=None, only_winning='N', uuid=8899757):
        info = self.carrier_header_query(card_encrypt, card_no, start_time, end_time, only_winning, uuid)
        
        if int(info['code']) != 200:
            msg = '查詢失敗... ' + info['msg']
            return msg

        msg = ''
        for i in info['details']:
            msg += i['invNum'][0:2] + '-' + i['invNum'][2:10] + '   ' + str(i['amount']) + '\n- '
            msg += self.format_date(i['invDate']['month'], (i['invDate']['date']), i['invoiceTime']) + '\n'
        return msg[0:len(msg)-1]

    def carrier_detail_query(self, card_type, inv_num, inv_date, card_encrypt, card_no, uuid=8899757):
        args_dict = self.args
        url = self.url_list['carrier_invoice_detail']
        args_dict['action'] = self.action_list['carrier_invoice_detail']
        args_dict['version'] = self.version_list['carrier_invoice_detail']

        inv_num = self.check_invoice_number(inv_num)
        inv_date = self.check_invoice_date(inv_date)
        if inv_num:
            args_dict['invNum'] = inv_num
        else:
            return {'code': -1, 'msg': '發票格式錯誤...'}
        if inv_date:
            args_dict['invDate'] = inv_date.strftime('%Y/%m/%d')
        else:
            return {'code': -1, 'msg': '日期格式錯誤...'}

        args_dict['cardType'] = card_type
        args_dict['cardNo'] = card_no
        args_dict['cardEncrypt'] = card_encrypt
        args_dict['uuid'] = uuid

        current = int(time.time())
        args_dict['timeStamp'] = current+20
        args_dict['expTimeStamp'] = current+87
        return self.handle_message(args_dict, url)

    def carrier_detail_get(self, inv_num, inv_date, card_encrypt, card_no, uuid=8899757):
        info = self.carrier_detail_query(inv_num, inv_date, card_encrypt, card_no, uuid)

        if int(info['code']) != 200:
            msg = '查詢失敗... ' + info['msg']
            return msg
        
        if info['invStatus'] != '已確認' and info['invStatus'] != '2':
            msg = '查詢失敗, 發票狀態 : ' + info['invStatus']
            return msg

        msg = info['invNum'][0:2] + '-' + info['invNum'][2:10] + '\n'
        msg += info['invDate'][0:4] + '-' + info['invDate'][4:6] + '-' + info['invDate'][6:8]
        msg += ' ' + info['invoiceTime'] + '\n'
        msg += info['sellerName'] + ' (' + info['sellerBan'] + ')\n'
        msg += info['sellerAddress']

        for i in info['details']:
            msg += i['description'] + ' ' + self.format_number(i['unitPrice']) + 'x'
            msg += self.format_number(i['quantity']) + ' = ' + self.format_number(i['amount']) + '\n'
        msg += '總價 : ' + info['amount']
        return msg

    # 似乎是任何欄位有錯都會報簽名有誤， 處理完後要改動檢查發票號碼日期的方式
    def carrier_donate_query(self, card_type, card_encrypt, card_no, inv_date, inv_num, love_code, uuid=8899757):
        args_dict = self.args
        url = self.url_list['carrier_invoice_donate']
        args_dict['action'] = self.action_list['carrier_invoice_donate']
        args_dict['version'] = self.version_list['carrier_invoice_donate']
        
        inv_num = self.check_invoice_number(inv_num)
        inv_date = self.check_invoice_date(inv_date)
        if inv_num:
            args_dict['invNum'] = inv_num
        else:
            return {'code': -1, 'msg': '發票格式錯誤...'}
        if inv_date:
            args_dict['invDate'] = inv_date.strftime('%Y/%m/%d')
        else:
            return {'code': -1, 'msg': '日期格式錯誤...'}

        args_dict['cardType'] = card_type
        args_dict['cardEncrypt'] = card_encrypt
        args_dict['cardNo'] = card_no
        args_dict['npoBan'] = love_code
        args_dict['uuid'] = uuid
        args_dict['serial'] = '00000' + str(random.randint(10000, 99999))

        current = int(time.time())
        args_dict['timeStamp'] = current+20
        args_dict['expTimeStamp'] = current+87
        return self.handle_message(args_dict, url, sign_or_not=True)
        
    def carrier_donate_get(self, card_type, card_encrypt, card_no, inv_date, inv_num, love_code, uuid=8899757):
        info = self.carrier_donate_query(card_type, card_encrypt, card_no, inv_date, inv_num, love_code, uuid)
        msg = info
        return msg

    # ?! sometimes goes wrong !?
    def carrier_aggregate_query(self, card_type, card_encrypt, card_no, uuid=8899757):
        args_dict = self.args
        url = self.url_list['query_carrier_aggregate']
        args_dict['action'] = self.action_list['query_carrier_aggregate']
        args_dict['version'] = self.version_list['query_carrier_aggregate']

        args_dict['serial'] = '00000' + str(random.randint(10000, 99999))
        args_dict['cardType'] = card_type
        args_dict['cardNo'] = card_no
        args_dict['cardEncrypt'] = card_encrypt
        args_dict['uuid'] = uuid
        args_dict['timeStamp'] = int(time.time()) + 20
        return self.handle_message(args_dict, url, sign_or_not=True)
    
    # ?! sometimes goes wrong !?
    def carrier_aggregate_get(self, card_type, card_encrypt, card_no, uuid=8899757):
        info = self.carrier_aggregate_query(card_type, card_encrypt, card_no, uuid)
        
        if int(info['code']) == 954:
            msg = '查詢失敗... ' + '未找到原因的常態異常錯誤...'
            return msg

        if int(info['code']) != 200:
            msg = '查詢失敗... ' + info['msg']
            return msg
        
        msg = ''
        for i in info['carriers']:
            msg += i['carrierName'] + ' : ' + i['carrierId2'] + '\n'
        return msg[0: len(msg)-1]

    def carrier_statistics_query(self, card_encrypt, card_no, start_time=None, end_time=None):
        args_dict = self.args
        url = self.url_list['query_carrier_statistics']
        args_dict['version'] = self.version_list['query_carrier_statistics']

        args_dict['verifyCode'] = card_encrypt
        args_dict['barcode'] = card_no

        today = datetime.datetime.now()
        if not end_time:
            end_time = today
        else:
            end_time = self.check_invoice_date(end_time)
        if not start_time:
            start_time = datetime.datetime(today.year, today.month-1, 1)
        else:
            start_time = self.check_invoice_date(start_time)

        if start_time == False or end_time == False:
            return {'code': -1, 'msg': '日期格式錯誤...'}
        if start_time.timestamp() - end_time.timestamp() > 0:
            return {'code': -1, 'msg': '結束時間早於起始時間...'}

        args_dict['invoiceDateS'] = start_time.strftime('%Y%m%d')
        args_dict['invoiceDateE'] = end_time.strftime('%Y%m%d')
        return self.handle_message(args_dict, url, special=True)

    def carrier_statistics_get(self, card_encrypt, card_no, start_time=None, end_time=None):
        info = self.carrier_statistics_query(card_encrypt, card_no, start_time, end_time)
        if int(info['code']) != 200:
            msg = '查詢失敗... ' + info['msg']
            return msg
        return info

    def blank_carrier_register(self, uuid=8899757):
        args_dict = self.args
        url = self.url_list['blank_carrier_register']
        args_dict['uuid'] = uuid
        return self.handle_message(args_dict, url, blank=True)

    def blank_carrier_link(self, card_type, card_encrypt, card_no, uuid=8899757):
        args_dict = self.args
        url = self.url_list['blank_carrier_link']
        args_dict['cardCode'] = card_type
        args_dict['verifyCode'] = card_encrypt
        args_dict['cardNo'] = card_no
        args_dict['uuid'] = uuid
        return self.handle_message(args_dict, url, blank=True)

    def blank_carrier_account(self, card_type, card_encrypt, card_no, uuid=8899757):
        args_dict = self.args
        url = self.url_list['blank_carrier_account']
        args_dict['cardCode'] = card_type
        args_dict['verifyCode'] = card_encrypt
        args_dict['cardNo'] = card_no
        args_dict['uuid'] = uuid
        return self.handle_message(args_dict, url, blank=True)

    def blank_carrier_donate(self, card_type, card_encrypt, card_no, love_code, inv_date, uuid=8899757):
        args_dict = self.args
        url = self.url_list['blank_carrier_donate']
        args_dict['cardCode'] = card_type
        args_dict['verifyCode'] = card_encrypt
        args_dict['cardNo'] = card_no
        args_dict['dntNo'] = love_code
        args_dict['qryYM'] = inv_date
        args_dict['uuid'] = uuid
        return self.handle_message(args_dict, url, blank=True)

