#!/usr/bin/python

print("Opening the file...")
target = open("script.txt", 'w')

target.truncate()

line1 = "Test passed"

target.write(line1)
print("Closing the file...")
target.close()
