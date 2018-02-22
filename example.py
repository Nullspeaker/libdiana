#!/usr/bin/python3
import diana
import diana.tracking

import pprint
pp = pprint.PrettyPrinter(indent=2)

tx, rx = diana.connect('172.16.104.171') # or whatever IP, this is my local server
tx(diana.packet.SetShipPacket(1)) # Select Ship 1

for console in diana.packet.Console: # select a bunch of consoles
    if console.value not in (1,2,3,4,5): continue
    tx(diana.packet.SetConsolePacket(console,True))
    # 1-5: helm,weapons,engineering,science,comms

tx(diana.packet.ReadyPacket())
tracker = diana.tracking.Tracker()

class ScienceAI:
    def update_scans():
        pass
    def reset():
        pass


while True:
    for packet in rx: # stream packets from the server
        tracker.rx(packet) # Update the tracker with new information
        #pp.pprint(tracker.objects)
        pp.pprint(tracker.player_ship)
