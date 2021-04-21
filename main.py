
from tracker import Tracker
from ui import Ui, UiThread
import threading, time


if __name__ == '__main__':
    tracker = Tracker()
    keepRunning=True
    tracker.readProcessToTrack()

    uiThread = UiThread(args=[tracker.processesToTrack])
    uiThread.start()    
    tracker.updateProcessesToTrack()
    
    uiThread.ui.reload()
    
    while uiThread.is_alive():
        for i in range(10):
            if uiThread.is_alive() != True:
                break
            time.sleep(tracker.delay)
            tracker.updateProcessesToTrack()
            uiThread.ui.reload()
            
        tracker.writeProcessToTrack()
            
    tracker.writeProcessToTrack()
    uiThread.join()

