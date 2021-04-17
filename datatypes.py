from dataclasses import dataclass
import datetime, wmi
from collections import UserList

@dataclass
class prozess:
    """Process information"""
    id : int
    name : str
    currentRuntime : datetime
    totalTime : datetime

    def __init__(self, parent : wmi._wmi_object ) -> None:
        self.id = parent.ProcessId
        self.name = parent.name

class processList(UserList):
    """List only for processes"""
    def __init__(self) -> None:
        UserList.__init__(self)
        self.prozessNames = []
    def append(self, item: prozess) -> None:
        self.prozessNames.append(item.name)
        return super().append(item)
        