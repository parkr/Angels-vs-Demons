#! /usr/bin/python

import cgi

def check_for_input():
	output = ""
	form = cgi.FieldStorage()
	if not form:
		output = "<!-- nothing submitted -->"
	elif "pickup" in form:
		picked_up = str(form["pickup"].value)
		output = picked_up
	elif "what_i_have" in form:
		what_i_have = str(form["what_i_have"].value)
		output = what_i_have
	return output

from random import choice

def form(id, list):
	output = """
	<form id='%s' method='post' action='activity.py'>
		<select name='pickup'>
			""" % (id)
	for thing in list:
		output += "<option value='"+thing+"'>"+thing.capitalize()+"</option>\n\t\t\t"
	output += """
		</select>
		<input value='%s' type='submit'>
	</form>
	""" % (id.capitalize())
	return output

def main():
	print "Content-type:text/html\n\n"
	f2 = open("inventory.csv", "r")
	stuff = f2.read().strip().split(", ")
	f1 = open("index.html", "r")
	#picked_up = choice(stuff)
	print f1.read() % (form("pickup", stuff), check_for_input())

main()
