import numpy as np
import pandas as pd
import altair as alt
import streamlit as st

import time
from random import randint
 	
from threading import Thread

class MyThread(Thread):
    def __init__(self, val):
        ''' Constructor. '''
 
        Thread.__init__(self)
        self.val = val
 
    def get_cache(self):
        return self.getName()

    def run(self):
        for i in range(1, self.val):
            print('Value %d in thread %s' % (i, self.getName()))
 
            # Sleep for random time between 1 ~ 3 second
            secondsToSleep = randint(1, 5)
            print('%s sleeping for %d seconds...' % (self.getName(), secondsToSleep))
            time.sleep(secondsToSleep)


@st.cache(hash_funcs={Thread: lambda _: None})
def get_thread():
    res = MyThread(10)
    res.setName('Thread 1')
    return res
 
thread = get_thread() 
thread.start()
 
thread.join()
st.write('Main Terminating...')