import datetime, wmi, datatypes, json, time
from collections import UserList
class Tracker:
    def __init__(self):
        self.processesNow = datatypes.processList() #for new processes
        self.processesLast = datatypes.processList() #for last timestamp. to check if sth stopped
        self.processGroups = [] #groups to check
        self.processesToTrack = datatypes.processList() #processes to check
        self.conn = wmi.WMI() #wrapper to win api?
        self.delay = 5 #Delay in sec between checks -> precision
        self.t1 = datetime.datetime.now()

    def getRunningProcesses(self):
        t1 = datetime.datetime.now()
        tasks = self.conn.Win32_Process()
        
        self.processesNow = datatypes.processList() #Empty the list
        for task in tasks:
            self.processesNow.append(datatypes.prozess(parent = task))
        print("readout time: ",(datetime.datetime.now() - t1))
    def updateProcessesToTrack(self):
        self.getRunningProcesses()
        deltaT = datetime.datetime.now()-self.t1 #Timedifference between last Processreadout and now
        self.t1 = datetime.datetime.now()
        print("timedelta: ", deltaT)
        for i in range(len(self.processesToTrack.prozessNames)):
            if self.processesToTrack.prozessNames[i] in self.processesNow.prozessNames:
                self.processesToTrack[i].running = True #Update state
                self.processesToTrack[i].currentRuntime += deltaT #Update runtime
                print(f'Programm: {self.processesToTrack[i].name} Runtime: {self.processesToTrack[i].currentRuntime}')
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
            print("yikes: ", i.totalTime)
        #get data from the existing file
        jsonFile : dict
        with open("processes.json", "r") as file:
            jsonFile = json.load(file)

        #Manipulate Json with new data
        newData = []
        for i in range(len(self.processesToTrack)):
            
            newData.append({
                "name" : self.processesToTrack.prozessNames[i],
                "totalTime" : self.processesToTrack[i].totalTime.seconds
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
    for i in range(10):
        time.sleep(test.delay)
        #test.getRunningProcesses()
        test.updateProcessesToTrack()
            
    test.writeProcessToTrack()

    #print(datetime.datetime.now()-t1)
    

