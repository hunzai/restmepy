from utils.thirft import get_connection, to_datetime, get_begining_of_month
from utils.thirft import get_transaction_in_month
from db.pls_accounts import get_products_for_months
from datetime import timedelta

months = {'2014-7-6' , '2014-8-6', '2014-9-6', '2014-10-6', '2014-11-6', '2014-12-6'} 
connection = get_connection("127.0.0.1", "root", "thrift", "Birdzlove1981")
account_number = 1
account_code = 2102

def get_last_month(this_month):
    last_month = get_begining_of_month(this_month) - timedelta(days=5)
    return last_month
    
def add_missing_date():
    for month in months:
        this_month =  to_datetime(month)
        transactions = get_transaction_in_month(connection, 2102, 1,this_month)
        if len(transactions) == 0:
            last_month = get_last_month(this_month)
            transactions_last_month = get_transaction_in_month(connection, account_code, account_number, last_month)
            


products = get_products_for_months(connection, 2102, 1, months)
add_missing_date()
