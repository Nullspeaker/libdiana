#!/usr/bin/python3
import diana
import diana.tracking

import pprint
pp = pprint.PrettyPrinter(indent=2)

# 172.16.104.171
tx, rx = diana.connect('127.0.0.1') # or whatever IP
tx(diana.packet.SetShipPacket(1)) # Select Ship by #, Artemis = 1, etc..

for console in diana.packet.Console: # select a bunch of consoles
    if console.value not in (3,4,5): continue
    # 3,4,5 = eng, sci, comms
    tx(diana.packet.SetConsolePacket(console,True))
    # 1-5: helm,weapons,engineering,science,comms

tx(diana.packet.ReadyPacket())
tracker = diana.tracking.Tracker()

class ScienceAI:
    def __init__(self,tx,rx,tracker):
        self._tx = tx
        self._rx = rx
        self._tracker = tracker

        self.scannable = [5,8,15] # other_ship, anomaly, creature
        self.known_objects = {}

    def try_scan(self,obj_id):
        self._tx(
            diana.packet.SciScanPacket(obj_id)
            )

    def is_scanning(self):
        try: return (self._tracker.player_ship['scanning-id'] not in (0,None))
        except KeyError:
            return False

    def tracker_callback(self,oid):
        try:
            if self._tracker.player_ship['object'] == oid:
                self.update() # update if player_ship updated, else give up
        except KeyError: # if we cant find player_ship yet, just ignore
            pass

    def update(self):
        # update list of known objects
        for _,obj in self._tracker.objects.items():
            try:
                assert type(obj['type']) is diana.enumerations.ObjectType
            except KeyError:
                raise Exception("Bad obj['type'] on object \""+repr(obj)+"\"")
            
            if obj['type'].value in self.scannable:
                obj_id = obj['object']
                if obj_id not in self.known_objects.keys():
                    self.known_objects[obj_id] = {
                        "scan-level":0, # not seen =?=> not scanned?
                        #"distance":None # calculate on demand
                        }
                else:
                    try:
                        self.known_objects[obj_id]['scan-level'] = self._tracker.objects[obj_id]['scan-level?']
                    except:
                        pass

        # print list of known objects
        if len(self.known_objects.keys()) > 0:
            print("ScienceAI update:")
            #print("\t%d objects known"%len(self.known_objects.keys()))
            print("\t ObjID\t Info")
            for k,v in self.known_objects.items():
                print("\t",k,"\t",v)
            print("\tSCANNING_STATE:\t",self.is_scanning())
            if(self.is_scanning()):
                print("\tSCANNING_PROGRESS:\t",
                      "%d"%(100*(self._tracker.player_ship['scanning-progress']),) + "%"
                )
        else:
            return # nothing to do anyway

        # if not scanning, scan!
        if not self.is_scanning():
            unscanned = [oid for oid in self.known_objects.keys()
                         if self.known_objects[oid]['scan-level'] < 1]
            if not len(unscanned): # no more to scan left = just stop
                return
            self.try_scan(unscanned[0])


if __name__ == "__main__":
    SciAI = ScienceAI(tx,rx,tracker) # instantiate science AI instance
    tracker.bind_to_updates(SciAI.tracker_callback) # call this func on obj updates
    while True:
        for packet in rx: # stream packets from the server
            tracker.rx(packet) # Update the tracker with new information
            #pp.pprint(tracker.objects)
            #for k,v in tracker.player_ship.items():
            #    if k in ["science-target","scanning-id","scanning-progress"]:
            #        print(k,v)


