#! /usr/bin/python

from random import choice

def form(list):
	output = """
	<form id='pickup' method='post' action='activity.py'>
		<select name='pickup'>
			"""
	for thing in list:
		output += "<option value='"+thing+"'>"+thing.capitalize()+"</option>\n"
	output += """
		</select>
		<input value='Pickup' type='submit'
	</form>
	"""
	return output

def main():
	print "Content-type:text/html\n\n"
	f2 = open("inventory.csv", "r")
	stuff = f2.read().strip().split(", ")
	f1 = open("index.html", "r")
	#picked_up = choice(stuff)
	print f1.read() % (form(stuff))

main()
