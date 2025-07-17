from Scripts.vcs import vCube
from Scripts.hexon import run_hexon
from Scripts.clock import run_clock

import threading as th

def ext(d_query, query):
    if 'cube' in d_query:
        th.Thread(target=vCube).start()
        return 'Virtual Cube Simulater'
    
    elif 'calc' in query or 'hexon' in d_query:
        th.Thread(target=run_hexon).start()
        return 'Calculator Hexon'

    elif 'clock' in d_query:
        th.Thread(target=run_clock).start()
        return 'The Clock'
    
    else:
        raise Exception
