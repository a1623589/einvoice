import configparser
from einvoice import Einvoice

conf = configparser.ConfigParser()
conf.read('config.ini')
APP_ID = conf.get('EINVOICE', 'APP_ID')
API_KEY = conf.get('EINVOICE', 'API_KEY')

url_list = dict(conf.items('EINVOICE_URL'))
version_list = dict(conf.items('EINVOICE_VERSION'))
action_list = dict(conf.items('EINVOICE_ACTION'))
card_type = dict(conf.items('EINVOICE_CARD_TYPE'))
card_info = dict(conf.items('CARD_INFO'))

e = Einvoice(APP_ID, API_KEY, url_list, version_list, action_list)

# (done) 查詢中獎發票號碼清單
#print(e.winning_list_get('10712'))
#print('======')
#print(e.winning_list_query('10712'))

# (done) 查詢發票表頭 
#print(e.invoice_header_get('MF-77991782', '2019/02/08'))
#print('======')
#print(e.invoice_header_query('MF77991782', '2019/02/08'))

# (done) 查詢發票明細
#print(e.invoice_detail_get('ML40953893', '2019/02/10', '0433', 'WGztteXieJ8lp/2MP1Cryg=='))
#print('======')
#print(e.invoice_detail_query('ML40953893', '2019/02/10', '0433', 'WGztteXieJ8lp/2MP1Cryg=='))

# (done) 查詢載具發票表頭
#print(e.carrier_header_get(card_type['mobile_barcode'], card_info['card_encrypt'], card_info['card_number'], '2019/1/30', '2019/2/11'))
#print('======')
#print(e.carrier_header_query(card_type['mobile_barcode'], card_info['card_encrypt'], card_info['card_number']))

# (done) 查詢載具發票明細
#print(e.carrier_detail_get(card_type['mobile_barcode'], 'LY67751449', '2019/02/08', card_info['card_encrypt'], card_info['card_number']))
#print('======')
#print(e.carrier_detail_query(card_type['mobile_barcode'], 'LY67751449', '2019/02/08', card_info['card_encrypt'], card_info['card_number']))

# (done) 手機條碼歸戶載具查詢
#print(e.carrier_aggregate_query(card_type['mobile_barcode'], card_info['card_encrypt'], card_info['card_number']))
#print('======')
#print(e.carrier_aggregate_get(card_type['mobile_barcode'], card_info['card_encrypt'], card_info['card_number']))

# (done) 捐贈碼查詢
#print(e.love_code_query('黨'))
#print('======')
#print(e.love_code_get('文教基金會'))

# (verifying) 載具發票捐贈
#print(e.carrier_donate_query(card_type['mobile_barcode'], card_info['card_encrypt'], card_info['card_number'], '2018/11/26', 'GW03356983', '2828'))
#print('======')
#print(e.carrier_donate_get(card_type['mobile_barcode'], card_info['card_encrypt'], card_info['card_number'], '2018/11/26', 'GW03356983', '2828'))

# (done) 已歸戶載具個別化主題 (??
#print(e.carrier_statistics_query(card_info['card_encrypt'], card_info['card_number'], '2018/10/01'))
#print('=====')
#print(e.carrier_statistics_get(card_info['card_encrypt'], card_info['card_number']))

# (done) 空白頁面API (??
#print(e.blank_carrier_register())
#print('=====')
#print(e.blank_carrier_link(card_type['mobile_barcode'], card_info['card_encrypt'], card_info['card_number']))
#print('=====')
#print(e.blank_carrier_account(card_type['mobile_barcode'], card_info['card_encrypt'], card_info['card_number']))
#print('=====')
#print(e.blank_carrier_donate(card_type['mobile_barcode'], card_info['card_encrypt'], card_info['card_number'], 2818, '201810'))
