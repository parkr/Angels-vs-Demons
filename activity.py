#! /usr/bin/python

import cgi

def cookie_stuff():
	expiration = datetime.datetime.now() + datetime.timedelta(days=30)
	cookie = Cookie.SimpleCookie()
	cookie["session"] = random.randint(1000000000)
	cookie["session"]["domain"] = ".jayconrod.com"
	cookie["session"]["path"] = "/"
	cookie["session"]["expires"] = \
	  expiration.strftime("%a, %d-%b-%Y %H:%M:%S PST")

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
	else:
		picked_up = "problem"
		droppped = "problem"
		what_i_have = "problem"
	if what_i_have == "" or what_i_have == " ":
		what_i_have = "nothing"
	# write changes to file
	f2 = open("inventory.csv", "w")
	f2.write(", ".join(stuff))
	f2.close()
	return {'picked_up':picked_up, 'what_i_have': what_i_have, 'dropped': dropped}

from random import choice

def pickup_form(on_ground, what_i_have):
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
			<input value='Pickup' type='submit'>
		</form>
	""" % (what_i_have)
	return output

def drop_form(what_i_have):
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
			<input value='Drop' type='submit'>
		</form>
	""" % (what_i_have)
	return output

def main():
	try:
		cookie_stuff()
		print "Content-type:text/html\n\n"
		f1 = open("index.html.pyt", "r")
		results = check_for_input()
		f2 = open("inventory.csv", "r")
		stuff = f2.read().strip().split(", ")
		pickup_form_stuff = pickup_form(stuff, results["what_i_have"])
		drop_form_stuff = drop_form(results["what_i_have"])
		print f1.read() % (pickup_form_stuff, drop_form_stuff, results["what_i_have"], results["picked_up"], results["dropped"])
	except Exception, e:
		import traceback
		print 'Content-type: text/html\n'
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
		print '</pre>'
		print '</body></html>'

main()
