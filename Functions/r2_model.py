import numpy as np
def r2_Model(RawSignal,ModelSignal):
    Signal_mean=np.mean(RawSignal)
    SS_tot=np.sum((RawSignal-Signal_mean)**2)
    SS_res=np.sum((ModelSignal-RawSignal)**2)
    r2=1-SS_res/SS_tot
    return r2
