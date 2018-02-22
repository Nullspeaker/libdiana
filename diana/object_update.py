import math
from .encoding import decode as unpack
from .enumerations import *

def unscramble_elites(field):
    return {ability for ability in EliteAbility
              if ability.value & field}

Object_Properties = {
        ObjectType.anomaly : {
            "1.1" : ('x','f'),
            "1.2" : ('y','f'),
            "1.3" : ('z','f'),
            "1.4" : ('upgrade','int')
            },
        ObjectType.base : {
            "1.1" : ('name','u'),
            "1.2" : ('shields','f'),
            "1.3" : ('aft-shields','f'),
            "1.4" : ('index','I'),
            "1.5" : ('vessel-type','I'),
            "1.6" : ('x','f'),
            "1.7" : ('y','f'),
            "1.8" : ('z','f'),

            "2.1" : ('unknown-1','I'),
            "2.2" : ('unknown-2','I'),
            "2.3" : ('unknown-3','I'),
            "2.4" : ('unknown-4','I'),
            "2.5" : ('unknown-5','B'),
            "2.6" : ('unknown-6','B')
            },
        ObjectType.creature : {
            "1.1" : ('x','f'),
            "1.2" : ('y','f'),
            "1.3" : ('z','f'),
            "1.4" : ('name','u'),
            "1.5" : ('heading','f'),
            "1.6" : ('pitch','f'),
            "1.7" : ('roll','f'),
            "1.8" : ('creature-type','I'),

            "2.1" : ('unknown-1','I'),
            "2.2" : ('unknown-2','I'),
            "2.3" : ('unknown-3','I'),
            "2.4" : ('unknown-4','I'),
            "2.5" : ('unknown-5','I'),
            "2.6" : ('unknown-6','I')
            },
        ObjectType.drone : {
            "1.1" : ('unknown-1','I'),
            "1.2" : ('x','f'),
            "1.3" : ('pitch/yaw?','f'), # seen from -0.01 to 53.7
            "1.4" : ('z','f'),
            "1.5" : ('pitch/yaw?-2','f'),
            "1.6" : ('y','f'),
            "1.7" : ('heading','f'),
            "1.8" : ('unknown-2','I'),

            "2.1" : ('unknown-3','I'),
            "2.2" : ('unknown-4','f')
            },
        ObjectType.engineering_console : {
            "1.1" : ('beams-heat','f'), # heat levels (f*)
            "1.2" : ('torps-heat','f'),
            "1.3" : ('sensors-heat','f'),
            "1.4" : ('maneuvering-heat','f'),
            "1.5" : ('impulse-heat','f'),
            "1.6" : ('warp-heat','f'),
            "1.7" : ('shields-heat','f'),
            "1.8" : ('aft-shields-heat','f'),

            "2.1" : ('beams-energy','f'), # energy levels (f*)
            "2.2" : ('torps-energy','f'),
            "2.3" : ('sensors-energy','f'),
            "2.4" : ('maneuvering-energy','f'),
            "2.5" : ('impulse-energy','f'),
            "2.6" : ('warp-energy','f'),
            "2.7" : ('shields-energy','f'),
            "2.8" : ('aft-shields-energy','f'),

            "3.1" : ('beams-coolant','B'), # coolant levels (b*)
            "3.2" : ('torps-coolant','B'),
            "3.3" : ('sensors-coolant','B'),
            "3.4" : ('maneuvering-coolant','B'),
            "3.5" : ('impulse-coolant','B'),
            "3.6" : ('warp-coolant','B'),
            "3.7" : ('shields-coolant','B'),
            "3.8" : ('aft-shields-coolant','B')
            },
        ObjectType.mesh : { # generic mesh
            "1.1" : ('x','f'),
            "1.2" : ('y','f'),
            "1.3" : ('z','f'),
            "1.4" : ('unk-1','I'),
            "1.5" : ('unk-2','I'),
            "1.6" : ('unk-3','II'), # long
            "1.7" : ('unk-4','I'),
            "1.8" : ('unk-5','I'),

            "2.1" : ('unk-6','I'),
            "2.2" : ('unk-7','II'), # long
            "2.3" : ('name','u'),
            "2.4" : ('meshtexture','I'), # meshfile and/or texturefile... i guess.
            #2.5 unused
            "2.6" : ('unk-8','I'),
            "2.7" : ('unk-9','S'),
            "2.8" : ('unk-a','B'),

            "3.1" : ('red','f'),
            "3.2" : ('green','f'),
            "3.3" : ('blue','f'),
            "3.4" : ('fore-shields','f'),
            "3.5" : ('aft-shields','f'),
            #... more unknown

            "4.1" : ('unk-b','I'),
            "4.2" : ('unk-c','I')
            },
        ObjectType.nebula : {
            "1.1" : ('x','f'),
            "1.2" : ('y','f'),
            "1.3" : ('z','f'),
            "1.4" : ('red','f'),
            "1.5" : ('green','f'),
            "1.6" : ('blau','f'),
            "1.7" : ('unused?-1','I'),
            "1.8" : ('unused?-2','I')
            },
        ObjectType.other_ship : { # NPC ship
            "1.1" : ('name',            'u'), # im too indecisive to pick whether
            "1.2" : ('throttle',        'f'), # i want any tab-alignment on this
            "1.3" : ('rudder',          'f'), # at all, or where when i do
            "1.4" : ('max-impulse',     'f'),
            "1.5" : ('max-turn-rate',   'f'), # NONE OF IT LOOKS RIGHT
            "1.6" : ('enemy?',          'I'),
            "1.7" : ('vessel-type',     'I'),
            "1.8" : ('x',       'f'),

            "2.1" : ('y',       'f'), # i dont know why im even working on this library
            "2.2" : ('z',       'f'), # in the first place
            "2.3" : ('pitch',   'f'),
            "2.4" : ('roll',    'f'),
            "2.5" : ('yaw',     'f'), # i should be studying
            "2.6" : ('heading', 'f'),
            "2.7" : ('velocity','f'),
            "2.8" : ('surrendered','B'), # why are so many of these fields being sent

            "3.1" : ('forward-shields','f'), 
            "3.2" : ('forward-shields-max','f'),
            "3.3" : ('aft-shields','f'),
            "3.4" : ('aft-shields-max','f'),
            "3.5" : ('unknown-1','S'),
            "3.6" : ('fleet-number','B'),
            "3.7" : ('special-abilities','I'),
            "3.8" : ('special-abilities-active','I'),

            "4.1" : ('scan-level?','I'),
            "4.2" : ('side?','I'),
            "4.3" : ('unknown-2','I'),
            "4.4" : ('unknown-3','B'),
            "4.5" : ('unknown-4','B'),
            "4.6" : ('unknown-5','B'),
            "4.7" : ('unknown-6','B'),
            "4.8" : ('unknown-7','f'),

            "5.1" : ('unknown-8','I'),
            "5.2" : ('unknown-9','I'),
            "5.3" : ('sys-beams-damage','f'), # system damage
            "5.4" : ('sys-torps-damage','f'),
            "5.5" : ('sys-sensors-damage','f'),
            "5.6" : ('sys-maneuvering-damage','f'),
            "5.7" : ('sys-impulse-damage','f'),
            "5.8" : ('sys-warp-damage','f'),

            "6.1" : ('sys-fore-shields-damage','f'),
            "6.2" : ('sys-aft-shields-damage','f'),
            "6.3" : ('freq-a-resistance','f'), # beam freq resistances
            "6.4" : ('freq-b-resistance','f'),
            "6.5" : ('freq-c-resistance','f'),
            "6.6" : ('freq-d-resistance','f'),
            "6.7" : ('freq-e-resistance','f')
            },
        ObjectType.player_vessel : {
            "1.1" : ('weapons-target','I'),
            "1.2" : ('impulse','f'),
            "1.3" : ('rudder','f'),
            "1.4" : ('top-speed','f'),
            "1.5" : ('turn-rate','f'),
            "1.6" : ('auto-beams','B'),
            "1.7" : ('warp-factor','B'),
            "1.8" : ('energy-reserves','f'),

            "2.1" : ('shields-up/down','S'),
            "2.2" : ('unknown-1','I'),
            "2.3" : ('ship-type?','I'),
            "2.4" : ('x','f'),
            "2.5" : ('y','f'),
            "2.6" : ('z','f'),
            "2.7" : ('pitch','f'),
            "2.8" : ('roll','f'),

            "3.1" : ('heading','f'),
            "3.2" : ('velocity','f'),
            "3.3" : ('in-a-nebula','S'),
            "3.4" : ('ship-name','u'),
            "3.5" : ('forward-shields','f'),
            "3.6" : ('forward-shields-max','f'),
            "3.7" : ('aft-shields','f'),
            "3.8" : ('aft-shields-max','f'),

            "4.1" : ('last-docked-base','I'),
            "4.2" : ('alert-status','B'),
            "4.3" : ('unknown-2','f'),
            "4.4" : ('main-screen-view','B'),
            "4.5" : ('beam-frequency','B'),
            "4.6" : ('available-coolant-or-missiles','B'),
            "4.7" : ('science-target','I'),
            "4.8" : ('captain-target','I'),

            "5.1" : ('drive-type','B'),
            "5.2" : ('scanning-id','I'),
            "5.3" : ('scanning-progress','f'),
            "5.4" : ('reverse','B'),
            "5.5" : ('unknown-3','f'), # 0.0 - 1.0 observed
            "5.6" : ('unknown-4','B'), # 0x02 observed
            "5.7" : ('visibility?','I'), # 0, 1 observed
            "5.8" : ('ship-index?','B'),

            "6.1" : ('capital-ship-object-id','I'),
            "6.2" : ('accent-color','f'), # colour >:l
            "6.3" : ('unknown-5','I'),
            "6.4" : ('beacon-creature-type','I'),
            "6.5" : ('beacon-mode','B')
            },
        #ObjectType.player_ship_upgrade : {
        #    },
        ObjectType.torpedo : {
            "1.1" : ('x','f'),
            "1.2" : ('y','f'),
            "1.3" : ('z','f'),
            "1.4" : ('delta-x','f'),
            "1.5" : ('delta-y','f'),
            "1.6" : ('delta-z','f'),
            "1.7" : ('unknown-1','I'),
            "1.8" : ('ordnance-type','I'),

            "2.1" : ('unknown-2','B'), # there's two bytes of bitfields...
            "2.2" : ('a','B'), # im lazy, these are unknown/unused fields
            "2.3" : ('aa','B'),
            "2.4" : ('aaa','B'),
            "2.5" : ('aaaa','B'),
            "2.6" : ('bbbb','B'),
            "2.7" : ('bbb','B'),
            "2.8" : ('bb','B')
            },
        ObjectType.weapons_console : {
            "1.1" : ('homing-count','B'),
            "1.2" : ('nuke-count','B'),
            "1.3" : ('mine-count','B'),
            "1.4" : ('emp-count','B'),
            "1.5" : ('pshock-count','B'),
            "1.6" : ('beacon-count','B'),
            "1.7" : ('probe-count','B'),
            "1.8" : ('tag-count','B'),

            "2.1" : ('tube-1-time','f'),
            "2.2" : ('tube-2-time','f'),
            "2.3" : ('tube-3-time','f'),
            "2.4" : ('tube-4-time','f'),
            "2.5" : ('tube-5-time','f'),
            "2.6" : ('tube-6-time','f'),
            "2.7" : ('tube-1-status','B'),
            "2.8" : ('tube-2-status','B'),

            "3.1" : ('tube-3-status','B'),
            "3.2" : ('tube-4-status','B'),
            "3.3" : ('tube-5-status','B'),
            "3.4" : ('tube-6-status','B'),
            "3.5" : ('tube-1-type','B'),
            "3.6" : ('tube-2-type','B'),
            "3.7" : ('tube-3-type','B'),
            "3.8" : ('tube-4-type','B'),

            "4.1" : ('tube-5-type','B'),
            "4.2" : ('tube-6-type','B')
            },
        ObjectType.asteroid : {
            "1.1" : ('x','f'),
            "1.2" : ('y','f'),
            "1.3" : ('z','f'),
            "1.4" : ('name','u'),
            }
        }
