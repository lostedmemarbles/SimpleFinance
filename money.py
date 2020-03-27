#!/usr/bin/env python3

import datetime
import os
import sys

def errMess(errCode):
    switch = {
            1: "Nothing entered. Run with \"help\" for usage.",
            2: "Nothing to undo.",
            3: "No date specified.",
            4: "Range is too large. There are only " + str(len(lines)) + " lines."
        }
    print("ERROR: " + switch.get(errCode))
    sys.exit()

def printTo():
    fileIn.write(dayOf + "\t" + str(monies) + "\t")
    spots = 0
    for word in spentOn:
        fileIn.write(word + " ")
        spots += (len(word) + 1)
    while spots < 30:
        fileIn.write(" ")
        spots += 1
    fileIn.write("\t" + str('{:02.2f}'.format(left)) + "\n")
    fileIn.close()
    sys.exit()

def calLeft(ret):
    i = int(lastDay)
    while i < int(dayOf):
        ret += dailyAllow
        i += 1
    ret = ret - float(monies)
    return ret

if len(sys.argv) < 2:
    sysMess(1)

if "help" in sys.argv:
    print("Run with amount spent followed by the item(s) bought(optional).")
    print("Run with \"undo\" to delete the last line written.")
    print("Run with \"view\" followed by number of transactions to be viewed(optional) to view current month statement.\n\tPrevious months will be archived and are not accessible through program.")
    print("If override is necessary for date, run with \"-d\"\n\tfollowed by the day of the month.")
    print("Run with \"today\" to see balance as of today.")
    sys.exit()
date = datetime.datetime.now()
dayOf = " "
isNewMonth = False
isDiffDate = False
putInto = "./" + date.strftime("%b") + "daily.txt"
if not os.path.isfile(putInto):
    today = datetime.date.today()
    first = today.replace(day = 1)
    lastMonth = first - datetime.timedelta(days=1)
    lastMonName = "./" + lastMonth.strftime("%b") + "daily.txt"
    isNewMonth = True
    fileIn = open(putInto, 'a+')
    fileIn.write("Date\tPrice\tBought\t\t\t\tLeft\n")
    fileIn.close()
if "view" in sys.argv:
    fileIn = open(putInto, "r")
    lines = fileIn.readlines()
    ind = sys.argv.index("view")
    if (ind+1) < len(sys.argv):
        numLines = int(sys.argv[ind+1])
        if(numLines > len(lines)):
            errMess(4)
        while numLines != 0:
            line = lines[-numLines]
            line = line[:-1]
            print(line)
            numLines -= 1
    else:
        for line in lines:
            line = line[:-1]
            print(line)
    sys.exit()
if "undo" in sys.argv:
    fileIn = open(putInto, "r")
    lines = fileIn.readlines()
    fileIn.close()
    if lines[-1] == "Date\tPrice\tBought\t\t\t\tLeft\n":
        errMess(2)
    else:
        del lines[-1]
    fileIn = open(putInto, "w")
    for line in lines:
        fileIn.write(line)
    fileIn.close()
    sys.exit()
if "clean" in sys.argv:
    fileIn = open(putInto, 'w')
    fileIn.write("Date\tPrice\tBought\tLeft\n")
    fileIn.close()
    sys.exit()
if "-d" in sys.argv:
    isDiffDate = True
    i = 1
    while i < len(sys.argv):
        if sys.argv[i] == "-d":
            if i+1 >= len(sys.argv):
                errMess(3)
            dayOf = sys.argv[i+1]
            del sys.argv[i]
            del sys.argv[i]
        i += 1
monies = sys.argv[1]
docSpent = False
if len(sys.argv) >= 3:
    spentOn = sys.argv[2:]
else:
    spentOn = " "
    
dailyAllow = 12.00
left = 0.00
fileIn = open(putInto, 'r')
lines = fileIn.readlines()
previous = lines[-1]
words = previous.split()
lastDay = words[0]
if isNewMonth == True:
    oldFile = open(lastMonName, 'r')
    oldLines = oldFile.readlines()
    getFrom = oldLines[-1]
    lastLeft = getFrom[-1]
    oldFile.close()
if isNewMonth == False:
    lastLeft = words[-1]

fileIn.close()
fileIn = open(putInto, 'a')
if lastDay == date.strftime("%d") or lastDay == "Date":
    if "today" in sys.argv:
        monies = 0
        print("Your balance as of today is $" + lastLeft)
        sys.exit()
    if type(lastDay) != int and isDiffDate == False:
        dayOf = date.strftime("%d")
    if lastLeft == "Left":
        left = 13.00 - float(monies)
    else:
        left = float(lastLeft) - float(monies)
    printTo()

if lastDay < date.strftime("%d"):
    left = float(lastLeft)
    if type(lastDay) != int and isDiffDate == False:
        dayOf = date.strftime("%d")
    if "today" in sys.argv:
        monies = 0
        print("Your current balance is $" + str(calLeft(float(lastLeft))))
        sys.exit()
    left = calLeft(left)
    printTo()
fileIn.close()
