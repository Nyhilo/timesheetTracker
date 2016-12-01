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
    #Convert from military to standard time
    if t.tm_hour > 12:
        hour = str(t.tm_hour-12)
        ampm = "pm"
    else:
        hour = str(t.tm_hour)
        ampm = "am"
    minute = str(t.tm_min)

    # Add some leading 0s to single digit values
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

    # Add some leading 0s to single digit values
    if len(month) < 2: month = "0" + month
    if len(day) < 2: day = "0" + day

    return month + "/" + day + "/" + year

def writefile(filename, writesetting, inDate, inTime, outTime):
    # Write the line to the csv file.
    with open('timesheet.csv', 'a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([inDate, inTime, outTime])


#main
def main():
    # Let the user initiate the clock in time.
    tin = input("Press enter to clock in or enter a custom value with '$'...")
    clockInTime = localtime()

    # Change the clock in time to the value the user entered if they typed
    # something like $<some value>. Ignore if anything but a $ is entered.
    if tin[:1] == "$":
        inTime = tin[1:]
    else:
        inTime = time(clockInTime)
    
    inDate = date(clockInTime)

    print("You're clocked in at " + inTime
            + " on " + inDate + ".")

    # Let the user initiate the clock out time.
    tout = input("Press enter to clock out or enter a custom value with '$'...")
    clockOutTime = localtime()

    # Custom values can be entered for outTime by inputting $<some value>
    if tout[:1] == "$":
        outTime = tout[1:]
    else:
        outTime = time(clockOutTime)
    
    outDate = date(clockOutTime)

    print("You're clocked out at " + outTime
            + " on " + outDate + ". Have a nice day!")

    # Wait for the user to close the window
    input("Press enter to exit...")

    # Write the date, inTime and outTimes to the file.
    writefile('timesheet.csv', 'a', inDate, inTime, outTime)
    # writefile('timesheet-test.csv', 'a', inDate, inTime, outTime)

if __name__ == '__main__':
    main()