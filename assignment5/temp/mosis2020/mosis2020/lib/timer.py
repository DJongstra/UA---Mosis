# YAKINDU's Default timer class, adapted to work with TkInter

import threading
import time
from functools import partial

class TimerService:

    """
    
    Default timer service for timed statecharts.
    
    """
    
    def __init__(self, tk):
        self.tk = tk
        self.is_default_timer = True
        self.timer_queue = {}

    def set_timer(self, callback, event_id, interval, periodic):
        """Schedule the time event.
        
        Checks if the given time event is already in queue and creates a
        timer based on the `periodic`parameter (Single or Repeat).
        
        Note: statemachine class converts time from sec to milliseconds,
        so do vice versa.
        """
        timer_id = (callback, event_id)
        if timer_id in self.timer_queue:
            self.unset_timer(callback, event_id)
        m_interval = float(interval)/1000.0
        if periodic is False:
            self.timer_queue[timer_id] = SingleTimer(self.tk, m_interval, callback, event_id)
        else:
            self.timer_queue[timer_id] = RepeatedTimer(self.tk, m_interval, callback, event_id)
    
    def unset_timer(self, callback, event_id):
        """Cancel a certain event identified bei `callback` and `event_id`.
        """
        timer_id = (callback, event_id)
        with threading.RLock():
            if timer_id in self.timer_queue:
                event_timer = self.timer_queue[timer_id]
                event_timer.stop()
                del event_timer
    
    def cancel(self):
        """Cancel all events that are currently running.
        """
        with threading.RLock():
            for (callback, event_id) in self.timer_queue:
                self.unset_timer(callback, event_id)
    

class SingleTimer:

    """Call `function` after `period` seconds."""
    
    def __init__(self, tk, period, callback, event_id):
        self.tk = tk
        self.callback = callback
        self.event_id = event_id
        def cb():
            self.callback.time_elapsed(self.event_id)
        self.sched_id = self.tk.after(int(period*1000), cb)
        # self.single_timer = threading.Timer(period, self.callback.time_elapsed, [self.event_id])
        # self.single_timer.start()

    def stop(self):
        self.tk.after_cancel(self.sched_id)

class RepeatedTimer:

    """Repeat `callback` every `interval` seconds."""
    
    def __init__(self, tk, interval, callback, event_id):
        raise Exception("RepeatedTimer unsupported. If you get this message, email me: joeri.exelmans@uantwerpen.be")
        self.interval = interval
        self.callback = callback
        self.event_id = event_id
        self.start = time.time()
        self.event = threading.Event()
        self.thread = threading.Thread(target=self._target)
        self.thread.start()
        
    def _target(self):
        while not self.event.wait(self._time):
            self.callback.time_elapsed(self.event_id)
            
    @property
    def _time(self):
        return self.interval - ((time.time() - self.start) % self.interval)
        
    def stop(self):
        self.event.set()
        try:
            self.thread.join()
        except RuntimeError:
            print('Can not join thread')
        
