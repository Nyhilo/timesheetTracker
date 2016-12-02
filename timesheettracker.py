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
    def __init__(self, FileName, WriteSetting='w'):
        self.filename = FileName
        self.writesetting = WriteSetting
        self.loadLastConfig()

    def __str__(self):
        return str(self.isRunning)+" "+self.lastInTime+" "+str(self.lastInDate)

    def update(self, IsRunning, LastInTime, LastInDate):
        self.isRunning = IsRunning
        self.lastInTime = LastInTime
        self.lastInDate = LastInDate

    def isDifferentDay(self, compareDate):
        if self.lastInDate != compareDate:
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

def standardUseDialog(writefilename, writesetting, config):
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

    # Set the config
    config.update(True, inTime, inDate)
    config.writeConfig()
    
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

    # Write the date, inTime and outTimes to the file. Set the config
    writefile(writefilename, writesetting, inDate, inTime, outTime)
    config.isRunning = False
    config.writeConfig()

    # Wait for the user to close the window
    input("Press enter to exit...")

def missedADayDialog(writefilename, writesetting, config):
    print("It seems you closed the program before you clocked out on "
        + config.lastInDate + ".")

    # Get some input from the user regarding if they want to fix the error
    cont = input(
            "Would you like to fix the clockout time of that day? [Y/N] "
            ).lower().strip()

    while not (cont == "y" or cont == "n"):
        cont = input(
            "Would you like to fix the clockout time of that day? [Y/N] "
            ).lower().strip()

    # If they don't want to fix the error, send them to the normal dialog
    if cont == "n":
        standardUseDialog(writefilename, writesetting, config)
    else:   # Otherwise they get a different dialog
        correctedOutTime = input(
            "Please enter the time you would've clocked out: "
            )

        # Write the correction to the file using the logged in time and date
        # found in the config file.
        writefile(writefilename, writesetting,
            config.lastInDate, config.lastInTime, correctedOutTime)

        # Write the config
        config.isRunning = False
        config.writeConfig()

        print("Your clock out time, " + correctedOutTime + " on "
            + config.lastInDate + " has been logged.")

        # Start the standard dialog.
        # The user can quit out before givng input here without issue
        standardUseDialog(writefilename, writesetting, config)

def wasInterruptedDialog(writefilename, writesetting, config):
    # Date to compare to the logged date in the config
    currentDate = date(localtime())

    # If the program closed just today, then the dialog is slightly different
    if config.isDifferentDay(currentDate):
        missedADayDialog(writefilename, writesetting, config)
    else:
        print("It seems you closed the program before you clocked out today.")
        print("You clocked in at " + config.lastInTime + ".")

        # Get some input from the user regarding if they want to fix the error
        cont = input(
            "Would you like to continue where you left off? [Y/N] "
            ).lower().strip()

        while not (cont == "y" or cont == "n"):
            cont = input(
                "Would you like to continue where you left off? [Y/N] "
                ).lower().strip()

        # If they don't want to fix the error, send them to the normal dialog
        if cont == "n":
            standardUseDialog(writefilename, writesetting, config)
        else:   # Otherwise they get a different dialog
            inTime = config.lastInTime
            inDate = config.lastInDate

            # Let the user initiate the clock out time.
            tout = input("Press enter to clock out "
                + "or enter a custom value with '$'...")
            clockOutTime = localtime()

            # Custom values can be entered for outTime by inputting $<some value>
            if tout[:1] == "$":
                outTime = tout[1:]
            else:
                outTime = time(clockOutTime)

            outDate = date(clockOutTime)

            print("You're clocked out at " + outTime
                    + " on " + outDate + ". Have a nice day!")

            # Write the date, inTime and outTimes to the file. Set the config
            writefile(writefilename, writesetting, inDate, inTime, outTime)
            config.isRunning = False
            config.writeConfig()

            # Wait for the user to close the window
            input("Press enter to exit...")


# main
def main():
    # Initiate the config object. This also loads in the last configuration
    config = Config('config')

    # If the program was closed before clocking off last time it was opened
    if config.wasInterrupted():
        wasInterruptedDialog('timesheet.csv', 'a', config)
    else:
        standardUseDialog('timesheet.csv', 'a', config)

if __name__ == '__main__':
    main()
