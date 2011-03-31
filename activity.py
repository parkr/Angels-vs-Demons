#! /usr/bin/python

import cgi

def check_for_input():
	output = ""
	form = cgi.FieldStorage()
	if not form:
		picked_up = "nothing"
		what_i_have = "nothing"
	elif "pickup" in form and "what_i_have" in form:
		picked_up = str(form["pickup"].value)
		what_i_have = str(form["what_i_have"].value)
		if what_i_have.find("nothing") >= 0:
			what_i_have = picked_up
		else:
			what_i_have += (", "+picked_up)
	else:
		picked_up = "problem"
		what_i_have = "problem"
	return {'picked_up':picked_up, 'what_i_have': what_i_have}

from random import choice

def pickup_form(list, what_i_have):
	output = """
		<form id='%s' method='post' action='activity.py'>
			<select name='pickup'>
			""" % (id)
	for thing in list:
		output += "<option value='"+thing+"'>"+thing.capitalize()+"</option>\n\t\t\t\t"
	output += """
			</select>
			<input type='hidden' name='what_i_have' value='%s'>
			<input value='%s' type='submit'>
		</form>
	""" % (what_i_have, id.capitalize())
	return output

def drop_form_stuff(what_i_have):
	holding = what_i_have.split(", ")
	

def main():
	print "Content-type:text/html\n\n"
	f2 = open("inventory.csv", "r")
	stuff = f2.read().strip().split(", ")
	f1 = open("index.html.pyt", "r")
	results = check_for_input()
	pickup_form_stuff = pickup_form(stuff, results["what_i_have"])
	drop_form_stuff = drop_form(results["what_i_have"])
	print f1.read() % (pickup_form_stuff, drop_form_stuff, results["what_i_have"], results["picked_up"])

main()
