import Tkinter as tk
from Tkinter import Button
from tkFileDialog import askopenfilename
from Tkinter import Text
from Tkinter import END

from RestMe import Tester, TestCase
import json
from lib2to3.main import diff_texts
import json_tools

class Application(tk.Frame):
    def __init__(self, master=None):
        self.file_path = ""
        tk.Frame.__init__(self, master)
        self.grid()
        self.createWidgets()
        
        
    def createWidgets(self):
        self.browse_button = Button(self, text="Browse", command=self.askopenfile, width=10).pack()
#         self.browse_button.grid()
        
        self.diff_text_box = Text(self, height=10, width=300).pack()
#         self.diff_text_box.grid()
        
        self.actual_text_box = Text(self, height=50, width=100).pack()
#         self.actual_text_box.grid()
        
        
        self.expected_text_box = Text(self, height=50, width=100).pack()
#         self.expected_text_box.grid()
        
    def askopenfile(self):
        self.file_path = askopenfilename(filetypes=(("Test Cases", "*.json"), ("All Files", "*.*"))) 
        self.actual_text_box.insert(END, self.file_path)
        
        tester = Tester()
        test_case_json = tester.read_json(self.file_path)
        test_case = TestCase(test_case_json)
                
        actual_response = tester.send(test_case.request_url, test_case.request_method, {})
        out_put_text = tester.make_it_pretty(actual_response.json())
        
        self.actual_text_box.insert(END, out_put_text)
        self.actual_text_box.tag_add("actual", "1.0", str(len(out_put_text))+".0")
        self.actual_text_box.tag_config("actual", background="white", foreground="blue")
        
        expected_response = tester.make_it_pretty(test_case.response_content)
        self.expected_text_box.insert(END, expected_response)
        self.expected_text_box.tag_add("actual", "1.0", str(len(expected_response))+".0")
        self.expected_text_box.tag_config("actual", background="white", foreground="green")
        
        diff = json_tools.diff(expected_response, actual_response)
        
        
                
app = Application()
app.master.title("Rester")
app.master.minsize(600, 600)
app.mainloop()
