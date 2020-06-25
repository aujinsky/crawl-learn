import parse
import re
import crawl_const
from crawl_const import SCR_ROW, SCR_COL, SCR_MSG
from crawl_info import PlayerInfo, MapInfo
from learn2crawl import Learn2Crawl
class CrawlParser:
    def __init__(self, crawl_fd, mapinfo, player, screen, stream):
        self.crawl_fd = crawl_fd
        self.player = player
        self.screen = screen
        self.stream = stream
        self.mapinfo = mapinfo
    def parse_mainscr(self):
        self.hp_str = self.screen.display[2][45:53]
        self.mp_str = self.screen.display[3][45:53]
        self.player.ac = int(self.screen.display[4][41:43])
        self.player.ev = int(self.screen.display[5][41:43])
        self.player.sh = int(self.screen.display[6][41:43])
        self.player.str = int(self.screen.display[4][60:62])
        self.player.int = int(self.screen.display[5][60:62])
        self.player.dex = int(self.screen.display[6][60:62])
        place_pattern = "[A-Za-z]+(?::[0-9]){0,1}[0-9]{0,1}"
        place = re.findall(place_pattern, self.screen.display[7][61:80])[0]
        place_pattern2 = "[A-za-z]+"
        floor_pattern = "[0-9]{1,2}"
        self.player.place = crawl_const.PLACE[re.findall(place_pattern2, self.screen.display[7][61:80])[0].lower()]
        floor = re.findall(floor_pattern, place)
        if(floor == None):
            self.player.floor = 1
        else:
            self.player.floor = floor[0]
        self.hp_list = self.hp_str.strip().split('/') 
        self.mp_list = self.mp_str.strip().split('/')
        self.player.chp = int(self.hp_list[0])
        self.player.hp = int(self.hp_list[1])
        self.player.cmp = int(self.mp_list[0])
        self.player.mp = int(self.mp_list[1])
        log_info = self.parse_mainlog()
        return log_info
        # self.player.print_info()
    def parse_levelmap(self):
        first_line = self.screen_display[0]
        coord_pattern = "\(\d+, \d+\)"
        chk = 0
        for coord in re.findall(coord_pattern, first_line):
            chk = chk + 1
            x_pattern = "\((\d+), \d+\)"
            y_pattern = "\(\d+, (\d+)\)"
            print(re.findall(x_pattern, first_line), re.findall(y_pattern, first_line))
        assert(chk == 1)
        return [x_pattern, y_pattern]
    def parse_mainlog(self):
        # mainlog is captured only when mainscr* or mainscr--more--
        # however, this function is called when it is not that case

        # we ensure that
        is_mainscr_st = ((self.screen.display)[crawl_const.SCR_ROW-1][0:4] == "CTRL")
        is_mainscr_more = ((self.screen.display)[crawl_const.SCR_ROW-1][0:8] == "--more--")
        last_line = 0
        for i in range(SCR_MSG,SCR_ROW):
            if self.screen.display[i] == ' '*SCR_COL:
                last_line = i
                break
        last_line = last_line - 1
        #print(*self.screen.display, sep='\n')
        print(self.screen.display[last_line])
            
        nearby_pattern = "[a-zA-Z\s]+nearby!"
        chk = 0
        nearby = bool(re.search(nearby_pattern, self.screen.display[last_line]))
        explore_done_pattern = "Done exploring"
        explore_done = bool(re.search(explore_done_pattern, self.screen.display[last_line]))
        return [nearby, explore_done, is_mainscr_st, is_mainscr_more]

    def parse_visible(self):
        if "Monster" in self.screen.display[1]:
            mon_visible = True
        else:
            mon_visible = False
        return [mon_visible]
    def parse_mon_data_h(self):
        # this is only executed once
        # make mob_index and mob_info from mon-data.h
        # formatted by name
        with open("mon-data.h", 'r') as f: # mon-data.h should be preprocessed
            mon_data = f.readlines()
            iter_line = 0
            mon_no = 0
            f_ln = len(mon_data)
            while iter_line < f_ln:
                if mon_data[iter_line] == "{\n":
                    start_line = iter_line
                    # we should concat data inside to a single string in order to use regex
                    iter_line = iter_line + 1
                    while mon_data[iter_line] != "},\n":
                        iter_line = iter_line + 1
                    end_line = iter_line
                    mon_entity = ' '.join(mon_data[start_line:end_line + 1])
                    mon_entity = mon_entity.replace("\n", "")
                    naming_pattern = "MONS_\w+,\s\'[a-zA-Z0-9;@(&{*]\',\s\w+,\s\"[a-zA-Z\s-]+\""
                    name_entity = re.findall(naming_pattern, mon_entity)[0]
                    naming_pattern2 = "\"[a-zA-Z\s-]+\""
                    mob_name = re.findall(naming_pattern2, name_entity)[0][1:-1]
                    print(mob_name)
                    mr_pattern = "MR_(?:VUL|RES|NO)_\w+"
                    for mr in re.findall(mr_pattern, mon_entity):
                        print(mr)
                    mrd_pattern = "mrd\(MR_RES_\w+(?: \| MR_RES_\w+)*, \d\)"
                    for mrd in re.findall(mrd_pattern, mon_entity):
                        print(mrd)
                        for mrdlvl in re.findall("\d", mrd):
                            mob_mrdlvl = int(mrdlvl)
                            print(mob_mrdlvl)
                        for mr in re.findall(mr_pattern, mrd):
                            print(mr)
                    mag_pattern = "\d+,\s+MONS_\w+,\s+MONS_\w+,\s+MH_\w+(?:\s+\| MH\w+)*,\s+(-{0,1}\d+|MAG_IMMUNE),"
                    chk = 0
                    for mag in re.findall(mag_pattern, mon_entity):
                        chk = chk + 1
                        if mag == "MAG_IMMUNE":
                            mob_mr = 400
                        else:
                            mob_mr = int(mag)
                        print(mob_mr)
                    assert(chk == 1)
                    atk_pattern = "\{ (?:(?:AT_NO_ATK|\{AT_\w+, AF_\w+, \d+\s{0,1}\}),\s+){3}(?:AT_NO_ATK|\{AT_\w+, AF_\w+, \d+\s{0,1}\}) \},"
                    chk = 0
                    for attack in re.findall(atk_pattern, mon_entity):
                        chk = chk + 1
                        print(attack)
                    assert(chk == 1)
                    atkent_pattern = "(?:AT_NO_ATK|\{AT_\w+, AF_\w+, \d+\s{0,1}\})"
                    chk = 0
                    for atkent in re.findall(atkent_pattern, attack):
                        chk = chk + 1
                        if(atkent == "AT_NO_ATK"):
                            print(atkent)
                        else:
                            print(atkent.split()[0][1:-1], atkent.split()[1][0:-1], atkent.split()[2][0:-1])
                    assert(chk == 4)
                    # this pattern occurs twice
                    # the first one is hd and hp
                    hdhp_pattern = "\d+, \d+,"
                    hdhp = re.search(hdhp_pattern, mon_entity)
                    mob_hd = hdhp[0].split()[0][:-1]
                    mob_hp = hdhp[0].split()[1][:-1]
                    print(mob_hd, mob_hp)
                    acevspl_pattern = "\d+, \d+, [A-Za-z_]+, [A-Za-z_]+(?: /\*\w+\*/)*, [A-Za-z_]+2{0,1},"
                    chk = 0
                    for acevsplent in re.findall(acevspl_pattern, mon_entity):
                        chk = chk + 1
                        acevspl = acevsplent.split()
                        mob_ac = int(acevspl[0][:-1])
                        mob_ev = int(acevspl[1][:-1])
                        mob_spl = acevspl[2][:-1]
                        print(mob_ac, mob_ev, mob_spl)
                    assert(chk == 1)
                    # this pattern occurs only once
                    spd_pattern = "\w+, \w+, \d+, (?:\w+|\{\d+, \d+, \d+, \d+, \d+, \d+, \d+, \d+\})"  # energy might contain brackets
                    chk = 0
                    for spdent in re.findall(spd_pattern, mon_entity):
                        chk = chk + 1
                        # energy is pretty important, but we ignore it
                        mob_spd = int(spdent.split()[2][:-1])
                        print(mob_spd)
                    assert(chk == 1)
                    # override mr_pattern with mrd_pattern if mrd exists
                    iter_line = iter_line + 1
                        
                else:
                    iter_line = iter_line + 1
    def parse_mon_spell():
        # parse mob spell set from x-v
        # screen state should be in x-v
        spl_pattern = "[a-z] - [a-zA-Z']\s+(?:\(\d{1,3}%\)){0,1}"
        for xvline in self.screen.display():
            for spl in re.findall(spl_pattern, xvline):
                print(spl)
                
            
