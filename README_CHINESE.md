台灣電子發票 1.7版
===
[Englisg version](https://github.com/a1623589/einvoice)

### [ 事前準備 ]
- 知道甚麼是[電子發票](https://www.einvoice.nat.gov.tw/)
- 申請 [電子發票API](https://www.einvoice.nat.gov.tw/APMEMBERVAN/APIService/Registration)
- 讀 [官方電子發票API文件](https://www.einvoice.nat.gov.tw/home/DownLoad?fileName=1510206773173_0.pdf)

### [ API 方法 ]
- 查詢中獎發票號碼清單
- 查詢發票表頭
- 查詢發票明細
- 捐贈碼查詢
- 載具發票表頭查詢
- 載具發票明細查詢
- 載具發票捐贈
- 手機條碼歸戶載具查詢
- 已歸戶載具個別化主題

API 空白頁面
- 手機條碼載具註冊
- 載具歸戶(手機條碼) 
- 手機條碼綁定金融帳戶
- 載具發票捐贈 

### [ 簡單的模組 ]
- API_Method_query()
  - return 原始訊息
- API_Method_get()
  - return 經過簡單處理的訊息
- 靜態方法 (Staticmethod)
  - sign()
  - check_invoice_number()
  - check_invoice_date()
  - invoice_date_to_term()
  - format_number()
  - format_date()

---

更多資訊請參考, 
- [財政部電子發票平台](https://www.einvoice.nat.gov.tw/)

- [電子發票API格式](https://www.einvoice.nat.gov.tw/home/DownLoad?fileName=1510206773173_0.pdf)

- [電子發票API使用規範](https://www.einvoice.nat.gov.tw/APMEMBERVAN/APIService/Registration!doc1)