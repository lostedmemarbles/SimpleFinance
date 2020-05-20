#!/usr/bin/env python3

import sys

def errMess(errCode, lenNum):
    switch = {
            1: "Nothing entered. Run with \"help\" for usage.",
            2: "Nothing to undo.",
            3: "No date specified.",
            4: "Range is too large. There are only " + str(lenNum) + " lines.",
            "INVIN": "Invalid input. Run with \"help\" for usage.",
            "NOEN": "There are no transaction entries yet for this month.",
            "GT": "Specified dat must be older than today's date.",
            "LTZ": "Date cannot be less than 1."
        }
    print("ERROR: " + switch.get(errCode))
    sys.exit()

def globTest():
    testGlobal = 10

def canBeFloat(inp):
    try:
        float(inp)
        return True
    except ValueError:
        return False

def calLeft(ret, i,dayOf, dailyAllow, monies):
    while i < dayOf:
        ret += dailyAllow
        i += 1
    ret = ret - monies
    return ret

def helpFun():
    print("Run with amount spent followed by the item(s) bought(optional).")
    print("Run with \"undo\" to delete the last line written.")
    print("Run with \"view\" followed by number of transactions to be viewed(optional) to view current month statement.\n\tPrevious months will be archived and are not accessible through program.")
    print("If override is necessary for date, run with \"-d\"\n\tfollowed by the day of the month.")
    print("Run with \"today\" to see balance as of today.")
    print("Run with \"clean\" to wipe this month's file.")
    print("Run with \"search\" followed by the search value to list all transactions with that value.")
    print("Run with \"sum\" followed by a search value to list all transactions with that value and print the sum of money spent on them.")

    sys.exit()