#        with open("mon-spell.h", 'r') as f: # mon-data.h should be preprocessed
#            mon_data = f.readlines()
#            iter_line = 0
#            f_ln = len(mon_data)
#            while iter_line < f_ln:
#                mst_pattern = "\s+P\s+MST_(\w+)"
#                chk = 0
#                for mstent in re.findall(mst_pattern, mon_data[iter_line]):
#                    mstname = mstent
#                    chk = chk + 1
#                if chk == 1:
#                    start_line = iter_line
#                    iter_line = iter_line + 1
#                    while "    },\n" not in mon_data[iter_line]:
#                        iter_line = iter_line + 1
#                    end_line = iter_line
#                    spl_entity = ' '.join(mon_data[start_line:end_line + 1])
#                    spl_entity = mon_entity.replace("\n", "")
#                    spl_pattern = "'{\s{0,1}SPELL_\w+,\s\d{1,3},\sMON_SPELL_\w+\s{0,1}\},"
#                    chk2 = 0
#                    splname_pattern = "SPELL_(\w+),"
#                    for splent in re.findall(splname_pattern, spl_entity):
#                        chk2 = chk2 + 1
#                        
#                    assert(chk2 == 1)
#
#                else:
#                    iter_line = iter_line + 1

#    def parse_mon_spell_h():



