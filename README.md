# Programm Tracker

>This tracker should track programm's runntime and store them somewhere. This will be extended by a "programm group" system where a user can define a few programms as a group which gets tracked.
 

### Planned Features

-[x]  Track time from programms 

-[x] track time in these programmgoups(automatically) 

-[x] store time localy

-[] store time in cloud

-[] should run in backround and ui can be opened via the task bar

-[] Open programmgroups for tasks
    bsp: Open spotify, chrome and vs for coding

## Track Times

For tracking we create the *process* and *processlist*. We access the wmi Api to get a list from every running Process and compaire them with a list of the programms what we should track. For every programm what we want to track we add the timedifference between messurements.



### Process
#### Attributes
*   id : int  
*    name : str     	                    
>Name of process
*    running : bool                         
*    currentRuntime : datetime.timedelta    
>Runtime since last save
*    pastTime : datetime.timedelta          
>Time read from a file/or before the last save
*    totalTime : datetime.timedelta         
*    path : str                             
>Path for an .exe for executing
*    displayName : str                      
>Name what should be displayed

> A Process can be created via a wmi._wmi_objekt (wmi.Win32_Process() retunes a list of this) or manualy what gets used in the lists read from a file.

#### Methods
*   process(parent : wmi._wmi_object = None, running = False, id = -1, name : str = None, pastTime : int = 0, path : str = "", displayName : str = "")
> If *parent* is left out *id* and  *name* gets read out from *parent*
*   addTimedelta(diff : datetime.timedelta) : void
> Adds diff to the *currentRuntime* and updates *totalTime*
*   applyCurrentRuntime() : void
>adds the *currentRuntime* to *totalRuntime* and reset *currentRuntime*
* getDisplayName() : str
>Returns *displayname*, if its "" or None this returns *name*.

### ProcessList
>ProcessList inherit from *collections.UserList* and is just a wrapper for a list of processes and a list of names : str.

#### Attributes
*   processNames : list
*   PocessList : list
> Still works like a normal *list*-object

#### Methods
*   append(item: process) : void
> appends *item* to *processList* and appends *item.name* to *processNames*
*   checkRunning() : bool
> Returns *true* if for every *item* *item.running* equals *true*

### processGroup
>ProcessGroup inherbits from *process* and *processList*



