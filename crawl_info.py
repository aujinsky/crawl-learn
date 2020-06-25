from crawl_const import PLACE, MobInfo 
import crawl_parse
import numpy
import json
import os.path

class PlayerInfo:
    def __init__(self):
        self.chp = -1
        self.hp = -1
        self.cmp = -1
        self.mp = -1
        self.ac = -1
        self.ev = -1
        self.sh = -1
        self.str = -1
        self.int = -1
        self.dex = -1
        self.xl = 1
        self.place = PLACE["outside"]
        self.floor = -1
    def print_info(self):
        print(self.chp,self.hp,self.cmp,self.mp,self.ac,self.ev,self.sh,self.str,self.int,self.dex,self.xl, self.place, self.floor)

class MapInfo:
    def __init__(self):
        self.LOS = numpy.zeros(shape=(15,15))
        self.down_stair_coord = {}
        for place in range(len(PLACE)):
            self.down_stair_coord[place] = {}   # contains place1: {floor1: [], floor2:[], ...}
    
class EnvInfo:
    def __init__(self):
        return
    # do nothing yet

class MobDex:
    def __init__(self):
        # read mob information from json file mobs_info.json
        # formatted by name: [ac, ev, sh, hp, mr, spd, attack1, count1, ego1, attack2, count2, ego2, attack3, count3, ego3, ability]
        if os.path.isfile("mob_dex.json"):
            with open("mob_dex.json",'r') as f:
                mob_dex = json.load(f)
            self.mob_index = mob_dex["mob_index"]
            self.mob_info = mob_dex["mob_info"]
        else:
            parse_mon_data_h()
            self.mob_index = {} 
            self.mob_info = numpy.zeros(shape=(1, MOB_INFO_SIZE))

    def mob_info(self, mob_name):
        mob_entity = self.mobs_info.get(mob_name)
        if self.mobs_info.get(mob_name) == None:
            # initiate ^X and parse_mob_info
            self.add_new_mob()
        else:
            return self.mobs_info.get(mobName)
    def add_new_mob(self):
        mob_info = crawl_parse.parse_mob_info()
        self.mobs_info[mob_info[0]] = mob_info[1:MOB_INFO_SIZE]
    def save(self):
        with open("mob_dex.json",'w') as f:
            json.dump(mob_dex, f)

class AbilitiesInfo:
    def __init__(self):
        # read ability informations from json file 
        with open("abilitiesInfo.csv", 'r') as f:
            # do no thing yet
            return
    def add_new_ability(self):
        # do nothing yet
        return
    def save(self):

        self.f
