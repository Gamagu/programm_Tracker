import datetime
import tkinter as tk
import datatypes , threading as th
class Ui(tk.Tk):
    """ Main Ui for the Prozess tracker"""

    def __init__(self, processlist : datatypes.processList = None,debug = False) -> None:
        
        super().__init__("Process Tracker")
        self.title("Prozess Tracker")
        #MainFrame
        self.debug = debug
        if processlist == None:
            debug = True
        self.processlist = processlist
        self.processlistFrames = []
        self.mainFrame = tk.Frame(self, width= 100, height= 100)
        self.prozessTop = ProzessFrameTop(self.mainFrame)
        self.prozessTop.pack(side=tk.TOP,fill=tk.BOTH)
        self.mainFrame.pack(fill=tk.BOTH) 
        #Create new event
        
        self.bind("<<OnUpdate>>", self.reload)
        self.initMenue()

        if debug == True:
            self.test()
            return

        self.initProcesses()

    def test(self):
        self.prozessTest = datatypes.prozess(parent=None,running=False,id=10,name="Spotify.exe")
        self.yikes = ProzessFrame(self.mainFrame,self.prozessTest)
        self.yikes.pack(fill=tk.BOTH)
    def initMenue(self):
        self.menu = tk.Menu(self)
        self.config(menu=self.menu)

        self.menu.add_command(label='Reload', command=self.reload)

    def initProcesses(self):
        for i in range(len(self.processlist)):
            print("Prozess: ", self.processlist[i].name, self.processlist[i].totalTime, self.processlist[i].running)
            h = ProzessFrame(self.mainFrame, self.processlist[i])
            self.processlistFrames.append(h)
            self.processlistFrames[i].pack(side=tk.TOP,fill=tk.BOTH)
    
    def reload(self):
        print("Aktualisiere")
        for i in self.processlistFrames:
            i.update()
        
        
    def run(processlist):
        Ui(processlist).mainloop()
    


class UiThread(th.Thread):
    def __init__(self, group= None, target=None, name= "", args=[], kwargs={}, daemon=False) -> None:
        super().__init__(group=group, target=target, name=name, args=args, kwargs=kwargs, daemon=daemon)
        self.ui : Ui = None
    def run(self):
        self.ui = Ui(*self._args)
        self.ui.mainloop()
    
    def update(self):
        print("yeet: ", self.ui)
        self.ui.event_generate(sequence="<<OnUpdate>>")

class ProzessFrame(tk.Frame):
    """Frame to display processes"""

    def __init__(self,parent, prozess) -> None:
        tk.Frame.__init__(self,parent)
        self.prozess : datatypes.prozess = prozess
        self.name = tk.Label(self,text=self.prozess.name, width=15, anchor=tk.W)
        self.status = tk.Label(self, width=8)
        self.timer = tk.Label(self, width=15, anchor=tk.E)
        zahl = self.prozess.totalTime.total_seconds()/60/60
        self.timer.config(text=f'{zahl:.2f}') # set Text to hours of the timedelta

        if self.prozess.running == True:
            self.status.config(bg='#008800', text="Active")
        else:
            self.status.config(bg='#990000', text="Inactive")
        
        self.name.pack(fill=tk.Y,side='left')
        
        self.status.pack(fill=tk.Y, side='right')
        self.timer.pack(fill=tk.Y,side='right')
    def update(self):
        """should update the Prozess in the UI"""
        zahl = self.prozess.totalTime.total_seconds()/60/60
        self.timer.config(text=f'{zahl:.2f}') # set Text to hours of the timedelta
        if self.prozess.running == True:
            self.status.config(bg='#008800', text="Active")
        else:
            self.status.config(bg='#990000', text="Inactive")
    
class ProzessFrameTop(tk.Frame):
    def __init__(self,parent) -> None:
        tk.Frame.__init__(self,parent)
        self.name = tk.Label(self,text="Name", width=15, anchor=tk.W)
        self.status = tk.Label(self, text='Status', width=8)
        self.timer = tk.Label(self,text='Time', width=15, anchor=tk.E)
        self.name.pack(fill=tk.Y,side='left')
        self.status.pack(fill=tk.Y, side='right')
        self.timer.pack(fill=tk.Y,side='right')

if __name__ == '__main__':
    test = Ui()
    test2 = datatypes.prozess(parent=None,running=False,id=10,name="Yikes")
    test.mainloop()
