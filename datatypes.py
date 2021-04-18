from dataclasses import dataclass
import datetime, wmi
from collections import UserList

@dataclass
class prozess:
    """Process information"""
    id : int
    name : str
    running : bool
    currentRuntime : datetime #Runtime since last save
    totalTime : datetime

    def __init__(self, parent : wmi._wmi_object = None, running = False, id = -1, name : str = None, totalTime : int = 0  ) -> None:
        if parent is not None:
            self.id = parent.ProcessId
            self.name = parent.name
            self.running = running
            self.totalTime = datetime.timedelta(seconds=0)
        else:
            self.id = id
            self.name = name
            self.running = running
            self.totalTime = datetime.timedelta(seconds=totalTime)
        self.currentRuntime = datetime.timedelta(seconds=0)
class processList(UserList):
    """List only for processes"""
    def __init__(self) -> None:
        UserList.__init__(self)
        self.prozessNames = []
    def append(self, item: prozess) -> None:
        self.prozessNames.append(item.name)
        return super().append(item)
        