def itobf(x):
    prefix = math.floor(x/8) + 1
    suffix = (x%8) + 1
    return str(prefix)+'.'+str(suffix)

player_ship_upgrades_list = [ 'infusion_p_coils', 'hydrogen_ram', 'tauron_focusers',
        'carapaction_coils', 'polyphasic_capacitors', 'cetrocite_crystals', 'lateral_array',
        'ecm_starpulse', 'double_agent', 'wartime_production', 'infusion_p_coils_perm',
        'protonic_verniers', 'tauron_focusers_perm', 'regenerative_pau_grids',
        'veteran_damcon_teams', 'cetrocite_heatsinks', 'tachyon_scanners',
        'gridscan_overload', 'override_authorization', 'resupply_imperatives',
        'patrol_group', 'fast_supply', 'vanguard_refit_helm', 'vanguard_refit_weap',
        'vanguard_refit_comm', 'vanguard_refit_station', 'vanguard_refit_eng',
        'vanguard_refit_systems' ] # so many oh my g*sh

ply_shp_upgrd = {}
i=0
for field,ftype in (('active_','B'),('count_','B'),('time_','S')):
    for upgrade in player_ship_upgrades_list:
        ply_shp_upgrd[itobf(i)] = (field+upgrade,ftype)
        i+=1
