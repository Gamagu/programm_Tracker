import win32serviceutil
import servicemanager
import win32event
import win32service

class SMWinservice(win32serviceutil.ServiceFramework):
    """Base class to create winservice in python"""

    _svc_name = 'Processtracker'
    _scv_display_name = 'Python prozess tracker'
    _svc_description_ = 'Python service to track programm usage via prozesses'

    @classmethod
    def parse_command_line(cls):
        """
        Classmethod to parse the command line
        """
    
    def __init__(self, args):
        '''
        Constructor of the winservice
        '''
        win32serviceutil.ServiceFramework.__init__(self, args)
        self.hWaitStop = win32event.CreateEvent(None, 0, 0, None)

    def SvcStop(self):
        '''
        Called when the service is asked to stop
        '''
        self.stop()
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        win32event.SetEvent(self.hWaitStop)

    def SvcDoRun(self):
        '''
        Called when the service is asked to start
        '''
        self.start()
        servicemanager.LogMsg(servicemanager.EVENTLOG_INFORMATION_TYPE,
                              servicemanager.PYS_SERVICE_STARTED,
                              (self._svc_name_, ''))
        self.main()
 
    def start(self):
        '''
        Override to add logic before the start
        eg. running condition
        '''
        pass

    def stop(self):
        '''
        Override to add logic before the stop
        eg. invalidating running condition
        '''
        pass

    def main(self):
        '''
        Main class to be ovverridden to add logic
        '''
        pass

if __name__ == '__main__':
    pass
    SMWinservice.parse_command_line()