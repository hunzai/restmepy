import requests
import json
from _io import open
import json_tools
import dpath.util
from urllib3.util import current_time

__ORIGINAL_JSON_NAME__ = "original"
__INTELLIGENCE_JSON_NAME__ = "intelligence"

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
        return json.dumps(json_content, indent=4, separators=(',', ': '))
    
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
    
    def write(self, filename, content):
        with open(filename, 'w') as outfile:
            outfile.write(content)
            
    def read(self, filename):
        with open(filename) as inputfile:
            return inputfile.read()
        
    def write_json(self, filename, content):
        with open(filename, 'wb') as outfile:
            json.dump(content, outfile, indent=4, separators=(',', ': '))
    
    def read_json(self, filename):
        with open(filename) as inputfile:
            return json.load(inputfile, encoding='utf-16')
    
    def are_same(self, actual, expected):
        diff = json_tools.diff(expected, actual)
        
        if len(diff) > 0:
            out_put_diff_name = "result/diff" + "_" + test_case.name.replace(" ", "_") + ".json"
            tester.write_json(out_put_diff_name, diff)
            raise Exception("differs from previous(expected) , %r" % json.dumps(diff))
        return diff
    
    def get_primitive_types_paths(self, json_object):
        primitive_type_keys = list()
        for p in dpath.util.search(json_object, "**", yielded=True):
            the_type = type(p[1])
            if(the_type is not dict and the_type is not list):
                primitive_type_keys.append(p[0])

        return primitive_type_keys
    
    def add_intelligence(self, original_json, where):
        value = dpath.util.get(original_json, where)
        node = {}
        node[__ORIGINAL_JSON_NAME__] = value
        
        intelligence = {}
        intelligence["dynamic"] = "false"
        intelligence["change_count"] = 0
        intelligence["last_changed"] = current_time()
        node[__INTELLIGENCE_JSON_NAME__] = intelligence
        
        dpath.util.new(original_json, where, node)
        return json
    
    def get_actual_path_from_intelligent_json_path(self, intelligence_json_path):
        return (intelligence_json_path.split("content")[1]).replace("/"+__ORIGINAL_JSON_NAME__, "")       
     
        
tester = Tester()
test_case_json = tester.read_json("testcase/verify_deal_title.json")
payLoad = {}

test_case = TestCase(test_case_json)

"""add intelligence to testcase content values - this should only happen once! """ 
# for path in tester.get_primitive_types_paths(test_case.response_content):
#     tester.add_intelligence(test_case.response_content, path)

""" compare intelligent test case json content values to original content (from testcase) """
intelligent_test_case_json = tester.read_json("intelligence.json")
intelligence_json_paths = tester.get_primitive_types_paths(intelligent_test_case_json)
actual_content  = tester.send(test_case.request_url, test_case.request_method, {}).json()

for intelligent_json_path in intelligence_json_paths:
    if(__ORIGINAL_JSON_NAME__ in intelligent_json_path):
        expected_value =  dpath.util.get(intelligent_test_case_json, intelligent_json_path)
        actual_path = tester.get_actual_path_from_intelligent_json_path(intelligent_json_path)
        actual_value = dpath.util.get(actual_content, actual_path)
        is_same = expected_value == actual_value
        if(is_same is False):
            print(expected_value, actual_value)
            intelligence_path = intelligent_json_path.replace(__ORIGINAL_JSON_NAME__, __INTELLIGENCE_JSON_NAME__) 
            dynamic_path = intelligence_path + "/dynamic"
            change_count_path = intelligence_path + "/change_count"
            last_change_path  = intelligence_path + "/last_changed"
            
            change_count = dpath.util.get(intelligent_test_case_json, change_count_path)
            
            dpath.util.set(intelligent_test_case_json, dynamic_path, "true")
            dpath.util.set(intelligent_test_case_json, change_count_path, change_count+1)
            dpath.util.set(intelligent_test_case_json, last_change_path, current_time())
            
          
tester.write_json("intelligence_2.json", intelligent_test_case_json)






