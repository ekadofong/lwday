import os
import numpy as np
from . import utils

class Log (object):
    def __init__ ( self, logfile='../logs/lwday_log',
                   timefile='../logs/lwday_time' ):
        if not os.path.exists ( logfile ):
            self.log = []
        else:
            self.log = open(logfile, 'r').read().splitlines(

        if not os.path.exists ( timefile ):
            self.tlog = []
        else:
            self.tlog = open(timefile, 'r').read().splitlines()

    def verify_checkin ( self, task ):
        is_task = np.array([task+',' in x for x in self.log])
        mre = np.arange(len(self.log))[is_task][-1]
        if ',in,' in self.log[mre]:
            return True
        elif ',out,' in self.log[mre]:
            return False
        else:
            raise ValueError (f"Invalid format in task {task}: {self.log[mre]}")

    def show_alltasks ( self ):
        larr = np.array([ x.split(',') for x in self.log ])[:,0]
        alltasks = np.unique(larr)
        return alltasks

    def show_activetasks ( self ):
        larr = np.array([ x.split(',') for x in self.log ])[:,0]
        alltasks = np.unique(larr)
        active = np.zeros_like(alltasks, dtype=bool)
        for idx,tsk in enumerate(alltasks):
            if self.verify_checkin(tsk):
                active[idx] = True
        return alltasks[active]

    def add_checkin ( self, task ):
        if np.array([task+',' in x for x in self.log]).any():
            is_in = self.verify_checkin ( task )

            if is_in:
                raise ValueError (f"{task} is already active!")
        self.log.append ( f'{task},in,{utils.now(as_string=True)}')

    def add_checkout ( self, task ):
        is_in = self.verify_checkin ( task )
        if not is_in:
            raise ValueError (f"Task {task} is not active!")
        self.log.append ( f'{task},out,{utils.now(as_string=True)}')
        
        
