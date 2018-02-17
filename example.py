import diana
import diana.tracking
import pprint
import random

pp = pprint.PrettyPrinter(indent=4)

tx, rx = diana.connect('127.0.0.1') # or whatever IP
tx(diana.packet.SetShipPacket(0)) # Select Ship 0 (Artemis)
tx(diana.packet.SetConsolePacket(diana.packet.Console.data, True))
tx(diana.packet.ReadyPacket())
tracker = diana.tracking.Tracker()
while True:
    for packet in rx: # stream packets from the server
        tracker.rx(packet) # Update the tracker with new information
        #print(packet)
        #pp.pprint(tracker.objects)
        if (random.random() > 0.99):
            pp.pprint(tracker.player_ship)
