import os
import numpy as np
import pandas as pd
from . import utils


class Log (object):
    def __init__ ( self, logfile, timefile ):
        self.logfile = logfile
        self.timefile = timefile
        
        if not os.path.exists ( logfile ):
            self.log = []
        else:
            self.log = open(logfile, 'r').read().splitlines()

        if not os.path.exists ( timefile ):
            self.tlog = pd.DataFrame ( index=[],
                                       columns=['elapsed','completed'],
                                       )
            self.tlog['completed'] = False
        else:
            self.tlog = pd.read_csv(timefile, index_col=0)

    def save_logs ( self ):
        has_active = self.show_activetasks ()
        if len(has_active) > 0:
            raise Exception ( f'''Cannot close logs when tasks are active.
Active tasks: {','.join(has_active)}''' )
        self.tlog.to_csv ( self.timefile )
        open(self.logfile, 'w').writelines([ x+'\n' for x in self.log])

    def verify_checkin ( self, task, return_log=False ):
        is_task = np.array([task+',' in x for x in self.log])
        mre = np.arange(len(self.log))[is_task]
        if len(mre) == 0:
            raise ValueError (f"Task {task} was never started!")
        else:
            mre = mre[-1]
        if return_log:
            if ',in,' in self.log[mre]:
                return True, self.log[mre].split(',')[-1]
            elif ',out,' in self.log[mre]:
                return False, None
            else:
                raise ValueError (f"Invalid format in task {task}: {self.log[mre]}")

        else:
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
        is_in, s1 = self.verify_checkin ( task, return_log=True )
        s2 = utils.now ( as_string=True )
        if not is_in:
            raise ValueError (f"Task {task} is not active!")
        self.log.append ( f'{task},out,{utils.now(as_string=True)}')

        if task in self.tlog.index:
            etime = self.tlog.loc[task,'elapsed']
        else:
            etime = 0.
            self.tlog.loc[task,'completed'] = False
        new_elapsed = utils.get_timediff ( s1, s2 ).total_seconds()
        self.tlog.loc[task, 'elapsed'] = etime + new_elapsed
        
        
