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

    if len(hour) < 2: hour = "0" + hour
    if len(minute) < 2: minute = "0" + minute

    return hour + ":" + minute + ampm

def date(t):
    """
    Takes a time.struct_time object as an argument.
    Returns a string in the format MM/DD/YYYY
    """
    month = str(t.tm_mon)
    day = str(t.tm_mday)
    year = str(t.tm_year)

    if len(month) < 2: month = "0" + month
    if len(day) < 2: day = "0" + day

    return month + "/" + day + "/" + year


#main
def main():
    tin = input("Press enter to clock in or enter a custom value with '$'...")
    clockInTime = localtime()

    if tin[:1] == "$":
        inTime = tin[1:]
    else:
        inTime = time(clockInTime)
    
    inDate = date(clockInTime)

    print("You're clocked in at " + inTime
            + " on " + inDate + ".")

    tout = input("Press enter to clock out or enter a custom value with '$'...")
    clockOutTime = localtime()

    if tout[:1] == "$":
        outTime = tout[1:]
    else:
        outTime = time(clockOutTime)
    
    outDate = date(clockOutTime)

    print("You're clocked out at " + outTime
            + " on " + outDate + ". Have a nice day!")

    input("Press enter to exit...") # Wait for the user to close the window

    # Write the line to the csv file.
    with open('timesheet.csv', 'a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([inDate, inTime, outTime])

if __name__ == '__main__':
    main()