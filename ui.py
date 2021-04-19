import datetime
import tkinter as tk
import datatypes 
class Ui(tk.Tk):
    """ Main Ui for the Prozess tracker"""

    def __init__(self) -> None:
        
        super().__init__("Process Tracker")
        self.title("Prozess Tracker")
        #MainFrame
        self.mainFrame = tk.Frame(self, width= 100, height= 100)
        self.mainFrame.pack(fill=tk.BOTH)
        
        self.test()
        self.initMenue()
    def test(self):
        
        self.prozessTest = datatypes.prozess(parent=None,running=False,id=10,name="Test")
        self.yikes = ProzessFrame(self.mainFrame,self.prozessTest)
        self.yikes.pack(fill=tk.BOTH)
    def initMenue(self):
        self.menu = tk.Menu(self)
        self.config(menu=self.menu)

        self.menu.add_command(label='Reload', command=self.reload)

    
    def reload(self):
        print("Aktualisiere")


class ProzessFrame(tk.Frame):
    """Frame to display processes"""

    def __init__(self,parent, prozess) -> None:
        tk.Frame.__init__(self,parent)
        self.prozess : datatypes.prozess = prozess
        self.prozess.running = False
        self.prozess.currentRuntime = datetime.timedelta(hours=1)
        self.name = tk.Label(self,text=self.prozess.name, width=15, anchor=tk.W)
        self.status = tk.Label(self, width=8)
        self.timer = tk.Label(self, width=15, anchor=tk.E)
        self.timer.config(text=str(self.prozess.currentRuntime.total_seconds()/60/60)) # set Text to hours of the timedelta

        if self.prozess.running == True:
            self.status.config(bg='#008800', text="Active")
        else:
            self.status.config(bg='#990000', text="Inactive")
        
        self.name.pack(fill=tk.Y,side='left')
        
        self.status.pack(fill=tk.Y, side='right')
        self.timer.pack(fill=tk.Y,side='right')
    def update(self):
        """should update the Prozess in the UI"""
        
        self.timer.config(text=str(self.prozess.currentRuntime.total_seconds()/60/60)) # set Text to hours of the timedelta
        if self.prozess.running == True:
            self.status.config(bg='#008800', text="Active")
        else:
            self.status.config(bg='#990000', text="Inactive")

if __name__ == '__main__':
    test = Ui()
    test2 = datatypes.prozess(parent=None,running=False,id=10,name="Yikes")
    test.mainloop()
