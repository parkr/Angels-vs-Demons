#! /usr/bin/python

print "Content-type: text/html\n\n"
import cgitb; cgitb.enable()

class Page:
	
	def __init__(self):
		self.template_page = "index.html.pyt"
		self.inventory_file = "inventory.csv"
		self.picked_up = "nothing"
		self.what_i_have = "nothing"
		self.dropped = "nothing"
		self.loyalty = "none"
		self.points = 0
		self.results = {}
		self.room_complete = 0
		
	def check_for_input(self):
		import cgi
		f2 = open(self.inventory_file, "r")
		stuff = f2.read().strip().split(", ")
		f2.close()
		output = ""
		form = cgi.FieldStorage()
		if not form:
			self.picked_up = "nothing"
			self.what_i_have = "nothing"
			self.dropped = "nothing"
			self.loyalty = "none"
			self.points = 0
			self.roomcomplete = 0
		elif form['action'].value == "pickup":
			self.picked_up = str(form["pickup"].value)
			self.what_i_have = str(form["what_i_have"].value)
			if self.what_i_have.find("nothing") >= 0:
				self.what_i_have = self.picked_up
			else:
				self.what_i_have += (", "+self.picked_up)
			self.dropped = "nothing"
			stuff.remove(self.picked_up)
		elif form['action'].value == "drop":
			self.dropped = str(form["drop"].value)
			self.what_i_have = str(form["what_i_have"].value)
			if self.what_i_have.find("nothing") >= 0:
				self.what_i_have = "nothing"
			else:
				if self.what_i_have.find(dropped) < self.what_i_have.rfind(", "):
					# the element must be deleted along with the comma and space
					self.what_i_have = self.what_i_have.replace(self.dropped+", ", "")
				elif self.what_i_have.find(",") == -1:
					#the element is the only element!
					self.what_i_have = self.what_i_have.replace(self.dropped, "")
				else:
					#the element is last in the list
					self.what_i_have = self.what_i_have.replace(", "+self.dropped, "")
			self.picked_up = "nothing"
			stuff.append(self.dropped)
		elif form['action'].value == "move":
			self.what_i_have = ""
			if form.has_key('inventory1') and form['inventory1'].value != "":
				self.what_i_have += str(form['inventory1'].value)
			if form.has_key('inventory2') and form['inventory2'].value != "":
				self.what_i_have += str(form['inventory2'].value)
			if form.has_key('inventory3') and form['inventory3'].value != "":
				self.what_i_have += str(form['inventory3'].value)
			if form.has_key('inventory4') and form['inventory4'].value != "":
				self.what_i_have += str(form['inventory4'].value)
			if form.has_key('inventory5') and form['inventory5'].value != "":
				self.what_i_have += str(form['inventory5'].value)
			if self.what_i_have == "":
				self.what_i_have = "nothing"
			self.dropped = "nothing"
			self.picked_up = "nothing"
		else:
			self.picked_up = "problem"
			self.droppped = "problem"
			self.what_i_have = "problem"
		#All pages have points. Get them.
		if form.has_key('points') and form['points'].value != "":
			self.points = int(form['points'].value)
		if form.has_key('loyalty') and form['loyalty'].value != "":
			self.loyalty = str(form['loyalty'].value)
		else:
			self.loyalty = "none"
		if self.what_i_have == "" or self.what_i_have == " ":
			self.what_i_have = "nothing"
		# write changes to file
		f2 = open(self.inventory_file, "w")
		f2.write(", ".join(stuff))
		f2.close()
	 	return {'picked_up': self.picked_up, 'what_i_have': self.what_i_have, 'dropped': self.dropped, 'points': self.points, 'loyalty': self.loyalty}

	def pickup_form(self):
		if self.loyalty == "none" or self.loyalty == "":
			output = """
			<form id='pickup' method='post' action='activity.py'>
				<select name='pickup'>
				"""
			for thing in self.stuff:
				output += "<option value='"+thing+"'>"+thing.title()+"</option>\n\t\t\t\t"
			output += """
				</select>
				<input type='hidden' name='what_i_have' value='%s'>
				<input type='hidden' name='action' value='pickup'>
				<input type='hidden' name='points' value='%d'>
				<input type='hidden' name='loyalty' value='%s'>
				<input type='hidden' name='roomcomplete' value='%d'>
				<input value='Pickup' type='submit'>
			</form>
		""" % (self.what_i_have, self.points, self.loyalty, self.room_complete)
		else:
			output = ""
		return output

	def drop_form(self):
		if self.loyalty == "none" or self.loyalty == "":
			holding = self.what_i_have.split(", ")
			output = """
			<form id='drop' method='post' action='activity.py'>
				<select name='drop'>
				"""
			for thing in holding:
				output += "<option value='"+thing+"'>"+thing.title()+"</option>\n\t\t\t\t"
			output += """
				</select>
				<input type='hidden' name='what_i_have' value='%s'>
				<input type='hidden' name='action' value='drop'>
				<input type='hidden' name='points' value='%d'>
				<input type='hidden' name='loyalty' value='%s'>
				<input type='hidden' name='roomcomplete' value='%d'>
				<input value='Drop' type='submit'>
			</form>
		""" % (self.what_i_have, self.points, self.loyalty, self.room_complete)
		else:
			output = ""
		return output
	
	def go_form(self, text, fid, link):
		holding = self.what_i_have.split(", ")
		output = "<form id='%s' method='post' action='%s'>" % (fid, link)
		for index in range(5):
			if index >= len(holding):
				output += "\n\t\t\t<input type='hidden' name = 'inventory%d' value=''>" % (index+1)
			else:	
				thing = holding[index]
				if thing == "nothing":
					thing = ""
				output += "\n\t\t\t<input type='hidden' name = 'inventory%d' value='%s'>" % (index+1, thing)
		if self.loyalty == "none":
			loyalty = ""
		else:
			loyalty = self.loyalty
		output += """
				<input type='hidden' name='points' value='%d'>
				<input type='hidden' name='loyalty' value='%s'>
				<input type='hidden' name='roomcomplete' value='%d'>
			</form>
		""" % (self.points, loyalty)
		return {'output': output, 'link': "<a href='#' onclick='submitForm(\"%s\")'>%s</a>" % (fid, text, self.room_complete)}
	
	def generate_page(self):
		try:
			f1 = open(self.template_page, "r")
			self.results = self.check_for_input()
			f2 = open(self.inventory_file, "r")
			self.stuff = f2.read().strip().split(", ")
			pickup_form_stuff = self.pickup_form()
			drop_form_stuff = self.drop_form()
			go_left_stuff = self.go_form('&larr;Go Left', 'left', 'http://cs.mcgill.ca/~pcrane/teamPage/cgi-bin/show.py')
			go_right_stuff = self.go_form('Go Right&rarr;', 'right', 'http://cs.mcgill.ca/~jmahen/cgi-bin/show.py')
			if self.loyalty == "none" or self.loyalty = "":
				self.loyalty = "none. Move left to choose a side."
			print f1.read() % (pickup_form_stuff, drop_form_stuff, self.what_i_have, self.picked_up, self.dropped, self.loyalty, self.points, go_left_stuff['link'], go_right_stuff['link'], go_left_stuff['output'], go_right_stuff['output'])
		except Exception, e:
			import traceback, sys
			print
			print '<html><head><title>'
			print str(e)
			print '</title>'
			print '</head><body>'
			print '<h1>TRACEBACK</h1>'
			print '<pre>'
			print str(e)
			traceback.print_exc()
			traceback.print_stack()
			print "Unexpected error:", sys.exc_info()[0]
			print '</pre>'
			print '</body></html>'

p = Page()
p.generate_page()