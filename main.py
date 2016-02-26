#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import webapp2
import datetime
from google.appengine.api import memcache
from google.appengine.ext import webapp
from google.appengine.ext import ndb


MAIN_PAGE_HTML = """\
       <html>
                <style>
                    form {background: #b3ffff;
                        width: 300px;
                        border: 1px solid blue;
                        box-sizing: border-box;}
                    body {background-color: #e6ffff;}
                    h1   {color:  #6666ff;}
                    p    {color: #6666ff;}
                </style>
         <body> <center> 
         <p>Welcome to the Number Box!</p>
           <form action="/yep" method="post">
              <p></ p>
              <div>
                 <p></p>
                 <p></p>
                    <input name="number1" rows="3" cols="20" placeholder = "   NUMBER 1"/>
                    <p></p>
                    <input name="number2" rows="3" cols="20" placeholder = "   NUMBER 2"/>
                    <p></p> 
                    <select name ="operation">
                          <option value="add">Add</option>
                          <option value="subtract">Subtract</option>
                          <option value="divide">Divide</option>
                          <option value="multiply">Multiply</option>
                     </select>   
                      <input type="submit" value = "Perform Operation!"/>
                </div>
              <p></ p>
            </form>"""

        
class MainHandler(webapp2.RequestHandler):
    def get(self):
        self.response.write(MAIN_PAGE_HTML)  
        self.response.write("</center></body></html>")
        
    def retVal(self,  op): 
        if op == "subtract":
            return "-"
        if op == "divide":
            return "/"
        if op == "multiply":
            return "*"
        return "+"
        
    def ansVal(self, op, n1, n2):
        if op == "subtract":
            return (n1-n2)
        if op == "divide":
            return (n1/n2)
        if op == "multiply":
            return (n1*n2)
        return (n1+n2)
    
    
    
    def post(self):
        self.response.write(MAIN_PAGE_HTML)
        num1 = self.request.get("number1")
        num2 = self.request.get("number2")
        operation = self.retVal(self.request.get("operation"))
        
        if( num1.isdigit() and num2.isdigit() ):
            answer = str(self.ansVal(self.request.get("operation"), int(num1), int(num2)))
            expires_date = datetime.datetime.utcnow() + datetime.timedelta(365)
            expires_str = expires_date.strftime("%d %b %Y %H:%M:%S GMT")       
            memSave = str(expires_str+ "&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;"+ num1+"&nbsp" +operation+ "&nbsp"+ num2 +"&nbsp=" + answer)
                        
            for x in range(10):
                if(memcache.get(str(x)) == None):
                      memcache.add(key=str(x), value=memSave, time=3600)     
                      self.response.write("<p>"+memcache.get(str(x))+"</p>")
                      if x == 9 :  
                        memcache.flush_all()
                        self.response.write("<p>MEMCACHE FLUSHED</p>")
                      break
                self.response.write("<p>"+memcache.get(str(x))+"</p>")
                               
        self.response.write("</center></body></html>")
        


app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/yep',  MainHandler)
], debug=True)