#    def parse_mob_info():
#        if mob.json
#
#    def parse_mob_info():
#        mob_info = {}
#        parse_iter = 0
#        # mob name is always on first line
#        # don't need to erase article since ctrl-x does contains article
#        # just make it lowercase
#        # erase full stop
#        line_split = self.screen.display[parse_iter].split()
#        if line_split[0] == "A" or line_split[0] == "An" or line_split[0] == "The":
#            line_split[0] = line_split[0].lower()
#        if line_split[-1][-1:] == ".":
#            line_split[-1] = line_split[-1][:-1]
#        mob_name = ' '.join(line_split)
#        mob_info[mob_name] = []
#        # next line is a guaranteed blank
#        parse_iter = parse_iter + 2
#        while 1:
#            line_split = self.screen.display[parse_iter].split()
#            if line_split[0] =="MAX" and line_split[1] == "HP:"
#                mob_hp = int(line_split[3])
#                parse_iter = parse_iter + 1
#                break
#            else:
#                parse_iter = parse_iter + 1
#        mob_ac = parse_acevmr(self.screen.display[parse_iter])
#        parse_iter = parse_iter + 1
#        mob_ev = parse_acevmr(self.screen.display[parse_iter])
#        parse_iter = parse_iter + 1
#        mob_mr = parse_acevmr(self.screen.display[parse_iter])
#
#        mob_ev = line_split[1]
#        parse_iter = parse_iter + 1
#
        # return dict so that it can be json.dumped in crawl_info
#        return mob_info
#    def parse_acevmr(line_split):
     ## if ev is 0 than it doesn't become 3 word
#     if len(line_split) == 3:
#         return len(line_split[1])
#     elif len(line_split) == 2:
#         return len(line_split[1])
#     elif len(line_split) == 1:
#            return 0


