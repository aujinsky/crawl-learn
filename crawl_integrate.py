# -*- coding: utf-8 -*-

from __future__ import print_function, unicode_literals

import os
import pty
import select
import signal
import sys
import time
import pyte

import crawl_const
import crawl_parse
import crawl_info
from crawl_const import key
class Learn2Crawl():
    def __init__(self, crawl_fd, mapinfo, parser, player, screen, stream):
        self.crawl_fd = crawl_fd
        self.stream = stream
        self.screen = screen
        self.player = player
        self.parser = parser
        self.mapinfo = mapinfo
        self.turn = 0
        self.inputkeys = 0
        self.debug = 0
    def check_mainscr(display):
        return 1
    def init():
    # make mob info matrix from mobs.txt
        return
    def more_solver(self):
        # (mainscr--more--) -> (main_scr) -> mainscr*
        # does main_scr* -> (main_scr*) really exists?
        # no since more_solver doesn't let "--more--" string live outside of it
        # this should also resolve death
        # os.read(self.crawl_fd, 10) # this doesn't work
        # empty read buffer
        print("more_solver1")
        print(*self.screen.display, sep='\n')
        print("@")
        os.write(self.crawl_fd, 'p'.encode())
        os.write(self.crawl_fd, ' '.encode())
        while 1:
            if "CTRL" in  (self.screen.display)[crawl_const.SCR_ROW-1][0:8]:
                # have no idea
                # why this CTRL appears
                # this function is called with empty read buffer

                break
            data2 = os.read(self.crawl_fd, 3200)
            self.stream.feed(data2)
        # os.read(self.crawl_fd, 3200) # empty read buffer here
        print("more_solver2")
        print(*self.screen.display, sep = "\n")
#        print("!")
        # if level up, increase (S)trength
        last_line = self.find_last_line()
        if "Increase (S)trength" in last_line:
            os.write(self.crawl_fd, 'S*'.encode())
#        elif "CTRL" in last_line:   # main_scr* -> (main_scr)
#            main_parse = self.parser.parse_mainscr()
        else:
            print("more_solver3")
            print(*self.screen.display, sep = "\n")
            os.write(self.crawl_fd, '*'.encode()) # to create dummy output from crawl
        while 1:
            print("&")
            if "CTRL" not in (self.screen.display)[crawl_const.SCR_ROW-1][0:4]:
                data = os.read(self.crawl_fd, 3200)
                self.stream.feed(data)
                print(data)
            else:
                break
        print(*self.screen.display, sep = "\n")
        data = os.read(self.crawl_fd, 3200)
        self.stream.feed(data)
        print(data)
        print(*self.screen.display, sep = "\n")
        # this prevents infinite wait of read because above statements exhausts read
        print("Turn: %d" % self.turn)
        self.player.print_info()
    def update_mainscr(self):
        # changes mainscr or mainscr--more-- to (mainscr*) by *
        # input should never be (mainscr--more--)
        # DOESN'T parses mainscr data, since mainscr is visited too many times
        # return to mainscr from (mainscr*) by *
        # print(*self.screen.display, sep = "\n")
        # print("ens")
        # print(self.screen.display[crawl_const.SCR_ROW-1][:8]) 
#        more = 0
#        if (self.screen.display)[crawl_const.SCR_ROW-1][0:8] == "--more--":
#            self.more_solver()
#            # os.write(self.crawl_fd, '\r'.encode())
#        else:
#            os.write(self.crawl_fd, '*'.encode()) # if "--more--" then no effect
        os.write(self.crawl_fd, '*'.encode())
        while 1:
            print("*")
            print((self.screen.display)[crawl_const.SCR_ROW-1].encode())
            data = os.read(self.crawl_fd, 3200)
            self.stream.feed(data)
            print(len(data))
            print((self.screen.display)[crawl_const.SCR_ROW-1].encode())
            if self.screen.display[crawl_const.SCR_ROW-1][0:4] == "CTRL":
                break
            if self.screen.display[crawl_const.SCR_ROW-1][0:8] == "--more--":
                # (main_scr--more--) or 
                # main_scr* which is from main_scr--more--
                self.more_solver()
                break
        main_parse = self.parser.parse_mainscr()
        print("O")
        print(*self.screen.display, sep = "\n")
        os.write(self.crawl_fd, '*'.encode()) # this adds "_Unknown command."
        # so this can be discarded
#        while(1):
#            data = os.read(crawl_fd, 3200)
#            stream.feed(data)
            # print((self.screen.display)[crawl_const.SCR_ROW-1].encode())
