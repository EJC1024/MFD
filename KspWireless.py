import krpc
import Globals
import threading
import queue

print("Running Wireless")

conn = krpc.connect(
    name = 'PiMFD',
    address = '192.168.1.38',
    rpc_port = 50000, stream_port = 50001
)

data_queue = queue.Queue
print(conn.krpc.get_status())

def begin_wireless():

    navball = Globals.screen_select[1].navball
    while(True):
    
        vessel = conn.space_center.active_vessel
        flight = vessel.flight()
        refframe = vessel.orbit.body.reference_frame
    
        
        print("Alt: ")
        print(flight.mean_altitude)
        print("Speed:" )
        print(flight.speed(refframe))