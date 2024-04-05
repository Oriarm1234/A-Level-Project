from threading import Thread
import time
class Timer:
    def __init__(self, delay):
        """time = delay in seconds"""
        self.delay = delay
        
        self.thread = Thread(target=self.check_time, args=(self,))
        self.complete = False
        self.completionArgs = []
        self.name = ""
        
        self.startTime = 1
        self.endTime = 1
    
    def begin(self):
        self.startTime = time.time()
        self.endTime = self.startTime+self.delay
        self.thread.start()
        
    @staticmethod
    def on_completion(self, *args, **kwargs):
        pass
        
    def check_time(self,*args):
        self.complete = False
        time.sleep(self.delay)
        self.on_completion(*self.completionArgs)
        self.complete = True
        
    def get_time_left(self):
        currentTime = time.time()
        return self.endTime - currentTime if currentTime < self.endTime else 0