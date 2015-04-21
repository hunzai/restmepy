import MySQLdb
import datetime
import calendar

def create_transaction(connection, transaction_data):
    transaction = (
                  "INSERT INTO transactions " + 
                  "(" + 
                  "account_number, m_number, registration_number, page_number, entry_date, narration, voucher_number," + 
                  "debit, credit, profit, account_code, balance, branch, account_id, since_last, employee_id, particulars," + 
                  "transaction_type, auto_voucher_number, check_book_series, voucher_path, created_at, updated_at" + 
                  ")" + 
              
                  "VALUES"
                  "( " + 
                  " %(account_number)s, %(m_number)s, %(registration_number)s, %(page_number)s, %(entry_date)s,  %(narration)s,  %(voucher_number)s ," + 
                  " %(debit)s,  %(credit)s,  %(profit)s,  %(account_code)s,  %(balance)s,  %(branch)s , %(account_id)s,  %(since_last)s,  %(employee_id)s,  %(particulars)s ," + 
                  " %(transaction_type)s,  %(auto_voucher_number)s,  %(check_book_series)s,  %(voucher_path)s,  %(created_at)s,  %(updated_at)s" + 
                  ")"
                  )
    return connection.cursor().execute(transaction, transaction_data)

def log(message):
    print("########### " + message + " #################")
    
def get_connection(url, user_name, db_name, password):
    return MySQLdb.connect(host= url, unix_socket='/tmp/mysql.sock', user=user_name, passwd=password, db=db_name)

def get_accounts(connection, account_code):
    cursor = connection.cursor()
    cursor.execute("SELECT DISTINCT(account_number),account_code, branch from transactions WHERE account_code='%s'  ORDER BY account_number LIMIT "%account_code)
    return cursor.fetchall()

def to_datetime(date_str):
    return datetime.datetime.strptime(date_str, "%Y-%m-%d")

def get_transaction_in_month(connection, account_code, account_number, month):
    date_and_time = to_datetime(month)

    cursor = connection.cursor()
    cursor.execute("SELECT * from transactions WHERE account_code = '%s' AND account_number='%s' AND created_at >='%s' AND created_at <= '%s'"
                   %(account_code, account_number, get_begining_of_month(date_and_time), get_end_of_month(date_and_time)))
    return cursor.fetchall()

def get_last_transaction(connection, account_code, account_number, this_month):
    cursor = connection.cursor()
    cursor.execute("SELECT * from transactions WHERE created_at < '%s'"%(this_month, this_month))
        
def get_begining_of_month(date):
    return datetime.datetime(date.year, date.month, 1)
    
def get_end_of_month(date):
    return datetime.datetime(date.year, date.month, calendar.monthrange(date.year, date.month)[1])