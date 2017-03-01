import csv

f1=open('super.csv', "r")
file1 = csv.reader(f1)
for row in file1:
    print row
