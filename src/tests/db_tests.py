from utils.thirft import get_transaction_in_month, get_connection
import unittest

class TestUtils(unittest.TestCase):
    
    def test_has_transactions(self):
        print("running")
        connection = get_connection("127.0.0.1","root", "thrift", "")
       
        self.assertEqual(len(get_transaction_in_month(connection, 2102, 1, "2014-07-2")), 1) 
        self.assertFalse(len(get_transaction_in_month(connection, 2102, 1, "2014-08-2")), 0) 
        

if __name__ == '__main__':
    unittest.main()
