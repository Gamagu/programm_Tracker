import datetime, wmi, datatypes, json, time
from os import name
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
        tasks = self.conn.Win32_Process()
        self.processesNow = datatypes.processList() #Empty the list
        for task in tasks:
            self.processesNow.append(datatypes.prozess(parent = task))

    def updateProcessesToTrack(self):
        # TODO Change time messurement for both groups and processes
        self.deltaT = datetime.datetime.now()-self.t1 #Timedifference between last Processreadout and now
        self.t1 = datetime.datetime.now()
        print("timedelta: ", self.deltaT)
        for i in range(len(self.processesToTrack.prozessNames)):
            if self.processesToTrack.prozessNames[i] in self.processesNow.prozessNames:
                self.processesToTrack[i].running = True #Update state
                #self.processesToTrack[i].currentRuntime += deltaT #Update runtime
                self.processesToTrack[i].addTimedelta(self.deltaT)
                print(f'Programm: {self.processesToTrack[i].name} Runtime: {self.processesToTrack[i].currentRuntime}')
            else:
                self.processesToTrack[i].running = False
    
    def updateGroupsToTrack(self):
        for i in range(len(self.processGroups)):
            self.processGroups[i].running =  self.processGroups[i].checkRunning()
            if self.processGroups[i].running == True:
                self.processGroups[i].addTimedelta(self.deltaT)
                print(f'Group: {self.processGroups[i].name} Runtime: {self.processGroups[i].currentRuntime}')

    def update(self):
        self.deltaT = datetime.datetime.now()-self.t1 #Timedifference between last Processreadout and now
        self.t1 = datetime.datetime.now()
        self.getRunningProcesses()
        self.updateProcessesToTrack()
        self.updateGroupsToTrack()
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
        
        for i in jsonFile["processes"]: #Für jeden prozess
            self.processesToTrack.append(datatypes.prozess( name=i["name"],
                                                            pastTime= i["totalTime"]))    
                                    
    def readProcessGroups(self):
        jsonFile : dict
        with open("groups.json", "r") as file:
            jsonFile = json.load(file)
        
        for group in range(len(jsonFile["groups"])): #Für jede gruppe   
            self.processGroups.append(datatypes.prozessGroup(name=jsonFile["groups"][group]["name"],pastTime = jsonFile["groups"][group]["totalTime"])) # Create a grouplist and save it
            for prozess in jsonFile["groups"][group]["programms"]: #For every programm, only programms in prozesses to track are able for tracking
                if prozess["name"] in self.processesToTrack.prozessNames: #if its already tracking
                    self.processGroups[group].append(self.processesToTrack[self.processesToTrack.prozessNames.index(prozess["name"])])

    def writeProcessGroups(self):
        pass
    def writeProcessToTrack(self):
        #Apply the prozess.currentRuntime to prozess.totalRuntime and reset currentRuntime
        for i in self.processesToTrack:
            i.totalTime += i.currentRuntime
            i.currentRuntime = datetime.timedelta(seconds=0)            

        newData ={
                    "processes": []         
                }

        for i in range(len(self.processesToTrack)):
            newData["processes"].append({
                "name" : self.processesToTrack.prozessNames[i],
                "totalTime" : self.processesToTrack[i].totalTime.seconds
            })
        
        #save
        with open("processes.json", "w") as file:
            json.dump(newData, file, indent=4 ,sort_keys = True)
   

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
    

