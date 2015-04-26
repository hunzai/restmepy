
class Transaction:
    
    def __init__(self, transaction):
        self.id = transaction[0]
        self.account_number = transaction[1]
        self.m_number = transaction[2]
        self.registration_number = transaction[3]
        self.page_number = transaction[4]
        self.entry_date = transaction[5]
        self.narration = transaction[6]
        self.voucher_number = transaction[7]
        self.debit = transaction[8]
        self.credit = transaction[9]
        self.profit = transaction[10]
        self.account_code = transaction[11]
        self.balance = transaction[12]
        self.branch = transaction[13]
        self.account_id = transaction[14]
        self.since_last = transaction[15]
        self.employee_id = transaction[16]
        self.particulars = transaction[17]
        self.transaction_type = transaction[18]
        self.auto_voucher_number = transaction[19]
        self.check_book_series = transaction[20]
        self.voucher_path = transaction[21]
        self.created_at = transaction[22]
        self.updated_at = transaction[23]


 

