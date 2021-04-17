import datetime, wmi, datatypes, json
from collections import UserList
class Tracker:
    def __init__(self):
        self.processesNow = datatypes.processList() #for new processes
        self.processesLast = datatypes.processList() #for last timestamp. to check if sth stopped
        self.processGroups = [] #groups to check
        self.processesToTrack = [] #procsss to check
        self.conn = wmi.WMI() #wrapper to win api?
        self.delay = 60 #Delay in sec between checks -> precision

    def getRunningProcesses(self):
        tasks = self.conn.Win32_Process()
        self.processes = datatypes.processList()
        for task in tasks:
            self.processes.append(datatypes.prozess(task))

    def test(self):
        for i in self.processes.prozessNames:
            print(i)

    def checkProcess(self, name  : str):
        if name in self.processes.prozessNames:
            return True
        return False

    def initProcessgroups(self):
        pass
    def checkProcessgroup(self):
        pass     

if __name__ == "__main__":
    test = Tracker()
    t1 = datetime.datetime.now()
    test.getRunningProcesses()
    
    test.test()
    print(test.checkProcess("firefox.exe"))
    print(datetime.datetime.now()-t1)
    

