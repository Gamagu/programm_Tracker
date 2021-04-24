
from tracker import Tracker
from ui import Ui, UiThread
import threading, time


if __name__ == '__main__':
    tracker = Tracker()
    keepRunning=True
    tracker.readProcessToTrack()
    tracker.readProcessGroups()
    uiThread = UiThread(args=[tracker.processesToTrack, tracker.processGroups])
    uiThread.start()    
    tracker.update()
    uiThread.ui.reload()
    while uiThread.is_alive():
        for i in range(10):
            if uiThread.is_alive() != True:
                break
            time.sleep(tracker.delay)
            try:
                tracker.update()
                uiThread.ui.reload()
            except Exception as e:
                print("Error: ", e)
        tracker.writeProcessToTrack()
            
    tracker.writeProcessToTrack()
    tracker.writeProcessGroups()
    uiThread.join()

