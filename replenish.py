#! /usr/bin/python

file = open("inventory.csv", "w")
stuff = ['apple', 'light sword', 'honey', 'friend', 'heavy sword', 'mystery potion']
file.write(", ".join(stuff))

print "Content-type: text/plain\n"
print

print ", ".join(stuff)
