import datetime
from os import terminal_size
import tkinter as tk
import datatypes , threading as th

IMG_SETTINGS = None

class Ui(tk.Tk):
    """ Main Ui for the Prozess tracker"""

    def __init__(self, processlist : datatypes.processList = None, groupList : list = None, debug = False) -> None:
        
        super().__init__("Process Tracker")
        self.title("Prozess Tracker")

        #Media
        global IMG_SETTINGS
        IMG_SETTINGS = tk.PhotoImage(file= "media/settingsbutton.png") #Image for button
        
        #MainFrame
        self.debug = debug
        if processlist == None:
            debug = True
        #Init processes
        self.processlist = processlist
        self.processlistFrames = []
        self.processFrame = tk.Frame(self, width= 100, height= 100)
        self.prozessTop = ProzessFrameHeader(self.processFrame)
        self.prozessTop.pack(side=tk.TOP,fill=tk.BOTH)
        self.processFrame.grid(row=0, column=0, sticky="nsew") 
        
        self.initProcesses()
        #Init Groupe
        self.useGroups = False
        if groupList != None:
            self.useGroups = True
            self.groupList = groupList
            self.gouplistFrames = []
            self.groupFrame = tk.Frame(self, width=100, height=100)
            self.groupHeader = ProzessFrameHeader(self.groupFrame)
            self.groupHeader.pack(side=tk.TOP)
            self.groupFrame.grid(row=0, column=0, sticky="nsew")
            self.initGroups()
        
        self.processFrame.tkraise()

        #Create new event
        self.bind("<<OnUpdate>>", self.reload)
        self.initMenue()

        if debug == True:
            self.test()
            return

    def initGroups(self):
        for i in range(len(self.groupList)):
            print("Prozess: ", self.groupList[i].name)
            h = ProzessGroupFrame(self.groupFrame,self.groupList[i])
            self.gouplistFrames.append(h)
            self.gouplistFrames[i].pack(side=tk.TOP,fill=tk.BOTH)

    def test(self):
        pass
    def initMenue(self):
        self.menu = tk.Menu(self)
        self.config(menu=self.menu)
        self.menu.add_command(label='Reload', command=self.reload)

        #Add switch groups<->processes
        if self.useGroups:
            self.switch = tk.Menu(self.menu,) #main switch menu
            # Processes tap
            self.switch.add_command(label="Processes", command=self.processFrame.tkraise)
            # Groups tap
            self.switch.add_command(label="Groups", command=self.groupFrame.tkraise)
            
            # TODO Make switcher for frames via dict -> shorter

            #app menu
            self.menu.add_cascade(label="Switch", menu=self.switch)

    def initProcesses(self):
        for i in range(len(self.processlist)):
            print("Prozess: ", self.processlist[i].name, self.processlist[i].totalTime, self.processlist[i].running)
            h = ProzessFrame(self.processFrame, self.processlist[i])
            self.processlistFrames.append(h)
            self.processlistFrames[i].pack(side=tk.TOP,fill=tk.BOTH)
    
    def reload(self):
        print("Aktualisiere")
        for i in self.processlistFrames:
            i.update()
        
        for i in self.gouplistFrames:
            i.update()
        
    def run(processlist):
        Ui(processlist).mainloop()
    
    @classmethod
    def getFormatedString(sec : int):
        """
        Returns a formated string for the ui
        """
        s =""



class UiThread(th.Thread):
    def __init__(self, group= None, target=None, name= "", args=[], kwargs={}, daemon=False) -> None:
        super().__init__(group=group, target=target, name=name, args=args, kwargs=kwargs, daemon=daemon)
        self.ui : Ui = None
    def run(self):
        self.ui = Ui(*self._args)
        self.ui.mainloop()
    
    def update(self):
        print("yeet: ", self.ui)
        self.ui.event_generate(sequence="<<OnUpdate>>")

