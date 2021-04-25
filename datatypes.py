from dataclasses import dataclass
import datetime, wmi
from collections import UserList

@dataclass
class prozess:
    """Process information"""
    id : int
    name : str
    running : bool
    currentRuntime : datetime.timedelta #Runtime since last save
    pastTime : datetime.timedelta
    totalTime : datetime.timedelta
    path : str
    displayName : str

    def __init__(self, parent : wmi._wmi_object = None, running = False, id = -1, name : str = None, pastTime : int = 0, path : str = "", displayName : str = ""  ) -> None:
        if parent is not None:
            #if a wmi objekt is given
            self.id = parent.ProcessId
            self.name = parent.name
            self.running = running
            
            
        else:
            #if its self created
            self.id = id
            self.name = name
            self.running = running
            self.pastTime = datetime.timedelta(seconds=pastTime)

        self.displayName = displayName
        self.path = path
        self.pastTime = datetime.timedelta(seconds=pastTime)
        self.currentRuntime = datetime.timedelta(seconds=0)
        self.totalTime = self.currentRuntime + self.pastTime
        

    def addTimedelta(self, diff : datetime.timedelta):
        self.currentRuntime += diff
        self.totalTime = self.currentRuntime + self.pastTime
    
    def applyCurrentRuntime(self):
        # apply the processGroup.currentRuntime to processGroup.totalRuntime
        # and reset currentRuntime
        print(self.name, "------")
        print("current: ", self.currentRuntime)
        print("total: ", self.totalTime)
        self.totalTime += self.currentRuntime
        self.currentRuntime = datetime.timedelta(seconds=0) 
    
    def getDisplayName(self):
        if self.displayName == "":
            return self.name
        else:
            return self.displayName

class processList(UserList):
    """List only for processes"""
    def __init__(self) -> None:
        UserList.__init__(self)
        self.prozessNames = []
    def append(self, item: prozess) -> None:
        self.prozessNames.append(item.name)
        return super().append(item)

    def checkRunning(self) -> bool:
        """Returns True if every process in this list is runnuing"""
        for i in self:
            if i.running == False:
                return False
        return True

        
class prozessGroup(processList,prozess):
    """List for Processes in for of a group."""

    def __init__(self, name = None,running = False, pastTime : int = 0, displayName : str = "" ) -> None:
        processList.__init__(self)
        self.name = name
        self.displayName = displayName
        self.running : bool = running 
        self.pastTime = datetime.timedelta(seconds=pastTime)
        self.currentRuntime = datetime.timedelta(seconds=0)
        self.totalTime = self.currentRuntime + self.pastTime
        