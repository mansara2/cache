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
import jinja2
import os
import re
from google.appengine.ext import db
import string


template_dir = os.path.join(os.path.dirname(__file__), 'simplemathhtml')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir),
                               autoescape = True)

def valid_answerm(mathA):
	if mathA == "4":
		return True
	else:
		return False
def valid_answerswag(swagA):
	if swagA == "hellaswag":
		return True
	else:
		return False
							   
def render_str(template, **params):
    t = jinja_env.get_template(template)
    return t.render(params)

class BaseHandler(webapp2.RequestHandler):
    def render(self, template, **kw):
        self.response.out.write(render_str(template, **kw))

    def write(self, *a, **kw):
		self.response.out.write(*a, **kw)
class MainHandler(BaseHandler):
	def get(self):
		self.render('simplemathmain.html')	
		
	def post(self):
		swagQ = self.request.get('swagQ')
		plustwoQ = self.request.get('plustwoQ')
		
		params = dict( plustwoQ = plustwoQ,swagQ = swagQ)
		if valid_answerm(plustwoQ) == True:
			params['correct_math'] = "Good Job you passed the first grade"
		elif valid_answerm(plustwoQ) == False:
			params['error_math'] = "Really? HAHAHAHA....try again "
		if valid_answerswag(swagQ) == True:
			params['correct_swag'] = "You got hella swag. *Hands you Communications Degree"
		elif valid_answerswag(swagQ) == False:
			params['error_swag'] = "Hey we can't all be cool I guess"
		self.render('simplemathmain.html',**params)	

		

		

	
app = webapp2.WSGIApplication([
    ('/', MainHandler)
], debug=True)
