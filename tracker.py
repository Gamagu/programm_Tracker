from dataclasses import dataclass
import datetime, wmi, datatypes
from collections import UserList
class Tracker:
    def __init__(self):
        self.processes = datatypes.processList()
        self.processGroups = []
        self.processesToTrack = []
        self.conn = wmi.WMI()
        self.delay = 60 #Delay in sec between checks -> precision

    def getRunningProcesses(self):
        tasks = self.conn.Win32_Process()
        self.processes = datatypes.processList()
        for task in tasks:
            self.processes.append(datatypes.prozess(task))

    def test(self):
        for i in self.processes.prozessNames:
            print(i)
    def checkProcess(self):
        pass
    def initProcessgroups(self):
        pass
    def checkProcessgroup(self):
        pass     

if __name__ == "__main__":
    test = Tracker()
    t1 = datetime.datetime.now()
    test.getRunningProcesses()
    print(datetime.datetime.now()-t1)
    test.test()
    

