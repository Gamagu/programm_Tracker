
from tracker import Tracker
from ui import Ui, UiThread
import threading, time


if __name__ == '__main__':
    #Tracker init
    tracker = Tracker()
    tracker.readProcessToTrack()
    tracker.readProcessGroups()

    #Ui init
    uiThread = UiThread(args=[tracker.processesToTrack, tracker.processGroups])
    uiThread.start()  

    #first update  
    tracker.update()
    uiThread.ui.reload()

    #While the ui is alive -> keep updating
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
        tracker.writeProcessToTrack() #Save every 10th run
        
    #Save if uiThread died(ui closed)
    tracker.writeProcessToTrack() 
    tracker.writeProcessGroups()
    uiThread.join()

