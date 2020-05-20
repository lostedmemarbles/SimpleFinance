#!/usr/bin/env python3

import datetime
import os
import sys
import regFun
import shutil

def printTo():
    fileIn.write(str('{:02d}'.format(int(dayOf))) + "\t" + str(monies) + "\t")
    spots = 0
    for word in spentOn:
        fileIn.write(word + " ")
        spots += (len(word) + 1)
    while spots < 30:
        fileIn.write(" ")
        spots += 1
    fileIn.write("\t" + str('{:02.2f}'.format(left)) + "\n")
    if isDiffDate == True:
        for line2 in bottom:
            wordInLines = line2.split()
            oldDate = wordInLines[0]
            oldPrice = wordInLines[1]
            lastMoney = wordInLines.pop(-1)
            oldSpentOn = wordInLines[2:]
            newIn = float(lastMoney) - float(monies)
            fileIn.write(oldDate + "\t" + oldPrice + "\t")
            spots = 0
            for word in oldSpentOn:
                fileIn.write(word + " ")
                spots += (len(word) + 1)
            while spots < 30:
                fileIn.write(" ")
                spots += 1
            fileIn.write("\t" + str('{:02.2f}'.format(newIn)) + "\n")
    fileIn.close()
    sys.exit()

if len(sys.argv) < 2:
    regFun.sysMess(1, 0)
if "help" in sys.argv:
    regFun.helpFun()
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
if "backup" in sys.argv:
    backFile = putInto[:-4] + "Back" + putInto[-4:]
    shutil.copyfile(putInto, backFile)
    sys.exit()
if "view" in sys.argv:
    fileIn = open(putInto, "r")
    lines = fileIn.readlines()
    ind = sys.argv.index("view")
    if (ind+1) < len(sys.argv):
        numLines = int(sys.argv[ind+1])
        if(numLines > len(lines)):
            regFun.errMess(4, len(lines))
        while numLines != 0:
            line = lines[-numLines]
            line = line[:-1]
            print(line)
            numLines -= 1
    else:
        for line in lines:
            line = line[:-1]
            print(line)
    fileIn.close()
    sys.exit()
if "undo" in sys.argv:
    fileIn = open(putInto, "r")
    lines = fileIn.readlines()
    fileIn.close()
    if lines[-1] == "Date\tPrice\tBought\t\t\t\tLeft\n":
        regFun.errMess(2, len(lines))
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
                regFun.errMess(3, len(lines))
            dayOf = sys.argv[i+1]
            del sys.argv[i]
            del sys.argv[i]
        i += 1
    if int(dayOf) >= int(date.strftime("%d")):
        regFun.errMess("GT", 0)
    if int(dayOf) < 1:
        regFun.errMess("LTZ", 0)

if "search" in sys.argv:
    searchVal = ""
    del sys.argv[0]
    sys.argv.remove('search')
    if len(sys.argv) > 1 or len(sys.argv) < 1:
        regFun.errMess("INVIN", 0)
    for word in sys.argv:
        searchVal += word
    fileIn = open(putInto, 'r')
    lines = fileIn.readlines()
    printThese = []
    for line in lines:
        if searchVal in line:
            line = line[:-1]
            printThese.append(line)
    if len(printThese) == 0:
        print("Text not found.")
    else:
        for each in printThese:
            print(each)
    fileIn.close()
    sys.exit()

if "sum" in sys.argv:
    searchVal = ""
    del sys.argv[0]
    sys.argv.remove('sum')
    if len(sys.argv) > 1 or len(sys.argv) < 1:
        regFun.errMess("INVIN", 0)
    for word in sys.argv:
        searchVal += word
    fileIn = open(putInto, 'r')
    lines = fileIn.readlines()
    sumThese = []
    sumValues = 0.00
    for line in lines:
        if searchVal in line:
            line = line[:-1]
            lineSplit = line.split()
            sumValues += float(lineSplit[1])
            sumThese.append(line)
    if len(sumThese) == 0:
        print("Text not found.")
    else:
        for each in sumThese:
            print(each)
        if sumValues < 0:
            print("You've made $" + str(abs(sumValues)) + " from " + searchVal + ".")
        else:
            print("You've spent $" + str(sumValues) + " on " + searchVal + ".")
    fileIn.close()
    sys.exit()
valid = regFun.canBeFloat(sys.argv[1])
if valid == False and "today" not in sys.argv:
    regFun.errMess("INVIN",0)
if len(sys.argv) < 3 and "today" not in sys.argv:
    regFun.errMess("INVIN",0)

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
lastLeft = words[-1]

fileIn.close()
if isDiffDate == True:
    fileIn = open(putInto, 'w')
    i = 1
    if lastLeft == "Left":
        left = dailyAllow - float(monies)
        bottom = ""
        printTo()
    else:
        left = float(lastLeft) - float(monies)
    while int(lastDay) > int(dayOf):
        splLines = lines[-i].split()
        lastDay = splLines[0]
        i += 1
    i -= 2
    spl = len(lines) - i
    top = lines[0:spl]
    bottom = lines[spl:]
    for line1 in top:
        fileIn.write(line1)
    lastTop = top[-1].split()
    lastLeft = lastTop[-1]
    if lastLeft == "Left":
        left = dailyAllow - float(monies)
    else:
        left = regFun.calLeft(float(lastLeft), int(lastDay), int(dayOf), float(dailyAllow), float(monies))
    printTo()

fileIn = open(putInto, 'a')
if lastDay == date.strftime("%d") or lastDay == "Date":
    if "today" in sys.argv:
        monies = 0
        if lastLeft == "Left":
            regFun.errMess("NOEN", 0)
        print("Your balance as of today is $" + str('{:02.2f}'.format(float(lastLeft))))
        sys.exit()
    if type(lastDay) != int and isDiffDate == False:
        dayOf = date.strftime("%d")
    if lastLeft == "Left":
        left = dailyAllow - float(monies)
    else:
        left = float(lastLeft) - float(monies)
    printTo()

if lastDay < date.strftime("%d"):
    left = float(lastLeft)
    if type(lastDay) != int and isDiffDate == False:
        dayOf = date.strftime("%d")
    if "today" in sys.argv:
        if lastLeft == "Left":
            regFun.errMess("NOEN", 0)
        monies = 0
        print("Your current balance is $" + str('{:02.2f}'.format(regFun.calLeft(float(lastLeft), int(lastDay), int(dayOf), int(dailyAllow), float(monies)))))
        sys.exit()
    left = regFun.calLeft(left, int(lastDay), int(dayOf), int(dailyAllow), float(monies))
    printTo()
fileIn.close()
