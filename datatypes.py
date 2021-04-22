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

    def __init__(self, parent : wmi._wmi_object = None, running = False, id = -1, name : str = None, totalTime : int = 0  ) -> None:
        if parent is not None:
            #if a wmi objekt is given
            self.id = parent.ProcessId
            self.name = parent.name
            self.running = running
            
            self.pastTime = datetime.timedelta(seconds=totalTime)
        else:
            #if its self created
            self.id = id
            self.name = name
            self.running = running
            self.pastTime = datetime.timedelta(seconds=totalTime)

        self.currentRuntime = datetime.timedelta(seconds=0)
        self.totalTime = self.currentRuntime + self.pastTime

    def addTimedelta(self, diff : datetime.timedelta):
        self.currentRuntime += diff
        self.totalTime = self.currentRuntime + self.pastTime

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

        
class prozessGroupList(processList):
    """List for Processes in for of a group."""

    def __init__(self, name) -> None:
        super().__init__()
        self.name = name
        