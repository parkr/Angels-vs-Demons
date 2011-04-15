#! /usr/bin/python

print "Content-type: text/html\n\n"

import cgi
import cgitb; cgitb.enable()

def check_for_input():
	f2 = open("inventory.csv", "r")
	stuff = f2.read().strip().split(", ")
	f2.close()
	output = ""
	form = cgi.FieldStorage()
	if not form:
		picked_up = "nothing"
		what_i_have = "nothing"
		dropped = "nothing"
		loyalty = "none"
		points = 0
	elif form['action'].value == "pickup":
		picked_up = str(form["pickup"].value)
		what_i_have = str(form["what_i_have"].value)
		if what_i_have.find("nothing") >= 0:
			what_i_have = picked_up
		else:
			what_i_have += (", "+picked_up)
		dropped = "nothing"
		stuff.remove(picked_up)
	elif form['action'].value == "drop":
		dropped = str(form["drop"].value)
		what_i_have = str(form["what_i_have"].value)
		if what_i_have.find("nothing") >= 0:
			what_i_have = "nothing"
		else:
			if what_i_have.find(dropped) < what_i_have.rfind(", "):
				# the element must be deleted along with the comma and space
				what_i_have = what_i_have.replace(dropped+", ", "")
			elif what_i_have.find(",") == -1:
				#the element is the only element!
				what_i_have = what_i_have.replace(dropped, "")
			else:
				#the element is last in the list
				what_i_have = what_i_have.replace(", "+dropped, "")
		picked_up = "nothing"
		stuff.append(dropped)
	elif form['action'].value == "move":
		what_i_have = ""
		if form.has_key('inventory1') and form['inventory1'].value != "":
			what_i_have += str(form['inventory1'].value)
		if form.has_key('inventory2') and form['inventory2'].value != "":
			what_i_have += str(form['inventory2'].value)
		if form.has_key('inventory3') and form['inventory3'].value != "":
			what_i_have += str(form['inventory3'].value)
		if form.has_key('inventory4') and form['inventory4'].value != "":
			what_i_have += str(form['inventory4'].value)
		if form.has_key('inventory5') and form['inventory5'].value != "":
			what_i_have += str(form['inventory5'].value)
		if what_i_have == "":
			what_i_have = "nothing"
		dropped = "nothing"
		picked_up = "nothing"
	else:
		picked_up = "problem"
		droppped = "problem"
		what_i_have = "problem"
	#All pages have points. Get them.
	points = 0
	if form.has_key('points') and form['points'].value != "":
		points = int(form['points'].value)
	if form.has_key('loyalty') and form['loyalty'].value != "":
		loyalty = str(form['loyalty'].value)
	else:
		loyalty = "none"
	if what_i_have == "" or what_i_have == " ":
		what_i_have = "nothing"
	# write changes to file
	f2 = open("inventory.csv", "w")
	f2.write(", ".join(stuff))
	f2.close()
	return {'picked_up':picked_up, 'what_i_have': what_i_have, 'dropped': dropped, 'points':points, 'loyalty': loyalty}

from random import choice

def pickup_form(on_ground, what_i_have, points, loyalty):
	output = """
		<form id='pickup' method='post' action='activity.py'>
			<select name='pickup'>
			"""
	for thing in on_ground:
		output += "<option value='"+thing+"'>"+thing.title()+"</option>\n\t\t\t\t"
	output += """
			</select>
			<input type='hidden' name='what_i_have' value='%s'>
			<input type='hidden' name='action' value='pickup'>
			<input type='hidden' name='points' value='%d'>
			<input type='hidden' name='loyalty' value='%s'>
			<input value='Pickup' type='submit'>
		</form>
	""" % (what_i_have, points, loyalty)
	return output

def drop_form(what_i_have, points, loyalty):
	holding = what_i_have.split(", ")
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
			<input value='Drop' type='submit'>
		</form>
	""" % (what_i_have, points, loyalty)
	return output
	
def go_form(text, link, what_i_have, points, loyalty):
	holding = what_i_have.split(", ")
	
	output = "<form id='go' method='post' action='%s'>" % (link)
	for index in range(5):
		if index >= len(holding):
			output += "\n\t\t\t<input type='hidden' name = 'inventory%d' value=''>" % (index+1)
		else:	
			thing = holding[index]
			if thing == "nothing":
				thing = ""
			output += "\n\t\t\t<input type='hidden' name = 'inventory%d' value='%s'>" % (index+1, thing)
	if loyalty == "none":
		loyalty = ""
	output += """
			<input type='hidden' name='points' value='%d'>
			<input type='hidden' name='loyalty' value='%s'>
			<input type='submit' value='%s'>
		</form>
	""" % (points, loyalty, text)
	return output

def main():
	try:
		f1 = open("index.html.pyt", "r")
		results = check_for_input()
		f2 = open("inventory.csv", "r")
		stuff = f2.read().strip().split(", ")
		pickup_form_stuff = pickup_form(stuff, results["what_i_have"], results["points"], results["loyalty"])
		drop_form_stuff = drop_form(results["what_i_have"], results["points"], results["loyalty"])
		go_left_stuff = go_form('&larr;Go Left', 'http://cs.mcgill.ca/~pcrane/teamPage/cgi-bin/show.py', results["what_i_have"], results["points"], results["loyalty"])
		go_right_stuff = go_form('Go Right&rarr;', 'http://cs.mcgill.ca/~jmahen/cgi-bin/show.py', results["what_i_have"], results["points"], results["loyalty"])
		print f1.read() % (pickup_form_stuff, drop_form_stuff, results["what_i_have"], results["picked_up"], results["dropped"], results["loyalty"], results["points"], go_left_stuff, go_right_stuff)
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

main()
