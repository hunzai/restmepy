import MySQLdb

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
 
def calculate_balance(cursor):
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
        
def get_monthy_transactions(cursor, year, month, day):
    cursor.execute("select * from transactions WHERE account_code=2102 AND account_number=10 AND DATE(created_at) <= '%s'-'%s'-'%s' ORDER BY balance LIMIT 1"%(year, month, day))
    balance_before = get_balance(cursor.fetchall()[0])
    
    cursor.execute("select * from transactions WHERE account_code=2102 AND account_number=10 AND DATE(created_at) > '%s'-'%s'-'%s' ORDER BY balance LIMIT 1"%(year, month, day))
    balance_after= get_balance(cursor.fetchall()[0])
    
    print(balance_before , balance_after)
    
connection =  get_connection("root", "thrift", "")
cursor = connection.cursor()
set_balance(cursor, 0)
calculate_balance(cursor)
connection.commit()

group_by_month = get_monthy_transactions(cursor, 2014, 7, 6)
print(group_by_month)
    

connection.close()