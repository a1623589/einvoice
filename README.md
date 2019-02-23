E-Invoice Taiwan v1.7
===
`※ English version is translated by myself, something might be wrong.`

[Chinese verion](https://github.com/a1623589/einvoice/blob/master/README_CHINESE.md)

### [ Preperation ]
- Know what is [e-inovice](https://www.einvoice.nat.gov.tw/)
- Register [e-invoice API](https://www.einvoice.nat.gov.tw/APMEMBERVAN/APIService/Registration)
- Read [e-invoice API document](https://www.einvoice.nat.gov.tw/home/DownLoad?fileName=1510206773173_0.pdf)


### [ API Method ]
- Query winning list
- Query invoice header
- Query invoice detail
- Query love code
- Query carrier invoice header
- Query carrier invoice detail
- Donate carrier invoice
- Query carrier aggregate
- Query carrier personal statistics

API blank page
- Register carrier barcode
- Register carrier to cellphone barcode
- Register bank account to cellphone barcode
- Donate carrier invoice

### [ Simple module ]
- API_Method_query()
  - return raw_msg
- API_Method_get()
  - return simple_processed_msg
- Staticmethod
  - sign()
  - check_invoice_number()
  - check_invoice_date()
  - invoice_date_to_term()
  - format_number()
  - format_date()

### [ Bomb ]
- Same argument, different name
  - eg. UUID & uuid
  - eg. cardEncrypt & verifyCode
- Wrong error report 
  - so many error will be reported as 'wrong signatrue', but they are all defined in response code
- Same request, different response
  - sometimes success, but sometimes fail...

---

For more information, 
- [E-invoice platform](https://www.einvoice.nat.gov.tw/)

- [E-inovoice API specification](https://www.einvoice.nat.gov.tw/home/DownLoad?fileName=1510206773173_0.pdf)

- [E-invoice API user term](https://www.einvoice.nat.gov.tw/APMEMBERVAN/APIService/Registration!doc1)