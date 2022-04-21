import datetime, wmi, datatypes, json, time
from os import name
from collections import UserList

class Tracker:
    def __init__(self):
        self.processesNow = datatypes.processList() #for new processes
        self.processGroups = [] #groups to check
        self.processesToTrack = datatypes.processList() #processes to check
        self.conn = wmi.WMI() #wrapper to win api?
        self.delay = 5 #Delay in sec between checks -> precision
        self.t1 = datetime.datetime.now()

    def getRunningProcesses(self):
        processes = self.conn.Win32_Process() #Retrieve all processes
        self.processesNow = datatypes.processList() #Empty the list
        for process in processes:
            self.processesNow.append(datatypes.prozess(parent = process))

    def updateProcessesToTrack(self):
        for i in range(len(self.processesToTrack.prozessNames)):
            if self.processesToTrack.prozessNames[i] in self.processesNow.prozessNames:
                self.processesToTrack[i].running = True #Update state
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
        #Timedifference between last Processreadout and now
        self.deltaT = datetime.datetime.now()-self.t1 
        self.t1 = datetime.datetime.now()

        self.getRunningProcesses()
        self.updateProcessesToTrack()
        self.updateGroupsToTrack()

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
                                                            pastTime= i["totalTime"],
                                                            displayName=i["displayName"],
                                                            path=i["path"]))    
                                    
    def readProcessGroups(self):
        jsonFile : dict
        with open("groups.json", "r") as file:
            jsonFile = json.load(file)
        
        for group in range(len(jsonFile["groups"])): #Für jede gruppe   
            self.processGroups.append(datatypes.prozessGroup(name=jsonFile["groups"][group]["name"],pastTime = jsonFile["groups"][group]["totalTime"],
                                                            displayName=jsonFile["groups"][group]["displayName"],
                                                            path=jsonFile["groups"][group]["path"])) # Create a grouplist and save it

            for prozess in jsonFile["groups"][group]["programms"]: #For every programm, only programms in prozesses to track are able for tracking
                if prozess["name"] in self.processesToTrack.prozessNames: #if its already tracking
                    self.processGroups[group].append(self.processesToTrack[self.processesToTrack.prozessNames.index(prozess["name"])])

    def writeProcessGroups(self):
        jsonFile : dict = {"groups":[]}
        # apply the processGroup.currentRuntime to processGroup.totalRuntime and reset currentRuntime
        for i in self.processGroups:
            i.applyCurrentRuntime()  
            programms = []
            for pro in i:
                programms.append({"name":pro.name})
            print("name:{i.name} totalTime:{i.totalTime}")
            jsonFile["groups"].append({"name": i.name,
                                        "totalTime": i.totalTime.seconds,
                                        "programms":programms,
                                        "displayName" : i.displayName,
                                        "path" : i.path
                                        })
        
        #save
        with open("groups.json", "w") as file:
            json.dump(jsonFile, file, indent=4 ,sort_keys = True)
        
    def writeProcessToTrack(self):
        #Apply the prozess.currentRuntime to prozess.totalRuntime and reset currentRuntime
        for i in self.processesToTrack:
            i.applyCurrentRuntime()            

        newData ={
                    "processes": []         
                }

        for i in range(len(self.processesToTrack)):
            newData["processes"].append({
                "name" : self.processesToTrack.prozessNames[i],
                "totalTime" : self.processesToTrack[i].totalTime.seconds,
                "displayName"  : self.processesToTrack[i].displayName,
                "path" : self.processesToTrack[i].path
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
    

