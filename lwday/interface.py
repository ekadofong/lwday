import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from . import logger,utils

formats = {'seconds':1., 'minutes':60., 'hours':3600., 'days':86400.0}

def plot_timeline ( log, ax=None ):
    if ax is None:
        ax = plt.subplot (111)
        
    log.save_logs ()
    df = pd.read_csv ( log.logfile, 
                       names='taskname status time'.split() )

    tasks = df.groupby('taskname' )
    colors = np.linspace(0.,1., tasks.ngroups )
    cm = plt.cm.viridis
    for idx,key in enumerate(log.tlog.index):

        grp = tasks.get_group ( key )

        assert grp.iloc[0]['status'] == 'in'
        for j in np.arange(0, grp.shape[0],2):
            times = [ utils.string_to_dt ( x ) for x in grp.iloc[j:j+2]['time'] ]
            ax.plot ( times,
                      [idx,idx], color=cm(colors[idx]), lw=3, zorder=0 )
            ax.scatter ( times[0],
                         idx, marker='>', color=cm(colors[idx]), s=100)
            ax.scatter ( times[1],
                         idx, marker='<', color=cm(colors[idx]), s=100)

    ax.set_yticks ( np.arange(log.tlog.shape[0]) )
    ax.set_yticklabels ( log.tlog.index )
    plt.gcf().autofmt_xdate()
    #ax.set_xticks ( ax.get_xticks()[::3] )
    return ax

def plot_totalelapsed ( log, ax=None, fmt='minutes' ):    
    if ax is None:
        ax = plt.subplot (111)

    divisor = formats[fmt] 

    colors = plt.cm.viridis ( np.linspace(0.,1., log.tlog.shape[0] ) )
    ax.bar ( log.tlog.index, log.tlog.elapsed / 60., color=colors )

    ax.set_ylabel ( f'total time elapsed ({fmt})' )
