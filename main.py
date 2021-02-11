from appJar import gui
import time
import os


class RemainingTime:
    def __init__(self):
        self.hours = 0
        self.mins = 30
        self.secs = 0

    def getHours(self):
        return int(self.hours)

    def getMins(self):
        return int(self.mins)

    def getSecs(self):
        return int(self.secs)

    def setHours(self, hours):
        self.hours = hours

    def setMins(self, mins):
        self.mins = mins

    def setSecs(self, secs):
        self.secs = secs

    def addHours(self, hours):
        self.hours += hours

    def addMins(self, mins):
        if self.mins + mins >= 60:
            self.addHours(int(mins / 60))
            mins -= int(mins / 60) * 60
        self.mins += mins

    def addSecs(self, secs):
        if self.secs + secs >= 60:
            self.addMins(int(secs / 60))
            secs -= int(secs / 60) * 60
        self.secs += secs

    def resetTime(self):
        self.hours = 0
        self.mins = 0
        self.secs = 0

    def checkTimerOveflow(self):
        if self.mins >= 60:
            self.addHours(int(self.mins / 60))
            self.mins -= int(self.mins / 60) * 60

        elif self.mins < 0 and self.hours > 0:
            self.hours -= 1
            self.mins = 59

        if self.secs >= 60:
            self.addMins(int(self.secs / 60))
            self.secs -= int(self.secs / 60) * 60

        elif self.secs < 0 and self.mins >= 0:
            self.mins -= 1
            self.secs = 59

    def prettyString(self):
        hours = int(self.hours)
        if hours / 10 < 1:
            hours = f"0{int(self.hours)}"

        mins = int(self.mins)
        if mins / 10 < 1:
            mins = f"0{int(self.mins)}"

        secs = int(self.secs)
        if secs / 10 < 1:
            secs = f"0{int(self.secs)}"

        return f"{hours}:{mins}:{secs}"

    def calculateSeconds(self):
        secs = self.hours * 3600
        secs += self.mins * 60
        secs += self.secs
        return secs

    def substract(self):
        global finish
        if self.calculateSeconds() == 1:
            self.secs -= 1
            finish = True
            action()
        else:
            self.secs -= 1
            self.checkTimerOveflow()


remainingTime = RemainingTime()
finish = True


def action():
    actionToDo = app.getRadioButton("action")
    if actionToDo == "Power off":
        os.system("shutdown -s")
    elif actionToDo == "Restart":
        os.system("shutdown -r")
    elif actionToDo == "Sleep":
        os.system("shutdown -h")
    elif actionToDo == "Logout":
        os.system("shutdown -l")
    elif actionToDo == "Custom command":
        os.system(app.getEntry("command"))


def updateTimeLabel():
    remainingTime.checkTimerOveflow()
    app.label("Time", remainingTime.prettyString())


def timer():
    global finish
    while not finish:
        if remainingTime.calculateSeconds() > 0:
            remainingTime.substract()
            app.queueFunction(updateTimeLabel)
            if remainingTime.calculateSeconds() != 0:
                time.sleep(1)
        else:
            finish = True
            app.queueFunction(app.setButtonState, "Start timer", "active")
            app.queueFunction(app.setButtonState, "Stop timer", "disabled")
            app.queueFunction(updateTimeLabel)
            action()


def startTimer():
    global finish
    app.setButtonState("Start timer", "disabled")
    app.setButtonState("Stop timer", "active")
    finish = False
    app.thread(timer)


def extendTimer():
    hours = app.getEntry("Hours")
    mins = app.getEntry("Minutes")
    secs = app.getEntry("Seconds")

    if hours:
        remainingTime.addHours(hours)

    if mins:
        remainingTime.addMins(mins)

    if secs:
        remainingTime.addSecs(secs)

    updateTimeLabel()


def stopTimer():
    global finish
    app.setButtonState("Start timer", "active")
    app.setButtonState("Stop timer", "disabled")
    app.queueFunction(updateTimeLabel)
    finish = True


def resetTimer():
    remainingTime.resetTime()
    stopTimer()
    updateTimeLabel()


def updateActionLabel():
    app.setLabel("showaction", app.getRadioButton("action"))
    if app.getRadioButton("action") == "Custom command":
        app.setEntryState("command", "normal")
    else:
        app.setEntryState("command", "disabled")


app = gui("Shutdown Timer")
app.setSize("420x220")
app.setFont(13)
app.setResizable(False)

app.startTabbedFrame("mainframe")
app.setTabbedFrameChangeCommand("mainframe", updateActionLabel)

app.startTab("Timer")
app.addLabel("selectedaction", "Action after timer:", row=0, column=2, colspan=2, rowspan=1)
app.addLabel("showaction", row=1, column=2, colspan=2, rowspan=1)
app.addLabel("Time", remainingTime.prettyString(), colspan=2, column=0, row=0, rowspan=2)
app.getLabelWidget("Time").config(font=("Sans Serif", "30", "bold"))
app.setLabelRelief("Time", "groove")

app.addLabelNumericEntry("Hours", row=2, colspan=4)
app.addLabelNumericEntry("Minutes", row=3, colspan=4)
app.addLabelNumericEntry("Seconds", row=4, colspan=4)

app.addButton("Start timer", startTimer, row=5, column=0)
app.addButton("Extend time", extendTimer, row=5, column=1)
app.addButton("Stop timer", stopTimer, row=5, column=2)
app.setButtonState("Stop timer", "disabled")
app.addButton("Reset timer", resetTimer, row=5, column=3)
app.stopTab()

app.startTab("Settings")
app.startLabelFrame("Action to do:")
app.addRadioButton("action", "Power off")
app.addRadioButton("action", "Restart")
app.addRadioButton("action", "Sleep")
app.addRadioButton("action", "Logout")
app.addRadioButton("action", "Custom command", column=0, row=5)
app.setRadioButtonChangeFunction("action", updateActionLabel)
app.addEntry("command", column=1, row=5)
app.stopLabelFrame()
app.stopTab()

app.stopTabbedFrame()

app.setLabel("showaction", app.getRadioButton("action"))

app.go()
