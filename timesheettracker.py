"""
This little program will help me keep my timesheets in order! All I will have to
do is open the program when I clock on and off and press enter. The program will
automatically add the time and date to a csv which can be opened in excel for 
nice viewing.
"""

#imports
import csv
from time import localtime

#functions
def time(t):
    """
    Takes a time.struct_time object as an argument.
    Returns a string in the format HH:mm<a/p>m.
    """
    hour = str(t.tm_hour)
    minute = str(t.tm_min)
    ampm = "am"

    if t.tm_hour > 12:  #Convert from military to standard time
        hour = str(t.tm_hour-12)
        ampm = "pm"

    return hour + ":" + minute + ampm

def date(t):
    """
    Takes a time.struct_time object as an argument.
    Returns a string in the format MM/DD/YYYY
    """
    month = str(t.tm_mon)
    day = str(t.tm_mday)
    year = str(t.tm_year)
    return month + "/" + day + "/" + year


#main
def main():
    currentTime = localtime()
    print(time(currentTime))
    print(date(currentTime))

if __name__ == '__main__':
    main()