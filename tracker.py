import datetime, wmi, datatypes, json, time
from collections import UserList
class Tracker:
    def __init__(self):
        self.processesNow = datatypes.processList() #for new processes
        self.processesLast = datatypes.processList() #for last timestamp. to check if sth stopped
        self.processGroups = [] #groups to check
        self.processesToTrack = datatypes.processList() #processes to check
        self.conn = wmi.WMI() #wrapper to win api?
        self.delay = 60 #Delay in sec between checks -> precision
        self.t1 = datetime.datetime.now()

    def getRunningProcesses(self):
        tasks = self.conn.Win32_Process()
        self.t1 = datetime.datetime.now()
        self.processesNow = datatypes.processList() #Empty the list
        for task in tasks:
            self.processesNow.append(datatypes.prozess(parent = task))

    def updateProcessesToTrack(self):
        deltaT = datetime.datetime.now()-self.t1 #Timedifference between last Processreadout and now
        for i in range(len(self.processesToTrack.prozessNames)):
            if self.processesToTrack.prozessNames[i] in self.processesNow.prozessNames:
                self.processesToTrack[i].running = True #Update state
                self.processesToTrack[i].currentRuntime += deltaT #Update runtime
            else:
                self.processesToTrack[i].running = False

    def test(self):
        for i in self.processes.prozessNames:
            print(i)

    def checkProcess(self, name : str):
        if name in self.processes.prozessNames:
            return True
        return False

    def readProcessToTrack(self):
        jsonFile : dict
        with open("processes.json", "r") as file:
            jsonFile = json.load(file)
        
        for i in jsonFile["processes"]:
            self.processesToTrack.append(datatypes.prozess( name=i["name"],
                                                            totalTime= i["totalTime"]))

    def writeProcessToTrack(self):
        #Apply the prozess.currentRuntime to prozess.totalRuntime and reset currentRuntime
        for i in self.processesToTrack:
            i.totalTime += i.currentRuntime
            i.currentRuntime = datetime.timedelta(seconds=0)            

        #get data from the existing file
        jsonFile : dict
        with open("processes.json", "r") as file:
            jsonFile = json.load(file)

        #Manipulate Json with new data
        newData = []
        for i in range(len(self.processesToTrack)):
            newData.append({
                "name" : self.processesToTrack.prozessNames[i],
                "totalTime" : self.processesToTrack[i].totalTime.total_seconds()
            })
        jsonFile["processes"] = newData 

        #save
        with open("processes.json", "w") as file:
            json.dump(jsonFile, file, indent=4 ,sort_keys = True)

    def checkProcessgroup(self):
        pass     

if __name__ == "__main__":
    test = Tracker()
    t1 = datetime.datetime.now()
    test.readProcessToTrack()
    test.getRunningProcesses()
    time.sleep(2)
    test.updateProcessesToTrack()
    test.writeProcessToTrack()

    #print(datetime.datetime.now()-t1)
    

