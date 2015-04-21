import calendar
import csv
import datetime
from src.utils.thirft import get_connection, get_accounts, to_datetime,\
    get_begining_of_month, get_end_of_month
    
def get_id(transaction):
    return transaction[0]
    
def get_debit(transaction):
    return transaction[8]

def get_account_number(transaction):
    return transaction[1]

def get_credit(transaction):
    return transaction[9]   

def get_balance(transaction):
    return transaction[12] 

def update_balance(cursor, balance, transaction_id):
    cursor.execute("UPDATE transactions SET balance = '%s' WHERE id = '%s'" % (balance, transaction_id))

def get_created_at(trasaction):
    return trasaction[22]

def set_balance(cursor, value):
    cursor.execute("UPDATE transactions SET balance = '%s'" % value)
 
    
def calculate_balance(connection, account_code, account_number):
    cursor = connection.cursor()
    set_balance(cursor, 0)
    cursor.execute("select * from transactions where account_code='%s' AND account_number='%s' ORDER BY DATE(created_at)" %(account_code,account_number))
    counter = 0
    last_balance = 0
    for transaction in cursor:
        credit = get_credit(transaction)
        debit = get_debit(transaction)
        
        if counter < 1 :
            last_balance = credit - debit
            update_balance(cursor, last_balance, get_id(transaction))
        else:
            balance = (credit - debit) + last_balance
            update_balance(cursor, balance, get_id(transaction))
            last_balance = balance
        counter += 1
    connection.commit()
      
def dummy_transaction_row():
    return (None, None, '', '', '', None, '', '', 0.0, 0.0, 0.0, 0.0, 0.0, '0', None, 0.0, None, None, None, None, None, None, None, None)
 
     
def get_monthly_product(connection, account_code, account_number, month):
    month = to_datetime(month)
    begining_of_month = get_begining_of_month(month)
    end_of_month = get_end_of_month(month)
    cursor = connection.cursor()

    begining_of_month = begining_of_month.strftime('%Y-%m-%d')
    end_of_month = end_of_month.strftime('%Y-%m-%d')
    
    before = None
    after = None
    cursor.execute("select * from transactions WHERE account_code='%s' AND account_number='%s' AND created_at >= '%s' AND created_at <= '%s'  ORDER BY balance LIMIT 1" % (account_code, account_number, begining_of_month, month))
    if cursor.rowcount == 1:
        before = cursor.fetchall()[0]
    cursor.execute("select * from transactions WHERE account_code='%s' AND account_number='%s' AND created_at  > '%s' AND created_at <= '%s'  ORDER BY balance LIMIT 1" % (account_code, account_number, month, end_of_month))
    if cursor.rowcount == 1:
        after = cursor.fetchall()[0]
 
    if((before is not None) and (after is not None)):
        if get_balance(after) < get_balance(before):
            return after
        else:
            return before
    elif(before is not None):
        return before
    elif((after is None) and (before is not None)):
        return dummy_transaction_row()
    else:
        return dummy_transaction_row()
    
def get_products_for_months(connection, account_code, account_number, months):
    product_list = list()
    for month in months:   
        product = get_monthly_product(connection, account_code, account_number, month)
        product_list.append(product)
    return product_list

def write_csv(filename, records_dict, row_header):
    csv_file = open(filename, 'w')
    wr = csv.writer(csv_file, delimiter=';', quoting=csv.QUOTE_ALL)
    wr.writerow(row_header)
    for account_number, records in records_dict.iteritems():
        wr.writerow((account_number, "", ""))
        product_amount = 0
        for row in records:
            product_amount += get_balance(row)
            wr.writerow(row)
        wr.writerow(("total", product_amount))
        

"''' program starts here '''"
connection = get_connection("127.0.0.1", "root", "thrift", "")                           
months = {'2014-7-6' , '2014-8-6', '2014-9-6', '2014-10-6', '2014-11-6', '2014-12-6'} 
profits = dict()
for row in get_accounts(connection, 2102):
    account_number = row[0]
    account_code = row[1]
    calculate_balance(connection,account_code, account_number)
    connection.commit()
    print(account_code, account_number)
    products = get_products_for_months(connection, account_code, account_number, months)
    profits[account_number] = products

transaction_header = ("id", "account_number", "m_number", "registration_number", "page_number", "entry_date", "narration", "voucher_number",  
                      "debit", "credit", "profit", "account_code", "balance", "branch", "account_id", "since_last", "employee_id", "particulars",  
                      "transaction_type", "auto_voucher_number", "check_book_series", "voucher_path", "created_at", "updated_at")
                  
write_csv("pls_products.csv", profits, transaction_header)    
connection.close()