#            if "CTRL" not in (self.screen.display)[crawl_const.SCR_ROW-1]:
#                break
#        if more == 1:
#            print(*self.screen.display, sep = "\n")
        return main_parse
    def update_levelmap(self, target_symbol, target_str, action):
        # mainscr to Xscr by X  # ensure by (Press ? for help)  # also get coord
        # Xscr to entscr by target_symbol+'v'
        # this function is called when we take a stair to the next floor
        # and when finished cleaning the whole floor
        os.write(self.crawl_fd, 'X'.encode())
        if target_symbol == '>':
            target_list = self.mapinfo.down_stair_coord[self.player.place][self.player.floor]
        while 1:
            data = os.read(self.crawl_fd, 3200)
            stream.feed(data)
            if "\(Press ? for help\)" in self.screen.display[0]:
                [selfx, selfy] = self.parser.parse_levelmap() 
                break
        for i in range(10): # this is slow, however this function is called rarely
            os.write(self.crawl_fd, (target_symbol+'v').encode())
            while 1:
                data = os.read(self.crawl_fd, 3200)
                stream.feed(data)
                first_line = self.screen.display[0] # only need first_line for detection
                if '.' in first_line:
                    break
            os.write(self.crawl_fd, key.ESC)
            if target_str in first_line:
                while 1:
                    data = os.read(self.crawl_fd, 3200)
                    stream.feed(data)
                    if "\(Press ? for help\)" in self.screen.display[0]:
                        target_list.append(self.parser.parse_levelmap())
                        break
                break
        if action == true:
            os.write(self.crawl_fd, ('\r'+target_str).encode())
            # this might cause --more-- appear!
            os.write('\r')
        else:
            os.write(self.crawl_fd, key.ESC)
    def stair_down_handler(self):
        self.update_levelmap('>', "stone staircase leading down", True)


        #print("unreachable")
    def find_last_line(self):
        ll = 0
        while 1:
            last_line = self.screen.display[crawl_const.SCR_ROW-2-ll]
            if last_line != ' ' * crawl_const.SCR_COL:
                break
            ll = ll + 1
        return last_line
##    def update_ctrlpscr(self):
        # changes mainscr to ctrlpscr by *p
        # parses data
        # then returns to mainscr
##        os.write(self.crawl_fd, '*'.encode()) # this changes the screen to mainscr*
##        while(1):
##            data = os.read(self.crawl_fd, 3200)
#            self.stream.feed(data)
#            # print((self.screen.display)[crawl_const.SCR_ROW-1].encode())
#            if (self.screen.display)[crawl_const.SCR_ROW-1][:4] == "CTRL":
#                break
#            if (self.screen.display)[crawl_const.SCR_ROW-1][1:9] == "--more--":
                # should be handled later?
                # or assert?
#                self.more_solver()
#        os.write(self.crawl_fd, 'p'.encode()) # this changes the scre to ctrlpscr
#        print("pre-ctrlp handle")
#        print(*self.screen.display, sep ="\n")
#        while(1):
#            data = os.read(self.crawl_fd, 10)
#            self.stream.feed(data)
#            print("ctrlp handle")
#            print(*self.screen.display, sep = "\n")
#            if "CTRL" not in (self.screen.display)[crawl_const.SCR_ROW-1]:
#                break
#        print("ctrl-p")
#        print(*self.screen.display, sep = "\n")
#        data = self.parser.parse_mainlog() # data is formatted [nearby] yet
#        # print(data[0])
#        os.write(self.crawl_fd, key.ESC)
#        self.ensure_mainscr()
#        return data
    def update_ctrlxscr(self):
        # changes mainscr to ctrlscr by *x
        # changes ctrlxscr to ctrlxscr! by !    # this capture (ctrlxscr) in the process
        # parses data   # this changes ctrlxscr! to (entscr)
        # then returns from (ctrlxscr) to mainscr by esc
        os.write(self.crawl_fd, '*x'.encode())
        while(1):
            print("cycle")
            data = os.read(self.crawl_fd, 3200)
            self.stream.feed(data)
            print(*self.screen.display, sep='\n')
            if "No monsters, items or features are visible." in self.screen.display[crawl_const.SCR_MSG]:
                return [False]
            #print((self.screen.display)[crawl_const.SCR_ROW-1].encode())
            if "(select to target/travel, \'!\' to examine):" in self.screen.display[0]:
                break
            # print(*self.screen.display, sep = "\n")
            assert(("--more--" in (self.screen.display)[crawl_const.SCR_ROW-1]) == False) # --more-- is impossible
        # ctrlxscr
        os.write(self.crawl_fd, '!'.encode())
        while(1):
            data = os.read(self.crawl_fd, 3200)
            self.stream.feed(data)
            if "(select to examine, \'!\' to target/travel):" in self.screen.display[0]:
                break
        # ctrlxscr!
        print(*self.screen.display, sep = "\n")
        visible = self.parser.parse_visible() # do nothing yet
        os.write(crawl_fd, key.ESC)
        return visible
    
    def update_statusscr(self):
        # do nothing yet
        return
        

        
    def state_peace(self):
        while(1):
            print("&")
            # print(*self.screen.display, sep = "\n")
            main_parse = self.update_mainscr()
            ctrlx = self.update_ctrlxscr()  # do we REALLY need this?
            # print(ctrlp[0])
            if main_parse[0] == True: # peace ends
                print("peace ends")
                # make state_battle know it
                # this structure need change...
                break
            else:
                if main_parse[1] == True: # go to next floor
                    print("go to next floor")
                    # consider other message as hungry, mobs while going to stairs
                    self.turn = self.turn + 1
                    # print("Turn: %d" % self.turn)
                    # want to avoid using hatches
                    # however, 'oscilation' between stairs might occur
                    self.stair_down_handler()
                    # else case is disturbed case
                    # this might contain above and hatch
                else:
                    self.turn = self.turn + 1
                    # print("Turn: %d" % self.turn)
                    os.write(self.crawl_fd, "o".encode())
            # should update item related infos constantly
    def state_battle(self):
        while(1):
            main_parse = self.update_mainscr()
            ctrlx = self.update_ctrlxscr()
            if ctrlx[0] == False: # battle ends
                print("battle ends")
                break
            # gather_battle_info()   # a.k.a.
            else:
                mv = self.select_next_move()
                self.turn = self.turn + 1
                # print("Turn: %d" % self.turn)
                os.write(self.crawl_fd, mv)
    def select_next_move(self):
        # do nothing yet
        return key.TAB
    def trans_state(self, state1, state2):
        if(state1 == crawl_const.PEACE and state2 == crawl_const.BATTLE):
            self.trans_peace_battle()
    def trans_peace_battle(self):
        # do nothing yet
        return        
            