class ProzessFrame(tk.Frame):
    """Frame to display processes"""
    
    def __init__(self,parent, prozess) -> None:
        tk.Frame.__init__(self,parent)
        self.prozess : datatypes.prozess = prozess
        self.initStructure()
    def initStructure(self):
        """ Add structure and fill widgets """
        self.name = tk.Label(self,text=self.prozess.getDisplayName(), width=15, anchor=tk.W)
        self.status = tk.Label(self, width=8)
        self.timer = tk.Label(self, width=15, anchor=tk.E)
        self.settingBt = SettingsButton(self,self.prozess)
        #sec = self.prozess.totalTime.total_seconds()

        self.timer.config(text=str(self.prozess.totalTime)) # set Text to hours of the timedelta

        if self.prozess.running == True:
            self.status.config(bg='#008800', text="Active")
        else:
            self.status.config(bg='#990000', text="Inactive")

        self.settingBt.pack(fill=tk.Y,side='right')
        self.name.pack(fill=tk.Y,side='left')
        
        self.status.pack(fill=tk.Y, side='right')
        self.timer.pack(fill=tk.Y,side='right')
        
    def update(self):
        """should update the Prozess in the UI"""
        # TODO Fix format of output
        #sec = self.prozess.totalTime.total_seconds()/60/60
        self.timer.config(text=str(self.prozess.totalTime)) # set Text to hours of the timedelta
        if self.prozess.running == True:
            self.status.config(bg='#008800', text="Active")
        else:
            self.status.config(bg='#990000', text="Inactive")

class ProzessGroupFrame( ProzessFrame):
    """Frame to display processgroups"""

    def __init__(self,parent, prozessGroup) -> None:
        tk.Frame.__init__(self,parent)
        self.prozess : datatypes.prozessGroup = prozessGroup
        self.initStructure()
    
    
class ProzessFrameHeader(tk.Frame):
    def __init__(self,parent) -> None:
        tk.Frame.__init__(self,parent)
        self.name = tk.Label(self,text="Name", width=15, anchor=tk.W)
        self.status = tk.Label(self, text='Status', width=8)
        self.timer = tk.Label(self,text='Time', width=15, anchor=tk.E)
        self.name.pack(fill=tk.Y,side='left')
        self.status.pack(fill=tk.Y, side='right')
        self.timer.pack(fill=tk.Y,side='right')

class SettingsButton(tk.Button):
    def __init__(self, parent,process):
        #Accsess the IMG, was initialisied in  Ui
        self.parent = parent
        self.process = process
        global IMG_SETTINGS
        tk.Button.__init__(self,parent, height = 20, width= 20, image=IMG_SETTINGS, command=self.open)
    
    def open(self):
        test = ProcessSettingsToplevel(self.parent, self.process)

class ProcessSettingsToplevel(tk.Toplevel):
    labelDirection = tk.E

    def __init__(self, master,process):
        tk.Toplevel.__init__(self, master)
        self.process : datatypes.prozess = process
        self.initLayout()
        self.read()

    def initLayout(self):

        self.btSave = tk.Button(self, command=self.save, text="Save")

        self.labelName = tk.Label(self, text="Name:")
        self.labelPath = tk.Label(self, text="Exe. Path:")
        self.inputName = tk.Entry(self)
        self.inputPath = tk.Entry(self)

        self.labelDisplayName = tk.Label(self, text = "Displayname:")
        self.inputDisplayName = tk.Entry(self)

        self.labelName.grid(column=0, row=0, sticky=ProcessSettingsToplevel.labelDirection)
        self.inputName.grid(column=1, row=0)

        self.labelPath.grid(column=0, row=1,sticky=ProcessSettingsToplevel.labelDirection)
        self.inputPath.grid(column=1, row=1)

        self.labelDisplayName.grid(column=0,row=2,sticky=ProcessSettingsToplevel.labelDirection)
        self.inputDisplayName.grid(column=1,row=2)

        self.btSave.grid(column=0, row=3, columnspan=2)

    def save(self):
        self.process.name = self.inputName.get()
        self.process.path = self.inputPath.get()
        self.process.displayName = self.inputDisplayName.get()
        self.destroy()
        
    def read(self):
        self.inputName.insert(0,self.process.name)
        self.inputPath.insert(0,self.process.path)
        self.inputDisplayName.insert(0,self.process.displayName)

if __name__ == '__main__':
    test = Ui()
    test2 = datatypes.prozess(parent=None,running=False,id=10,name="Yikes")
    test.mainloop()
