
from tracker import Tracker
from ui import Ui, UiThread
import threading, time

def createUi(ui,processlist):
    ui = Ui(processlist).mainloop()

if __name__ == '__main__':
    tracker = Tracker()
    keepRunning=True
    tracker.readProcessToTrack()

    uiThread = UiThread(args=[tracker.processesToTrack])
    uiThread.start()
    time.sleep(0.5)
    tracker.updateProcessesToTrack()
    try:
        uiThread.ui.update()
    except Exception as e:
        print(e) 
    while uiThread.is_alive():
        for i in range(10):
            if uiThread.is_alive() != True:
                break
            time.sleep(tracker.delay)
            tracker.updateProcessesToTrack()
            uiThread.update()
            
        tracker.writeProcessToTrack()
            
    tracker.writeProcessToTrack()
    uiThread.join()

