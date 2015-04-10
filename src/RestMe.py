import requests
import difflib
import  json
import pprint
from _io import open

class Request:
    GET = "get"
    POST = "post"
    PUT = "put"
    DELETE = "delete"
    
    def send(self, url, method, payLoad):
        response = ""
        if method == self.GET:
            response = requests.get(dealUrl)
        elif method == self.POST:
            response = requests.post(dealUrl, payLoad)
        elif method == self.PUT:
            response = requests.put(dealUrl, payLoad)
        elif method == self.DELETE:
            response = requests.delete(dealUrl)
        else:
            return ""
        return response
    
    def write(self, content, filename):
        with open(filename, 'wb') as outfile:
            json.dump(content, outfile)
            
    def read(self, filename):
        with open(filename) as inputfile:
            return json.load(inputfile)
    
    def getdifference(self, actual, expected):
        diff = difflib.ndiff(actual, expected)
        difference = ""
        for d in diff:
            if(d.startswith("+")):
                difference += d
        return difference
       
dealUrl = ""
payLoad = {}

request = Request()
response = request.send(dealUrl, "get", payLoad)
request.write(response.json(), "expected.json")

actual = request.read("expected.json")
expected = request.read("expected.json")

print(request.getdifference("amjad", "amjap"))


