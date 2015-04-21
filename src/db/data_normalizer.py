import src.utils.thirft
from utils.thirft import get_accounts
from utils.thirft import get_connection
from src.utils.thirft import get_transaction_in_month

def add_missing_date():
    months = {'2014-7-6' , '2014-8-6', '2014-9-6', '2014-10-6', '2014-11-6', '2014-12-6'} 
    connection = get_connection("127.0.0.1", "root", "thrift", "")
    
    for month in months:
        transactions = get_transaction_in_month(connection, 2102, 10, month)
        print(transactions)