# no way in hell i was writing that out one-by-one. 84 bitfields!
Object_Properties[ObjectType.player_ship_upgrade] = ply_shp_upgrd

Object_Properties[ObjectType.mine] = Object_Properties[ObjectType.asteroid]
Object_Properties[ObjectType.blackhole] = Object_Properties[ObjectType.asteroid]

def decode_obj_update_packet(packet):
    entries = []
    while packet:
        update_type = packet[0]
        obj = {}
        if update_type == 0x00:
            break
        if ObjectType(update_type) in Object_Properties.keys():
            properties = Object_Properties[ObjectType(update_type)]
            fieldcount = max([int(fk.split('.')[0]) for fk in properties.keys()])
            unpacked = list(unpack('BIfbs*'.replace('fbs','B'*fieldcount),packet))
            # _id = unpacked[0]
            # oid = unpacked[1]
            # fields_k = unpacked[1+k]
            # packet = unpacked[2+fieldcount]
            obj['object']   = unpacked[1] # oid
            obj['type']     = ObjectType(update_type)
            for fdotb in properties:
                prop = properties[fdotb]
                f,b = [int(k) for k in fdotb.split(".")] # "byte.bit" -> (byte, bit)
                propname, proptype = prop
                if unpacked[1+f] & 2**(b-1): # field_f & (bit b)
                    value,pktremaining = unpack(
                            '%s*'%proptype, unpacked[2+fieldcount]
                            )
                    obj[propname] = value
                    unpacked[2+fieldcount] = pktremaining
            packet = unpacked[2+fieldcount]
        else:
            raise ValueError('Unknown object type {}'.format(update_type))
        entries.append(obj)
    return entries

    # From here-on is the old object_update code

    while packet:
        update_type = packet[0]
        obj = {}
        if update_type == 0x00: # end of ObjectUpdatePacket
            break
        elif update_type == ObjectType.player_vessel.value: # player ship
            _id, oid, fields_1, fields_2, fields_3, fields_4, fields_5, fields_6, packet = unpack('BIBBBBBB*', packet)
            obj['object'] = oid
            obj['type'] = ObjectType.player_vessel
            if fields_1 & 0x01:
                obj['tgt-weapons'], packet = unpack('I*', packet)
            if fields_1 & 0x02:
                obj['impulse'], packet = unpack('f*', packet)
            if fields_1 & 0x04:
                obj['rudder'], packet = unpack('f*', packet)
            if fields_1 & 0x08:
                obj['top-speed'], packet = unpack('f*', packet)
            if fields_1 & 0x10:
                obj['turn-rate'], packet = unpack('f*', packet)
            if fields_1 & 0x20:
                ab, packet = unpack('B*', packet)
                obj['auto-beams'] = bool(ab)
            if fields_1 & 0x40:
                obj['warp'], packet = unpack('B*', packet)
            if fields_1 & 0x80:
                obj['energy'], packet = unpack('f*', packet)
				
            if fields_2 & 0x01:
                obj['shields-state'], packet = unpack('S*', packet)
            if fields_2 & 0x02:
                packet = packet[4:] #now unknown
                #obj['index'], packet = unpack('I*', packet)
            if fields_2 & 0x04:
                obj['vtype'], packet = unpack('I*', packet)
            if fields_2 & 0x08:
                obj['x'], packet = unpack('f*', packet)
            if fields_2 & 0x10:
                obj['y'], packet = unpack('f*', packet)
            if fields_2 & 0x20:
                obj['z'], packet = unpack('f*', packet)
            if fields_2 & 0x40:
                obj['pitch'], packet = unpack('f*', packet)
            if fields_2 & 0x80:
                obj['roll'], packet = unpack('f*', packet)
				
            if fields_3 & 0x01:
                obj['heading'], packet = unpack('f*', packet)
            if fields_3 & 0x02:
                obj['speed'], packet = unpack('f*', packet)
            if fields_3 & 0x04:
                obj['in-a-nebula'], packet = unpack('S*', packet)
            if fields_3 & 0x08:
                obj['name'], packet = unpack('u*', packet)
            if fields_3 & 0x10:
                obj['shields'], packet = unpack('f*', packet)
            if fields_3 & 0x20:
                obj['shields-max'], packet = unpack('f*', packet)
            if fields_3 & 0x40:
                obj['shields-aft'], packet = unpack('f*', packet)
            if fields_3 & 0x80:
                obj['shields-aft-max'], packet = unpack('f*', packet)
				
            if fields_4 & 0x01:
                obj['docked'], packet = unpack('I*', packet)
            if fields_4 & 0x02:
                red_alert, packet = unpack('B*', packet)
                obj['red-alert'] = bool(red_alert)
            if fields_4 & 0x04:
                packet = packet[4:] # unknown
            if fields_4 & 0x08:
                ms, packet = unpack('B*', packet)
                obj['main-view'] = MainView(ms)
            if fields_4 & 0x10:
                obj['beam-frequency'], packet = unpack('B*', packet)
            if fields_4 & 0x20:
                obj['coolant-avail'], packet = unpack('B*', packet)
            if fields_4 & 0x40:
                obj['tgt-science'], packet = unpack('I*', packet)
            if fields_4 & 0x80:
                obj['tgt-captain'], packet = unpack('I*', packet)
				
            if fields_5 & 0x01:
                dt, packet = unpack('B*', packet)
                obj['drive-type'] = DriveType(dt)
            if fields_5 & 0x02:
                obj['tgt-scan'], packet = unpack('I*', packet)
            if fields_5 & 0x04:
                obj['scan-progress'], packet = unpack('f*', packet)
            if fields_5 & 0x08:
                rv, packet = unpack('B*', packet)
                obj['reverse'] = bool(rv)
            if fields_5 & 0x10:
                packet = packet[4:] # float
            if fields_5 & 0x20:
                packet = packet[1:]
            if fields_5 & 0x40:
                packet = packet[4:] # int
            if fields_5 & 0x80:
                obj['ship-index?'], packet = unpack('B*', packet)
				
            if fields_6 & 0x01:
                obj['capital-ship-obj-id'], packet = unpack('I*', packet)
            if fields_6 & 0x02:
                obj['accent-colour'], packet = unpack('f*', packet)
            if fields_6 & 0x04:
                packet = packet[4:] # unknown
            if fields_6 & 0x08:
                obj['beacon-creature-type'], packet = unpack('I*', packet)
            if fields_6 & 0x10:
                obj['beacon-mode'], packet = unpack('B*', packet)
            if fields_6 & 0x20:
                raise ValueError('Unknown data keys for player vessel')
            if fields_6 & 0x40:
                raise ValueError('Unknown data keys for player vessel')
            if fields_6 & 0x80:
                raise ValueError('Unknown data keys for player vessel')
        elif update_type == ObjectType.weapons_console.value: # weapons console
            _id, oid, fields_1, fields_2, fields_3, packet = unpack('BIBBB*', packet)
            obj['object'] = oid
            obj['type'] = ObjectType.weapons_console
            if fields_1 & 0x01: # TODO: use the enum here
                obj['store-missile'], packet = unpack('B*', packet)
            if fields_1 & 0x02:
                obj['store-nuke'], packet = unpack('B*', packet)
            if fields_1 & 0x04:
                obj['store-mine'], packet = unpack('B*', packet)
            if fields_1 & 0x08:
                obj['store-emp'], packet = unpack('B*', packet)
            if fields_1 & 0x10:
                packet = packet[1:]
            if fields_1 & 0x20:
                obj['load-time-0'], packet = unpack('f*', packet)
            if fields_1 & 0x40:
                obj['load-time-1'], packet = unpack('f*', packet)
            if fields_1 & 0x80:
                obj['load-time-2'], packet = unpack('f*', packet)
            if fields_2 & 0x01:
                obj['load-time-3'], packet = unpack('f*', packet)
            if fields_2 & 0x02:
                obj['load-time-4'], packet = unpack('f*', packet)
            if fields_2 & 0x04:
                obj['load-time-5'], packet = unpack('f*', packet)
            if fields_2 & 0x08:
                ts, packet = unpack('B*', packet)
                obj['status-0'] = TubeStatus(ts)
            if fields_2 & 0x10:
                ts, packet = unpack('B*', packet)
                obj['status-1'] = TubeStatus(ts)
            if fields_2 & 0x20:
                ts, packet = unpack('B*', packet)
                obj['status-2'] = TubeStatus(ts)
            if fields_2 & 0x40:
                ts, packet = unpack('B*', packet)
                obj['status-3'] = TubeStatus(ts)
            if fields_2 & 0x80:
                ts, packet = unpack('B*', packet)
                obj['status-4'] = TubeStatus(ts)
            if fields_3 & 0x01:
                ts, packet = unpack('B*', packet)
                obj['status-5'] = TubeStatus(ts)
            if fields_3 & 0x02:
                ot, packet = unpack('B*', packet)
                obj['contents-0'] = OrdnanceType(ot)
            if fields_3 & 0x04:
                ot, packet = unpack('B*', packet)
                obj['contents-1'] = OrdnanceType(ot)
            if fields_3 & 0x08:
                ot, packet = unpack('B*', packet)
                obj['contents-2'] = OrdnanceType(ot)
            if fields_3 & 0x10:
                ot, packet = unpack('B*', packet)
                obj['contents-3'] = OrdnanceType(ot)
            if fields_3 & 0x20:
                ot, packet = unpack('B*', packet)
                obj['contents-4'] = OrdnanceType(ot)
            if fields_3 & 0x40:
                ot, packet = unpack('B*', packet)
                obj['contents-5'] = OrdnanceType(ot)
            if fields_3 & 0x80:
                raise ValueError('Unknown fields for weapons console')
        elif update_type == ObjectType.engineering_console.value: # engineering console
            _id, oid, fields_heat, fields_enrg, fields_coolant, fields_unk, packet = unpack('BIBBBB*', packet)
            obj['object'] = oid
            obj['type'] = ObjectType.engineering_console
            if fields_unk:
                raise ValueError('Undecodable fields in engineering status')
            systems = (('beams', 0x01),
                       ('torps', 0x02),
                       ('sensors', 0x04),
                       ('maneuvering', 0x08),
                       ('impulse', 0x10),
                       ('warp', 0x20),
                       ('shields', 0x40),
                       ('shields-aft', 0x80))
            types = (('heat', fields_heat, 'f'),
                     ('energy', fields_enrg, 'f'),
                     ('coolant', fields_coolant, 'B'))
            for status, mask, fmt in types:
                for syst, flag in systems:
                    if fields_heat & flag:
                        obj['{}-{}'.format(status, syst)], packet = unpack(fmt + '*', packet)
        elif update_type == ObjectType.player_ship_upgrade.value: # player ship upgrades
            _id, oid, fields, packet = unpack('BIB*', packet)
            obj['object'] = oid
            obj['type'] = ObjectType.player_ship_upgrade
            if fields & 0x01:
                obj['x'], packet = unpack('f*', packet)
            if fields & 0x02:
                obj['y'], packet = unpack('f*', packet)
            if fields & 0x04:
                obj['z'], packet = unpack('f*', packet)
            if fields & 0x08:
                obj['upgrade'], packet = unpack('I*', packet)
            if fields & 0x10:
                packet = packet[4:]
            if fields & 0x20:
                packet = packet[4:]
            if fields & 0x40:
                packet = packet[4:]
            if fields & 0x80:
                packet = packet[4:]
        elif update_type == ObjectType.other_ship.value: # NPC ship
            _id, oid, fields_1, fields_2, fields_3, fields_4, fields_5, fields_6, packet = unpack('BIBBBBBB*', packet)
            obj['object'] = oid
            obj['type'] = ObjectType.other_ship
            if fields_1 & 0x01:
                obj['name'], packet = unpack('u*', packet)
            if fields_1 & 0x02:
                packet = packet[4:]
            if fields_1 & 0x04:
                obj['rudder'], packet = unpack('f*', packet)
            if fields_1 & 0x08:
                obj['max-impulse'], packet = unpack('f*', packet)
            if fields_1 & 0x10:
                obj['max-turn-rate'], packet = unpack('f*', packet)
            if fields_1 & 0x20:
                fef, packet = unpack('I*', packet)
                obj['iff-friendly'] = not bool(fef)
            if fields_1 & 0x40:
                obj['vtype'], packet = unpack('I*', packet)
            if fields_1 & 0x80:
                obj['x'], packet = unpack('f*', packet)
            if fields_2 & 0x01:
                obj['y'], packet = unpack('f*', packet)
            if fields_2 & 0x02:
                obj['z'], packet = unpack('f*', packet)
            if fields_2 & 0x04:
                obj['pitch'], packet = unpack('f*', packet)
            if fields_2 & 0x08:
                obj['roll'], packet = unpack('f*', packet)
            if fields_2 & 0x10:
                obj['heading'], packet = unpack('f*', packet)
            if fields_2 & 0x20:
                obj['speed'], packet = unpack('f*', packet)
            if fields_2 & 0x40:
                surr, packet = unpack('B*', packet)
                obj['surrender'] = bool(surr)
            if fields_2 & 0x80:
                packet = packet[2:]
            if fields_3 & 0x01:
                obj['shields'], packet = unpack('f*', packet)
            if fields_3 & 0x02:
                obj['shields-max'], packet = unpack('f*', packet)
            if fields_3 & 0x04:
                obj['shields-aft'], packet = unpack('f*', packet)
            if fields_3 & 0x08:
                obj['shields-aft-max'], packet = unpack('f*', packet)
            if fields_3 & 0x10:
                packet = packet[2:]
            if fields_3 & 0x20:
                packet = packet[1:]
            if fields_3 & 0x40:
                elt, packet = unpack('I*', packet)
                obj['elite'] = unscramble_elites(elt)
            if fields_3 & 0x80:
                elt, packet = unpack('I*', packet)
                obj['elite-active'] = unscramble_elites(elt)
            if fields_4 & 0x01:
                scn, packet = unpack('I*', packet)
                obj['scanned'] = bool(scn)
            if fields_4 & 0x02:
                obj['iff-side'], packet = unpack('I*', packet)
            if fields_4 & 0x04:
                packet = packet[4:]
            if fields_4 & 0x08:
                packet = packet[1:]
            if fields_4 & 0x10:
                packet = packet[1:]
            if fields_4 & 0x20:
                packet = packet[1:]
            if fields_4 & 0x40:
                packet = packet[1:]
            if fields_4 & 0x80:
                packet = packet[4:]
            if fields_5 & 0x01:
                packet = packet[4:]
            if fields_5 & 0x02:
                packet = packet[4:]
            if fields_5 & 0x04:
                obj['damage-beams'], packet = unpack('f*', packet)
            if fields_5 & 0x08:
                obj['damage-tubes'], packet = unpack('f*', packet)
            if fields_5 & 0x10:
                obj['damage-sensors'], packet = unpack('f*', packet)
            if fields_5 & 0x20:
                obj['damage-maneuvering'], packet = unpack('f*', packet)
            if fields_5 & 0x40:
                obj['damage-impulse'], packet = unpack('f*', packet)
            if fields_5 & 0x80:
                obj['damage-warp'], packet = unpack('f*', packet)
            if fields_6 & 0x01:
                obj['damage-shields'], packet = unpack('f*', packet)
            if fields_6 & 0x02:
                obj['damage-shields'], packet = unpack('f*', packet)
            if fields_6 & 0x04:
                obj['shields-0'], packet = unpack('f*', packet)
            if fields_6 & 0x08:
                obj['shields-1'], packet = unpack('f*', packet)
            if fields_6 & 0x10:
                obj['shields-2'], packet = unpack('f*', packet)
            if fields_6 & 0x20:
                obj['shields-3'], packet = unpack('f*', packet)
            if fields_6 & 0x40:
                obj['shields-4'], packet = unpack('f*', packet)
            if fields_6 & 0x80:
                raise ValueError('Unknown data key for NPC')
        elif update_type == ObjectType.base.value: # base
            _id, oid, fields_1, fields_2, packet = unpack('BIBB*', packet)
            obj['object'] = oid
            obj['type'] = ObjectType.base
            if fields_1 & 0x01:
                obj['name'], packet = unpack('u*', packet)
            if fields_1 & 0x02:
                obj['shields'], packet = unpack('f*', packet)
            if fields_1 & 0x04:
                obj['shields-aft'], packet = unpack('f*', packet)
            if fields_1 & 0x08:
                obj['index'], packet = unpack('I*', packet)
            if fields_1 & 0x10:
                obj['vtype'], packet = unpack('I*', packet)
            if fields_1 & 0x20:
                obj['x'], packet = unpack('f*', packet)
            if fields_1 & 0x40:
                obj['y'], packet = unpack('f*', packet)
            if fields_1 & 0x80:
                obj['z'], packet = unpack('f*', packet)
            if fields_2 & 0x01:
                packet = packet[4:]
            if fields_2 & 0x02:
                packet = packet[4:]
            if fields_2 & 0x04:
                packet = packet[4:]
            if fields_2 & 0x08:
                packet = packet[4:]
            if fields_2 & 0x10:
                packet = packet[1:]
            if fields_2 & 0x20:
                packet = packet[1:]
            if fields_2 & 0xc0:
                raise ValueError('Unknown data keys for base')
        elif update_type == ObjectType.mine.value: # mine
            _id, oid, fields, packet = unpack('BIB*', packet)
            obj['object'] = oid
            obj['type'] = ObjectType.mine
            if fields & 0x01:
                obj['x'], packet = unpack('f*', packet)
            if fields & 0x02:
                obj['y'], packet = unpack('f*', packet)
            if fields & 0x04:
                obj['z'], packet = unpack('f*', packet)
            if fields & 0x08:
                packet = packet[4:]
            if fields & 0x10:
                packet = packet[4:]
            if fields & 0x20:
                packet = packet[4:]
            if fields & 0x40:
                packet = packet[4:]
            if fields & 0x80:
                packet = packet[4:]
        elif update_type == ObjectType.anomaly.value: # anomaly
            _id, oid, fields, packet = unpack('BIB*', packet)
            obj['object'] = oid
            obj['type'] = ObjectType.anomaly
            if fields & 0x01:
                obj['x'], packet = unpack('f*', packet)
            if fields & 0x02:
                obj['y'], packet = unpack('f*', packet)
            if fields & 0x04:
                obj['z'], packet = unpack('f*', packet)
            if fields & 0x08:
                obj['upgrade'], packet = unpack('I*', packet)
            if fields & 0x10:
                packet = packet[4:]
            if fields & 0x20:
                packet = packet[4:]
            if fields & 0x40:
                packet = packet[4:]
            if fields & 0x80:
                packet = packet[4:]
        elif update_type == 0x09: # unused
            _id, oid, fields, packet = unpack('BIB*', packet)
            obj['object'] = oid
            obj['type'] = ObjectType.anomaly
            if fields & 0x01:
                obj['x'], packet = unpack('f*', packet)
            if fields & 0x02:
                obj['y'], packet = unpack('f*', packet)
            if fields & 0x04:
                obj['z'], packet = unpack('f*', packet)
            if fields & 0x08:
                obj['name'], packet = unpack('u*', packet)
            if fields & 0x10:
                packet = packet[4:]
            if fields & 0x20:
                packet = packet[4:]
            if fields & 0x40:
                packet = packet[4:]
            if fields & 0x80:
                packet = packet[4:]
        elif update_type == ObjectType.nebula.value: # nebula
            _id, oid, fields, packet = unpack('BIB*', packet)
            obj['object'] = oid
            obj['type'] = ObjectType.nebula
            if fields & 0x01:
                obj['x'], packet = unpack('f*', packet)
            if fields & 0x02:
                obj['y'], packet = unpack('f*', packet)
            if fields & 0x04:
                obj['z'], packet = unpack('f*', packet)
            if fields & 0x08:
                obj['red'], packet = unpack('f*', packet)
            if fields & 0x10:
                obj['green'], packet = unpack('f*', packet)
            if fields & 0x20:
                obj['blue'], packet = unpack('f*', packet)
            if fields & 0x40:
                packet = packet[4:]
            if fields & 0x80:
                packet = packet[4:]
        elif update_type == ObjectType.torpedo.value: # torpedo
            _id, oid, fields, packet = unpack('BIB*', packet)
            obj['object'] = oid
            obj['type'] = ObjectType.torpedo
            if fields & 0x01:
                obj['x'], packet = unpack('f*', packet)
            if fields & 0x02:
                obj['y'], packet = unpack('f*', packet)
            if fields & 0x04:
                obj['z'], packet = unpack('f*', packet)
            if fields & 0x08:
                packet = packet[4:]
            if fields & 0x10:
                packet = packet[4:]
            if fields & 0x20:
                packet = packet[4:]
            if fields & 0x40:
                packet = packet[4:]
            if fields & 0x80:
                packet = packet[4:]
        elif update_type == ObjectType.blackhole.value: # black hole
            _id, oid, fields, packet = unpack('BIB*', packet)
            obj['object'] = oid
            obj['type'] = ObjectType.blackhole
            if fields & 0x01:
                obj['x'], packet = unpack('f*', packet)
            if fields & 0x02:
                obj['y'], packet = unpack('f*', packet)
            if fields & 0x04:
                obj['z'], packet = unpack('f*', packet)
            if fields & 0x08:
                packet = packet[4:]
            if fields & 0x10:
                packet = packet[4:]
            if fields & 0x20:
                packet = packet[4:]
            if fields & 0x40:
                packet = packet[4:]
            if fields & 0x80:
                packet = packet[4:]
        elif update_type == ObjectType.asteroid.value: # asteroid
            _id, oid, fields, packet = unpack('BIB*', packet)
            obj['object'] = oid
            obj['type'] = ObjectType.asteroid
            if fields & 0x01:
                obj['x'], packet = unpack('f*', packet)
            if fields & 0x02:
                obj['y'], packet = unpack('f*', packet)
            if fields & 0x04:
                obj['z'], packet = unpack('f*', packet)
            if fields & 0x08:
                packet = packet[4:]
            if fields & 0x10:
                packet = packet[4:]
            if fields & 0x20:
                packet = packet[4:]
            if fields & 0x40:
                packet = packet[4:]
            if fields & 0x80:
                packet = packet[4:]
        elif update_type == ObjectType.mesh.value: # generic mesh
            _id, oid, fields, packet = unpack('BIB*', packet)
            obj['object'] = oid
            obj['type'] = ObjectType.mesh
            if fields & 0x01:
                obj['x'], packet = unpack('f*', packet)
            if fields & 0x02:
                obj['y'], packet = unpack('f*', packet)
            if fields & 0x04:
                obj['z'], packet = unpack('f*', packet)
            if fields & 0x08:
                packet = packet[4:]
            if fields & 0x10:
                packet = packet[4:]
            if fields & 0x20:
                packet = packet[4:]
            if fields & 0x40:
                packet = packet[4:]
            if fields & 0x80:
                packet = packet[4:]
        elif update_type == ObjectType.creature.value: # creature
            _id, oid, fields, packet = unpack('BIB*', packet)
            obj['object'] = oid
            obj['type'] = ObjectType.monster
            if fields & 0x01:
                obj['x'], packet = unpack('f*', packet)
            if fields & 0x02:
                obj['y'], packet = unpack('f*', packet)
            if fields & 0x04:
                obj['z'], packet = unpack('f*', packet)
            if fields & 0x08:
                obj['name'], packet = unpack('u*', packet)
            if fields & 0x10:
                packet = packet[4:]
            if fields & 0x20:
                packet = packet[4:]
            if fields & 0x40:
                packet = packet[4:]
            if fields & 0x80:
                packet = packet[4:]
        elif update_type == ObjectType.drone.value: # drone
            _id, oid, fields_1, fields_2, packet = unpack('BIBB*', packet)
            obj['object'] = oid
            obj['type'] = ObjectType.drone
            if fields_1 & 0x01:
                packet = packet[4:]
            if fields_1 & 0x02:
                obj['x'], packet = unpack('f*', packet)
            if fields_1 & 0x04:
                packet = packet[4:]
            if fields_1 & 0x08:
                obj['z'], packet = unpack('f*', packet)
            if fields_1 & 0x10:
                packet = packet[4:]
            if fields_1 & 0x20:
                obj['y'], packet = unpack('f*', packet)
            if fields_1 & 0x40:
                obj['heading'], packet = unpack('f*', packet)
            if fields_1 & 0x80:
                packet = packet[4:]
            if fields_2:
                raise ValueError('Unknown data keys for drone')
        else:
            raise ValueError('Unknown object type {}'.format(update_type))
        entries.append(obj)
    return entries

