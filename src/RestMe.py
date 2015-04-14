import requests
import json
from _io import open
import json_tools

class TestCase:
    def __init__(self, test_json):
        self.test_data = test_json
        self.name = self.test_data["name"]
        self.request_url = self.test_data["request"]["url"] 
        self.request_method = self.test_data["request"]["method"]
        self.response_content = self.test_data["response"]["content"]
        
        
class Tester:
    GET = "get"
    POST = "post"
    PUT = "put"
    DELETE = "delete"
    
    def make_it_pretty(self, json_content):
        return json.dumps(json_content,  indent=4, separators=(',', ': '))
    
    def send(self, url, method, payLoad):
        response = ""
        if not url:
            raise Exception("url is empty")
        elif method == self.GET:
            response = requests.get(url)
        elif method == self.POST:
            response = requests.post(url, payLoad)
        elif method == self.PUT:
            response = requests.put(url, payLoad)
        elif method == self.DELETE:
            response = requests.delete(url)
        else:
            return ""
        return response
    
    def write(self, content, filename):
        with open(filename, 'w') as outfile:
            outfile.write(content)
            
    def read(self, filename):
        with open(filename) as inputfile:
            return inputfile.read()
        
    def write_json(self, filename, content):
        with open(filename, 'wb') as outfile:
            json.dump(content, outfile)
    
    def read_json(self, filename):
        with open(filename) as inputfile:
            return json.load(inputfile)
    
    def are_same(self, actual, expected):
        diff = json_tools.diff(expected, actual)
        
        if len(diff) > 0:
            out_put_diff_name = "result/diff" + "_" + test_case.name.replace(" ", "_") + ".json"
            tester.write_json(out_put_diff_name, diff)
            #raise Exception("differs from previous(expected) , %r" % diff)
        return diff
        
       
tester = Tester()
test_case_json = tester.read_json("testcase/verify_deal_title.json")
payLoad = {}

test_case = TestCase(test_case_json)
response = tester.send(test_case.request_url, test_case.request_method, payLoad)

actual = response.json()
expected = test_case.response_content

tester.are_same(actual, expected)






