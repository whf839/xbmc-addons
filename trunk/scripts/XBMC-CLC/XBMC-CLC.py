import __builtin__, os, string, sys, thread, time, traceback, xbmc, xbmcgui
import StringIO
import typewriter
try: Emulating = xbmcgui.Emulating
except: Emulating = False

RootDir = os.getcwd().replace( ";", "" )

NUM_LINES = 25

g = globals()
l = locals()

class MyClass(xbmcgui.Window):
    def __init__(self):
        if Emulating: xbmcgui.Window.__init__(self)
        self.setCoordinateResolution(4)

        # Initialize class variables
        self.typewriter = typewriter.Typewriter()
        self.commandListIndex = 0
        self.commandList = []
        self.promptPos = 0
        self.cursorPos = 0
        self.overwrite = False
        self.multiline = False
        
        # Redirect stdout to print to our client
        self.text = NewOut()
        sys.stdout = self.text
        sys.displayhook = self.text.display

        self.g = globals()
        self.l = locals()

        # Set up the GUI
        self.pic = xbmcgui.ControlImage(0,0,0,0, os.path.join(RootDir, "background.png"))   # (0,0,0,0) Makes it draw the image full size, starting at the top left
        self.addControl(self.pic)
        self.textBox = xbmcgui.ControlTextBox(9,36,686,436)
        self.addControl(self.textBox)

        # Then activate the command prompt
        self.getInput()
        thread.start_new_thread(self.startBlinker, ())
        #self.startBlinker()

    def onAction(self, action):
        BUTTON_CTRL_Z = 61602
        BUTTON_CTRL_D = 61603
        
        BUTTON_ESCAPE = 61467
        BUTTON_BACKSPACE = 61448
        BUTTON_ENTER = 61453
        
        BUTTON_END = 61475
        BUTTON_HOME = 61476
        BUTTON_LEFT = 61477
        BUTTON_UP = 61478
        BUTTON_RIGHT = 61479
        BUTTON_DOWN = 61480
        #BUTTON_CTRL_LEFT = 61477
        #BUTTON_CTRL_RIGHT = 61479
        BUTTON_INSERT = 61485
        BUTTON_DELETE = 61486

        bc = action.getButtonCode()
        allText = self.text.getvalue()
        if bc == BUTTON_CTRL_Z or bc == BUTTON_CTRL_D:
            self.close()
        elif bc == BUTTON_ESCAPE:
            if self.multiline:
                text = allText[:-len(allText.split("\n...")[-1])]
            else:
                text = allText[:self.promptPos]
            self.text.reset()
            self.text.write(text)
        elif bc == BUTTON_BACKSPACE:
            if self.multiline:
                bumper = (len(allText)-self.promptPos)-len(allText.split("\n...")[-1])
            else:
                bumper = 0
            if self.cursorPos > bumper:
                text = allText

                if self.promptPos + self.cursorPos == len(self.text):
                    text = text[:-1]
                else:
                    text = text[:self.promptPos + self.cursorPos - 1] + text[self.promptPos + self.cursorPos:]
                self.text.reset()
                self.text.write(text)
                self.cursorPos -= 1

        elif bc == BUTTON_END:
            if self.promptPos + self.cursorPos < len(self.text):
                self.cursorPos = len(self.text) - self.promptPos
        elif bc == BUTTON_HOME:
            if self.cursorPos > 0:
                self.cursorPos = 0
        elif bc == BUTTON_LEFT:
            if self.cursorPos > 0:
                self.cursorPos -= 1
        elif bc == BUTTON_UP:
            text = allText[:self.promptPos]
            self.text.reset()
            self.text.write(text)
            if self.commandListIndex < len(self.commandList):
                self.commandListIndex += 1
            if self.commandListIndex > 0:
                self.text.write(self.commandList[-self.commandListIndex])
                self.cursorPos = len(self.commandList[-self.commandListIndex])
        elif bc == BUTTON_RIGHT:
            if self.promptPos + self.cursorPos < len(self.text):
                self.cursorPos += 1
        elif bc == BUTTON_DOWN:
            if self.commandList:
                text = allText[:self.promptPos]
                self.text.reset()
                self.text.write(text)
                if self.commandListIndex > 1:
                    self.commandListIndex -= 1
                self.text.write(self.commandList[-self.commandListIndex])
                self.cursorPos = len(self.commandList[-self.commandListIndex])
        elif bc == BUTTON_INSERT:
            self.overwrite = not self.overwrite
            
        elif bc == BUTTON_ENTER:
            self.text.write("\n")
            self.getCommandLine()
        else:
            new = self.typewriter.getChar(bc)
            if self.promptPos + self.cursorPos == len(self.text):
                self.text.write(new)
            else:
                text = allText
                if self.overwrite:
                    text = text[:self.promptPos + self.cursorPos] + new + text[self.promptPos + self.cursorPos + 1:]
                else:
                    text = text[:self.promptPos + self.cursorPos] + new + text[self.promptPos + self.cursorPos:]
                self.text.reset()
                self.text.write(text)
            self.cursorPos += len(new)

    def screenSize(self):
        #for i in range(30):
        #    line = str(i + 1)
        #    if i == 0: line += " " + str(self.getHeight())
        #    self.chatOut(line)
        print self.chatOut("W" * 76)

    def getInput(self):
        if self.multiline:
            self.chatOut("...", True)
            self.cursorPos = len(self.text.getvalue()[self.promptPos:])
        else:
            self.chatOut(">>>", True)
            self.promptPos = len(self.text)
            self.cursorPos = 0
        self.idle = True

    def startBlinker(self):
        self.dying = False
        self.cursorOn = False
        while True:
            self.blink()
            if self.dying: break
            time.sleep(0.3)
            if self.dying: break
            
    def blink(self):
        if self.idle:
            text = self.text.getvalue()
            self.cursorOn = not self.cursorOn
            if self.cursorOn:
                if self.overwrite:
                    text = text[:self.promptPos + self.cursorPos] + "[]" + text[self.promptPos + self.cursorPos + 1:]
                else:
                    text = text[:self.promptPos + self.cursorPos] + "_" + text[self.promptPos + self.cursorPos:]
            else:
                if not self.overwrite:
                    text = text[:self.promptPos + self.cursorPos] + " " + text[self.promptPos + self.cursorPos:]
            self.textBox.setText(text)

    def chatOut(self, text, suppressNewline = False):
        self.text.write(text)
        if not suppressNewline:
            self.text.write("\n")
        #self.textBox.setText(self.text.getvalue())

    def close(self):
        self.dying = True
        time.sleep(1)
        xbmcgui.Window.close(self)

    def getCommandLine(self):
        self.idle = False
        command = self.text.getvalue()[self.promptPos:].strip()
        if command and not command.endswith("\n..."):
            if command.find("\n") > -1:
                saveCommand = command.split("\n")[-1][3:]
            else:
                saveCommand = command
            if not saveCommand in self.commandList:
                self.commandList.append(saveCommand)
                self.commandListIndex = 0
        if command.endswith(":") or (self.multiline and not command.endswith("\n...")):
            self.multiline = True
        else:
            if self.multiline:
                command = command.replace("\n...", "\n")
            try:
                exec(command, self.g, self.l)
            except Exception:
                self.printError(sys.exc_info())
            self.multiline = False
        self.getInput()

    def printError(self, exception):
        name = exception[0].__name__
        if exception[1].__dict__.has_key("args"):
            name += ": " + str(exception[1].__dict__["args"][0])#string.join(exception[1].__dict__["args"])
        self.chatOut(name)
        #trace = "Traceback (most recent call last):\n" + string.join(traceback.format_tb(exception[2]), "\n")
        #self.chatOut(trace)

class NewOut:
    def __init__(self):
        self.text = StringIO.StringIO()

    def __len__(self):
        return len(self.text.getvalue())

    def reset(self):
        self.text = StringIO.StringIO()
    
    def getvalue(self):
        return self.text.getvalue()

    def write(self, text):
        oldout.write(text)
        self.text.write(text)

    def display(self, item):
        if item is not None:
            __builtin__._ = item
            self.write(str(item))

oldout = sys.stdout
olderr = sys.stderr
win = MyClass()
win.doModal()
del win
sys.stdout = oldout
sys.stderr = olderr