if __name__ == "__main__":

    screen = pyte.Screen(crawl_const.SCR_COL, crawl_const.SCR_ROW)
    stream = pyte.ByteStream(screen)

    p_pid, crawl_fd = pty.fork()
    if p_pid == 0:  # child
        os.execvpe("crawl/crawl-ref/source/crawl", ['crawl/crawl-ref/source/crawl','-rc',"init.rc"],
                   env=dict(TERM="linux", COLUMNS=str(crawl_const.SCR_COL), LINES=str(crawl_const.SCR_ROW)))

    try:
        [_crawl_fd], _wlist, _xlist = select.select(
            [crawl_fd], [], [], 1)
    except (KeyboardInterrupt,  # Stop right now!
                ValueError):        # Nothing to read.
        print("KeyboardInterrupt or ValueError")
    else:   # parent
        mapinfo = crawl_info.MapInfo()
        player = crawl_info.PlayerInfo()
        parser = crawl_parse.CrawlParser(crawl_fd, mapinfo, player, screen, stream)
        learn2crawl = Learn2Crawl(crawl_fd, mapinfo, parser, player, screen, stream)
        data = os.read(crawl_fd, 3200)
        stream.feed(data)
        #print(*screen.display, sep="\n")
        name_eraser = "\b"*32
        os.write(crawl_fd, (name_eraser+crawl_const.PLAYER_NAME+'\r').encode())
        while 1:
            data = os.read(crawl_fd, 3200)
            stream.feed(data)
            if ("Welcome, " + crawl_const.PLAYER_NAME) in screen.display[0]:
                os.write(crawl_fd, "vac".encode())
                break
            elif (" " * 37 + crawl_const.PLAYER_NAME) in screen.display[0]:
                os.write(crawl_fd, "\n".encode()) # to make unstable state
                break
        print("Started crawl with player name: %s" % crawl_const.PLAYER_NAME)
        # crawl might start with "--more--"
        # print(*screen.display, sep="\n")
        while 1:
            state = learn2crawl.state_peace()
            learn2crawl.trans_state(crawl_const.PEACE, crawl_const.BATTLE)
            state = learn2crawl.state_battle()
            # read mainscreen
            #read_mainscr(master_fd, screen, stream)
            # parse current state
            #parser.parse_mainscr(master_fd, player)
            # choose next input
            # this is actually not action or
            # since you might need additional 
            #player.print_info()
            # input_mainscr()
            #os.write(master_fd, "*X".encode())

            #data = os.read(master_fd, 3200)
            #stream.feed(data)
            #print(data)
            #print(len(data.decode()))
            #print(*screen.display, sep="\n")
            #os.write(master_fd, "\r".encode())
    os.write(crawl_fd, key.CTRLS)
   



#def read_acquire(target_str, fd, stream, screen):
# how do we ensure input is done?
# by checking p?
# by input length? will input length always be constant?
#    while(1):
        # busy wait
#        data = os.read(master_fd, 1920)
#        stream.feed(data)

#def read_scr(target_str, stream):

