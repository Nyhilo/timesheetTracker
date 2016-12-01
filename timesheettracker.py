"""
This little program will help me keep my timesheets in order! All I will have to
do is open the program when I clock on and off and press enter. The program will
automatically add the time and date to a csv which can be opened in excel for 
nice viewing.
"""

#imports
import csv
from time import localtime

#classes
class Config:
    def __init__(self, FileName, WriteSetting):
        self.filename = FileName
        self.writesetting = WriteSetting
        self.loadLastConfig()

    def __str__(self):
        return str(self.isRunning)+" "+self.lastInTime+" "+str(self.lastInDate)

    def update(self, IsRunning, LastInTime, LastInDate):
        self.isRunning = IsRunning
        self.lastInTime = LastInTime
        self.lastInDate = LastInDate

    def isSameDay(self, compareDate):
        if self.lastInDate == compareDate:
            return True
        else: return False

    def wasInterrupted(self):
        return self.isRunning

    def writeConfig(self):
        """
        We're utilizing the csv module for this to avoid an unnedded additional
        imort. The file in question will have 3 lines with the isRunning,
        lastInTime, and lastInDate values respectively.
        """
        # Not sure if we can write a boolean to a file so let's just convert it
        # to a string first
        if self.isRunning:
            isRunningStr = "1"
        else:
            isRunningStr = "0"

        # Then we write the information
        with open(self.filename, self.writesetting, newline='') as file:
            writer = csv.writer(file)
            writer.writerows([
                [isRunningStr],[self.lastInTime],[self.lastInDate]
                ])

    def loadLastConfig(self):
        import os.path
        if not os.path.exists(self.filename):
            self.isRunning = False
            self.lastInTime = ""
            self.lastInDate = ""
        else:
            configList = []
            with open(self.filename, newline='') as file:
                reader = csv.reader(file, delimiter=' ', quotechar='|')
                for row in reader:
                    configList.append(row)
            # Now we set the config variables to the output of the file
            if configList[0][0] == '1':
                self.isRunning = True
            else:
                self.isRunning = False

            self.lastInTime = configList[1][0]
            self.lastInDate = configList[2][0]

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
    """
    Writes a row containing a Date and two Time values to the specified file.
    """
    with open(filename, writesetting, newline='') as file:
        writer = csv.writer(file)
        writer.writerow([inDate, inTime, outTime])


# main

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

"""
def main(): #For testing
    config = Config('config.txt', 'w')
    config.update(True, 'someTime', 'someDate')
    config.writeConfig()
    config.loadLastConfig()
    print(config)
"""

if __name__ == '__main__':
    main()
