import MySQLdb
import datetime
import calendar


def get_connection(user_name, db_name, password):
    return MySQLdb.connect(host='127.0.0.1', unix_socket='/tmp/mysql.sock', user=user_name, passwd=password, db=db_name)

def get_id(transaction):
    return transaction[0]
    
def get_debit(transaction):
    return transaction[8]

def get_credit(transaction):
    return transaction[9]   

def get_balance(transaction):
    return transaction[12] 

def update_balance(cursor, balance, transaction_id):
    cursor.execute("UPDATE transactions SET balance = '%s' WHERE id = '%s'"% (balance, transaction_id))

def set_balance(cursor, value):
    cursor.execute("UPDATE transactions SET balance = '%s'"%value)
 
def calculate_balance(connection):
    cursor = connection.cursor()
    set_balance(cursor, 0)
    cursor.execute("select * from transactions where account_code=2102 AND account_number=10 ORDER BY DATE(created_at)")
    counter = 0
    last_balance = 0
    for transaction in cursor:
        credit = get_credit(transaction)
        debit = get_debit(transaction)
        
        if counter < 1 :
            last_balance = credit-debit
            update_balance(cursor, last_balance, get_id(transaction))
        else:
            balance = (credit-debit) + last_balance
            update_balance(cursor, balance, get_id(transaction))
            last_balance= balance
        counter +=1
    connection.commit()
        
def get_monthly_product(connection, month):
    month = datetime.datetime.strptime(month, "%Y-%m-%d")
    begining_of_month  = datetime.datetime(month.year,month.month, 1)
    end_of_month = datetime.datetime(month.year, month.month, calendar.monthrange(month.year,month.month)[1])
    cursor = connection.cursor()

    begining_of_month = begining_of_month.strftime('%Y-%m-%d')
    end_of_month = end_of_month.strftime('%Y-%m-%d')
    
    print(begining_of_month, end_of_month)
    
    cursor.execute("select * from transactions WHERE account_code=2102 AND account_number=10 AND created_at >= '%s' AND created_at <= '%s'  ORDER BY balance LIMIT 1"%(begining_of_month, month))
    before = cursor.fetchall()
    
    print(cursor.rowcount)
    
    cursor.execute("select * from transactions WHERE account_code=2102 AND account_number=10 AND created_at  > '%s' AND created_at <= '%s'  ORDER BY balance LIMIT 1"%(month, end_of_month))
    after = cursor.fetchall()[0]

    if get_balance(after) < get_balance(before):
        return after
    else:
        return before
    
connection =  get_connection("root", "thrift", "")
calculate_balance(connection)

months = {'2014-7-6' , '2014-8-6', '2014-9-6', '2014-10-6', '2014-11-6', '2014-12-6'} 

for month in months:   
    product = get_monthly_product(connection, month)
    print(get_balance(product))
    
connection.close()