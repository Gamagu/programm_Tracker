from dataclasses import dataclass
import datetime, wmi
class Tracker:
    def __init__(self):
        self.processes = processList()
        self.processGroups = []
        self.processesToTrack = []
        self.conn = wmi.WMI()
        self.delay = 10 #Delay in sec between checks -> precision

    def getRunningProcesses(self):
        tasks = self.conn.Win32_Process()
        self.processes = processList()
        for task in tasks:
            self.processes.append(prozess(task))

    def checkProcess(self):
        pass
    def initProcessgroups(self):
        pass
    def checkProcessgroup(self):
        pass
    """
instance of Win32_Process
{
        Caption = "powershell.exe";
        CommandLine = "C:\\WINDOWS\\System32\\WindowsPowerShell\\v1.0\\powershell.exe";
        CreationClassName = "Win32_Process";
        CreationDate = "20210416215511.520947+120";
        CSCreationClassName = "Win32_ComputerSystem";
        CSName = "DESKTOP-KNF5O3E";
        Description = "powershell.exe";
        ExecutablePath = "C:\\WINDOWS\\System32\\WindowsPowerShell\\v1.0\\powershell.exe";
        Handle = "12672";
        HandleCount = 608;
        KernelModeTime = "7968750";
        MaximumWorkingSetSize = 1380;
        MinimumWorkingSetSize = 200;
        Name = "powershell.exe";
        OSCreationClassName = "Win32_OperatingSystem";
        OSName = "Microsoft Windows 10 Home|C:\\WINDOWS|\\Device\\Harddisk1\\Partition4";
        OtherOperationCount = "4666";
        OtherTransferCount = "72012";
        PageFaults = 135172;
        PageFileUsage = 56672;
        ParentProcessId = 6876;
        PeakPageFileUsage = 60964;
        PeakVirtualSize = "2204000677888";
        PeakWorkingSetSize = 72708;
        Priority = 8;
        PrivatePageCount = "58032128";
        ProcessId = 12672;
        QuotaNonPagedPoolUsage = 37;
        QuotaPagedPoolUsage = 397;
        QuotaPeakNonPagedPoolUsage = 86;
        QuotaPeakPagedPoolUsage = 415;
        ReadOperationCount = "160";
        ReadTransferCount = "1315108";
        SessionId = 3;
        ThreadCount = 18;
        UserModeTime = "24843750";
        VirtualSize = "2203986788352";
        WindowsVersion = "10.0.19041";
        WorkingSetSize = "70807552";
        WriteOperationCount = "96";
        WriteTransferCount = "4093";
};"""
@dataclass
class prozess:
    """Process information"""
    id : int
    name : str
    
    currentRuntime : datetime
    totalTime : datetime

    def __init__(self, parent : wmi._wmi_object ) -> None:
        id = parent.ProcessId
        name = parent.name

class processList(list):
    """List only for processes"""
    def __init__(self) -> None:
        self.prozessNames = []
        return super.__init__()
    def append(self, __object: wmi._wmi_object) -> None:
        self.prozessNames.append(__object.Name)
        return super().append(__object)

if __name__ == "__main__":
    test = Tracker()
    test.getRunningProcesses()


